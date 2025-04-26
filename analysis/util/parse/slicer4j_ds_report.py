from pathlib import Path

from util.database.add import add_sliced_line_to_db
from util.database.totals import get_num_covered_lines_in_project, get_num_checked_slicer4j_ds_lines_in_project
from util.parse.util.string_utils import extract_line_number, extract_package


def _create_file_name_regex(package):
    split = package.split('.')
    subclass = split[-1].find('$')
    if subclass > -1:
        split[-1] = split[-1][:subclass]
    regex_str = "^.*{0}\\.java$".format('\/'.join(split))
    return regex_str


def parse(session, project_name):
    slicer4j_ds_report_path = Path(f"project-data/{project_name}/slicer4j_cc_slice.txt")

    with open(slicer4j_ds_report_path, "r", encoding="utf-8") as txt:
        lines = txt.readlines()

        for line in lines:
            if line.startswith("criterion"):
                continue
            line = line.strip()
            line_number = extract_line_number(line)
            package = extract_package(line)
            session = add_sliced_line_to_db(line_number, package, project_name, session,
                                            _create_file_name_regex(package), "slicer4j")
        session.commit()
        return session


def get_pct_checked_slicer4j_ds(project_name, session):
    num_covered = get_num_covered_lines_in_project(project_name, session)
    num_checked = get_num_checked_slicer4j_ds_lines_in_project(project_name, session)
    if num_covered > 0:
        pct_checked_slicer4j_ds = num_checked / num_covered * 100
        print(f"    -- Slicer4j DS: {num_checked}, Covered: {num_covered},  {pct_checked_slicer4j_ds}%")
        return pct_checked_slicer4j_ds
    print(f"    -- Slicer4j DS: Num covered == 0. Pct cannot be calculated.")
    return 0
