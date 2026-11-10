"""Concurrent duplicate creates settle as exactly one success + clean 409s.

Each test fires ``N`` independent sessions at the same unique key simultaneously.
The invariant the PR-#79 constraint-backed handling guarantees:

* exactly ONE writer wins (the unique index admits one row),
* every loser is caught as an ``IntegrityError`` and re-raised as the domain's
  intended 409 — never an unhandled 500, and
* exactly one row is persisted (no duplicates slip through the check-then-insert
  window).

This exercises the real InnoDB unique index under real contention — the
fakes-only ``test_*_service`` unit tests can't prove the cross-transaction race.
"""

from __future__ import annotations

import pytest

from app.domains.events.application.service import (
    EventApplicationError,
    EventApplicationService,
)
from app.domains.events.models.events import Event
from app.domains.events.schemas.events import EventIn
from app.domains.learners.application.service import (
    LearnerApplicationError,
    LearnerApplicationService,
)
from app.domains.learners.models.learner import LearnerProfile
from app.domains.learners.schemas import LearnerCreateRequest
from app.domains.school.application.errors import SchoolApplicationError
from app.domains.school.application.service import SchoolApplicationService
from app.domains.school.models.structure import School
from app.domains.school.schemas import SchoolCreateRequest
from app.domains.users.application.service import (
    UserAlreadyExistsError,
    UserApplicationService,
)
from app.domains.users.models import User

pytestmark = pytest.mark.asyncio

_N = 10  # concurrent racers


def _is_409(exc: BaseException) -> bool:
    """Domain errors that carry an HTTP-style ``status_code`` of 409."""
    return getattr(exc, "status_code", None) == 409


async def test_concurrent_create_user_one_wins(run_race, count_rows) -> None:
    async def op(session, i):
        # Same login code (the contended unique auth_id); distinct emails so the
        # loss is decided by the code, not the email's own unique index.
        return await UserApplicationService().create_user(
            db=session,
            code="RACE-USER",
            email=f"racer{i}@x.test",
            full_name="Racer",
            role="teacher",
        )

    out = await run_race(op, lambda e: isinstance(e, UserAlreadyExistsError), n=_N)

    assert out.others == [], f"a lost race surfaced as a non-409 error: {out.others}"
    assert len(out.wins) == 1
    assert len(out.conflicts) == _N - 1
    assert await count_rows(User, auth_id="code|RACE-USER") == 1


async def test_concurrent_create_learner_one_wins(run_race, count_rows) -> None:
    async def op(session, i):
        return await LearnerApplicationService().create_learner(
            db=session,
            payload=LearnerCreateRequest(
                code="RACE-LRN",
                full_name=f"Racer {i}",
                grade="9",
                track="general",
            ),
        )

    out = await run_race(op, lambda e: isinstance(e, LearnerApplicationError) and _is_409(e), n=_N)

    assert out.others == [], f"a lost race surfaced as a non-409 error: {out.others}"
    assert len(out.wins) == 1
    assert len(out.conflicts) == _N - 1
    assert await count_rows(LearnerProfile, code="RACE-LRN") == 1


async def test_concurrent_create_school_one_wins(run_race, count_rows) -> None:
    async def op(session, i):
        return await SchoolApplicationService().create_school(
            db=session,
            payload=SchoolCreateRequest(name="Race High", school_code="RACE"),
        )

    out = await run_race(op, lambda e: isinstance(e, SchoolApplicationError) and _is_409(e), n=_N)

    assert out.others == [], f"a lost race surfaced as a non-409 error: {out.others}"
    assert len(out.wins) == 1
    assert len(out.conflicts) == _N - 1
    assert await count_rows(School, code="RACE") == 1


async def test_concurrent_ingest_event_one_wins(run_race, count_rows) -> None:
    async def op(session, i):
        return await EventApplicationService().ingest_event(
            db=session,
            payload=EventIn(event_id="RACE-EVT", event_type="view", payload={"i": i}),
        )

    out = await run_race(op, lambda e: isinstance(e, EventApplicationError) and _is_409(e), n=_N)

    assert out.others == [], f"a lost race surfaced as a non-409 error: {out.others}"
    assert len(out.wins) == 1
    assert len(out.conflicts) == _N - 1
    assert await count_rows(Event, event_id="RACE-EVT") == 1
