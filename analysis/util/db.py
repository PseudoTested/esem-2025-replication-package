import os
from pathlib import Path

from sqlalchemy import create_engine

from models.models import Base, Project
from util.database.add import (
    add_clover_score_to_db,
    add_porbs_gap_pct_to_db,
    add_pseudotested_score_to_db,
    add_required_score_to_db,
    add_pseudosweep_covered_score_to_db,
    add_slicer4j_ds_gap_pct_to_db,
)

from util.database.calculate import (
    set_coverage_gap_slicer4j_lines_in_project,
    set_coverage_gap_porbs_lines_in_project,
)
from util.parse import (
    clover_report,
    porbs_report,
    pseudosweep_report,
    slicer4j_ds_report,
)
from util.parse.clover_report import get_pct_covered

from util.parse.porbs_report import get_pct_checked_porbs
from util.parse.pseudosweep_report import (
    get_pct_pseudo_tested,
    get_pct_required,
    get_pct_pseudosweep_covered,
)
from util.parse.slicer4j_ds_report import get_pct_checked_slicer4j_ds


def create_projects_db():
    sqlite_filepath = Path("resources/projects.db")

    # TODO: Check data base exists
    if os.path.exists(sqlite_filepath):
        os.remove(sqlite_filepath)

    engine = create_engine(f"sqlite:///{sqlite_filepath}")
    Base.metadata.create_all(engine)
    return engine


def _update_project_totals(session, project_name):
    session = add_clover_score_to_db(
        session, project_name, get_pct_covered(project_name, session)
    )
    session = add_slicer4j_ds_gap_pct_to_db(
        session, project_name, get_pct_checked_slicer4j_ds(project_name, session)
    )
    session = add_porbs_gap_pct_to_db(
        session, project_name, get_pct_checked_porbs(project_name, session)
    )
    session = add_pseudosweep_covered_score_to_db(
        session, project_name, get_pct_pseudosweep_covered(project_name, session)
    )
    session = add_required_score_to_db(
        session, project_name, get_pct_required(project_name, session)
    )
    session = add_pseudotested_score_to_db(
        session, project_name, get_pct_pseudo_tested(project_name, session)
    )

    # coverage gaps
    session = set_coverage_gap_porbs_lines_in_project(project_name, session)
    session = set_coverage_gap_slicer4j_lines_in_project(project_name, session)

    return session


def _add_project_to_db(session, project_name):
    project = (
        session.query(Project)
        .filter(Project.project_name == project_name)
        .one_or_none()
    )

    if project is None:
        print(f"-- Importing: {project_name} ")
        project = Project(project_name=project_name)
        session.add(project)
        session.commit()

    porbs_report.parse(session, project_name)
    clover_report.parse(session, project_name)
    slicer4j_ds_report.parse(session, project_name)
    pseudosweep_report.parse(session, project_name)

    session = _update_project_totals(session, project_name)

    return session


def add_projects_to_db(session, project_list):
    print("-------- Adding Projects: Start --------")
    for project in project_list:
        session = _add_project_to_db(session, project)

    session.close()
    print("-------- Adding Projects: Complete --------")
