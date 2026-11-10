"""A lesson with no textbook linkage takes its curriculum objectives from its subtopic."""

from __future__ import annotations

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.application.payload_builder import (
    SessionContextPayloadBuilder,
)
from app.domains.artefacts.types.lesson_plan.domain.objective_ids import performance_objective_id
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.domains.artefacts.types.lesson_plan.infrastructure.curriculum_objectives import (
    ensure_curriculum_objectives,
)
from app.domains.curriculum.models.curriculum import (
    CurriculumPerformanceObjective,
    CurriculumSubtopic,
)

SUBTOPIC = "jss1-basic-science-living-things-characteristics-of-living-things"
OBJECTIVES = ["State the seven characteristics of living things", "Classify objects as living"]


def _context(grounding_mode: str = "curriculum_only") -> SessionContext:
    return SessionContext(
        session_id="S1",
        subject="Basic Science",
        track="General",
        grade="JSS1",
        term="Third Term",
        week=1,
        day_index=1,
        topic="Living and Non-living Things",
        subtopic="Characteristics of living things",
        duration_minutes=45,
        session_objectives=OBJECTIVES,
        general_objectives=[],
        reference_materials=[],
        performance_objectives=OBJECTIVES,
        grounding_mode=grounding_mode,
        subtopic_id=SUBTOPIC,
    )


def test_objectives_of_a_lesson_without_a_textbook_are_named_after_its_subtopic() -> None:
    scope = SessionContextPayloadBuilder().build(_context()).curriculum_scope

    assert [o["curriculum_objective_id"] for o in scope.curriculum_objectives] == [
        performance_objective_id(SUBTOPIC, 1),
        performance_objective_id(SUBTOPIC, 2),
    ]
    assert performance_objective_id(SUBTOPIC, 2).endswith("-po02")


async def _rows(db: AsyncSession) -> list[tuple[str, str]]:
    found = await db.execute(
        select(
            CurriculumPerformanceObjective.curriculum_objective_id,
            CurriculumPerformanceObjective.curriculum_objective_text,
        ).order_by(CurriculumPerformanceObjective.curriculum_objective_id)
    )
    return [(row[0], row[1]) for row in found.all()]


@pytest.mark.asyncio
async def test_each_objective_gets_its_row_once(db: AsyncSession) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(
        CurriculumSubtopic(
            subtopic_id=SUBTOPIC, topic_key="t", title="Characteristics", performance_objectives=[]
        )
    )
    await db.flush()

    await ensure_curriculum_objectives(db, _context())
    await ensure_curriculum_objectives(db, _context())

    assert await _rows(db) == [
        (performance_objective_id(SUBTOPIC, 1), OBJECTIVES[0]),
        (performance_objective_id(SUBTOPIC, 2), OBJECTIVES[1]),
    ]


@pytest.mark.asyncio
async def test_a_lesson_linked_to_the_textbook_adds_none(db: AsyncSession) -> None:
    await ensure_curriculum_objectives(db, _context("manual_linkage"))

    assert await _rows(db) == []
