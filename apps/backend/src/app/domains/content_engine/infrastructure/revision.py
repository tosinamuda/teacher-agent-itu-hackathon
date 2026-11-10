"""Revise engine-built content in place from the teacher's feedback.

The content is reopened as a draft with its parts, the writer changes the parts the feedback
concerns, and the revised version goes back to pending review.
"""

from __future__ import annotations

from dataclasses import replace

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.artefact_revision.application.executor import RevisionExecutionOutcome
from app.domains.artefact_revision.application.highlight import format_highlight
from app.domains.artefact_revision.models.revision import RevisionThread
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content.application.errors import ContentError
from app.domains.content.domain.types import Engine as BuildEngine
from app.domains.content_engine.application.drafting_ports import ContentReader
from app.domains.content_engine.domain.turn import TurnStoppedError
from app.domains.content_engine.infrastructure.chat import ThreadTap
from app.domains.content_engine.infrastructure.engine import (
    Built,
    Engine,
    EngineIncompleteError,
    EngineRefusedError,
    Request,
)
from app.domains.content_engine.infrastructure.live import (
    LiveConversations,
    TooManyConversationsError,
)
from app.domains.content_engine.infrastructure.tap import AgentChatEvent, Tap
from app.domains.content_engine.infrastructure.writer import WriterStoppedError
from app.shared.json_types import JsonObject
from app.shared.keyed_locks import KeyedLocks

#: One chat works on a content at a time: each turn starts from the version the last one made.
_CONTENT = KeyedLocks()

#: Where in content a teacher can point: a unit and the path of a field in its part, or, in a
#: lesson plan, a step, a block of it, or a lesson objective.
_ANCHORS = ("unit_id", "path", "step_id", "block_id", "lesson_objective_id")


def _feedback(instruction: str, highlight: JsonObject | None) -> str:
    lines = [instruction]
    if pointed := format_highlight(highlight, _ANCHORS):
        lines.append(f"The teacher pointed at: {pointed}")
    return "\n\n".join(lines)


def _unplaced_text(highlight: JsonObject | None) -> str:
    """The text a highlight selects when it does not say where in the content it is."""
    if highlight is None or any(highlight.get(anchor) for anchor in _ANCHORS):
        return ""
    return str(highlight.get("selected_text") or "").strip()


def _earlier(conversation_summary: str) -> str:
    return (
        f"Earlier turns of this conversation:\n{conversation_summary}"
        if conversation_summary
        else ""
    )


class EngineRevisionExecutor:
    """The revision executor for engine types, and for lesson plans, which the engine drafts too.

    Registered under ``artefact_type``: the service falls back to the default one for every
    type that has no executor of its own.
    """

    def __init__(
        self,
        engine: Engine,
        content: ContentReader,
        catalogue: ContentCatalogue,
        live: LiveConversations | None = None,
        chat: ChatFeed | None = None,
        artefact_type: str = "engine",
    ) -> None:
        """With ``live``, the writer is kept between a chat's turns, so each turn continues.

        Without it, each turn is a run of its own, told what the turns before it did. With
        ``chat``, what happens in a turn is kept in the chat's transcript and shown to whoever
        watches it.
        """
        self._engine = engine
        self._content = content
        self._catalogue = catalogue
        self._live = live
        self._chat = chat
        self.artefact_type = artefact_type

    async def current_artefact(
        self, *, db: AsyncSession, subject_id: str
    ) -> tuple[str | None, JsonObject | None]:
        stored = await self._content.get(db, subject_id)
        return (stored.content_id, stored.manifest) if stored is not None else (None, None)

    async def revise(
        self,
        *,
        db: AsyncSession,
        subject_id: str,
        thread_id: str,
        instruction: str,
        highlight: JsonObject | None,
        conversation_summary: str,
    ) -> RevisionExecutionOutcome:
        request = await self._request(db, subject_id)
        key = await db.scalar(
            select(RevisionThread.agent_key).where(RevisionThread.revision_thread_id == thread_id)
        )
        tap = ThreadTap(self._chat, thread_id) if self._chat is not None else None
        if tap is not None:
            await tap.emit(AgentChatEvent("user_message", _said(instruction, highlight)))
        try:
            async with _CONTENT.of(subject_id):
                built = await self._built(
                    request,
                    thread_id,
                    key or subject_id,
                    _feedback(instruction, highlight),
                    _earlier(conversation_summary),
                    tap,
                    _unplaced_text(highlight),
                )
        except TurnStoppedError:
            if tap is not None:
                await tap.emit(AgentChatEvent("turn_stopped", {}))
            raise
        except Exception as error:
            problem = _translated(error)
            if tap is not None:
                await tap.emit(AgentChatEvent("turn_failed", {"error": str(problem) or "failed"}))
            raise problem from error
        if tap is not None:
            await _report(tap, built, subject_id)
        summary = built.summary if built.changed else f"No change was made. {built.summary}".strip()
        return RevisionExecutionOutcome(
            base_version_id=subject_id,
            result_version_id=built.saved_as,
            session_plan=built.content,
            change_summary=summary,
            validation_passed=True,
        )

    async def _request(self, db: AsyncSession, subject_id: str) -> Request:
        stored = await self._content.get(db, subject_id)
        if stored is None:
            raise LookupError("artefact_not_found")
        try:
            definition = await self._catalogue.type_of_kind(db, stored.kind)
        except ContentError as error:
            raise LookupError("artefact_not_found") from error
        if stored.session_id is not None:
            return Request(
                type=definition.slug, session_id=stored.session_id, content_id=subject_id
            )
        if definition.engine is not BuildEngine.MCP:
            raise LookupError("artefact_not_found")
        return Request(
            type=definition.slug, plan_version_id=stored.plan_version_id, content_id=subject_id
        )

    async def _built(
        self,
        request: Request,
        thread_id: str,
        key: str,
        feedback: str,
        earlier: str,
        tap: Tap | None,
        pointed: str,
    ) -> Built:
        if self._live is None:
            told = "\n\n".join(filter(None, (feedback, earlier)))
            return await self._engine.build(replace(request, feedback=told))
        return await self._live.say(
            thread_id,
            lambda: self._engine.converse(request, key=key),
            feedback,
            earlier,
            tap,
            pointed,
        )


def _said(instruction: str, highlight: JsonObject | None) -> JsonObject:
    return {"text": instruction, **({"highlight": highlight} if highlight else {})}


def _translated(error: Exception) -> Exception:
    """The error as the revision service reads it: a refusal, or a failure to be retried."""
    if isinstance(error, EngineRefusedError):
        return ValueError(str(error))
    if isinstance(error, EngineIncompleteError | WriterStoppedError | TooManyConversationsError):
        return RuntimeError(str(error))
    return error


async def _report(tap: Tap, built: Built, content_id: str) -> None:
    """The end of a turn: what the agent said it did, and, if the content changed, the content."""
    done: JsonObject = {"summary": built.summary, "changed": built.changed}
    if built.version is not None:
        done["version"] = built.version
    await tap.emit(AgentChatEvent("turn_done", done))
    if built.changed:
        view: JsonObject = {"tool": "show_content", "input": {"content_id": content_id}}
        await tap.emit(AgentChatEvent("view", view))
