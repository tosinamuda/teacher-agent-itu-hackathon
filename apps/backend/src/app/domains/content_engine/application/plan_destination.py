"""Save a finished plan draft as the lesson's plan: a draft plan version for the teacher.

The sections are put together into the plan, and the plan is checked and saved exactly as a
teacher's own plan is, so it becomes a draft the teacher approves. A plan written from a
document is saved as the teacher's; one written from the curriculum is also held to the
spec's requirements.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.parts import Unit
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.lesson_plan.domain.plan_sections import (
    AssembledPlan,
    ObjectiveSection,
    assemble_plan,
    issue_lines,
)
from app.domains.content_engine.application.planning_ports import Planning, PlanRefusedError
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.shared.json_types import JsonObject


def assembled(draft: Draft) -> AssembledPlan:
    lesson = next((part for unit, part in draft.written() if unit.unit is Unit.LESSON), None)
    sections = [
        ObjectiveSection(unit.unit_id, unit.label, part)
        for unit, part in draft.written()
        if unit.unit is Unit.CURRICULUM_OBJECTIVE
    ]
    return assemble_plan(lesson, sections)


#: How a plan is recorded among plan versions: written from a teacher's document, or by the app.
DOCUMENT_IMPORT = "document_import"
GENERATED = "generated"


def session_of(draft: Draft) -> str:
    if draft.session_id is None:
        raise DraftError("a lesson plan is written for a lesson period")
    return draft.session_id


class PlanDestination:
    def __init__(self, planning: Planning) -> None:
        self._planning = planning

    async def issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        """Nothing: the plugin's check tool, ``check_lesson_plan``, reads the plan."""
        return []

    def preview(self, draft: Draft) -> JsonObject:
        return assembled(draft).content

    async def save(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, generator: JsonObject
    ) -> str:
        plan = assembled(draft)
        try:
            if draft.saved_as is not None:
                return await self._planning.revise(
                    db, draft.saved_as, session_of(draft), plan.content, generator=generator
                )
            return await self._planning.save(
                db,
                session_of(draft),
                plan.content,
                draft.author,
                source_type=DOCUMENT_IMPORT if draft.source else GENERATED,
                generator=generator,
            )
        except PlanRefusedError as error:
            lines = issue_lines(error.issues, plan.places)
            raise DraftError("the plan cannot be saved yet: " + "; ".join(lines)) from error
