"""What a teacher has switched: optional materials they hide, and whether runs replay.

Revision ID: 0039_teacher_preferences
Revises: 0038_plan_version_closed
Create Date: 2026-11-09
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0039_teacher_preferences"
down_revision = "0038_plan_version_closed"
branch_labels = None
depends_on = None

_TABLE = "teacher_preferences"


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds the table on a fresh DB (see migration_utils).
    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("auth_id", sa.String(128), nullable=False),
        sa.Column("hidden_types", sa.JSON(), nullable=False),
        sa.Column("replay_runs", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("auth_id", name="uq_teacher_preferences_auth_id"),
    )


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        op.drop_table(_TABLE)
