"""Background work is a table: jobs, and the runners that run them.

A job row is written in the same transaction as the change that asks for it, and the API
process's runner claims it from here. The launch outbox, ``experiment_launch_events``, was
the same idea for one kind of work, and goes.

``active_subject`` holds the subject while a job is unfinished and is NULLed when it ends.
MySQL allows repeated NULLs in a unique index, so "at most one unfinished job of a kind per
subject" needs no partial index, which MySQL does not have.

Revision ID: 0023_jobs
Revises: 0022_study_transcripts
Create Date: 2026-09-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

from app.db.coltypes import JSON, MICROSECOND_DATETIME, UUID

revision = "0023_jobs"
down_revision = "0022_study_transcripts"
branch_labels = None
depends_on = None

_OUTBOX = "experiment_launch_events"


def upgrade() -> None:
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    if not has_table("jobs"):
        op.create_table(
            "jobs",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("job_id", sa.String(64), nullable=False),
            sa.Column("kind", sa.String(128), nullable=False),
            sa.Column("args", JSON, nullable=False),
            sa.Column("subject", sa.String(128), nullable=True),
            sa.Column("active_subject", sa.String(128), nullable=True),
            sa.Column("state", sa.String(16), nullable=False),
            sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("runner", sa.String(128), nullable=True),
            sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("last_error", sa.Text(), nullable=True),
            sa.Column("created_at", MICROSECOND_DATETIME, nullable=False),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
            sa.UniqueConstraint("active_subject", "kind", name="uq_jobs_active_subject"),
        )
        op.create_index("ix_jobs_job_id", "jobs", ["job_id"], unique=True)
        op.create_index("ix_jobs_kind", "jobs", ["kind"])
        op.create_index("ix_jobs_subject", "jobs", ["subject"])
        op.create_index("ix_jobs_state_created_at", "jobs", ["state", "created_at"])
        op.create_index("ix_jobs_state_lease_expires_at", "jobs", ["state", "lease_expires_at"])
    if not has_table("job_runners"):
        op.create_table(
            "job_runners",
            sa.Column("runner", sa.String(128), primary_key=True),
            sa.Column("slots", sa.Integer(), nullable=False),
            sa.Column("running", sa.Integer(), nullable=False),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("seen_at", sa.DateTime(timezone=True), nullable=False),
        )
    if has_table(_OUTBOX):
        # Dropping the table takes its indexes with it; MySQL refuses to drop the index
        # backing a foreign key on its own (errno 1553).
        op.drop_table(_OUTBOX)


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if not has_table(_OUTBOX):
        op.create_table(
            _OUTBOX,
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
            sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["execution_db_id"], ["experiment_executions.id"]),
            sa.UniqueConstraint(
                "pending_execution_db_id", "dispatch_kind", name="uq_launch_event_undelivered"
            ),
        )
        op.create_index(f"ix_{_OUTBOX}_launch_event_id", _OUTBOX, ["launch_event_id"], unique=True)
        op.create_index(f"ix_{_OUTBOX}_execution_db_id", _OUTBOX, ["execution_db_id"])
        op.create_index(f"ix_{_OUTBOX}_delivery_state", _OUTBOX, ["delivery_state"])
    for table in ("job_runners", "jobs"):
        if has_table(table):
            op.drop_table(table)
