"""Record each install, update and removal of an artefact plugin.

Revision ID: 0031_content_plugins
Revises: 0030_spec_external_mcp
Create Date: 2026-09-30
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0031_content_plugins"
down_revision = "0030_spec_external_mcp"
branch_labels = None
depends_on = None

_TABLE = "content_plugins"


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds the table on a fresh DB (see migration_utils).
    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("version", sa.String(64), nullable=False),
        sa.Column("digest", sa.String(64), nullable=False),
        sa.Column("type_slug", sa.String(64), nullable=False),
        sa.Column("spec_revision", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("installed_by", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("name", "revision", name="uq_content_plugins_revision"),
    )
    op.create_index("ix_content_plugins_name", _TABLE, ["name"])
    op.create_index("ix_content_plugins_type_slug", _TABLE, ["type_slug"])


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        op.drop_table(_TABLE)
