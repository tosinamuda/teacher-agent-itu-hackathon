"""Let a content draft adapt a lesson's content to one learner.

Revision ID: 0037_draft_student
Revises: 0036_artefact_review_reason
Create Date: 2026-10-19
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0037_draft_student"
down_revision = "0036_artefact_review_reason"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds this column on a fresh DB.
    if not has_column("content_drafts", "student_id"):
        op.add_column("content_drafts", sa.Column("student_id", sa.String(64), nullable=True))
        op.create_index("ix_content_drafts_student_id", "content_drafts", ["student_id"])


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column("content_drafts", "student_id"):
        op.drop_index("ix_content_drafts_student_id", table_name="content_drafts")
        op.drop_column("content_drafts", "student_id")
