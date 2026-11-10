"""Keep the MSc study's published transcripts: how each lesson and script became data.

Revision ID: 0022_study_transcripts
Revises: 0021_submission_survey_pending
Create Date: 2026-09-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0022_study_transcripts"
down_revision = "0021_submission_survey_pending"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if has_table("study_transcripts"):
        return
    op.create_table(
        "study_transcripts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("plan_version_id", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("student_id", sa.String(64), nullable=True),
        sa.Column("pages", sa.JSON(), nullable=False),
        sa.Column("header", sa.JSON(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("source_path", sa.String(255), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.ForeignKeyConstraint(
            ["plan_version_id"],
            ["plan_versions.version_id"],
            name="fk_study_transcripts_plan_version_id",
        ),
    )
    op.create_index(
        "ix_study_transcripts_plan_version_id", "study_transcripts", ["plan_version_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_study_transcripts_plan_version_id", table_name="study_transcripts")
    op.drop_table("study_transcripts")
