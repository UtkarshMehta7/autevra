"""Create the Part Design parts table

Revision ID: b6c7d8e9f0a1
Revises: a3b4c5d6e7f8
Create Date: 2026-10-15 02:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b6c7d8e9f0a1"
down_revision: str | None = "a3b4c5d6e7f8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "parts",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=32), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("document_json", sa.Text(), nullable=False),
        sa.Column("undo_json", sa.Text(), nullable=False),
        sa.Column("redo_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_parts_project_id"), "parts", ["project_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_parts_project_id"), table_name="parts")
    op.drop_table("parts")
