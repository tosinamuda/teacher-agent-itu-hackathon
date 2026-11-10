"""Let a spec list the external MCP servers its content is written with.

Revision ID: 0030_spec_external_mcp
Revises: 0029_skill_reference_files
Create Date: 2026-09-29
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0030_spec_external_mcp"
down_revision = "0029_skill_reference_files"
branch_labels = None
depends_on = None

_TABLE = "content_specifications"


def upgrade() -> None:
    from app.db.coltypes import JSON
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds the column on a fresh DB (see migration_utils).
    if not has_column(_TABLE, "mcp"):
        op.add_column(_TABLE, sa.Column("mcp", JSON(), nullable=True))


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column(_TABLE, "mcp"):
        op.drop_column(_TABLE, "mcp")
