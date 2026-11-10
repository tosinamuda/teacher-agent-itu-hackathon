"""Draft a lesson plan with the engine, from the lesson's own sources.

The engine's writer reads the lesson period: its facts, the curriculum's notes and the textbook
records its objectives link to. What it writes is saved as a draft plan version for the teacher
to review, and its work is kept as the plan's first chat, which the teacher's comments continue.
While it works, a page that follows the lesson reads what it is doing from a progress channel.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.lesson_plan.jobs import drafting_channel
from app.domains.content.domain.types import BuiltIn
from app.domains.content_engine.infrastructure.chat import HeldTap
from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.creation_chat import OpenChat, keep_creation_chat
from app.domains.content_engine.infrastructure.engine import (
    Engine,
    EngineIncompleteError,
    EngineRefusedError,
    Request,
)
from app.domains.content_engine.infrastructure.progress_tap import ProgressTap
from app.domains.content_engine.infrastructure.tap import TapGroup, tapping
from app.domains.content_engine.infrastructure.writer import WriterStoppedError

_STOPPED = (EngineRefusedError, EngineIncompleteError, WriterStoppedError, CheckerStoppedError)


#: The most of the engine's own reason a teacher is shown when a draft fails.
_REASON_CHARACTERS = 300


class PlanDraftError(RuntimeError):
    """The agent could not write a plan that passes the checks; the message says why."""


@dataclass(frozen=True)
class DraftedPlan:
    plan_id: str
    version_id: str


class PlanGenerator:
    def __init__(self, engine: Engine, feed: ChatFeed, open_chat: OpenChat) -> None:
        self._engine = engine
        self._feed = feed
        self._open_chat = open_chat

    async def draft(
        self, db: AsyncSession, *, session_id: str, for_teacher: str | None
    ) -> DraftedPlan:
        """Write the lesson's plan, save it as a draft, and say where it is."""
        key, held = f"new-{uuid.uuid4().hex}", HeldTap()
        request = Request(type=BuiltIn.LESSON_PLAN.value, session_id=session_id)
        watched = ProgressTap(drafting_channel(session_id))
        await watched.start()
        try:
            with tapping(TapGroup((held, watched))):
                built = await self._engine.build_kept(request, key=key, for_teacher=for_teacher)
        except _STOPPED as error:
            reason = str(error)[:_REASON_CHARACTERS]
            raise PlanDraftError(
                f"The agent could not finish a plan that passes the checks: {reason}"
            ) from error
        # The engine saves the plan in sessions of its own. Ending this session's transaction
        # lets its next read see the new row under repeatable read.
        await db.commit()
        plan_id = await db.scalar(
            select(PlanVersion.plan_id).where(PlanVersion.version_id == built.saved_as)
        )
        if plan_id is None:
            raise LookupError(f"plan_version_not_found:{built.saved_as}")
        await keep_creation_chat(
            self._feed,
            self._open_chat,
            db,
            content_id=plan_id,
            key=key,
            held=held,
            built=built,
            instructions=None,
        )
        return DraftedPlan(plan_id, built.saved_as)
