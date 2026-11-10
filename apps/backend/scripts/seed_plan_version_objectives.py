"""Seed the P5.6 ``plan_version_objectives`` table from the JSON source.

Invocation::

    uv run python -m scripts.seed_plan_version_objectives

Idempotent (select-then-insert/update on the ``(plan_version_id,
lesson_objective_id)`` natural key): re-running mirrors any JSON drift back
into the table. Run this AFTER the Alembic migration creates the table and
BEFORE the composite FK is enforced (the FK addition would fail otherwise).
Prints the scan/write count and confirms 0 exit_ticket orphans.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.p56_plan_version_objectives_backfill import (
    backfill_plan_version_objectives,
)


def main() -> int:
    with sync_engine.begin() as conn:
        result = backfill_plan_version_objectives(conn)
    print("plan_version_objectives backfill complete:")
    print(f"  plan_versions_scanned  = {result.plan_versions_scanned}")
    print(f"  objectives_written     = {result.objectives_written}")
    print(f"  exit_ticket_orphans    = {result.exit_ticket_orphans}")
    return 0 if result.exit_ticket_orphans == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
