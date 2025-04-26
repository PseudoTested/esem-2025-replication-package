import xml.etree.ElementTree as ET
from pathlib import Path

from util.database.add import add_clover_line_to_db, add_file_to_db
from util.database.totals import get_num_covered_lines_in_project, get_num_lines_in_project


def parse(session, project_name):
    clover_report_path = Path(f"project-data/{project_name}/clover.xml")

    tree = ET.parse(clover_report_path)
    root = tree.getroot()
    files = root.findall("./project/package/file")

    for file_xml in files:
        print(file_xml.get("name"))
        session, file = add_file_to_db(session, file_xml, project_name)
        num_lines = int(file_xml.find("./metrics").get("loc"))
        lines = file_xml.findall("./line")

        for line_number in range(1, num_lines + 1):
            covered = False
            for line in lines:
                if line_number == int(line.get("num")) and line.get("count") is not None and int(line.get("count")) > 0:
                    covered = True

            session = add_clover_line_to_db(session, line_number, file_xml, file, project_name, covered)

    return session


def get_pct_covered(project_name, session):
    num_lines = get_num_lines_in_project(project_name, session)
    num_covered = get_num_covered_lines_in_project(project_name, session)
    print(f"    -- Covered: {num_covered}, Total: {num_lines}")
    if num_covered > 0:
        pct_covered = num_covered / num_lines * 100
        return pct_covered
    return 0
