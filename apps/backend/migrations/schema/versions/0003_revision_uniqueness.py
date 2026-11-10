"""Enforce one revision thread per artefact + unique turn numbers per thread.

The (artefact_type, subject_id) pair was a non-unique index with "one thread per
artefact" treated as an in-code invariant; concurrent "open revision chat" could
fork it. Promote it to a unique constraint, and add (thread_db_id, turn_number)
uniqueness so a concurrent turn can't reuse a number. Fresh deploys get these via
``create_all``; this runs only on already-deployed DBs.

Revision ID: 0003_revision_uniqueness
Revises: 0002_concurrency_constraints
Create Date: 2026-06-16
"""

from __future__ import annotations

from alembic import op

revision = "0003_revision_uniqueness"
down_revision = "0002_concurrency_constraints"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_index, has_unique_constraint

    # Replace the non-unique (artefact_type, subject_id) index with a unique one. On a fresh
    # DB 0001's create_all already builds the model's CURRENT shape (the unique constraint, no
    # old index), so the drop/creates are guarded to be idempotent (see migration_utils).
    if has_index("revision_threads", "ix_revision_threads_type_subject"):
        op.drop_index("ix_revision_threads_type_subject", table_name="revision_threads")
    if not has_unique_constraint("revision_threads", "uq_revision_thread_type_subject"):
        op.create_unique_constraint(
            "uq_revision_thread_type_subject",
            "revision_threads",
            ["artefact_type", "subject_id"],
        )
    if not has_unique_constraint("revision_turns", "uq_revision_turn_thread_number"):
        op.create_unique_constraint(
            "uq_revision_turn_thread_number",
            "revision_turns",
            ["thread_db_id", "turn_number"],
        )


def downgrade() -> None:
    op.drop_constraint("uq_revision_turn_thread_number", "revision_turns", type_="unique")
    op.drop_constraint("uq_revision_thread_type_subject", "revision_threads", type_="unique")
    op.create_index(
        "ix_revision_threads_type_subject",
        "revision_threads",
        ["artefact_type", "subject_id"],
    )
