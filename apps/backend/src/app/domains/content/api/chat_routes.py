"""Chats on content: list them, start one, send a message to one, and follow one live."""

from __future__ import annotations

from datetime import datetime
from typing import NoReturn

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.db.session import AsyncSessionLocal
from app.domains.artefact_revision.application.chat_feed import StoredEvent
from app.domains.artefact_revision.application.chat_stream import stream
from app.domains.artefact_revision.application.service import ChatRecord
from app.domains.artefacts.types.lesson_plan.application.ownership import teacher_owns_plan_version
from app.domains.content.application.errors import ContentError
from app.domains.content.application.records import ContentRecord
from app.domains.content.infrastructure.wiring import (
    CHAT_FEED,
    COMMENT_DESK,
    LIVE_CONVERSATIONS,
    build_content_service,
)
from app.domains.content_engine.application.comments import Comment
from app.shared.auth import ROLE_TEACHER, Actor, actor_for_code
from app.shared.authz import enforce, requires
from app.shared.json_types import JsonObject

router = APIRouter(prefix="/content", tags=["content-chats"])

MAX_MESSAGE = 4000


class ChatResponse(BaseModel):
    chat_id: str
    #: 0 is the content's own chat, the one its agent began in.
    slot: int
    title: str | None
    created_by: str | None
    created_at: datetime
    working: bool

    @classmethod
    def of(cls, chat: ChatRecord, content_id: str) -> ChatResponse:
        return cls(
            chat_id=chat.chat_id,
            slot=chat.slot,
            title=chat.title,
            created_by=chat.created_by,
            created_at=chat.created_at,
            working=bool(COMMENT_DESK.standing(content_id, _desk_chat(chat)).get("working")),
        )


class NewChatRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)


class MessageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_MESSAGE)
    unit_id: str | None = None
    path: str | None = None
    #: Where in a lesson plan the teacher pointed: a step, a block of it, a lesson objective.
    step_id: str | None = Field(None, max_length=64)
    block_id: str | None = Field(None, max_length=64)
    lesson_objective_id: str | None = Field(None, max_length=64)
    selected_text: str | None = Field(None, max_length=2000)


class Accepted(BaseModel):
    waiting: int


class Stopped(BaseModel):
    #: Whether a turn was in progress and was stopped.
    stopped: bool
    #: How many messages that had not begun were dropped.
    dropped: int


def _desk_chat(chat: ChatRecord) -> str | None:
    """The comment desk names the content's own chat by leaving the chat out."""
    return None if chat.slot == 0 else chat.chat_id


def _raise(error: ContentError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail) from error


async def _owned(actor: Actor, db: AsyncSession, content_id: str) -> ContentRecord:
    try:
        record = await build_content_service().record(db, content_id)
    except ContentError as error:
        _raise(error)
    if (
        actor.role == ROLE_TEACHER
        and actor.teacher_id is not None
        and not await teacher_owns_plan_version(
            db, teacher_id=actor.teacher_id, plan_version_id=record.plan_version_id
        )
    ):
        raise HTTPException(status_code=403, detail="not_your_class")
    return record


@router.get("/{content_id}/chats", response_model=list[ChatResponse])
async def list_chats(
    content_id: str,
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[ChatResponse]:
    """Every chat on the content, the first first: the page shows any of them, not one session."""
    await _owned(actor, db, content_id)
    try:
        return [
            ChatResponse.of(c, content_id)
            for c in await build_content_service().chats(db, content_id)
        ]
    except ContentError as error:
        _raise(error)


@router.post("/{content_id}/chats", response_model=ChatResponse, status_code=201)
async def start_chat(
    content_id: str,
    body: NewChatRequest,
    actor: Actor = Depends(requires(obj="artefact_revision:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Start another chat on the content, with an agent of its own."""
    await _owned(actor, db, content_id)
    try:
        chat = await build_content_service().new_chat(
            db, content_id=content_id, requested_by=actor.display_name, title=body.title
        )
    except ContentError as error:
        _raise(error)
    return ChatResponse.of(chat, content_id)


@router.post("/{content_id}/chats/{chat_id}/messages", response_model=Accepted, status_code=202)
async def send_message(
    content_id: str,
    chat_id: str,
    body: MessageRequest,
    actor: Actor = Depends(requires(obj="artefact_revision:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> Accepted:
    """Send a message to the chat's agent. It is taken at once and answered in the background."""
    await _owned(actor, db, content_id)
    try:
        chat = await build_content_service().chat(db, content_id, chat_id)
    except ContentError as error:
        _raise(error)
    highlight: JsonObject = {
        key: value
        for key, value in (
            ("unit_id", body.unit_id),
            ("path", body.path),
            ("step_id", body.step_id),
            ("block_id", body.block_id),
            ("lesson_objective_id", body.lesson_objective_id),
            ("selected_text", (body.selected_text or "").strip() or None),
        )
        if value
    }
    comment = Comment(body.text.strip(), highlight or None, actor.display_name)
    return Accepted(waiting=COMMENT_DESK.take(content_id, comment, _desk_chat(chat)))


@router.post("/{content_id}/chats/{chat_id}/stop", response_model=Stopped)
async def stop_chat(
    content_id: str,
    chat_id: str,
    actor: Actor = Depends(requires(obj="artefact_revision:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> Stopped:
    """Stop what the chat's agent is doing, and drop the messages waiting. Nothing is saved.

    The content stays as it was, and the agent keeps what it did, so the next message goes on
    from there. The chat's stream says the turn stopped.
    """
    await _owned(actor, db, content_id)
    try:
        chat = await build_content_service().chat(db, content_id, chat_id)
    except ContentError as error:
        _raise(error)
    dropped = COMMENT_DESK.drop_waiting(content_id, _desk_chat(chat))
    return Stopped(stopped=await LIVE_CONVERSATIONS.stop(chat.chat_id), dropped=dropped)


@router.get("/{content_id}/chats/{chat_id}/events")
async def follow_chat(
    request: Request,
    content_id: str,
    chat_id: str,
    after: int = 0,
    x_teacher_code: str | None = Header(default=None, alias="x-teacher-code"),
) -> StreamingResponse:
    """The chat as a server-sent stream, from the event after ``after``, until the page leaves.

    The caller is checked here, with a session that is closed before the stream starts, so a
    page that stays open holds no database connection.
    """
    async with AsyncSessionLocal() as db:
        actor = await actor_for_code(db, x_teacher_code)
        await enforce(actor, obj="content:*", act="read", db=db)
        await _owned(actor, db, content_id)
        try:
            await build_content_service().chat(db, content_id, chat_id)
        except ContentError as error:
            _raise(error)
        earlier = await _turns_before_events(db, content_id, chat_id) if after == 0 else []
    frames = stream(CHAT_FEED, chat_id, after, request.is_disconnected, earlier=earlier)
    return StreamingResponse(
        frames,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


async def _turns_before_events(
    db: AsyncSession, content_id: str, chat_id: str
) -> list[StoredEvent]:
    """The turns of a chat that has none of its events, as events, so an older chat reads too."""
    if await CHAT_FEED.since(chat_id, 0, limit=1):
        return []
    chat = await build_content_service().chat(db, content_id, chat_id)
    if chat.slot != 0:
        return []
    events: list[StoredEvent] = []
    for turn in await build_content_service().revisions(db, content_id):
        said: JsonObject = {"text": turn.instruction}
        if turn.highlight:
            said["highlight"] = turn.highlight
        events.append(StoredEvent(None, "user_message", said))
        events.append(
            StoredEvent(None, "turn_done", {"summary": turn.summary or "Done.", "changed": True})
        )
    return events
