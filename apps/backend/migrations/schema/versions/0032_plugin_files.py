"""Keep the files a plugin was installed with, so a run can copy them.

Revision ID: 0032_plugin_files
Revises: 0031_content_plugins
Create Date: 2026-09-30
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0032_plugin_files"
down_revision = "0031_content_plugins"
branch_labels = None
depends_on = None

_TABLE = "content_plugins"


def upgrade() -> None:
    from app.db.coltypes import JSON
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds the column on a fresh DB (see migration_utils).
    if not has_column(_TABLE, "files"):
        op.add_column(_TABLE, sa.Column("files", JSON(), nullable=True))


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column(_TABLE, "files"):
        op.drop_column(_TABLE, "files")
