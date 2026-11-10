"""Seed the P5.7-finish curriculum-identity reference catalogs.

Invocation::

    uv run python -m scripts.seed_curriculum_subject_grade_term_catalogs

Idempotent. Runs AFTER the Alembic migration that creates the 4 catalog tables
and BEFORE the migration that adds FK constraints to the existing string
columns on `curriculum_topics` / `class_sessions` / `reference_materials`.
Exits non-zero if any string column would orphan against its catalog.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.p57b_curriculum_string_catalogs_backfill import (
    backfill_curriculum_string_catalogs,
)


def main() -> int:
    with sync_engine.begin() as conn:
        result = backfill_curriculum_string_catalogs(conn)
    print("curriculum reference catalogs backfill complete:")
    print(f"  dirty_term_rows_repaired   = {result.dirty_term_rows_repaired}")
    print(f"  subjects_inserted          = {result.subjects_inserted}")
    print(f"  tracks_inserted            = {result.tracks_inserted}")
    print(f"  grades_inserted            = {result.grades_inserted}")
    print(f"  terms_inserted             = {result.terms_inserted}")
    print(f"  orphans_against_catalogs   = {result.orphans_against_catalogs}")
    return 0 if result.orphans_against_catalogs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
