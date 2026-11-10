"""Live progress is a table: each event a row on a channel, read by the experiment's WebSocket.

A job's process writes events here and the API relays the new ones, so progress needs
nothing but the database the job already writes to.

Revision ID: 0024_progress_events
Revises: 0023_jobs
Create Date: 2026-09-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

from app.db.coltypes import JSON, MICROSECOND_DATETIME

revision = "0024_progress_events"
down_revision = "0023_jobs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if has_table("progress_events"):
        return
    op.create_table(
        "progress_events",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("channel", sa.String(128), nullable=False),
        sa.Column("payload", JSON, nullable=False),
        sa.Column("created_at", MICROSECOND_DATETIME, nullable=False),
    )
    op.create_index("ix_progress_events_channel", "progress_events", ["channel"])
    op.create_index("ix_progress_events_created_at", "progress_events", ["created_at"])


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table("progress_events"):
        op.drop_table("progress_events")
