"""Let a skill carry reference files, markdown a writer reads when its instructions say so.

Revision ID: 0029_skill_reference_files
Revises: 0028_content_skills
Create Date: 2026-09-29
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0029_skill_reference_files"
down_revision = "0028_content_skills"
branch_labels = None
depends_on = None

_TABLE = "content_skills"


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
