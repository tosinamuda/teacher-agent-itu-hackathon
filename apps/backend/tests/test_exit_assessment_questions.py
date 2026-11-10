"""A class test is served objective by objective, in the order the lesson plan teaches them."""

from __future__ import annotations

import pytest
from sqlalchemy import text

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.assessments.application.service import AssessmentApplicationService
from app.domains.curriculum.models.exit_tickets import ExitTicketItem

PLAN = "LPV-ORDER"


def _item(objective: str, stem: str) -> ExitTicketItem:
    return ExitTicketItem(
        subtopic_id="sub",
        plan_version_id=PLAN,
        lesson_objective_id=objective,
        stem=stem,
        correct_option="A",
        options={"A": "1", "B": "2", "C": "3", "D": "4"},
        difficulty="easy",
    )


@pytest.mark.asyncio
async def test_objectives_come_in_the_plan_s_order_whatever_order_the_items_were_saved(db) -> None:  # type: ignore[no-untyped-def]
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(
        PlanVersion(
            version_id=PLAN,
            plan_id="P-ORDER",
            source_type="generated",
            session_plan={
                "lesson_plan_objectives": [
                    {"lesson_objective_id": "lop02", "objective_text": "Taught first"},
                    {"lesson_objective_id": "lop01", "objective_text": "Taught second"},
                    {"lesson_objective_id": "lop03", "objective_text": "Taught third"},
                ]
            },
            status=PlanVersionStatus.APPROVED,
        )
    )
    db.add_all([_item("lop03", "c"), _item("lop01", "b"), _item("lop02", "a")])
    await db.flush()

    served = await AssessmentApplicationService().get_exit_assessment_questions(
        db=db, plan_version_id=PLAN
    )

    assert [(o.lesson_objective_id, o.objective_text) for o in served.objectives] == [
        ("lop02", "Taught first"),
        ("lop01", "Taught second"),
        ("lop03", "Taught third"),
    ]
