"""Record when a plan version's study concluded; its lesson's record is read-only from then.

Revision ID: 0015_plan_version_concluded_at
Revises: 0014_drop_lesson_notes
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0015_plan_version_concluded_at"
down_revision = "0014_drop_lesson_notes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_column

    if not has_column("plan_versions", "concluded_at"):
        op.add_column("plan_versions", sa.Column("concluded_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column("plan_versions", "concluded_at"):
        op.drop_column("plan_versions", "concluded_at")
