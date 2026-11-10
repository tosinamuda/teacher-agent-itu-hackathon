"""Generate content of any engine type: the content service's generator for every one."""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.domain.types import Level
from app.domains.content.progress import generation_channel
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


class EngineGenerator:
    def __init__(
        self, engine: Engine, feed: ChatFeed | None = None, open_chat: OpenChat | None = None
    ) -> None:
        """With ``feed`` and ``open_chat``, what the agent did is kept as the content's own chat."""
        self._engine = engine
        self._feed = feed
        self._open_chat = open_chat

    def check(self, level: Level, choices: GenerationChoices) -> None:
        if level is not Level.CLASS:
            raise ContentError(422, "engine_types_are_class_level_only")

    async def generate(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> str:
        self.check(level, choices)
        kept, held = f"new-{uuid.uuid4().hex}", HeldTap()
        request = Request(
            type=type,
            plan_version_id=plan_version_id,
            feedback=choices.instructions or "",
            generator=choices.pipeline,
        )
        watched = ProgressTap(generation_channel(plan_version_id, type))
        await watched.start()
        try:
            with tapping(TapGroup((held, watched))):
                built = await self._engine.build_kept(request, key=kept)
        except EngineRefusedError as error:
            raise ContentError(422, str(error)) from error
        except (EngineIncompleteError, WriterStoppedError, CheckerStoppedError) as error:
            raise ContentError(502, str(error)) from error
        # The engine stores the content in sessions of its own. Ending this session's
        # transaction lets its next read see the new row under repeatable read.
        await db.commit()
        if self._feed is not None and self._open_chat is not None:
            await keep_creation_chat(
                self._feed,
                self._open_chat,
                db,
                content_id=built.saved_as,
                key=kept,
                held=held,
                built=built,
                instructions=choices.instructions,
            )
        return built.saved_as
