"""Reusing an existing plan as a lesson's plan: what the use case decides for the asker."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from types import SimpleNamespace

import pytest

from app.domains.artefacts.types.lesson_plan.api.schemas import PlanReuseRequest
from app.domains.artefacts.types.lesson_plan.application import plan_reuse as reuse_logic
from app.domains.artefacts.types.lesson_plan.application import reuse_for_teacher as module
from app.domains.artefacts.types.lesson_plan.application.errors import (
    PlanLookupNotFoundError,
    PlanNotOwnedByTeacherError,
    SessionNotFoundError,
)
from app.shared.auth import ROLE_RESEARCH_MANAGER, ROLE_TEACHER, Actor

pytestmark = pytest.mark.asyncio

LESSON = uuid.uuid4()
OTHER_LESSON = uuid.uuid4()
TEACHER = Actor(role=ROLE_TEACHER, auth_id="code|teacher-1", teacher_id=uuid.uuid4())
MANAGER = Actor(role=ROLE_RESEARCH_MANAGER, auth_id="code|researcher")


#: The lesson the plan version being reused belongs to; `_world` sets it for each test.
SOURCE_LESSON: list[uuid.UUID] = []


@dataclass
class PlanService:
    outcome: reuse_logic.ReusedPlan
    calls: list[dict[str, object]] = field(default_factory=list)

    async def reusable_source(self, plan_or_version_id: str) -> reuse_logic.ReuseSource:
        if plan_or_version_id == "LPV-MISSING":
            raise PlanLookupNotFoundError(plan_or_version_id)
        return reuse_logic.ReuseSource({"steps": []}, plan_or_version_id, SOURCE_LESSON[-1])

    async def reuse_plan(self, **call: object) -> reuse_logic.ReusedPlan:
        self.calls.append(call)
        return self.outcome


def _saved() -> reuse_logic.ReusedPlan:
    return reuse_logic.ReusedPlan(SimpleNamespace(version_id="LPV-NEW"), [], [])  # type: ignore[arg-type]


def _world(
    monkeypatch: pytest.MonkeyPatch, *, owned: set[uuid.UUID], source_lesson: uuid.UUID
) -> None:
    async def owns(db: object, *, teacher_id: uuid.UUID, lesson_period_id: uuid.UUID) -> bool:
        return lesson_period_id in owned

    monkeypatch.setattr(module, "teacher_owns_lesson_period", owns)
    SOURCE_LESSON.append(source_lesson)


async def _reuse(actor: Actor, service: PlanService, **over: object) -> reuse_logic.ReusedPlan:
    request = PlanReuseRequest(
        **{"session_id": str(LESSON), "source_plan_version_id": "LPV-SRC", **over}  # type: ignore[arg-type]
    )
    return await module.reuse_plan_for_lesson(
        object(),  # type: ignore[arg-type]
        service,  # type: ignore[arg-type]
        actor,
        session_id=request.session_id,
        source_plan_version_id=request.source_plan_version_id,
        session_plan=request.session_plan,
        curriculum_choices=request.curriculum_choices,
    )


async def test_a_teacher_reuses_the_plan_of_one_of_their_lessons_and_it_names_where_it_came_from(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _world(monkeypatch, owned={LESSON, OTHER_LESSON}, source_lesson=OTHER_LESSON)
    service = PlanService(_saved())

    await _reuse(TEACHER, service, curriculum_choices={"lop01": "cur01"})

    assert service.calls == [
        {
            "session_id": str(LESSON),
            "source": {"steps": []},
            "chosen": {"lop01": "cur01"},
            "teacher_id": str(TEACHER.teacher_id),
            "imported_from": "LPV-SRC",
        }
    ]


async def test_a_teacher_cannot_put_a_plan_on_a_lesson_they_do_not_teach(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _world(monkeypatch, owned={OTHER_LESSON}, source_lesson=OTHER_LESSON)

    with pytest.raises(PlanNotOwnedByTeacherError):
        await _reuse(TEACHER, PlanService(_saved()))


async def test_a_teacher_cannot_reuse_the_plan_of_a_lesson_they_do_not_teach(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _world(monkeypatch, owned={LESSON}, source_lesson=OTHER_LESSON)

    with pytest.raises(PlanNotOwnedByTeacherError):
        await _reuse(TEACHER, PlanService(_saved()))


async def test_a_plan_that_does_not_exist_and_a_lesson_that_is_not_an_id_are_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _world(monkeypatch, owned={LESSON}, source_lesson=LESSON)

    with pytest.raises(PlanLookupNotFoundError):
        await _reuse(TEACHER, PlanService(_saved()), source_plan_version_id="LPV-MISSING")
    with pytest.raises(SessionNotFoundError):
        await _reuse(TEACHER, PlanService(_saved()), session_id="not-an-id")


async def test_a_research_manager_is_not_held_to_the_lessons_they_teach(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _world(monkeypatch, owned=set(), source_lesson=OTHER_LESSON)
    service = PlanService(_saved())

    await _reuse(MANAGER, service)

    assert service.calls[0]["teacher_id"] is None


async def test_content_sent_with_the_request_is_reused_with_no_source_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _world(monkeypatch, owned={LESSON}, source_lesson=LESSON)
    service = PlanService(_saved())

    await _reuse(TEACHER, service, source_plan_version_id=None, session_plan={"steps": []})

    assert (service.calls[0]["source"], service.calls[0]["imported_from"]) == ({"steps": []}, None)


def test_a_request_names_a_plan_version_or_content_never_both_or_neither() -> None:
    with pytest.raises(ValueError, match="not both or neither"):
        PlanReuseRequest(session_id="S", source_plan_version_id="V", session_plan={})
    with pytest.raises(ValueError, match="not both or neither"):
        PlanReuseRequest(session_id="S")
