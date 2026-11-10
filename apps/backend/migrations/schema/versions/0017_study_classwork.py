"""Keep the MSc study's classwork as the study recorded it, beside the lessons it came from.

Revision ID: 0017_study_classwork
Revises: 0016_study_ratings
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0017_study_classwork"
down_revision = "0016_study_ratings"
branch_labels = None
depends_on = None

_TABLES = ("study_classwork_answers", "study_classwork_scripts", "study_classwork_questions")


def _plan_version(name: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(["plan_version_id"], ["plan_versions.version_id"], name=name)


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    if not has_table("study_classwork_questions"):
        op.create_table(
            "study_classwork_questions",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("plan_version_id", sa.String(64), nullable=False),
            sa.Column("assessed_set", sa.Text(), nullable=False),
            sa.Column("question_n", sa.Integer(), nullable=False),
            sa.Column("lesson_objective_id", sa.String(64), nullable=False),
            sa.Column("text", sa.Text(), nullable=False),
            sa.Column("answer", sa.Text(), nullable=True),
            sa.Column("answer_source", sa.String(32), nullable=True),
            _plan_version("fk_study_questions_plan_version_id"),
        )
        op.create_index(
            "ix_study_classwork_questions_plan_version_id",
            "study_classwork_questions",
            ["plan_version_id"],
        )
    if not has_table("study_classwork_scripts"):
        op.create_table(
            "study_classwork_scripts",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("plan_version_id", sa.String(64), nullable=False),
            sa.Column("student_id", sa.String(64), nullable=False),
            sa.Column("teacher_total", sa.String(16), nullable=False),
            sa.Column("capture_complete", sa.Boolean(), nullable=False),
            _plan_version("fk_study_scripts_plan_version_id"),
            sa.ForeignKeyConstraint(
                ["student_id"], ["student_profiles.student_id"], name="fk_study_scripts_student_id"
            ),
        )
        op.create_index(
            "ix_study_classwork_scripts_plan_version_id",
            "study_classwork_scripts",
            ["plan_version_id"],
        )
    if not has_table("study_classwork_answers"):
        op.create_table(
            "study_classwork_answers",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("script_id", UUID(as_uuid=True), nullable=False),
            sa.Column("plan_version_id", sa.String(64), nullable=False),
            sa.Column("question_n", sa.Integer(), nullable=False),
            sa.Column("mark", sa.String(16), nullable=False),
            sa.Column("uncertain", sa.Boolean(), nullable=False),
            sa.Column("working", sa.Text(), nullable=False),
            sa.Column("misconception_code", sa.String(64), nullable=True),
            sa.Column("misconception_why", sa.Text(), nullable=True),
            sa.ForeignKeyConstraint(
                ["script_id"], ["study_classwork_scripts.id"], name="fk_study_answers_script_id"
            ),
            _plan_version("fk_study_answers_plan_version_id"),
        )
        op.create_index(
            "ix_study_classwork_answers_script_id", "study_classwork_answers", ["script_id"]
        )


def downgrade() -> None:
    from app.db.migration_utils import has_table

    for table in _TABLES:
        if has_table(table):
            op.drop_table(table)
