from pathlib import Path

from util.database.add import add_porbs_line_to_db
from util.database.totals import (
    get_num_checked_porbs_lines_in_project,
    get_num_covered_lines_in_project,
)


def parse(session, project_name):
    porbs_report_path = Path(f"project-data/{project_name}/orbs_deleted_lines.txt")
    file_path = ""
    with (open(porbs_report_path, "r") as file):
        line_marker = 1
        for row in file:

            if row[0].isnumeric():
                line_number = int(row.split(":")[0])
                for i in range(line_marker, line_number):
                    session = add_porbs_line_to_db(
                        file_path, i, project_name, session, True
                    )

                if file_path != "":
                    session = add_porbs_line_to_db(
                        file_path, line_number, project_name, session, False
                    )
                else:
                    raise Exception(
                        f"File name invalid in orbs_deleted_lines.txt for {project_name}"
                    )
                line_marker = line_number + 1
            elif row.startswith("src/"):
                file_path = f"{project_name}/{row.strip()}"
                line_marker = 1

    return session


def get_pct_checked_porbs(project_name, session):
    num_covered = get_num_covered_lines_in_project(project_name, session)
    num_checked = get_num_checked_porbs_lines_in_project(project_name, session)

    if num_covered > 0:
        pct_checked_porbs = num_checked / num_covered * 100
        print(
            f"    -- PORBS: {num_checked}, Covered: {num_covered},  {pct_checked_porbs}%"
        )
        return pct_checked_porbs
    print(f"    -- PORBS: Num covered == 0. Pct cannot be calculated.")
    return 0
