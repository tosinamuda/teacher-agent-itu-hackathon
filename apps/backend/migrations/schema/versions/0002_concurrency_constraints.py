"""Composite unique constraints that close get-or-create concurrency races.

Several provisioning/dispatch paths are "find by natural key, else insert" — a
read-then-write race where two concurrent callers both miss and both insert
(duplicate classes / courses / offerings / workspaces; duplicate execution
attempt numbers). Backing each natural key with a DB unique constraint makes the
loser fail at commit, where the application catches it and re-selects/retries.

Fresh deploys get these via ``create_all`` (the constraints live on the models)
and are stamped to head, so this revision runs only on already-deployed DBs. It
is dialect-agnostic (``create_unique_constraint`` on both MySQL and Postgres).

Revision ID: 0002_concurrency_constraints
Revises: 0001_baseline
Create Date: 2026-06-16
"""

from __future__ import annotations

from alembic import op

revision = "0002_concurrency_constraints"
down_revision = "0001_baseline"
branch_labels = None
depends_on = None

# (constraint_name, table, columns) — the natural keys made unique.
_CONSTRAINTS: list[tuple[str, str, list[str]]] = [
    ("uq_classes_school_name", "classes", ["school_id", "name"]),
    ("uq_courses_subject_grade", "courses_curriculum", ["subject_id", "grade_level_id"]),
    (
        "uq_tcs_class_course_term_year",
        "term_class_subjects",
        ["class_id", "course_id", "term", "year"],
    ),
    ("uq_workspace_teacher_tcs", "teacher_workspaces", ["teacher_id", "term_class_subject_id"]),
    (
        "uq_execution_attempt",
        "experiment_executions",
        ["experiment_db_id", "hypothesis", "attempt_number"],
    ),
]


def upgrade() -> None:
    from app.db.migration_utils import has_unique_constraint

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    for name, table, columns in _CONSTRAINTS:
        if not has_unique_constraint(table, name):
            op.create_unique_constraint(name, table, columns)


def downgrade() -> None:
    for name, table, _columns in reversed(_CONSTRAINTS):
        op.drop_constraint(name, table, type_="unique")
