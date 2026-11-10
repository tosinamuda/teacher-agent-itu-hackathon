"""The lesson plan an agent has written so far, read from its open draft."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content_engine.application.plan_outline import PlanOutline, outline_of
from app.domains.content_engine.infrastructure.drafts import SqlAlchemyDrafts

LESSON_PLAN_TYPE = "lesson-plan"


async def drafting_outline(db: AsyncSession, session_id: str) -> PlanOutline | None:
    """What the lesson's open plan draft sets out so far, or none when no draft is open."""
    draft = await SqlAlchemyDrafts().latest_open(db, LESSON_PLAN_TYPE, session_id)
    return outline_of(draft.units, draft.parts) if draft is not None else None
