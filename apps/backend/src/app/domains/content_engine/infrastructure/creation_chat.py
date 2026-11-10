"""The agent's work in creating content, kept as the content's first chat."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.content_engine.infrastructure.chat import HeldTap
from app.domains.content_engine.infrastructure.engine import Built
from app.domains.content_engine.infrastructure.tap import AgentChatEvent
from app.shared.json_types import JsonObject

#: Opens the content's own chat, for the agent kept under a key, and says what the chat is.
OpenChat = Callable[[AsyncSession, str, str], Awaitable[str]]


def _done(built: Built) -> JsonObject:
    done: JsonObject = {"summary": built.summary, "changed": True}
    if built.version is not None:
        done["version"] = built.version
    return done


async def keep_creation_chat(
    feed: ChatFeed,
    open_chat: OpenChat,
    db: AsyncSession,
    *,
    content_id: str,
    key: str,
    held: HeldTap,
    built: Built,
    instructions: str | None,
) -> None:
    """Make what the agent did the content's first chat, which the teacher's comments continue."""
    chat = await open_chat(db, content_id, key)
    events = [
        *([AgentChatEvent("user_message", {"text": instructions})] if instructions else []),
        *held.held,
        AgentChatEvent("turn_done", _done(built)),
        AgentChatEvent("view", {"tool": "show_content", "input": {"content_id": content_id}}),
    ]
    for event in events:
        await feed.record(chat, event.kind, event.data)
