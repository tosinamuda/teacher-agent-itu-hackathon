"""The curriculum's own objective rows for a lesson whose subtopic has no textbook linkage."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.domain.objective_ids import performance_objective_id
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.domains.curriculum.models.curriculum import CurriculumPerformanceObjective


async def ensure_curriculum_objectives(db: AsyncSession, context: SessionContext) -> None:
    """Add the rows a plan's lesson objectives point at, for each performance objective it lacks.

    A subtopic linked to the textbook has its rows from that linkage. Any other subtopic's plan
    refers to ids made from the subtopic and the objective's position, and a plan version
    can be stored only when those rows exist.
    """
    if context.grounding_mode == "manual_linkage" or not context.subtopic_id:
        return
    for position, text in enumerate(context.performance_objectives, start=1):
        objective_id = performance_objective_id(context.subtopic_id, position)
        held = await db.execute(
            select(CurriculumPerformanceObjective.id).where(
                CurriculumPerformanceObjective.curriculum_objective_id == objective_id
            )
        )
        if held.first() is None:
            db.add(
                CurriculumPerformanceObjective(
                    subtopic_id=context.subtopic_id,
                    curriculum_objective_id=objective_id,
                    curriculum_objective_text=text.strip(),
                )
            )
    await db.flush()
