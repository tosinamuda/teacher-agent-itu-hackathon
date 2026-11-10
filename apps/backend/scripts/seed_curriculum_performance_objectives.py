"""Seed the P5.6 Phase 2 ``curriculum_performance_objectives`` table.

Invocation::

    uv run python -m scripts.seed_curriculum_performance_objectives

Idempotent (select-then-insert/update on ``curriculum_objective_id``). Source:
the existing ``ao_textbook_objective_links`` rows in the expert_content domain, projected
to the canonical one-row-per-objective grain.

Runs AFTER the Alembic migration that creates the table and BEFORE the
``plan_version_objectives.curriculum_objective_id`` FK is added — exits
non-zero if any plan_version_objective would orphan.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.p56_phase2_curriculum_performance_objectives_backfill import (
    backfill_curriculum_performance_objectives,
)


def main() -> int:
    with sync_engine.begin() as conn:
        result = backfill_curriculum_performance_objectives(conn)
    print("curriculum_performance_objectives backfill complete:")
    print(f"  rows_written                        = {result.rows_written}")
    print(f"  distinct_subtopics                  = {result.distinct_subtopics}")
    print(f"  plan_version_objectives_orphans     = {result.plan_version_objectives_orphans}")
    return 0 if result.plan_version_objectives_orphans == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
