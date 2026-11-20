"""Create the feature templates (power copies) table

Revision ID: d8e9f0a1b2c3
Revises: c7d8e9f0a1b2
Create Date: 2026-11-04 23:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d8e9f0a1b2c3"
down_revision: str | None = "c7d8e9f0a1b2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "feature_templates",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("owner", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("document_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_feature_templates_owner"), "feature_templates", ["owner"])


def downgrade() -> None:
    op.drop_index(op.f("ix_feature_templates_owner"), table_name="feature_templates")
    op.drop_table("feature_templates")
