"""The events of a chat: kept in order so a page can replay them, and handed to whoever watches.

Each event a chat keeps gets the next sequence number. A page that opens the chat, or that lost
its connection, asks for what came after the last number it saw, then watches. What is only for
a page that is watching, such as the text written so far, is handed to the watchers and never kept.
Watchers in another process of the app are served by reading what was kept.
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.models.revision import ChatEvent, RevisionThread
from app.shared.json_types import JsonObject
from app.shared.time import utc_now

Sessions = Callable[[], AbstractAsyncContextManager[AsyncSession]]


@dataclass(frozen=True)
class StoredEvent:
    #: Its place in the chat's transcript; none for an event that was not kept.
    seq: int | None
    kind: str
    data: JsonObject
    at: datetime | None = None


class ChatFeed:
    def __init__(self, sessions: Sessions) -> None:
        self._sessions = sessions
        self._watchers: dict[str, set[asyncio.Queue[StoredEvent]]] = {}

    async def record(self, thread_id: str, kind: str, data: JsonObject) -> StoredEvent:
        """Keep an event in the chat's transcript, and hand it to the watchers."""
        async with self._sessions() as db:
            thread_db_id = await self._thread(db, thread_id)
            event = ChatEvent(thread_db_id=thread_db_id, kind=kind, data=data, created_at=utc_now())
            db.add(event)
            await db.commit()
            stored = StoredEvent(event.seq, kind, data, event.created_at)
        self._hand_out(thread_id, stored)
        return stored

    def show(self, thread_id: str, kind: str, data: JsonObject) -> None:
        """Hand an event to the watchers without keeping it."""
        self._hand_out(thread_id, StoredEvent(None, kind, data))

    async def since(self, thread_id: str, after: int, limit: int = 200) -> list[StoredEvent]:
        """The kept events after sequence number ``after``, in order."""
        async with self._sessions() as db:
            thread_db_id = await self._thread(db, thread_id)
            rows = await db.execute(
                select(ChatEvent)
                .where(ChatEvent.thread_db_id == thread_db_id)
                .where(ChatEvent.seq > after)
                .order_by(ChatEvent.seq.asc())
                .limit(limit)
            )
            return [StoredEvent(e.seq, e.kind, e.data, e.created_at) for e in rows.scalars()]

    @asynccontextmanager
    async def watching(self, thread_id: str) -> AsyncIterator[asyncio.Queue[StoredEvent]]:
        """A queue of what is handed out for the chat while the block runs."""
        queue: asyncio.Queue[StoredEvent] = asyncio.Queue()
        self._watchers.setdefault(thread_id, set()).add(queue)
        try:
            yield queue
        finally:
            self._watchers[thread_id].discard(queue)
            if not self._watchers[thread_id]:
                del self._watchers[thread_id]

    def _hand_out(self, thread_id: str, event: StoredEvent) -> None:
        for queue in self._watchers.get(thread_id, ()):
            queue.put_nowait(event)

    @staticmethod
    async def _thread(db: AsyncSession, thread_id: str) -> uuid.UUID:
        found = await db.scalar(
            select(RevisionThread.id).where(RevisionThread.revision_thread_id == thread_id)
        )
        if found is None:
            raise LookupError(f"revision_thread_not_found:{thread_id}")
        return found
