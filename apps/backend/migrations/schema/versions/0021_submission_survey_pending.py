"""Record on a submission that its post-class survey has not arrived yet.

Revision ID: 0021_submission_survey_pending
Revises: 0020_figures
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0021_submission_survey_pending"
down_revision = "0020_figures"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if not has_column("exit_ticket_submissions", "survey_pending"):
        op.add_column(
            "exit_ticket_submissions",
            sa.Column("survey_pending", sa.Boolean(), nullable=False, server_default=sa.false()),
        )


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column("exit_ticket_submissions", "survey_pending"):
        op.drop_column("exit_ticket_submissions", "survey_pending")
