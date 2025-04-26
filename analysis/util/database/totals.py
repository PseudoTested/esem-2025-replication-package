from sqlalchemy import select

from models.models import Line, File


def get_num_lines_in_project(project_name, session):
    lines = session.scalars(
        select(Line.line_number)
        .join(File)
        .where(File.project_name == f"{project_name}")
    ).all()
    return len(lines)


def get_num_covered_lines_in_project(project_name, session):
    covered = session.scalars(
        select(Line.is_covered_clover)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.is_covered_clover == True)
    ).all()
    num_covered = len(covered)
    return num_covered


def get_num_checked_porbs_lines_in_project(project_name, session):
    checked = session.scalars(
        select(Line.on_porbs_slice)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.on_porbs_slice == True)
        .where(Line.is_covered_clover == True)
    ).all()

    num_checked = len(checked)
    return num_checked


def get_num_checked_javaslicer_ds_lines_in_project(project_name, session):
    checked = session.scalars(
        select(Line.on_javaslicer_ds_slice)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.on_javaslicer_ds_slice == True)
        .where(Line.is_covered_clover == True)
    ).all()

    num_checked = len(checked)
    return num_checked


def get_num_checked_slicer4j_ds_lines_in_project(project_name, session):
    checked = session.scalars(
        select(Line.on_slicer4j_ds_slice)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.on_slicer4j_ds_slice == True)
        .where(Line.is_covered_clover == True)
    ).all()

    num_checked = len(checked)
    return num_checked


def get_num_pseudo_tested_stmts_in_project(project_name, session):
    pseudo_tested = session.scalars(
        select(Line.is_pseudotested_ps)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.is_pseudotested_ps == True)
    ).all()

    num_pseudo_tested = len(pseudo_tested)
    return num_pseudo_tested


def get_num_required_stmts_in_project(project_name, session):
    required = session.scalars(
        select(Line.is_required_ps)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.is_required_ps == True)
    ).all()

    num_required = len(required)
    return num_required


def get_num_ps_covered_stmts_in_project(project_name, session):
    ps_covered = session.scalars(
        select(Line.is_covered_ps)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.is_covered_ps == True)
    ).all()

    num_ps_covered = len(ps_covered)
    return num_ps_covered
