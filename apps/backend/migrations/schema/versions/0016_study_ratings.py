"""Keep the MSc study's ratings in the study's own instrument, beside the notes they rated.

Revision ID: 0016_study_ratings
Revises: 0015_plan_version_concluded_at
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0016_study_ratings"
down_revision = "0015_plan_version_concluded_at"
branch_labels = None
depends_on = None


def _common() -> list[sa.Column]:
    from app.db.coltypes import UUID

    return [
        sa.Column("rater", sa.String(32), nullable=False),
        sa.Column("rater_db_id", UUID(as_uuid=True), nullable=False),
        sa.Column("delivery_order", sa.Integer(), nullable=False),
        sa.Column("packet", sa.String(32), nullable=False),
    ]


def _rater(name: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(["rater_db_id"], ["evaluation_raters.id"], name=name)


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    if not has_table("study_criterion_scores"):
        op.create_table(
            "study_criterion_scores",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("artefact_id", sa.String(64), nullable=False),
            *_common(),
            sa.Column("objective_index", sa.Integer(), nullable=False),
            sa.Column("lesson_objective_id", sa.String(64), nullable=False),
            sa.Column("criterion_id", sa.String(64), nullable=False),
            sa.Column("score", sa.Integer(), nullable=False),
            sa.Column("comment", sa.Text(), nullable=True),
            sa.Column("document", sa.String(512), nullable=False),
            sa.ForeignKeyConstraint(
                ["artefact_id"], ["artefacts.artefact_id"], name="fk_study_scores_artefact_id"
            ),
            _rater("fk_study_scores_rater_db_id"),
        )
        op.create_index(
            "ix_study_criterion_scores_rater_db_id", "study_criterion_scores", ["rater_db_id"]
        )
        op.create_index(
            "ix_study_criterion_scores_artefact_id", "study_criterion_scores", ["artefact_id"]
        )
    if not has_table("study_comparative_judgements"):
        op.create_table(
            "study_comparative_judgements",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("artefact_a_id", sa.String(64), nullable=False),
            sa.Column("artefact_b_id", sa.String(64), nullable=False),
            *_common(),
            sa.Column("ability_stratum", sa.String(16), nullable=False),
            sa.Column("objective_index", sa.Integer(), nullable=False),
            sa.Column("criterion_id", sa.String(64), nullable=False),
            sa.Column("choice", sa.String(32), nullable=False),
            sa.Column("favoured_condition", sa.String(8), nullable=True),
            sa.Column("comment", sa.Text(), nullable=True),
            sa.Column("document", sa.String(512), nullable=False),
            sa.ForeignKeyConstraint(
                ["artefact_a_id"], ["artefacts.artefact_id"], name="fk_study_judgements_a_id"
            ),
            sa.ForeignKeyConstraint(
                ["artefact_b_id"], ["artefacts.artefact_id"], name="fk_study_judgements_b_id"
            ),
            _rater("fk_study_judgements_rater_db_id"),
        )
        for column in ("artefact_a_id", "artefact_b_id", "rater_db_id"):
            op.create_index(
                f"ix_study_comparative_judgements_{column}",
                "study_comparative_judgements",
                [column],
            )


def downgrade() -> None:
    from app.db.migration_utils import has_table

    for table in ("study_comparative_judgements", "study_criterion_scores"):
        if has_table(table):
            op.drop_table(table)
