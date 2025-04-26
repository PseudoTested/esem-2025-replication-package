from sqlalchemy import select, update

from models.models import Line, File


def set_coverage_gap_slicer4j_lines_in_project(project_name, session):
    coverage_gap = session.scalars(
        select(Line)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.on_slicer4j_ds_slice == None)
        .where(Line.is_covered_clover == True)
    ).all()
    print(f"    -- Slicer4J coverage gap: {len(coverage_gap)}")
    for line in coverage_gap:
        stmt = (
            update(Line)
            .where(Line.file_path == line.file_path)
            .where(Line.line_number == line.line_number)
            .values(in_slicer4j_coverage_gap=True)
        )
        session.execute(stmt)
    session.commit()
    return session


def set_coverage_gap_porbs_lines_in_project(project_name, session):
    coverage_gap = session.scalars(
        select(Line)
        .join(File)
        .where(File.project_name == f"{project_name}")
        .where(Line.on_porbs_slice == False)
        .where(Line.is_covered_clover == True)
    ).all()
    print(f"    -- Porbs coverage gap: {len(coverage_gap)}")
    for line in coverage_gap:
        stmt = (
            update(Line)
            .where(Line.file_path == line.file_path)
            .where(Line.line_number == line.line_number)
            .values(in_porbs_coverage_gap=True)
        )
        session.execute(stmt)
    session.commit()
    return session
