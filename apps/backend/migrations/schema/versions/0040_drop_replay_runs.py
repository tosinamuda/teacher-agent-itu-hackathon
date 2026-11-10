"""Drop the teacher setting that played back recorded runs.

Revision ID: 0040_drop_replay_runs
Revises: 0039_teacher_preferences
Create Date: 2026-11-09
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0040_drop_replay_runs"
down_revision = "0039_teacher_preferences"
branch_labels = None
depends_on = None

_TABLE = "teacher_preferences"
_COLUMN = "replay_runs"


def upgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column(_TABLE, _COLUMN):
        op.drop_column(_TABLE, _COLUMN)


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if not has_column(_TABLE, _COLUMN):
        op.add_column(
            _TABLE, sa.Column(_COLUMN, sa.Boolean(), server_default=sa.text("0"), nullable=False)
        )
