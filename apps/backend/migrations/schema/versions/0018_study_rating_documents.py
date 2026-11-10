"""Keep each returned rating document: how much came back answered, when, and its comment.

Revision ID: 0018_study_rating_documents
Revises: 0017_study_classwork
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0018_study_rating_documents"
down_revision = "0017_study_classwork"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_column, has_table

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    if not has_column("study_comparative_judgements", "lesson_objective_id"):
        op.add_column(
            "study_comparative_judgements",
            sa.Column("lesson_objective_id", sa.String(64), nullable=True),
        )
    if not has_table("study_rating_documents"):
        op.create_table(
            "study_rating_documents",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("document", sa.String(512), nullable=False, unique=True),
            sa.Column("rater", sa.String(32), nullable=False),
            sa.Column("rater_db_id", UUID(as_uuid=True), nullable=False),
            sa.Column("delivery_order", sa.Integer(), nullable=False),
            sa.Column("packet", sa.String(32), nullable=False),
            sa.Column("artefact_a_id", sa.String(64), nullable=False),
            sa.Column("artefact_b_id", sa.String(64), nullable=True),
            sa.Column("part", sa.Integer(), nullable=False),
            sa.Column("answer_sheets", sa.Integer(), nullable=False),
            sa.Column("marks", sa.Integer(), nullable=False),
            sa.Column("rows_unanswered", sa.Integer(), nullable=False),
            sa.Column("state", sa.String(16), nullable=False),
            sa.Column("date_completed", sa.String(64), nullable=True),
            sa.Column("closing_comment", sa.Text(), nullable=True),
            sa.ForeignKeyConstraint(
                ["artefact_a_id"], ["artefacts.artefact_id"], name="fk_study_documents_a_id"
            ),
            sa.ForeignKeyConstraint(
                ["artefact_b_id"], ["artefacts.artefact_id"], name="fk_study_documents_b_id"
            ),
            sa.ForeignKeyConstraint(
                ["rater_db_id"], ["evaluation_raters.id"], name="fk_study_documents_rater_db_id"
            ),
        )
        for column in ("artefact_a_id", "artefact_b_id", "rater_db_id"):
            op.create_index(
                f"ix_study_rating_documents_{column}", "study_rating_documents", [column]
            )


def downgrade() -> None:
    from app.db.migration_utils import has_column, has_table

    if has_table("study_rating_documents"):
        op.drop_table("study_rating_documents")
    if has_column("study_comparative_judgements", "lesson_objective_id"):
        op.drop_column("study_comparative_judgements", "lesson_objective_id")
