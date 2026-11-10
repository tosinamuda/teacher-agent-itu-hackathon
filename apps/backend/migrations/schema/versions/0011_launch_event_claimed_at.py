"""Record when a relay claimed a launch event.

A relay that dies between claiming and publishing leaves the row CLAIMED. Reconciliation
returns it to PENDING once the claim is older than the lease, which needs the timestamp.

Revision ID: 0011_launch_event_claimed_at
Revises: 0010_experiment_launch_event_outbox
Create Date: 2026-08-14
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0011_launch_event_claimed_at"
down_revision = "0010_experiment_launch_event_outbox"
branch_labels = None
depends_on = None

_TABLE = "experiment_launch_events"


def upgrade() -> None:
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if not has_column(_TABLE, "claimed_at"):
        op.add_column(_TABLE, sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column(_TABLE, "claimed_at"):
        op.drop_column(_TABLE, "claimed_at")
