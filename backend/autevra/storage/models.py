"""SQLAlchemy models. The schema is managed by Alembic (``backend/migrations``)."""

from datetime import UTC, datetime

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class ProjectRow(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(default=_now)
    updated_at: Mapped[datetime] = mapped_column(default=_now, onupdate=_now)
    values_json: Mapped[str] = mapped_column(Text)
    cursor: Mapped[int] = mapped_column(Integer, default=0)

    history: Mapped[list["HistoryRow"]] = relationship(
        back_populates="project", cascade="all, delete-orphan", order_by="HistoryRow.seq"
    )


class HistoryRow(Base):
    __tablename__ = "history_entries"
    __table_args__ = (UniqueConstraint("project_id", "seq"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    seq: Mapped[int] = mapped_column(Integer)
    entry_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=_now)

    project: Mapped[ProjectRow] = relationship(back_populates="history")


class TestRunRow(Base):
    """One component test run; ``record_json`` holds the full, self-describing record."""

    __tablename__ = "test_runs"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    test_id: Mapped[str] = mapped_column(String(64))
    target: Mapped[str] = mapped_column(String(32))
    scenario_id: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    values_hash: Mapped[str] = mapped_column(String(32))
    inputs_hash: Mapped[str] = mapped_column(String(32), index=True)
    created_at: Mapped[datetime] = mapped_column(default=_now)
    record_json: Mapped[str] = mapped_column(Text)


class RequirementRow(Base):
    __tablename__ = "requirements"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(default=_now)
    requirement_json: Mapped[str] = mapped_column(Text)


class StudyRow(Base):
    """Optimisation studies and engineering-loop sessions, with their decision."""

    __tablename__ = "studies"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    kind: Mapped[str] = mapped_column(String(32))  # optimization | loop
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(default=_now)
    record_json: Mapped[str] = mapped_column(Text)


class SpecificationRow(Base):
    """The vehicle specification of a project (one per project)."""

    __tablename__ = "specifications"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    updated_at: Mapped[datetime] = mapped_column(default=_now, onupdate=_now)
    spec_json: Mapped[str] = mapped_column(Text)
