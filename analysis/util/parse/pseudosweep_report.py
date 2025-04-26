import json
import os
from pathlib import Path

from util.database.add import (
    add_ps_lines_covered_to_db,
    add_ps_lines_required_to_db,
    add_ps_lines_pseudo_tested_to_db,
)
from util.database.totals import (
    get_num_lines_in_project,
    get_num_pseudo_tested_stmts_in_project,
    get_num_required_stmts_in_project,
    get_num_ps_covered_stmts_in_project,
)


def parse(session, project_name):
    covered = {}
    required = {}

    ps_classes_report_path = _read_pseudosweep_analysis(covered, project_name, required)

    lines_covered, lines_pseudo_tested, lines_required = _get_element_locations(
        covered, ps_classes_report_path, required
    )

    session_list = [
        add_ps_lines_covered_to_db(f, l, project_name, session)
        for (f, ls) in lines_covered.items()
        for l in ls
    ]
    session = session_list[-1] if len(session_list) > 0 else session
    session_list = [
        add_ps_lines_required_to_db(f, l, project_name, session)
        for (f, ls) in lines_required.items()
        for l in ls
    ]
    session = session_list[-1] if len(session_list) > 0 else session

    session_list = [
        add_ps_lines_pseudo_tested_to_db(f, l, project_name, session)
        for (f, ls) in lines_pseudo_tested.items()
        for l in ls
    ]
    session = session_list[-1] if len(session_list) > 0 else session

    return session


def _get_element_locations(covered, ps_classes_report_path, required):
    files_covered = {}
    files_required = {}
    files_pseudo_tested = {}
    for path, dirs, files in os.walk(ps_classes_report_path):
        for file_name in files:
            file_path = Path(f"{path}/{file_name}")
            with open(file_path) as json_file:
                data = json.load(json_file)
                elements_covered = {
                    element: (
                        data["coverageElementPositions"][element]["startLine"],
                        data["coverageElementPositions"][element]["endLine"],
                    )
                    for element in set(covered.keys()).intersection(
                        set(data["coverageElementPositions"].keys())
                    )
                }
                elements_required = {
                    element: (
                        data["coverageElementPositions"][element]["startLine"],
                        data["coverageElementPositions"][element]["endLine"],
                    )
                    for element in set(required.keys()).intersection(
                        set(data["coverageElementPositions"].keys())
                    )
                }

                covered_lines_set = set(s for (s, e) in elements_covered.values())

                files_covered = _add_to_dict(covered_lines_set, data, files_covered)

                required_lines_set = set(s for (s, e) in elements_required.values())

                files_required = _add_to_dict(required_lines_set, data, files_required)

                files_pseudo_tested = _add_to_dict(
                    covered_lines_set - required_lines_set, data, files_pseudo_tested
                )

    return files_covered, files_pseudo_tested, files_required


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


def _read_pseudosweep_analysis(covered, project_name, required):
    ps_analysis_report_path = Path(f"project-data/{project_name}/PS-data/analysis-sdl/")
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
    ps_classes_report_path = Path(f"project-data/{project_name}/PS-data/classes-sdl/")
    return ps_classes_report_path


# TODO: UPDATE TOTAL PCTS TO USE TOTAL STMTS FROM PSEUDOSWEEP


def get_pct_pseudo_tested(project_name, session):
    num_lines = get_num_lines_in_project(project_name, session)
    if num_lines > 0:
        num_pseudo_tested = get_num_pseudo_tested_stmts_in_project(project_name, session)
        pct_pseudo_tested = num_pseudo_tested / num_lines * 100
        print(
            f"    -- PS Pseudo-tested: {num_pseudo_tested}, Total: {num_lines}, {pct_pseudo_tested}%"
        )
        return pct_pseudo_tested
    return 0


def get_pct_required(project_name, session):
    num_lines = get_num_lines_in_project(project_name, session)
    if num_lines > 0:
        num_required = get_num_required_stmts_in_project(project_name, session)
        pct_required = num_required / num_lines * 100
        print(f"    -- PS Required: {num_required}, Total: {num_lines}, {pct_required}%")
        return pct_required
    return 0


def get_pct_pseudosweep_covered(project_name, session):
    num_lines = get_num_lines_in_project(project_name, session)
    if num_lines > 0:
        num_ps_covered = get_num_ps_covered_stmts_in_project(project_name, session)
        pct_ps_covered = num_ps_covered / num_lines * 100
        print(f"    -- PS Covered: {num_ps_covered}, Total: {num_lines}, {pct_ps_covered}%")
        return pct_ps_covered
    return 0
