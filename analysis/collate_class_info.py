import json
import os
import re
from pathlib import Path

import numpy as np
import xml.etree.ElementTree as ET
import pandas as pd

from util.parse.util.string_utils import (
    extract_clazz,
    extract_line_number,
    extract_package,
)
from util.read import read_project_list


def parse_clover_report(project_name: str, project_df: pd.DataFrame):
    CLOVER_REPORT_PATH = Path(f"./project_data/{project_name}/clover.xml")

    if not CLOVER_REPORT_PATH.is_file():
        print("WARN: clover.xml does not exist for", project_name, CLOVER_REPORT_PATH)
        return project_df

    CLASS_NAME = project_name.split("_")[-1]

    tree = ET.parse(CLOVER_REPORT_PATH)
    root = tree.getroot()
    files = root.findall("./project/package/file")

    for file_xml in files:
        FILE_NAME = os.path.basename(file_xml.get("name")).removesuffix(".java")
        if FILE_NAME == CLASS_NAME:

            num_lines = int(file_xml.find("./metrics").get("loc"))
            lines = file_xml.findall("./line")

            for line_number in range(1, num_lines + 1):
                covered = False
                for line in lines:

                    if (
                        line_number == int(line.get("num"))
                        and line.get("count") is not None
                        and int(line.get("count")) > 0
                    ):
                        covered = True
                row = {
                    "project": project_name,
                    "class": CLASS_NAME,
                    "line_no": line_number,
                    "is_clover_covered": covered,
                }
                project_df = pd.concat(
                    [project_df, pd.DataFrame([row])], ignore_index=True
                )

    return project_df


def parse_slicer4j_report(project_name: str, project_df: pd.DataFrame):
    CLASS_NAME = project_name.split("_")[-1]

    slicer4j_ds_report_path = Path(f"project_data/{project_name}/slicer4j_cc_slice.txt")

    if not slicer4j_ds_report_path.is_file():
        print(
            "WARN: slicer4j_cc_slice.txt does not exist for",
            project_name,
            slicer4j_ds_report_path,
        )
        return project_df

    with open(slicer4j_ds_report_path, "r", encoding="utf-8") as txt:
        lines = txt.readlines()

        project_df["on_slicer4j_slice"] = False
        for line in lines:
            if line.startswith("criterion"):
                continue

            line = line.strip()
            line_number = extract_line_number(line)
            package = extract_package(line)
            class_name = extract_clazz(package)
            if class_name == CLASS_NAME:
                project_df.loc[
                    project_df["line_no"] == int(line_number), "on_slicer4j_slice"
                ] = True

    return project_df


def parse_porbs_report(project_name: str, project_df: pd.DataFrame):
    porbs_report_path = Path(f"project_data/{project_name}/orbs_deleted_lines.txt")
    file_path = ""

    if not porbs_report_path.is_file():
        print(
            "WARN: orbs_deleted_lines.txt does not exist for",
            project_name,
            porbs_report_path,
        )
        return project_df
    project_df["on_porbs_slice"] = True
    with open(porbs_report_path, "r") as file:
        line_marker = 1
        for row in file:

            if row[0].isnumeric():
                line_number = int(row.split(":")[0])
                # for i in range(line_marker, line_number):
                #     project_df.loc[
                #         project_df["line_no"] == int(i), "on_porbs_slice"
                #     ] = True

                if file_path != "":
                    project_df.loc[
                        project_df["line_no"] == int(line_number), "on_porbs_slice"
                    ] = False
                else:
                    print(
                        f"File name invalid in orbs_deleted_lines.txt for {project_name}"
                    )
                    return
                line_marker = line_number + 1
            elif row.startswith("src/"):
                file_path = f"{project_name}/{row.strip()}"
                line_marker = 1

    return project_df


def parse_pseudosweep_report(project_name: str, project_df: pd.DataFrame):
    covered = {}
    required = {}
    pseudotested = {}

    ps_data_analysis_path = Path(
        f"project_data/{project_name}/PS-data/analysis-sdl/project-overview/project-overview.json"
    )

    if not ps_data_analysis_path.is_file():
        print(
            "WARN: project-overview.json does not exist for",
            project_name,
            ps_data_analysis_path,
        )
        return project_df

    ps_classes_report_path = _read_pseudosweep_analysis(
        covered, project_name, required, pseudotested
    )

    class_name = project_name.split("_")[-1]
    (
        lines_statements,
        lines_covered,
        lines_pseudo_tested,
        lines_required,
        line_statement_types,
    ) = _get_element_locations(
        covered, ps_classes_report_path, required, class_name, pseudotested
    )

    project_df["covered_ps"] = False
    project_df["required_ps"] = False
    project_df["pseudotested_ps"] = False

    for statement in lines_statements.values():
        for line_number in statement:
            project_df.loc[
                project_df["line_no"] == int(line_number), "statement_ps"
            ] = True

    # Mark covered lines as True
    for cov in lines_covered.values():
        for line_number in cov:
            project_df.loc[project_df["line_no"] == int(line_number), "covered_ps"] = (
                True
            )

    for req in lines_required.values():
        for line_number in req:
            project_df.loc[project_df["line_no"] == int(line_number), "required_ps"] = (
                True
            )

    for ps in lines_pseudo_tested.values():
        for line_number in ps:
            project_df.loc[
                project_df["line_no"] == int(line_number), "pseudotested_ps"
            ] = True

    # check for inner pseudo-testedness

    # project_df["pseudotested_ps"] = np.where(
    #     (project_df["required_ps"] == True) & (project_df["pseudotested_ps"] == True),
    #     False,
    #     project_df["pseudotested_ps"],
    # )

    for line_number in line_statement_types.keys():
        if len(project_df) != 0:
            project_df.loc[
                project_df["line_no"] == int(line_number), "statement_type"
            ] = line_statement_types[line_number]

    return project_df


def _get_element_locations(
    covered, ps_classes_report_path, required, class_name, pseudotested
):
    files_statements = {}
    files_covered = {}
    files_required = {}
    files_pseudo_tested = {}
    statement_types = {}
    for path, dirs, files in os.walk(ps_classes_report_path):
        for file_name in files:
            if class_name != file_name.removesuffix(".json"):
                continue

            file_path = Path(f"{path}/{file_name}")
            with open(file_path) as json_file:
                data = json.load(json_file)

                statements = {
                    element: (
                        data["coverageElementPositions"][element]["startLine"],
                        data["coverageElementPositions"][element]["endLine"],
                    )
                    for element in set(data["coverageElementPositions"].keys())
                    if not element.startswith("Decision")
                }

                elements_covered = {
                    element: (
                        data["coverageElementPositions"][element]["startLine"],
                        data["coverageElementPositions"][element]["endLine"],
                    )
                    for element in set(covered.keys()).intersection(
                        set(data["coverageElementPositions"].keys())
                    )
                    if not element.startswith("Decision")
                }

                elements_required = {
                    element: (
                        data["coverageElementPositions"][element]["startLine"],
                        data["coverageElementPositions"][element]["endLine"],
                    )
                    for element in set(required.keys()).intersection(
                        set(data["coverageElementPositions"].keys())
                    )
                    if not element.startswith("Decision")
                }

                elements_pseudotested = {
                    element: (
                        data["coverageElementPositions"][element]["startLine"],
                        data["coverageElementPositions"][element]["endLine"],
                    )
                    for element in set(pseudotested.keys()).intersection(
                        set(data["coverageElementPositions"].keys())
                    )
                    if not element.startswith("Decision")
                }

                def extract_statement_type(stmt_string):
                    match = re.search(r"Stmt\(([^,]+),", stmt_string)
                    if match:
                        return match.group(1)
                    else:
                        return None

                # update primary statement type on each line
                [
                    statement_types.update({i: extract_statement_type(key)})
                    for key, value in data["coverageElementPositions"].items()
                    for i in range(int(value["startLine"]), int(value["endLine"]) + 1)
                ]

                statements_lines_set = set(s for (s, e) in statements.values())
                files_statements = _add_to_dict(
                    statements_lines_set, data, files_statements
                )

                covered_lines_set = set(s for (s, e) in elements_covered.values())
                files_covered = _add_to_dict(covered_lines_set, data, files_covered)

                required_lines_set = set(s for (s, e) in elements_required.values())

                pseudotested_lines_set = set(
                    s for (s, e) in elements_pseudotested.values()
                )

                required_lines_set = required_lines_set - pseudotested_lines_set

                files_required = _add_to_dict(required_lines_set, data, files_required)

                files_pseudo_tested = _add_to_dict(
                    pseudotested_lines_set, data, files_pseudo_tested
                )

    return (
        files_statements,
        files_covered,
        files_pseudo_tested,
        files_required,
        statement_types,
    )


def _add_to_dict(line_set, data, dict_to_update):
    if dict_to_update.get(str(data["fileName"])) is None:
        dict_to_update.update({str(data["fileName"]): line_set})
    else:
        dict_to_update.update(
            {
                str(data["fileName"]): dict_to_update[str(data["fileName"])].union(
                    line_set
                )
            }
        )
    return dict_to_update


def _read_pseudosweep_analysis(covered, project_name, required, pseudotested):
    ps_analysis_report_path = Path(f"project_data/{project_name}/PS-data/analysis-sdl/")
    if not ps_analysis_report_path.is_dir():
        print(ps_analysis_report_path, "does not exist")
        return

    for path, dirs, files in os.walk(ps_analysis_report_path):
        if path.endswith("analysis-sdl/project-overview"):
            continue

        for file_name in files:
            if not file_name.endswith(".json"):
                continue
            file_path = Path(f"{path}/{file_name}")

            with open(file_path) as json_file:
                data = json.load(json_file)
                covered.update({element: -1 for element in data["covered"]})
                required.update({element: -1 for element in data["effectualCovered"]})
                pseudotested.update(
                    {
                        element: -1
                        for statement_type in data["typeMetricsHashMap"]
                        for element in data["typeMetricsHashMap"][statement_type][
                            "coverageGap"
                        ]
                    }
                )

    ps_classes_report_path = Path(f"project_data/{project_name}/PS-data/classes-sdl/")
    return ps_classes_report_path


def get_mutant_counts(project_name: str, project_df: pd.DataFrame):
    project_df["pit_total"] = 0
    project_df["pit_killed"] = 0
    project_df["pit_survived"] = 0
    project_df["pit_uncovered"] = 0

    mutants_csv_path = f"./project_data/{project_name}/pit-reports/mutations.csv"
    columns = [
        "sourceFile",
        "mutatedClass",
        "mutator",
        "mutatedMethod",
        "lineNumber",
        "status",
        "killingTest",
    ]
    
    df_mutants = pd.read_csv(mutants_csv_path, names=columns)
    for index, row in df_mutants.iterrows():
        if row["sourceFile"].removesuffix(".java") != project_df["class"].iloc[0]:
            continue

        current_count = project_df.loc[
            project_df["line_no"] == int(row["lineNumber"]), "pit_total"
        ].iloc[0]
        project_df.loc[project_df["line_no"] == int(row["lineNumber"]), "pit_total"] = (
            current_count + 1
        )

        if row["status"] == "KILLED":
            current_count = project_df.loc[
                project_df["line_no"] == int(row["lineNumber"]), "pit_killed"
            ].iloc[0]
            project_df.loc[
                project_df["line_no"] == int(row["lineNumber"]), "pit_killed"
            ] = (current_count + 1)

        if row["status"] == "SURVIVED":
            current_count = project_df.loc[
                project_df["line_no"] == int(row["lineNumber"]), "pit_survived"
            ].iloc[0]
            project_df.loc[
                project_df["line_no"] == int(row["lineNumber"]), "pit_survived"
            ] = (current_count + 1)

        if row["status"] == "NO_COVERAGE":
            current_count = project_df.loc[
                project_df["line_no"] == int(row["lineNumber"]), "pit_uncovered"
            ].iloc[0]
            project_df.loc[
                project_df["line_no"] == int(row["lineNumber"]), "pit_uncovered"
            ] = (current_count + 1)

    print(f"Total Mutants in {project_name}", project_df["pit_total"].sum())
    return project_df


def main():
    # setup
    columns = [
        "project",
        "class",
        "line_no",
        "is_clover_covered",
        "on_slicer4j_slice",
        "on_porbs_slice",
        "statement_ps",
        "covered_ps",
        "required_ps",
        "pseudotested_ps",
        "pit_total",
        "pit_killed",
        "pit_survived",
        "pit_uncovered",
    ]

    project_list = read_project_list(Path("./resources/class_projects.csv"))
    data_dir = "./project_data/"

    for project in project_list:
        print("\n", project)
        project_df = pd.DataFrame(columns=columns)

        # get num lines in class
        project_df = parse_clover_report(project, project_df)
        # read Slicer4J
        project_df = parse_slicer4j_report(project, project_df)
        # read PORBS
        project_df = parse_porbs_report(project, project_df)

        # read PseudoSweep
        project_df = parse_pseudosweep_report(project, project_df)

        # read PIT mutants
        project_df = get_mutant_counts(project, project_df)

        project_df["covered_porbs"] = (
            project_df["on_porbs_slice"] & project_df["covered_ps"]
        )
        project_df["covered_slicer4J"] = (
            project_df["on_slicer4j_slice"] & project_df["covered_ps"]
        )

        project_df["covgap_on_porbs_slice"] = np.where(
            (project_df["covered_ps"] == 1) & (project_df["on_porbs_slice"] != 1),
            True,
            False,
        )
        project_df["covgap_on_slicer4j_slice"] = np.where(
            (project_df["covered_ps"] == 1) & (project_df["on_slicer4j_slice"] != 1),
            True,
            False,
        )

        # calculate coverage gaps

        # write to csv in project file
        csv_path = data_dir + project + f"/{project}.csv"
        project_df.to_csv(csv_path, index=False)

    # create overall data frame
    columns = [
        "project",
        "class",
        "line_no",
        "is_clover_covered",
        "on_slicer4j_slice",
        "on_porbs_slice",
        "statement_ps",
        "covered_ps",
        "required_ps",
        "pseudotested_ps",
        "domain",
        "pit_total",
        "pit_killed",
        "pit_survived",
        "pit_uncovered",
    ]
    project_list = read_project_list(Path("./resources/class_projects.csv"))
    data_dir = "./project_data/"

    df = pd.DataFrame(columns=columns)
    df_domains = pd.read_csv(data_dir + "domains.csv")

    for project in project_list:
        project_name = project.rsplit("_", 1)[0]
        domain = str(
            df_domains.loc[df_domains["name"] == project_name].iloc[0]["domain"]
        )
        csv_path = data_dir + project + f"/{project}.csv"
        project_df = pd.read_csv(csv_path)
        project_df = project_df.assign(domain=domain)
        project_df = project_df.assign(project=project_name)
        df = pd.concat([df, project_df])

    df.to_csv(data_dir + "all_projects.csv", index=False)

    print(df)  # create overall data frame


if __name__ == "__main__":
    main()
