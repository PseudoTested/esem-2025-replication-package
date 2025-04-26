import sys

from sqlalchemy import select

from models.models import Line, File, Project
from util.database.exists import (
    line_exists_for_file,
    file_exists_for_project,
    file_exists_for_project_regex,
    line_exists_for_project_regex,
)
from util.read import get_relative_file_path


def add_clover_line_to_db(session, line_number, file_xml, file, project_name, covered):
    file_path = get_relative_file_path(file_xml.get("path"), project_name)

    line_db = line_exists_for_file(session, line_number, file_path)
    if line_db is None:
        line_db = Line(line_number=line_number, file_path=file_path)
        file.lines.append(line_db)
    line_db.is_covered_clover = covered
    session.add(line_db)
    session.add(file)
    session.commit()

    return session


def add_file_to_db(session, file_xml, project_name):
    file_path = get_relative_file_path(file_xml.get("path"), project_name)

    file_db = session.query(File).filter(File.file_path == file_path).one_or_none()

    if file_db is None:
        file_db = File(file_path=file_path, project_name=project_name)
    else:
        return session, file_db

    project = (
        session.query(Project)
        .filter(Project.project_name == project_name)
        .one_or_none()
    )

    if (
        project is not None
        and (file_exists_for_project(session, project_name, File.file_path)) is None
    ):
        project.files.append(file_db)

    session.add(file_db)
    session.commit()
    return session, file_db


def add_sliced_line_to_db(
    line_number, package, project_name, session, package_regex, slicer
):
    file_db = file_exists_for_project_regex(session, project_name, package_regex)
    if file_db is None:
        print(f"INFO - file does not exist: {line_number}, {package}")
    else:
        line_db = line_exists_for_project_regex(session, package_regex, line_number)
        if line_db is None:
            print(f"ERROR - line does not exist: {line_number}, {package}")
            # sys.exit(0)
        else:
            if slicer == "slicer4j":
                line_db.on_slicer4j_ds_slice = True
            elif slicer == "javaslicer":
                line_db.on_javaslicer_ds_slice = True

            session.add(line_db)
    return session


def add_porbs_line_to_db(file_path, line_number, project_name, session, on_slice):
    file_path = get_relative_file_path(file_path, project_name)
    line_db = line_exists_for_file(session, line_number, file_path)
    if line_db is None:
        line_db = Line(line_number=line_number, file_path=file_path)
    line_db.on_porbs_slice = on_slice

    file_db = _create_file_if_none(file_path, line_db, project_name, session)

    session.add(line_db)
    session.add(file_db)
    session.commit()
    return session


def add_ps_lines_covered_to_db(file_path, line_number, project_name, session):
    file_path_db, line_db = _get_line(file_path, line_number, project_name, session)

    line_db.is_covered_ps = True

    file_db = _create_file_if_none(file_path_db, line_db, project_name, session)
    session.add(line_db)
    session.add(file_db)
    session.commit()
    return session


def add_ps_lines_required_to_db(file_path, line_number, project_name, session):
    file_path_db, line_db = _get_line(file_path, line_number, project_name, session)
    line_db.is_required_ps = True
    file_db = _create_file_if_none(file_path_db, line_db, project_name, session)
    session.add(line_db)
    session.add(file_db)
    session.commit()
    return session


def add_ps_lines_pseudo_tested_to_db(file_path, line_number, project_name, session):
    file_path_db, line_db = _get_line(file_path, line_number, project_name, session)
    line_db.is_pseudotested_ps = True
    file_db = _create_file_if_none(file_path_db, line_db, project_name, session)
    session.add(line_db)
    session.add(file_db)
    session.commit()
    return session


def _get_line(file_path, line_number, project_name, session):
    file_path_db = project_name + "/" + str(file_path)
    line_db = line_exists_for_file(session, line_number, file_path_db)
    if line_db is None:
        line_db = Line(line_number=line_number, file_path=file_path_db)
    return file_path_db, line_db


def _create_file_if_none(file_path_db, line_db, project_name, session):
    project_db = (
        session.query(Project)
        .filter(Project.project_name == project_name)
        .one_or_none()
    )
    if project_db is None:
        print("ERROR - project not found")

    file_db = file_exists_for_project(session, project_name, file_path_db)
    if file_db is None:
        file_db = File(file_path=file_path_db, project_name=project_name)
        file_db.lines.append(line_db)
        project_db.files.append(file_db)
    return file_db


def add_clover_score_to_db(session, project_name, pct_covered):
    project = session.scalars(
        select(Project).where(Project.project_name == f"{project_name}")
    ).one_or_none()
    project.clover_stmt_coverage_score = pct_covered
    session.add(project)
    session.commit()

    return session


def add_porbs_gap_pct_to_db(session, project_name, pct_checked):
    project = session.scalars(
        select(Project).where(Project.project_name == f"{project_name}")
    ).one_or_none()
    project.cc_porbs_coverage_gap = pct_checked
    session.add(project)
    session.commit()

    return session


def add_slicer4j_ds_gap_pct_to_db(session, project_name, pct_checked):
    project = session.scalars(
        select(Project).where(Project.project_name == f"{project_name}")
    ).one_or_none()
    project.cc_slicer4j_coverage_gap = pct_checked
    session.add(project)
    session.commit()

    return session


def add_required_score_to_db(session, project_name, pct_covered):
    project = session.scalars(
        select(Project).where(Project.project_name == f"{project_name}")
    ).one_or_none()
    project.ps_required = pct_covered
    session.add(project)
    session.commit()

    return session


def add_pseudotested_score_to_db(session, project_name, pct_covered):
    project = session.scalars(
        select(Project).where(Project.project_name == f"{project_name}")
    ).one_or_none()
    project.ps_pt = pct_covered
    session.add(project)
    session.commit()

    return session


def add_pseudosweep_covered_score_to_db(session, project_name, pct_covered):
    project = session.scalars(
        select(Project).where(Project.project_name == f"{project_name}")
    ).one_or_none()
    project.ps_covered = pct_covered
    session.add(project)
    session.commit()

    return session
