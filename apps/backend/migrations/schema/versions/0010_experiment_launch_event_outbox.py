"""Add the experiment launch-event outbox.

Launch commits a QUEUED execution and then publishes to Celery. A crash between the two
strands the execution at QUEUED with no message, and there is no reconcile sweep. This table
gives each launch intent a durable row written in the same transaction as the execution, so
EXP-005A can relay what was never published.

``pending_execution_db_id`` holds the execution id while the event is undelivered and is
NULLed on delivery. Both MySQL and PostgreSQL allow repeated NULLs in a unique index, so the
"at most one undelivered event per execution and dispatch kind" rule needs no partial index —
which MySQL does not support.

Revision ID: 0010_experiment_launch_event_outbox
Revises: 0009_attachments_and_onbehalf
Create Date: 2026-08-14
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

from app.db.coltypes import JSON, UUID

revision = "0010_experiment_launch_event_outbox"
down_revision = "0009_attachments_and_onbehalf"
branch_labels = None
depends_on = None

_TABLE = "experiment_launch_events"


def upgrade() -> None:
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if has_table(_TABLE):
        return

    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("launch_event_id", sa.String(64), nullable=False),
        sa.Column("execution_db_id", UUID(as_uuid=True), nullable=False),
        sa.Column("pending_execution_db_id", UUID(as_uuid=True), nullable=True),
        sa.Column("dispatch_kind", sa.String(64), nullable=False),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("payload", JSON, nullable=False),
        sa.Column("delivery_state", sa.String(16), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["execution_db_id"], ["experiment_executions.id"]),
        sa.UniqueConstraint(
            "pending_execution_db_id", "dispatch_kind", name="uq_launch_event_undelivered"
        ),
    )
    op.create_index(f"ix_{_TABLE}_launch_event_id", _TABLE, ["launch_event_id"], unique=True)
    op.create_index(f"ix_{_TABLE}_execution_db_id", _TABLE, ["execution_db_id"])
    op.create_index(f"ix_{_TABLE}_delivery_state", _TABLE, ["delivery_state"])


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if not has_table(_TABLE):
        return
    # Drop the table outright rather than its indexes first: MySQL refuses to drop the
    # index backing a foreign key (errno 1553), and dropping the table takes them with it.
    op.drop_table(_TABLE)
