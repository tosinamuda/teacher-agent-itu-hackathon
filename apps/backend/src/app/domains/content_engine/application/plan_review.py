"""The check tool of a lesson-plan draft: the plan as the teacher's own edit screen checks it."""

from __future__ import annotations

import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.domain.plan_sections import issue_lines
from app.domains.content_engine.application.plan_destination import assembled, session_of
from app.domains.content_engine.application.planning_ports import Planning
from app.domains.content_engine.domain.draft import Draft
from app.domains.content_engine.domain.lesson import LESSON_UNIT_ID
from app.shared.rounding_text import wrong_roundings

#: The name of the check tool a plugin lists to have a lesson plan checked.
PLAN_CHECK_TOOL = "check_lesson_plan"


class PlanReview:
    """Finds what stops a plan draft being saved as a plan version, naming each part."""

    def __init__(self, planning: Planning) -> None:
        self._planning = planning

    async def faults(self, db: AsyncSession, draft: Draft) -> list[str]:
        if await self._unchanged(db, draft):
            return []
        plan = assembled(draft)
        found = await self._planning.issues(
            db, session_of(draft), plan.content, strict=not draft.source
        )
        lines = issue_lines(found, plan.places)
        if draft.source:
            return lines
        return [*lines, *wrong_roundings(json.dumps(plan.content, ensure_ascii=False))]

    async def _unchanged(self, db: AsyncSession, draft: Draft) -> bool:
        """Whether a draft that revises a plan holds the plan as it stands, part for part."""
        if draft.saved_as is None:
            return False
        record = await self._planning.current(db, draft.saved_as)
        return record is not None and draft.parts == {
            LESSON_UNIT_ID: record.lesson,
            **record.sections,
        }
