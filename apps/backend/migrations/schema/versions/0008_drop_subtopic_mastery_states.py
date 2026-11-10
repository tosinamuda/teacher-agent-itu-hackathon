"""Drop the dormant subtopic_mastery_states table.

The per-subtopic ``SubtopicMasteryState`` was superseded by the per-objective
``ObjectiveLearnerState`` (computed from the diagnostic and carried on the
focal-case ``learner_state_snapshot``); nothing has read or written the table.
Pure-schema removal of dead state.

Idempotent: a fresh DB never creates it (0001's ``create_all`` reads the ORM
metadata, which no longer defines the model), so the drop is guarded by an
existence check; the downgrade only recreates it when absent.

Revision ID: 0008_drop_subtopic_mastery_states
Revises: 0007_delivery_count_poison_bound
Create Date: 2026-06-19
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0008_drop_subtopic_mastery_states"
down_revision = "0007_delivery_count_poison_bound"
branch_labels = None
depends_on = None

_TABLE = "subtopic_mastery_states"


def upgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        op.drop_table(_TABLE)


def downgrade() -> None:
    from app.db.coltypes import JSON, UUID
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "student_id",
            sa.String(64),
            sa.ForeignKey("student_profiles.student_id"),
            nullable=False,
        ),
        sa.Column(
            "subtopic_id",
            sa.String(200),
            sa.ForeignKey("curriculum_subtopics.subtopic_id"),
            nullable=False,
        ),
        sa.Column(
            "plan_version_id",
            sa.String(64),
            sa.ForeignKey("plan_versions.version_id"),
            nullable=False,
        ),
        sa.Column("mastery_score", sa.Float, nullable=False),
        sa.Column("policy", sa.String(32), nullable=False),
        sa.Column("diagnosed_misconceptions", JSON, nullable=True),
        sa.Column("item_count", sa.Integer, nullable=False),
        sa.Column("computed_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )
