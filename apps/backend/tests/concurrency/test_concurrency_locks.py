"""Row-lock serialization + unique-code retry hold under real contention.

* ``assign_h1`` caps raters per scope with a COUNT — which a unique
  constraint can't express — so it serializes the count+insert behind a
  ``SELECT ... FOR UPDATE`` on the experiment row. Without that lock, N concurrent
  assignments all read "under cap" and overflow it. This test proves the cap holds
  at exactly the limit under a real concurrent burst.

* ``commit_with_unique_retry`` allocates a code from ``MAX(existing)+1`` — a
  read-then-write race that previously produced duplicate-key 500s. This test
  proves N racers converge on N DISTINCT sequential codes with nothing escaping.
"""

from __future__ import annotations

import asyncio
import re
import uuid

import pytest
from sqlalchemy import select, text

from app.db.retry import commit_with_unique_retry
from app.domains.evaluation.application.assignment_commands import assign_h1
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.infrastructure.models import EvaluationRater, RaterAssignment
from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
    SqlAlchemyEvaluationStore,
)
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.domains.school.models.structure import School

pytestmark = pytest.mark.asyncio

_H1_CAP = 3
_LESSON_ID = uuid.UUID(int=0xA11CE)


async def test_concurrent_h1_rater_cap_holds_at_limit(
    run_race, count_rows, session_factory
) -> None:
    n_raters = _H1_CAP + 3  # more racers than slots

    # Seed an experiment + raters. The experiment's investigation/workspace FKs
    # are irrelevant to the cap path (it locks + counts by experiment id), so we
    # insert with FK checks off rather than build the whole upstream graph. Its
    # lesson_period_id matches what we assign, so the lesson-belongs check
    # short-circuits without needing a LessonPeriod row.
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            Experiment(
                experiment_id="EXP-RACE",
                experiment_code="RACE-001",
                investigation_db_id=uuid.uuid4(),
                teacher_workspace_id=uuid.uuid4(),
                lesson_period_id=_LESSON_ID,
            )
        )
        seed.add_all(
            EvaluationRater(rater_id=f"EVR-{i}", display_name=f"Rater {i}") for i in range(n_raters)
        )
        await seed.commit()

    async def op(session, i):
        # The experiments repo is session-bound, so each racer builds its own.
        experiments = ExperimentRepository(session)
        store = SqlAlchemyEvaluationStore(session, assignment_scopes=experiments)
        # Distinct raters → no idempotent short-circuit; the cap is the only gate.
        return await assign_h1(
            store,
            experiment_id="EXP-RACE",
            rater_id=f"EVR-{i}",
            lesson_period_id=_LESSON_ID,
            assigned_by="researcher",
        )

    out = await run_race(
        op,
        lambda e: isinstance(e, EvaluationApplicationError) and e.status_code == 409,
        n=n_raters,
    )

    assert out.others == [], f"a capped-out assignment surfaced as non-409: {out.others}"
    # Exactly the cap is admitted — the lock prevents the overflow that a bare
    # count-then-insert would allow.
    assert len(out.wins) == _H1_CAP
    assert len(out.conflicts) == n_raters - _H1_CAP
    assert await count_rows(RaterAssignment) == _H1_CAP


def _next_sequence(codes: list[str]) -> int:
    """Next sequence number from the existing ``SCH-NNN`` codes (MAX+1)."""
    nums = [int(m.group(1)) for c in codes if (m := re.fullmatch(r"SCH-(\d+)", c))]
    return (max(nums) + 1) if nums else 1


async def test_concurrent_unique_code_retry_allocates_distinct(count_rows, session_factory) -> None:
    n = 8

    async def alloc(i: int) -> str:
        async with session_factory() as session:

            async def build() -> School:
                codes = (await session.execute(select(School.code))).scalars().all()
                school = School(name=f"race-{i}", code=f"SCH-{_next_sequence(codes):03d}")
                session.add(school)
                return school

            # conflict_token="code" → only the code's unique index counts as a
            # retryable collision; anything else is a real anomaly and propagates.
            school = await commit_with_unique_retry(
                session, build, conflict_token="code", base_delay=0
            )
            return school.code

    results = await asyncio.gather(*(alloc(i) for i in range(n)), return_exceptions=True)

    errors = [r for r in results if isinstance(r, BaseException)]
    codes = [r for r in results if not isinstance(r, BaseException)]
    assert errors == [], f"unique-retry let an error escape: {errors}"
    assert len(codes) == n
    assert len(set(codes)) == n, f"codes collided: {sorted(codes)}"
    assert await count_rows(School) == n
