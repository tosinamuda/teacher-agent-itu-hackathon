"""The class note is grounded in the teacher's approved lesson note, and records that it was."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    ApprovedLessonNote,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    SourceEvidenceProjector,
    reads_lesson_note,
)
from app.domains.experiments.application.conditioned_plan import validated_session_plan
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_views.readiness import readiness_response
from app.domains.experiments.application.service import ExperimentApplicationService
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.condition_runs.records import recorded_grounding
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.auth import ROLE_RESEARCH_MANAGER, Actor
from app.shared.session_plan_view import SessionPlanView

PLAN = {
    "plan_id": "LP-1",
    "session_id": "s1",
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lo1", "objective_text": "convert improper fractions"}
    ],
    "steps": [
        {
            "step_id": "step1",
            "step_kind": "core",
            "lesson_objective_id": "lo1",
            "title": "Divide",
            "content": "Work examples.",
        }
    ],
}
NOTE = ApprovedLessonNote(
    note_id="AT-note", version=2, origin="generated", sections={"step1": "Divide 22 by 5."}
)


class _Plans:
    def __init__(self, note: ApprovedLessonNote | None) -> None:
        self._note = note

    async def get_plan_version(self, plan_version_id: str):
        return SimpleNamespace(
            version_id=plan_version_id, session_plan=PLAN, status=PlanVersionStatus.APPROVED
        )

    async def approved_lesson_note(self, plan_version_id: str):
        return self._note


def test_the_conditions_read_the_plan_with_its_approved_lesson_note() -> None:
    plan = asyncio.run(validated_session_plan(_Plans(NOTE), "LPV-1"))

    assert plan.session_plan.steps[0].note == "Divide 22 by 5."
    assert plan.grounding == {
        "expert_sources": "lesson-note",
        "lesson_note": {"id": "AT-note", "version": 2, "origin": "generated"},
    }


def test_a_plan_without_an_approved_note_is_read_as_it_is() -> None:
    plan = asyncio.run(validated_session_plan(_Plans(None), "LPV-1"))

    assert plan.session_plan.steps[0].note is None
    assert plan.grounding == {"expert_sources": "textbook", "lesson_note": None}


def test_only_a_condition_that_reads_the_note_records_it() -> None:
    grounding = {"expert_sources": "lesson-note", "lesson_note": {"id": "AT-note"}}

    assert recorded_grounding(Hypothesis.H1, ConditionCode.C0, grounding) == {}
    assert recorded_grounding(Hypothesis.H1, ConditionCode.C3, grounding) == grounding


@pytest.mark.parametrize(
    ("hypothesis", "condition"),
    [
        *((Hypothesis.H1, code) for code in ("C0", "C1", "C2", "C3", "C4")),
        *((Hypothesis.H2, code) for code in ("P0", "P1")),
    ],
)
def test_the_note_reading_rule_answers_as_the_evidence_it_describes(hypothesis, condition) -> None:
    policy = profile_for(hypothesis, ConditionCode(condition)).generation_policy()
    step = SessionPlanView.model_validate(
        {**PLAN, "steps": [{**PLAN["steps"][0], "note": "Divide 22 by 5."}]}
    ).steps[0]

    assert bool(SourceEvidenceProjector().for_step(step, policy)) == reads_lesson_note(policy)


class _Experiments(_Plans):
    async def get_experiment(self, experiment_id: str):
        return SimpleNamespace(experiment_id=experiment_id, plan_version_id="LPV-1")


def _create_review_note(note: ApprovedLessonNote | None) -> list[object]:
    launched: list[object] = []

    async def launch(request):
        launched.append(request)

    asyncio.run(
        ExperimentApplicationService(_Experiments(note)).create_review_note(  # type: ignore[arg-type]
            db=None,  # type: ignore[arg-type]
            experiment_id="EXP-1",
            actor=Actor(role=ROLE_RESEARCH_MANAGER, auth_id="code|researcher"),
            launch=launch,
        )
    )
    return launched


def test_the_class_note_waits_for_an_approved_lesson_note() -> None:
    with pytest.raises(ExperimentApplicationError) as refused:
        _create_review_note(None)

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "approve_the_lesson_note_first",
    )


def test_an_approved_lesson_note_lets_the_class_note_be_made() -> None:
    assert len(_create_review_note(NOTE)) == 1


def _readiness(**note):
    return readiness_response(
        experiment=SimpleNamespace(focal_learner_ids=[]),  # type: ignore[arg-type]
        context=SimpleNamespace(  # type: ignore[arg-type]
            plan_version=SimpleNamespace(status=PlanVersionStatus.APPROVED), diagnostic_count=0
        ),
        selected_focal_learners=[],
        base_pack_artefact_id=None,
        base_pack_approved=False,
        **note,
    )


def test_h1_is_ready_only_once_the_lesson_note_is_approved() -> None:
    assert not _readiness(lesson_note_artefact_id="AT-note", lesson_note_approved=False).h1_ready
    ready = _readiness(lesson_note_artefact_id="AT-note", lesson_note_approved=True)
    assert (ready.h1_ready, ready.lesson_note_artefact_id) == (True, "AT-note")
