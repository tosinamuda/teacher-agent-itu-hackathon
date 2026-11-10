"""FD-02: classwork coverage report + the entry guards (DB-backed).

Runs against the MySQL test DB. FK checks are relaxed for lightweight setup — the
behaviour under test is the coverage computation and the freeze/responses guards,
not the foreign keys.
"""

from __future__ import annotations

import pytest
from sqlalchemy import text

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.assessments.application.classwork_service import ClassworkApplicationService
from app.domains.assessments.application.service import AssessmentApplicationError
from app.domains.assessments.classwork_schemas import ManualClassworkItem
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.shared.time import utc_now

pytestmark = pytest.mark.asyncio

_THREE_OBJECTIVES = {
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lop01", "objective_text": "Add"},
        {"lesson_objective_id": "lop02", "objective_text": "Subtract"},
        {"lesson_objective_id": "lop03", "objective_text": "Check"},
    ]
}


def _plan_version(version_id: str, **overrides: object) -> PlanVersion:
    fields: dict[str, object] = {
        "version_id": version_id,
        "plan_id": f"PLAN-{version_id}",
        "source_type": "experiment_manual",
        "session_plan": _THREE_OBJECTIVES,
        "status": PlanVersionStatus.DRAFT,
    }
    fields.update(overrides)
    return PlanVersion(**fields)  # type: ignore[arg-type]


def _exit_item(plan_version_id: str, objective_id: str) -> ExitTicketItem:
    return ExitTicketItem(
        subtopic_id="sub-1",
        plan_version_id=plan_version_id,
        lesson_objective_id=objective_id,
        stem="q",
        correct_option="A",
        options={"A": "1", "B": "2"},
    )


def _manual_item(objective_id: str = "lop01") -> ManualClassworkItem:
    return ManualClassworkItem(
        lesson_objective_id=objective_id,
        stem="What is 2 + 2?",
        options={"A": "3", "B": "4"},
        correct_option="B",
    )


async def test_coverage_flags_objectives_with_no_items(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_plan_version("LPV-CW-COV"))
    for objective_id, count in [("lop01", 2), ("lop02", 1)]:
        for _ in range(count):
            db.add(_exit_item("LPV-CW-COV", objective_id))
    await db.flush()

    coverage = await ClassworkApplicationService().compute_classwork_coverage(
        db=db, plan_version_id="LPV-CW-COV"
    )

    assert coverage.total_items == 3
    by_id = {objective.lesson_objective_id: objective for objective in coverage.objectives}
    assert by_id["lop01"].item_count == 2 and by_id["lop01"].has_items
    assert by_id["lop02"].item_count == 1 and by_id["lop02"].has_items
    # lop03 has no items — it must still appear, flagged, so the gap is visible.
    assert by_id["lop03"].item_count == 0 and not by_id["lop03"].has_items
    assert coverage.objectives_without_items == ["lop03"]


async def test_create_refuses_once_assessment_released(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_plan_version("LPV-CW-FROZEN", assessment_released_at=utc_now()))
    await db.flush()

    with pytest.raises(AssessmentApplicationError) as exc:
        await ClassworkApplicationService().create_manual_classwork(
            db=db, plan_version_id="LPV-CW-FROZEN", items=[_manual_item()]
        )
    assert exc.value.status_code == 409
    assert exc.value.detail == "assessment_released"


async def test_create_refuses_when_a_student_has_answered(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_plan_version("LPV-CW-ANSWERED"))
    item = _exit_item("LPV-CW-ANSWERED", "lop01")
    db.add(item)
    await db.flush()
    db.add(
        StudentItemResponse(
            item_id=item.id, student_id="ST-1", choice="A", is_correct=True, score=1.0
        )
    )
    await db.flush()

    with pytest.raises(AssessmentApplicationError) as exc:
        await ClassworkApplicationService().create_manual_classwork(
            db=db, plan_version_id="LPV-CW-ANSWERED", items=[_manual_item()]
        )
    assert exc.value.status_code == 409
    assert exc.value.detail == "assessment_has_responses"
