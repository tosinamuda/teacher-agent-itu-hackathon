"""Keep each content type's specification as data, one row per revision.

Revision ID: 0012_content_specifications
Revises: 0011_launch_event_claimed_at
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0012_content_specifications"
down_revision = "0011_launch_event_claimed_at"
branch_labels = None
depends_on = None

_TABLE = "content_specifications"


def upgrade() -> None:
    from app.db.coltypes import JSON, UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("material", sa.Text(), nullable=False),
        sa.Column("audience", sa.Text(), nullable=False),
        sa.Column("levels", JSON(), nullable=False),
        sa.Column("structure", JSON(), nullable=False),
        sa.Column("requirements", JSON(), nullable=False),
        sa.Column("adaptable", JSON(), nullable=False),
        sa.Column("created_by", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("kind", "revision", name="uq_content_specifications_kind_revision"),
    )
    op.create_index("ix_content_specifications_kind", _TABLE, ["kind"])


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        op.drop_table(_TABLE)
