"""Add delivery_count to the durable-task rows (poison-message redelivery bound).

Under acks_late + reject_on_worker_lost a task that crashes the worker is redelivered and
re-claimed. ``delivery_count`` (incremented on each claim) lets the claim cap the number of
attempts, so a poison message — a task that crashes every time — is marked FAILED instead of
looping forever on the single solo worker. Additive: existing rows backfill to 0.

Revision ID: 0007_delivery_count_poison_bound
Revises: 0006_student_pack_gen_artefact_version
Create Date: 2026-06-17
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0007_delivery_count_poison_bound"
down_revision = "0006_student_pack_gen_artefact_version"
branch_labels = None
depends_on = None

_TABLES = ("experiment_executions", "student_pack_generations")


def upgrade() -> None:
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    for table in _TABLES:
        if not has_column(table, "delivery_count"):
            op.add_column(
                table,
                sa.Column("delivery_count", sa.Integer(), nullable=False, server_default="0"),
            )


def downgrade() -> None:
    for table in _TABLES:
        op.drop_column(table, "delivery_count")
