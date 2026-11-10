"""Artefact-revision orchestration: threads, turns, and per-type executor dispatch."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.concluded_record import is_concluded
from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.executor import (
    RevisionExecutionOutcome,
    RevisionExecutor,
)
from app.domains.artefact_revision.models.revision import RevisionThread, RevisionTurn
from app.domains.generation_log.application.recorder import log_context
from app.shared.concluded import ConcludedLessonError
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.keyed_locks import KeyedLocks
from app.shared.time import utc_now

#: A thread's turns run one at a time: each reads the turns before it and numbers the next.
_TURNS = KeyedLocks()


@dataclass(frozen=True)
class RevisionRecord:
    """One revision turn as a reader needs it: what was asked, and what changed."""

    turn_number: int
    instruction: str
    summary: str | None
    result_version_id: str | None
    created_at: datetime
    #: Where the teacher pointed, when they did: unit, path and the selected text.
    highlight: JsonObject | None = None


@dataclass(frozen=True)
class ChatRecord:
    """One chat on an artefact, as a reader needs it."""

    chat_id: str
    #: 0 for the artefact's own conversation; each chat started after it takes the next number.
    slot: int
    title: str | None
    created_by: str | None
    created_at: datetime
    #: The key the agent's kept session is stored under; none for a chat with no agent of its own.
    agent_key: str | None = None


def _record(thread: RevisionThread) -> ChatRecord:
    return ChatRecord(
        thread.revision_thread_id,
        thread.slot,
        thread.title,
        thread.created_by,
        thread.created_at,
        thread.agent_key,
    )


@dataclass(frozen=True)
class ThreadView:
    """A thread plus its turns and the current artefact (the chat seed)."""

    thread: RevisionThread
    turns: list[RevisionTurn]
    current_version_id: str | None
    current_session_plan: JsonObject | None


class ArtefactRevisionService:
    """One chat-style revision conversation per artefact, dispatched by type.

    ``fallback`` revises every kind without an executor of its own: the content engine's
    types, registered as data.
    """

    def __init__(
        self,
        executors: Sequence[RevisionExecutor],
        fallback: RevisionExecutor | None = None,
    ) -> None:
        self._executors: dict[str, RevisionExecutor] = {
            executor.artefact_type: executor for executor in executors
        }
        self._fallback = fallback

    def _executor(self, artefact_type: str) -> RevisionExecutor | None:
        return self._executors.get(artefact_type, self._fallback)

    async def get_or_create_thread(
        self, *, db: AsyncSession, artefact_type: str, subject_id: str, created_by: str | None
    ) -> RevisionThread:
        """The artefact's own conversation (slot 0), opened if it is not yet."""
        return await self._thread_in_slot(
            db, artefact_type, subject_id, slot=0, created_by=created_by, title=None
        )

    async def create_chat(
        self,
        *,
        db: AsyncSession,
        artefact_type: str,
        subject_id: str,
        created_by: str | None,
        title: str | None,
    ) -> ChatRecord:
        """Another chat on the artefact, with an agent of its own."""
        key = f"chat-{new_public_id(PublicIdPrefix.REVISION_THREAD)}"
        for _ in range(3):
            taken = await db.scalar(
                select(func.max(RevisionThread.slot))
                .where(RevisionThread.artefact_type == artefact_type)
                .where(RevisionThread.subject_id == subject_id)
            )
            try:
                return _record(
                    await self._thread_in_slot(
                        db,
                        artefact_type,
                        subject_id,
                        slot=0 if taken is None else taken + 1,
                        created_by=created_by,
                        title=title,
                        agent_key=key,
                        strict=True,
                    )
                )
            except IntegrityError:
                continue
        raise ArtefactRevisionError(409, "chat_slot_conflict")

    async def open_creation_chat(
        self,
        *,
        db: AsyncSession,
        artefact_type: str,
        subject_id: str,
        created_by: str | None,
        agent_key: str,
    ) -> ChatRecord:
        """The artefact's own conversation, for the agent that made it, so it carries on."""
        thread = await self._thread_in_slot(
            db,
            artefact_type,
            subject_id,
            slot=0,
            created_by=created_by,
            title="Creation",
            agent_key=agent_key,
        )
        if thread.agent_key is None:
            thread.agent_key = agent_key
            await db.commit()
        return _record(thread)

    async def chats(
        self, *, db: AsyncSession, artefact_type: str, subject_id: str
    ) -> list[ChatRecord]:
        """Every chat on the artefact, the first first."""
        return [_record(t) for t in await self._threads(db, artefact_type, subject_id)]

    @staticmethod
    async def _threads(
        db: AsyncSession, artefact_type: str, subject_id: str
    ) -> list[RevisionThread]:
        rows = await db.execute(
            select(RevisionThread)
            .where(RevisionThread.artefact_type == artefact_type)
            .where(RevisionThread.subject_id == subject_id)
            .order_by(RevisionThread.slot.asc())
        )
        return list(rows.scalars().all())

    async def chat_of(
        self, *, db: AsyncSession, artefact_type: str, subject_id: str, chat_id: str
    ) -> ChatRecord:
        """The chat ``chat_id``, when it is one of the artefact's."""
        thread = await self._thread_or_error(db=db, thread_id=chat_id)
        if (thread.artefact_type, thread.subject_id) != (artefact_type, subject_id):
            raise ArtefactRevisionError(404, "revision_thread_not_found")
        return _record(thread)

    async def _thread_in_slot(
        self,
        db: AsyncSession,
        artefact_type: str,
        subject_id: str,
        *,
        slot: int,
        created_by: str | None,
        title: str | None,
        agent_key: str | None = None,
        strict: bool = False,
    ) -> RevisionThread:
        if self._executor(artefact_type) is None:
            raise ArtefactRevisionError(422, f"unsupported_artefact_type:{artefact_type}")
        existing = await self._thread_at(db, artefact_type, subject_id, slot)
        if existing is not None:
            return existing
        thread_id = new_public_id(PublicIdPrefix.REVISION_THREAD)
        thread = RevisionThread(
            revision_thread_id=thread_id,
            artefact_type=artefact_type,
            subject_id=subject_id,
            slot=slot,
            title=title,
            agent_key=agent_key,
            created_by=created_by,
            created_at=utc_now(),
        )
        db.add(thread)
        try:
            await db.commit()
        except IntegrityError:
            # Concurrent "open revision chat" created the thread first — return
            # the winner's so both callers converge on one thread.
            await db.rollback()
            if strict:
                raise
            existing = await self._thread_at(db, artefact_type, subject_id, slot)
            if existing is None:
                raise
            return existing
        await db.refresh(thread)
        return thread

    @staticmethod
    async def _thread_at(
        db: AsyncSession, artefact_type: str, subject_id: str, slot: int
    ) -> RevisionThread | None:
        return (
            (
                await db.execute(
                    select(RevisionThread)
                    .where(RevisionThread.artefact_type == artefact_type)
                    .where(RevisionThread.subject_id == subject_id)
                    .where(RevisionThread.slot == slot)
                )
            )
            .scalars()
            .first()
        )

    async def get_thread_view(self, *, db: AsyncSession, thread_id: str) -> ThreadView:
        thread = await self._thread_or_error(db=db, thread_id=thread_id)
        turns = await self._turns(db=db, thread=thread)
        current_version_id, current_session_plan = await self._current_artefact(
            db=db, thread=thread
        )
        return ThreadView(
            thread=thread,
            turns=turns,
            current_version_id=current_version_id,
            current_session_plan=current_session_plan,
        )

    async def submit_turn(
        self,
        *,
        db: AsyncSession,
        thread_id: str,
        instruction: str,
        highlight: JsonObject | None,
    ) -> tuple[RevisionTurn, RevisionExecutionOutcome]:
        async with _TURNS.of(thread_id):
            return await self._take_turn(
                db=db, thread_id=thread_id, instruction=instruction, highlight=highlight
            )

    async def _take_turn(
        self, *, db: AsyncSession, thread_id: str, instruction: str, highlight: JsonObject | None
    ) -> tuple[RevisionTurn, RevisionExecutionOutcome]:
        thread = await self._thread_or_error(db=db, thread_id=thread_id)
        executor = self._executor(thread.artefact_type)
        if executor is None:
            raise ArtefactRevisionError(422, f"unsupported_artefact_type:{thread.artefact_type}")

        if await is_concluded(db, thread.subject_id):
            raise ArtefactRevisionError(409, ConcludedLessonError.detail)
        prior_turns = await self._turns(db=db, thread=thread)
        try:
            with log_context(
                kind=f"{thread.artefact_type}_revision",
                correlation_id=thread.revision_thread_id,
                subject_id=thread.subject_id,
            ):
                outcome = await executor.revise(
                    db=db,
                    subject_id=thread.subject_id,
                    thread_id=thread.revision_thread_id,
                    instruction=instruction,
                    highlight=highlight,
                    conversation_summary=self._conversation_summary(prior_turns),
                )
        except LookupError as error:
            raise ArtefactRevisionError(404, str(error)) from error

        turn = RevisionTurn(
            revision_turn_id=new_public_id(PublicIdPrefix.REVISION_TURN),
            thread_db_id=thread.id,
            turn_number=len(prior_turns) + 1,
            instruction=instruction,
            highlight=highlight,
            base_version_id=outcome.base_version_id,
            result_version_id=outcome.result_version_id,
            summary=outcome.change_summary,
            validation_passed=outcome.validation_passed,
            created_at=utc_now(),
        )
        db.add(turn)
        try:
            await db.commit()
        except IntegrityError as exc:
            # Concurrent turn on this thread took the same turn_number — surface a
            # clean 409 so the caller retries (sequentially it gets the next number).
            await db.rollback()
            raise ArtefactRevisionError(409, "revision_turn_conflict") from exc
        await db.refresh(turn)
        return turn, outcome

    async def history(
        self, *, db: AsyncSession, artefact_type: str, subject_id: str
    ) -> list[RevisionRecord]:
        """An artefact's revision turns across its chats, oldest first, opening no thread."""
        ordered = [
            (turn, thread.slot)
            for thread in await self._threads(db, artefact_type, subject_id)
            for turn in await self._turns(db=db, thread=thread)
        ]
        # Times are whole seconds, so turns in one second keep their chat's order, then their own.
        ordered.sort(key=lambda found: (found[0].created_at, found[1], found[0].turn_number))
        turns = [turn for turn, _ in ordered]
        return [
            RevisionRecord(
                turn_number=number,
                instruction=turn.instruction,
                summary=turn.summary,
                result_version_id=turn.result_version_id,
                created_at=turn.created_at,
                highlight=turn.highlight,
            )
            for number, turn in enumerate(turns, start=1)
        ]

    async def _thread_or_error(self, *, db: AsyncSession, thread_id: str) -> RevisionThread:
        thread = (
            (
                await db.execute(
                    select(RevisionThread).where(RevisionThread.revision_thread_id == thread_id)
                )
            )
            .scalars()
            .first()
        )
        if thread is None:
            raise ArtefactRevisionError(404, "revision_thread_not_found")
        return thread

    async def _turns(self, *, db: AsyncSession, thread: RevisionThread) -> list[RevisionTurn]:
        rows = await db.execute(
            select(RevisionTurn)
            .where(RevisionTurn.thread_db_id == thread.id)
            .order_by(RevisionTurn.turn_number.asc())
        )
        return list(rows.scalars().all())

    async def _current_artefact(
        self, *, db: AsyncSession, thread: RevisionThread
    ) -> tuple[str | None, JsonObject | None]:
        """Delegate to the per-type executor — the registry decides; the service forwards."""
        executor = self._executor(thread.artefact_type)
        if executor is None:
            return None, None
        return await executor.current_artefact(db=db, subject_id=thread.subject_id)

    def _conversation_summary(self, turns: list[RevisionTurn]) -> str:
        if not turns:
            return ""
        return "\n".join(
            f"{turn.turn_number}. asked: {turn.instruction} -> {turn.summary or 'revised'}"
            for turn in turns
        )
