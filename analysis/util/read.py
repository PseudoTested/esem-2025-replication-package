import csv
from pathlib import Path

def get_relative_file_path(full_file_path, project_name):
    start = full_file_path.find(f"{project_name}")
    return full_file_path[start:]

def read_project_list(path):
    project_list_path = path
    with open(project_list_path, "r") as project_list_csv:
        # read project csv
        csv_reader = csv.DictReader(project_list_csv)
        project_dict = [row for row in csv_reader]

        # import each active project
        project_list = []

        for project in project_dict:
            if project["active"] == "true".strip():
                project_list.append(project["name"])

        return project_list
