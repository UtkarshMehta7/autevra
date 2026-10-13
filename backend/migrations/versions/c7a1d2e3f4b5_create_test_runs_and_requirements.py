"""Create test runs and requirements

Revision ID: c7a1d2e3f4b5
Revises: b5816405a443
Create Date: 2026-10-13 18:30:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c7a1d2e3f4b5"
down_revision: str | None = "b5816405a443"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "test_runs",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=32), nullable=False),
        sa.Column("test_id", sa.String(length=64), nullable=False),
        sa.Column("target", sa.String(length=32), nullable=False),
        sa.Column("scenario_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("values_hash", sa.String(length=32), nullable=False),
        sa.Column("inputs_hash", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("record_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("test_runs", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_test_runs_project_id"), ["project_id"])
        batch_op.create_index(batch_op.f("ix_test_runs_inputs_hash"), ["inputs_hash"])
    op.create_table(
        "requirements",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("requirement_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("requirements", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_requirements_project_id"), ["project_id"])


def downgrade() -> None:
    with op.batch_alter_table("requirements", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_requirements_project_id"))
    op.drop_table("requirements")
    with op.batch_alter_table("test_runs", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_test_runs_inputs_hash"))
        batch_op.drop_index(batch_op.f("ix_test_runs_project_id"))
    op.drop_table("test_runs")
