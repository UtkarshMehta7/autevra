"""Add the project domain and contact messages

Revision ID: f1a2b3c4d5e6
Revises: e9c3f4a5b6d7
Create Date: 2026-10-14 03:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f1a2b3c4d5e6"
down_revision: str | None = "e9c3f4a5b6d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("domain", sa.String(length=32), nullable=False, server_default="automotive")
        )
    op.create_table(
        "contact_messages",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("topic", sa.String(length=64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("contact_messages")
    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.drop_column("domain")
