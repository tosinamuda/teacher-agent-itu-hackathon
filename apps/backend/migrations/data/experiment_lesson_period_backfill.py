"""Backfill ``experiments.lesson_period_id`` from each experiment's plan version.

Decoupling the experiment from the production plan adds ``experiments.
lesson_period_id`` (the lesson the experiment studies). Existing experiments
only carry ``plan_version_id``; this derives the lesson from it:

    experiment.plan_version_id -> plan_versions.version_id
        -> lesson_plans.plan_id -> lesson_plans.lesson_period_id

Idempotent (``WHERE lesson_period_id IS NULL`` guard). Run AFTER the Alembic
migration adds the column and BEFORE the ``(workspace, lesson_period_id)`` unique
constraint is created (the constraint addition would otherwise allow duplicate
NULLs to slip the intended one-experiment-per-lesson rule).

Invocation: see ``scripts/seed_experiment_lesson_period.py``.
"""

from __future__ import annotations

from dataclasses import dataclass

import sqlalchemy as sa


@dataclass(frozen=True)
class _BackfillReport:
    experiments_scanned: int
    experiments_updated: int
    residual_null: int


def backfill_experiment_lesson_period(conn: sa.Connection) -> _BackfillReport:
    """Derive ``lesson_period_id`` for every experiment that lacks one."""
    scanned = conn.execute(sa.text("SELECT count(*) FROM experiments")).scalar_one()
    updated = conn.execute(
        sa.text(
            """
            UPDATE experiments e
            SET lesson_period_id = lp.lesson_period_id
            FROM plan_versions pv
            JOIN lesson_plans lp ON lp.plan_id = pv.plan_id
            WHERE e.plan_version_id = pv.version_id
              AND e.lesson_period_id IS NULL
              AND lp.lesson_period_id IS NOT NULL
            """
        )
    ).rowcount
    residual = conn.execute(
        sa.text("SELECT count(*) FROM experiments WHERE lesson_period_id IS NULL")
    ).scalar_one()
    return _BackfillReport(
        experiments_scanned=int(scanned),
        experiments_updated=int(updated),
        residual_null=int(residual),
    )
