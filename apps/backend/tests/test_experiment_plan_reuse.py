"""Reusing an existing plan as an experiment's plan: what the use case decides.

The lesson-plan service, the plan lookup, the ownership checks and the binding are stood in for,
so each test shows one decision of the use case itself.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from types import SimpleNamespace

import pytest

from app.domains.artefacts.types.lesson_plan.application import plan_reuse as reuse_logic
from app.domains.artefacts.types.lesson_plan.application.errors import PlanLookupNotFoundError
from app.domains.experiments.application import experiment_plan_reuse as module
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_plan_reuse import (
    ExperimentPlanReuse,
    PlanReuseRequest,
)
from app.shared.auth import ROLE_RESEARCH_MANAGER, ROLE_TEACHER, Actor
from app.shared.json_types import JsonObject

pytestmark = pytest.mark.asyncio

LESSON = uuid.uuid4()
EXPERIMENT = SimpleNamespace(experiment_id="EXP-1", lesson_period_id=LESSON)
MANAGER = Actor(role=ROLE_RESEARCH_MANAGER, auth_id="code|researcher")
TEACHER = Actor(role=ROLE_TEACHER, auth_id="code|teacher-1", teacher_id=uuid.uuid4())


@dataclass
class Queries:
    experiment: object | None = field(default_factory=lambda: EXPERIMENT)

    async def get_experiment(self, experiment_id: str) -> object | None:
        return self.experiment


#: The saved plan version being reused: its content (`None` when there is none) and its lesson.
SOURCE: dict[str, object] = {}


@dataclass
class PlanService:
    outcome: reuse_logic.ReusedPlan
    calls: list[dict[str, object]] = field(default_factory=list)

    async def reusable_source(self, plan_or_version_id: str) -> reuse_logic.ReuseSource:
        if SOURCE["content"] is None:
            raise PlanLookupNotFoundError(plan_or_version_id)
        return reuse_logic.ReuseSource(
            SOURCE["content"],  # type: ignore[arg-type]
            plan_or_version_id,
            SOURCE["lesson"],  # type: ignore[arg-type]
        )

    async def reuse_plan(self, **call: object) -> reuse_logic.ReusedPlan:
        self.calls.append(call)
        return self.outcome


def _request(**overrides: object) -> PlanReuseRequest:
    fields: dict[str, object] = {
        "experiment_id": "EXP-1",
        "actor": MANAGER,
        "source_plan_version_id": "LPV-SOURCE",
        "session_plan": None,
        "curriculum_choices": {},
    }
    fields.update(overrides)
    return PlanReuseRequest(**fields)  # type: ignore[arg-type]


@pytest.fixture
def bound(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """The plan versions bound to the experiment."""
    versions: list[str] = []

    async def bind(store: object, *, experiment_id: str, plan_version_id: str) -> None:
        versions.append(plan_version_id)

    monkeypatch.setattr(module, "bind_experiment_plan_version", bind)
    return versions


def _plans(monkeypatch: pytest.MonkeyPatch, service: PlanService) -> None:
    monkeypatch.setattr(module, "lesson_plan_service", lambda db: service)


def _source(monkeypatch: pytest.MonkeyPatch, content: JsonObject | None, lesson: uuid.UUID) -> None:
    SOURCE.update(content=content, lesson=lesson)


def _use_case(queries: Queries | None = None) -> ExperimentPlanReuse:
    return ExperimentPlanReuse(object(), queries or Queries(), object())  # type: ignore[arg-type]


async def test_a_reused_plan_is_bound_and_names_the_version_it_came_from(
    monkeypatch: pytest.MonkeyPatch, bound: list[str]
) -> None:
    service = PlanService(
        reuse_logic.ReusedPlan(SimpleNamespace(version_id="LPV-NEW"), [], [])  # type: ignore[arg-type]
    )
    _plans(monkeypatch, service)
    _source(monkeypatch, {"steps": []}, uuid.uuid4())

    outcome = await _use_case()(_request(curriculum_choices={"lop01": "cur01"}))

    assert outcome.experiment_id == "EXP-1"
    assert bound == ["LPV-NEW"]
    assert service.calls == [
        {
            "session_id": str(LESSON),
            "source": {"steps": []},
            "chosen": {"lop01": "cur01"},
            "teacher_id": None,
            "imported_from": "LPV-SOURCE",
        }
    ]


async def test_content_sent_with_the_request_is_reused_without_a_source_version(
    monkeypatch: pytest.MonkeyPatch, bound: list[str]
) -> None:
    service = PlanService(
        reuse_logic.ReusedPlan(SimpleNamespace(version_id="LPV-NEW"), [], [])  # type: ignore[arg-type]
    )
    _plans(monkeypatch, service)

    await _use_case()(_request(source_plan_version_id=None, session_plan={"steps": []}))

    assert service.calls[0]["source"] == {"steps": []}
    assert service.calls[0]["imported_from"] is None


async def test_objectives_that_need_a_choice_are_returned_and_nothing_is_bound(
    monkeypatch: pytest.MonkeyPatch, bound: list[str]
) -> None:
    unmapped: list[JsonObject] = [{"lesson_objective_id": "lop02", "objective_text": "x"}]
    choices: list[JsonObject] = [{"curriculum_objective_id": "cur01", "objective_text": "y"}]
    _plans(monkeypatch, PlanService(reuse_logic.ReusedPlan(None, unmapped, choices)))
    _source(monkeypatch, {"steps": []}, uuid.uuid4())

    outcome = await _use_case()(_request())

    assert outcome.experiment_id is None
    assert (outcome.unmapped, outcome.choices) == (unmapped, choices)
    assert bound == []


async def test_a_plan_that_does_not_exist_is_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    _plans(monkeypatch, PlanService(reuse_logic.ReusedPlan(None, [], [])))
    _source(monkeypatch, None, uuid.uuid4())

    with pytest.raises(ExperimentApplicationError) as refused:
        await _use_case()(_request())

    assert (refused.value.status_code, refused.value.detail) == (404, "source_plan_not_found")


async def test_a_teacher_cannot_reuse_the_plan_of_a_lesson_they_do_not_teach(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def owns_experiment_lesson_only(
        db: object, *, teacher_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> bool:
        return lesson_period_id == LESSON

    async def owns_the_experiment_lesson(
        db: object, *, actor: Actor, lesson_period_id: uuid.UUID
    ) -> None:
        return None

    _plans(monkeypatch, PlanService(reuse_logic.ReusedPlan(None, [], [])))
    _source(monkeypatch, {"steps": []}, uuid.uuid4())
    monkeypatch.setattr(module, "teacher_owns_lesson_period", owns_experiment_lesson_only)
    monkeypatch.setattr(module, "assert_actor_owns_lesson", owns_the_experiment_lesson)

    with pytest.raises(ExperimentApplicationError) as refused:
        await _use_case()(_request(actor=TEACHER))

    assert (refused.value.status_code, refused.value.detail) == (403, "not_your_lesson")


async def test_an_experiment_that_does_not_exist_is_not_found() -> None:
    with pytest.raises(ExperimentApplicationError) as refused:
        await _use_case(Queries(experiment=None))(_request())

    assert refused.value.status_code == 404


async def test_an_experiment_without_a_lesson_is_refused() -> None:
    no_lesson = SimpleNamespace(experiment_id="EXP-1", lesson_period_id=None)

    with pytest.raises(ExperimentApplicationError) as refused:
        await _use_case(Queries(experiment=no_lesson))(_request())

    assert (refused.value.status_code, refused.value.detail) == (409, "experiment_lesson_missing")
