"""Create studies

Revision ID: d8b2e3f4a5c6
Revises: c7a1d2e3f4b5
Create Date: 2026-10-13 22:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d8b2e3f4a5c6"
down_revision: str | None = "c7a1d2e3f4b5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "studies",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=32), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("record_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("studies", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_studies_project_id"), ["project_id"])


def downgrade() -> None:
    with op.batch_alter_table("studies", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_studies_project_id"))
    op.drop_table("studies")
