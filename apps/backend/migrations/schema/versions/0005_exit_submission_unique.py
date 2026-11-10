"""Enforce one exit-ticket submission per (student, lesson).

A student could submit the same lesson's assessment multiple times: the read path is
newest-wins, but each submit appended a fresh ``ExitTicketSubmission`` AND a full set
of ``StudentItemResponse`` rows, double-counting per-objective mastery and learner-
evidence. Product decision (2026-06-17): first submission wins; a re-submit is a 409.

De-dups any existing rows — keeping the NEWEST per (student, plan), to match the prior
newest-wins read — before adding the unique. The de-dup is MySQL multi-table-DELETE
syntax; the unique itself is dialect-agnostic and also lives on the model (create_all).

Revision ID: 0005_exit_submission_unique
Revises: 0004_casbin_rule_unique
Create Date: 2026-06-17
"""

from __future__ import annotations

from alembic import op

revision = "0005_exit_submission_unique"
down_revision = "0004_casbin_rule_unique"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop older duplicates, keeping the newest submission per (student, plan). Tie-break
    # on id so the delete is deterministic when created_at collides.
    op.execute(
        """
        DELETE older FROM exit_ticket_submissions older
        JOIN exit_ticket_submissions newer
          ON older.student_id = newer.student_id
         AND older.plan_version_id = newer.plan_version_id
         AND (newer.created_at > older.created_at
              OR (newer.created_at = older.created_at AND newer.id > older.id))
        """
    )
    from app.db.migration_utils import has_unique_constraint

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    # (The de-dup DELETE above is a harmless no-op on the empty fresh DB.)
    if not has_unique_constraint(
        "exit_ticket_submissions", "uq_exit_ticket_submission_student_plan"
    ):
        op.create_unique_constraint(
            "uq_exit_ticket_submission_student_plan",
            "exit_ticket_submissions",
            ["student_id", "plan_version_id"],
        )


def downgrade() -> None:
    op.drop_constraint(
        "uq_exit_ticket_submission_student_plan",
        "exit_ticket_submissions",
        type_="unique",
    )
