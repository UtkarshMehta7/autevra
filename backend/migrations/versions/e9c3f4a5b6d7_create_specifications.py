"""Create specifications

Revision ID: e9c3f4a5b6d7
Revises: d8b2e3f4a5c6
Create Date: 2026-10-13 23:30:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e9c3f4a5b6d7"
down_revision: str | None = "d8b2e3f4a5c6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "specifications",
        sa.Column("project_id", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("spec_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id"),
    )


def downgrade() -> None:
    op.drop_table("specifications")
