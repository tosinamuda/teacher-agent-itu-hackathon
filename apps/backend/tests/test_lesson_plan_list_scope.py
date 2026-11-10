"""Over HTTP: who may list lesson plans, and a student sees only their own class's lessons.

Two classes in two schools share a grade. The routing, the Casbin policy the seed writes, the
learner lookup and the plan query are real; only the enforcer's storage is in memory.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass

import casbin
import pytest
import pytest_asyncio
from casbin.persist.adapters.string_adapter import StringAdapter
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.db.deps import get_db
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.learners.models.learner import LearnerProfile
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models.syllabus import LessonPeriod, SchemeOfWork
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from migrations.data.casbin_policy_seed import _CAPABILITY_POLICIES

STUDENT = uuid.UUID(int=801)
UNENROLLED_STUDENT = uuid.UUID(int=802)
TEACHER = uuid.UUID(int=803)
OWN_CLASS = uuid.uuid4()
OTHER_SCHOOL_CLASS = uuid.uuid4()


@dataclass
class _Caller:
    actor: Actor


def _actor(user_id: uuid.UUID, role: str) -> Actor:
    return Actor(role=role, auth_id=f"code|{user_id}", teacher_id=user_id)


def _policy() -> str:
    rows = [f"p, {role}, {obj}, {act}, allow" for role, obj, act in _CAPABILITY_POLICIES]
    rows += [
        f"g, {STUDENT}, student",
        f"g, {UNENROLLED_STUDENT}, student",
        f"g, {TEACHER}, teacher",
    ]
    return "\n".join(rows)


def _lesson(class_id: uuid.UUID, name: str) -> list[object]:
    offering, scheme, period = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    return [
        TermClassSubject(
            id=offering, course_id=uuid.uuid4(), class_id=class_id, term="Term 1", year="2026"
        ),
        SchemeOfWork(id=scheme, term_class_subject_id=offering, week_number=1, title=name),
        LessonPeriod(id=period, scheme_of_work_id=scheme, period_number=1),
        LessonPlan(
            plan_id=f"P-{name}",
            lesson_period_id=period,
            title=name,
            subject="Mathematics",
            track="General",
            grade="JSS1",
        ),
        PlanVersion(
            version_id=f"LPV-{name}",
            plan_id=f"P-{name}",
            source_type="manual",
            session_plan={"subject": "Mathematics", "grade": "JSS1", "topic": name},
            status=PlanVersionStatus.APPROVED,
        ),
    ]


@pytest_asyncio.fixture
async def client(db, monkeypatch) -> AsyncIterator[tuple[AsyncClient, _Caller]]:  # type: ignore[no-untyped-def]
    enforcer = casbin.Enforcer(authz.MODEL_PATH, StringAdapter(_policy()))

    async def _enforcer() -> casbin.Enforcer:
        return enforcer

    monkeypatch.setattr(authz, "get_enforcer", _enforcer)

    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            *_lesson(OWN_CLASS, "Fractions"),
            *_lesson(OTHER_SCHOOL_CLASS, "Integers"),
            LearnerProfile(
                student_id="STU-OWN",
                full_name="Student One",
                grade="JSS1",
                track="General",
                class_id=OWN_CLASS,
                user_id=STUDENT,
            ),
            LearnerProfile(
                student_id="STU-NONE",
                full_name="Student Two",
                grade="JSS1",
                track="General",
                user_id=UNENROLLED_STUDENT,
            ),
        ]
    )
    await db.flush()

    caller = _Caller(_actor(STUDENT, "student"))

    async def _db() -> AsyncIterator:
        yield db

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_actor] = lambda: caller.actor
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
            yield http, caller
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_a_student_lists_only_their_own_class_lessons(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client

    listed = await http.get("/artefacts/lesson-plans/for-my-class")

    assert listed.status_code == 200, listed.text
    assert [row["version_id"] for row in listed.json()] == ["LPV-Fractions"]


@pytest.mark.asyncio
async def test_a_student_cannot_list_every_school_lessons(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client

    assert (await http.get("/artefacts/lesson-plans?grade=JSS1")).status_code == 403
    assert (await http.get("/artefacts/lesson-plans/LPV-Integers")).status_code == 403


@pytest.mark.asyncio
async def test_a_student_with_no_class_is_refused(client) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    caller.actor = _actor(UNENROLLED_STUDENT, "student")

    refused = await http.get("/artefacts/lesson-plans/for-my-class")

    assert refused.status_code == 403
    assert refused.json()["detail"] == "no_student_class_bound_to_this_user"


@pytest.mark.asyncio
async def test_a_teacher_lists_plans_but_has_no_class_of_their_own(client) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    caller.actor = _actor(TEACHER, "teacher")

    listed = await http.get("/artefacts/lesson-plans?grade=JSS1")

    assert listed.status_code == 200
    assert {row["version_id"] for row in listed.json()} == {"LPV-Fractions", "LPV-Integers"}
    assert {row["source_type"] for row in listed.json()} == {"manual"}
    assert (await http.get("/artefacts/lesson-plans/for-my-class")).status_code == 403
