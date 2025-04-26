from sqlalchemy import join

from models.models import File, Line, Project


def line_exists_for_file(session, line_number, file_path):
    lines = (
        session.query(Line)
        .filter(Line.file_path == file_path)
        .filter(Line.line_number == line_number)
        .all()
    )

    # print("Line Number:", line_number, "Lines existing:", len(lines))

    if len(lines) > 0:
        for line in lines:
            return line

    return None


def file_exists_for_project(session, project_name, file_path):
    files = (
        session.query(File)
        .filter(File.file_path == file_path)
        .filter(File.project_name == project_name)
        .all()
    )

    # print("File exists for project:", files)
    if len(files) > 0:
        for file in files:
            return file
    return None


def file_exists_for_project_regex(session, project_name, regex_str):
    files = (
        session.query(File)
        .filter(File.project_name == project_name)
        .filter(File.file_path.op('regexp')(regex_str))
        .all()
    )

    if len(files) > 0:
        for file in files:
            return file
    return None


def line_exists_for_project_regex(session, regex_str, line_number):

    lines = (
        session.query(Line)
        .filter(Line.file_path.op('regexp')(regex_str))
        .filter(Line.line_number == line_number)
        .all()
    )

    # print("Line Number:", line_number, "Lines existing:", len(lines))

    if len(lines) > 0:
        for line in lines:
            return line

    return None
