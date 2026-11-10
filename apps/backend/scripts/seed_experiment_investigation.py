"""File every experiment into a parent study (``experiments.investigation_db_id``).

Invocation::

    uv run python -m scripts.seed_experiment_investigation

Idempotent. Run AFTER ``20260608_study_parent_a`` adds the nullable column and
BEFORE ``20260608_study_parent_b`` enforces NOT NULL + drops ``investigation_lessons``.
Exits nonzero if any experiment is left without a study.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.experiment_investigation_backfill import (
    backfill_experiment_investigation,
)


def main() -> int:
    with sync_engine.begin() as conn:
        result = backfill_experiment_investigation(conn)
    print("experiment investigation backfill complete:")
    print(f"  unfiled_created     = {result.unfiled_created}")
    print(f"  filed_into_demo     = {result.filed_into_demo}")
    print(f"  filed_into_unfiled  = {result.filed_into_unfiled}")
    print(f"  residual_null       = {result.residual_null}")
    return 0 if result.residual_null == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
