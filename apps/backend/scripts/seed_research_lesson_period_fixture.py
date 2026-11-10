"""Seed the P5.7 research-fixture lesson_period + repoint the 5 outlier lesson_plans.

Invocation::

    uv run python scripts/seed_research_lesson_period_fixture.py

Idempotent: every step is gated on a "does it exist?" lookup, so re-running
against a DB that already has the fixture is a no-op. Prints the resulting
fixture ids and how many lesson_plan rows were repointed (0 on a re-run).
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.p57_research_lesson_period_fixture import (
    seed_research_lesson_period_fixture,
)


def main() -> int:
    with sync_engine.begin() as conn:
        result = seed_research_lesson_period_fixture(conn)
    print("Research fixture seeded / re-discovered:")
    print(f"  school_id              = {result.school_id}")
    print(f"  class_id               = {result.class_id}")
    print(f"  teacher_id             = {result.teacher_id}")
    print(f"  course_id              = {result.course_id}")
    print(f"  term_class_subject_id  = {result.term_class_subject_id}")
    print(f"  teacher_workspace_id   = {result.teacher_workspace_id}")
    print(f"  scheme_of_work_id      = {result.scheme_of_work_id}")
    print(f"  lesson_period_id       = {result.lesson_period_id}")
    print(f"  outliers_repointed     = {result.outliers_repointed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
