from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Double,
    Boolean,
)

from sqlalchemy.orm import relationship, declarative_base, backref

Base = declarative_base()

# Relation Tables
project_file = Table(
    "project_file",
    Base.metadata,
    Column("project_name", String, ForeignKey("project.project_name")),
    Column("file_path", String, ForeignKey("file.file_path")),
)

file_line = Table(
    "file_line",
    Base.metadata,
    Column("file_path", String, ForeignKey("file.file_path")),
    Column("line_number", Integer, ForeignKey("line.line_number")),
)


# Classes
class Project(Base):
    __tablename__ = "project"
    project_name = Column(String, primary_key=True, unique=True)
    clover_stmt_coverage_score = Column(Double)
    # cc_javaslicer_ds_score = Column(Double)
    # cc_slicer4j_ds_score = Column(Double)
    # cc_porbs_score = Column(Double)
    cc_slicer4j_coverage_gap = Column(Double)
    cc_porbs_coverage_gap = Column(Double)
    ps_covered = Column(Double)
    ps_pt = Column(Double)
    ps_required = Column(Double)
    files = relationship("File", secondary=project_file, backref=backref("project"))


class File(Base):
    __tablename__ = "file"
    file_path = Column(String, primary_key=True)
    project_name = Column(String, ForeignKey("project.project_name"))
    lines = relationship("Line", secondary=file_line, backref=backref("file"))


class Line(Base):
    __tablename__ = "line"
    line_number = Column(Integer, primary_key=True)
    file_path = Column(String, ForeignKey("file.file_path"), primary_key=True)
    on_javaslicer_ds_slice = Column(Boolean)
    on_slicer4j_ds_slice = Column(Boolean)
    on_porbs_slice = Column(Boolean)
    is_covered_clover = Column(Boolean)
    is_covered_ps = Column(Boolean)
    is_pseudotested_ps = Column(Boolean)
    is_required_ps = Column(Boolean)
    in_slicer4j_coverage_gap = Column(Boolean)
    in_porbs_coverage_gap = Column(Boolean)
