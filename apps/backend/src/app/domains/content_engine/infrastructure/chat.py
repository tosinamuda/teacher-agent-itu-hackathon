"""Taps that carry an agent's events into a chat: into its transcript, or held until it exists."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.content_engine.infrastructure.tap import AgentChatEvent


@dataclass(frozen=True)
class ThreadTap:
    """What happens in a message goes to the chat's transcript, and to whoever is watching it."""

    feed: ChatFeed
    thread_id: str

    async def emit(self, event: AgentChatEvent) -> None:
        if event.persisted:
            await self.feed.record(self.thread_id, event.kind, event.data)
        else:
            self.feed.show(self.thread_id, event.kind, event.data)


@dataclass
class HeldTap:
    """The events of a run whose chat does not exist yet, to be written into it once it does."""

    held: list[AgentChatEvent] = field(default_factory=list)

    async def emit(self, event: AgentChatEvent) -> None:
        """Keep the event with the time it happened: written later, its row would say when."""
        if event.persisted:
            self.held.append(
                AgentChatEvent(event.kind, {**event.data, "at": round(time.time(), 2)})
            )

    async def write_into(self, feed: ChatFeed, thread_id: str) -> None:
        for event in self.held:
            await feed.record(thread_id, event.kind, event.data)
