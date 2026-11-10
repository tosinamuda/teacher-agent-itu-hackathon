"""Backfill ``experiments.lesson_period_id`` from each experiment's plan version.

Invocation::

    uv run python -m scripts.seed_experiment_lesson_period

Idempotent. Run AFTER the Alembic migration adds ``lesson_period_id`` and BEFORE
the ``(workspace, lesson_period_id)`` unique constraint migration. Exits nonzero
if any experiment is left with a NULL ``lesson_period_id`` (a legacy experiment
whose plan_version was deleted — investigate before adding the constraint).
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.experiment_lesson_period_backfill import (
    backfill_experiment_lesson_period,
)


def main() -> int:
    with sync_engine.begin() as conn:
        result = backfill_experiment_lesson_period(conn)
    print("experiment lesson_period backfill complete:")
    print(f"  experiments_scanned = {result.experiments_scanned}")
    print(f"  experiments_updated = {result.experiments_updated}")
    print(f"  residual_null       = {result.residual_null}")
    return 0 if result.residual_null == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
