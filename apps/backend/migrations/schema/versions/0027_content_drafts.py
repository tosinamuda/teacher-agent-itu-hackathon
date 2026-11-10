"""Keep drafts of content written part by part: one checked part per unit until submitted.

Revision ID: 0027_content_drafts
Revises: 0026_content_types
Create Date: 2026-09-26
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0027_content_drafts"
down_revision = "0026_content_types"
branch_labels = None
depends_on = None

_TABLE = "content_drafts"


def upgrade() -> None:
    from app.db.coltypes import JSON, UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("draft_id", sa.String(64), nullable=False),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("spec_revision", sa.Integer(), nullable=False),
        sa.Column("plan_version_id", sa.String(64), nullable=True),
        sa.Column("session_id", sa.String(64), nullable=True),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("unit", sa.String(32), nullable=False),
        sa.Column("units", JSON(), nullable=False),
        sa.Column("parts", JSON(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("saved_as", sa.String(64), nullable=True),
        sa.Column("created_by", sa.String(128), nullable=False),
        sa.Column("author", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_content_drafts_draft_id", _TABLE, ["draft_id"], unique=True)
    op.create_index("ix_content_drafts_plan_version_id", _TABLE, ["plan_version_id"])
    op.create_index("ix_content_drafts_session_id", _TABLE, ["session_id"])


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        op.drop_table(_TABLE)
