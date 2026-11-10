"""A job keeps what its handler returned, and who asked for it.

A teacher's generation runs as a job, so the page that asked for it follows the job: the
result says where the made content is, and the requester is who may follow it.

Revision ID: 0025_job_results
Revises: 0024_progress_events
Create Date: 2026-09-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

from app.db.coltypes import JSON

revision = "0025_job_results"
down_revision = "0024_progress_events"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_column, has_index

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    if not has_column("jobs", "result"):
        op.add_column("jobs", sa.Column("result", JSON, nullable=True))
    if not has_column("jobs", "requested_by"):
        op.add_column("jobs", sa.Column("requested_by", sa.String(128), nullable=True))
    if not has_index("jobs", "ix_jobs_requested_by"):
        op.create_index("ix_jobs_requested_by", "jobs", ["requested_by"])


def downgrade() -> None:
    from app.db.migration_utils import has_column, has_index

    if has_index("jobs", "ix_jobs_requested_by"):
        op.drop_index("ix_jobs_requested_by", table_name="jobs")
    for column in ("requested_by", "result"):
        if has_column("jobs", column):
            op.drop_column("jobs", column)
