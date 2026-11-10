"""FD-04: on-behalf student-response entry → graded diagnostic + learner state."""

from __future__ import annotations

import pytest
from pydantic import ValidationError
from sqlalchemy import func, select, text

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.assessments.application.onbehalf_service import OnBehalfResponseService
from app.domains.assessments.application.service import (
    AssessmentApplicationError,
    AssessmentApplicationService,
)
from app.domains.assessments.infrastructure.repository import AssessmentRepository
from app.domains.assessments.models.exit_ticket import ExitTicketSubmission
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.assessments.onbehalf_schemas import (
    ManualObjectiveScore,
    OnBehalfResponseRequest,
)
from app.domains.assessments.schemas import ExitAssessmentAnswer
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.learners.models import LearnerProfile

_TWO_OBJECTIVES = {
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lop01", "objective_text": "Add"},
        {"lesson_objective_id": "lop02", "objective_text": "Subtract"},
    ]
}


async def _noop_request(self, *args: object, **kwargs: object) -> None:
    return None


def _student(student_id: str) -> LearnerProfile:
    return LearnerProfile(student_id=student_id, full_name="Student", grade="JSS1", track="General")


def _plan(version_id: str) -> PlanVersion:
    return PlanVersion(
        version_id=version_id,
        plan_id=f"P-{version_id}",
        source_type="experiment_manual",
        session_plan=_TWO_OBJECTIVES,
        status=PlanVersionStatus.DRAFT,
    )


# --- schema (pure) ---


def test_request_requires_exactly_one_mode() -> None:
    answer = ExitAssessmentAnswer(item_id="i", selected_option="A")
    score = ManualObjectiveScore(lesson_objective_id="lop01", score=1, max_score=2)
    with pytest.raises(ValidationError):  # neither
        OnBehalfResponseRequest(student_id="s")
    with pytest.raises(ValidationError):  # both
        OnBehalfResponseRequest(student_id="s", answers=[answer], objective_scores=[score])
    # exactly one is accepted
    OnBehalfResponseRequest(student_id="s", objective_scores=[score])


def test_enter_on_behalf_capability_is_seeded() -> None:
    from migrations.data.casbin_policy_seed import _CAPABILITY_POLICIES, CASBIN_ROLE_TEACHER

    assert (CASBIN_ROLE_TEACHER, "submission:*", "enter_on_behalf") in _CAPABILITY_POLICIES


# --- service (DB-backed) ---


@pytest.mark.asyncio
async def test_score_only_entry_yields_bandable_results_and_attribution(db, monkeypatch) -> None:
    monkeypatch.setattr(AssessmentApplicationService, "_request_student_pack", _noop_request)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_student("ST-OB1"))
    db.add(_plan("LPV-OB1"))
    await db.flush()

    request = OnBehalfResponseRequest(
        student_id="ST-OB1",
        objective_scores=[
            ManualObjectiveScore(lesson_objective_id="lop01", score=1, max_score=4),
            ManualObjectiveScore(lesson_objective_id="lop02", score=4, max_score=4),
        ],
        provenance_attachment_id="att-123",
    )
    result = await OnBehalfResponseService().enter(
        db=db, plan_version_id="LPV-OB1", request=request, entered_by="Teacher One (teacher)"
    )

    assert result.objectives_scored == 2
    submission = await AssessmentRepository().get_submission_by_diagnostic_id(
        db, result.diagnostic_id
    )
    assert submission is not None
    assert submission.entered_by == "Teacher One (teacher)"
    assert submission.provenance_attachment_id == "att-123"
    by_id = {o["lesson_objective_id"]: o for o in submission.results["objectives"]}
    assert by_id["lop01"]["score"] == 1 and by_id["lop01"]["max_score"] == 4
    # Score-only → no chosen distractor → no misconception (dropped by exclude_none).
    assert "misconception_code" not in by_id["lop01"]


@pytest.mark.asyncio
async def test_chosen_option_entry_persists_responses_and_misconception(db, monkeypatch) -> None:
    monkeypatch.setattr(AssessmentApplicationService, "_request_student_pack", _noop_request)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_student("ST-OB2"))
    db.add(_plan("LPV-OB2"))
    item = ExitTicketItem(
        subtopic_id="sub",
        plan_version_id="LPV-OB2",
        lesson_objective_id="lop01",
        stem="q",
        correct_option="B",
        options={"A": "x", "B": "y"},
        option_misconceptions={"A": "mc_a"},
    )
    db.add(item)
    await db.flush()

    request = OnBehalfResponseRequest(
        student_id="ST-OB2",
        answers=[ExitAssessmentAnswer(item_id=str(item.id), selected_option="A")],
    )
    result = await OnBehalfResponseService().enter(
        db=db, plan_version_id="LPV-OB2", request=request, entered_by="Researcher"
    )

    responses = await db.scalar(
        select(func.count())
        .select_from(StudentItemResponse)
        .where(StudentItemResponse.item_id == item.id)
    )
    assert responses == 1
    submission = await AssessmentRepository().get_submission_by_diagnostic_id(
        db, result.diagnostic_id
    )
    assert submission.entered_by == "Researcher"
    objective = next(
        o for o in submission.results["objectives"] if o["lesson_objective_id"] == "lop01"
    )
    assert objective["score"] == 0 and objective["max_score"] == 1
    # Chose the wrong, tagged distractor → the misconception surfaces.
    assert objective["misconception_code"] == "mc_a"


@pytest.mark.asyncio
async def test_rejects_duplicate_submission(db, monkeypatch) -> None:
    monkeypatch.setattr(AssessmentApplicationService, "_request_student_pack", _noop_request)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_student("ST-OB3"))
    db.add(_plan("LPV-OB3"))
    db.add(
        ExitTicketSubmission(
            diagnostic_id="DIAG-OB3", student_id="ST-OB3", plan_version_id="LPV-OB3", results={}
        )
    )
    await db.flush()

    request = OnBehalfResponseRequest(
        student_id="ST-OB3",
        objective_scores=[ManualObjectiveScore(lesson_objective_id="lop01", score=1, max_score=2)],
    )
    with pytest.raises(AssessmentApplicationError) as exc:
        await OnBehalfResponseService().enter(
            db=db, plan_version_id="LPV-OB3", request=request, entered_by="T"
        )
    assert exc.value.status_code == 409
    assert exc.value.detail == "already_submitted"


@pytest.mark.asyncio
async def test_onbehalf_entry_requests_pack_immediately(db, monkeypatch) -> None:
    # FD-05 AC#1: the field flow never waits for a survey — the pack is asked for now, and
    # the learner-pack gate makes it once the class pack is approved.
    requested: list[str] = []

    async def spy_request(self, db_, student_id, plan_version_id):
        requested.append(student_id)

    monkeypatch.setattr(AssessmentApplicationService, "_request_student_pack", spy_request)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_student("ST-OB-ENQ"))
    db.add(_plan("LPV-OB-ENQ"))
    await db.flush()

    await OnBehalfResponseService().enter(
        db=db,
        plan_version_id="LPV-OB-ENQ",
        request=OnBehalfResponseRequest(
            student_id="ST-OB-ENQ",
            objective_scores=[
                ManualObjectiveScore(lesson_objective_id="lop01", score=1, max_score=2)
            ],
        ),
        entered_by="T",
    )
    assert requested == ["ST-OB-ENQ"]
