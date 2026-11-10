"""The generators that can make content of a type, and the default for each type and level.

Revision ID: 0034_content_type_generators
Revises: 0033_chat_threads
Create Date: 2026-10-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0034_content_type_generators"
down_revision = "0033_chat_threads"
branch_labels = None
depends_on = None

_TABLE = "content_type_generators"


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds the table on a fresh DB (see migration_utils).
    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("type_slug", sa.String(64), nullable=False),
        sa.Column("level", sa.String(16), nullable=False),
        sa.Column("harness", sa.String(32), nullable=False),
        sa.Column("schema_source", sa.String(16), nullable=False),
        sa.Column("ref", sa.String(128), nullable=False),
        sa.Column("spec_revision", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("default_key", sa.String(96), nullable=True),
        sa.Column("changed_by", sa.String(128), nullable=True),
        sa.Column("changed_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint(
            "type_slug", "level", "harness", "ref", name="uq_content_type_generators"
        ),
        sa.UniqueConstraint("default_key", name="uq_content_type_generators_default"),
    )
    op.create_index("ix_content_type_generators_type_slug", _TABLE, ["type_slug"])


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        op.drop_table(_TABLE)
