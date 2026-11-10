"""A chat's events as a server-sent stream: what was kept, then whatever happens next.

The stream starts after the sequence number the page last saw, so a page that lost its
connection asks again from there and misses nothing that was kept. Each event is a frame
``id`` (when kept), ``event`` and ``data``; a page that sends no ``after`` gets the whole chat.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence

from app.domains.artefact_revision.application.chat_feed import ChatFeed, StoredEvent

#: How long the stream waits for the chat to do something before it reads what was kept again,
#: which is how a chat worked on in another process of the app is followed.
POLL_SECONDS = 1.0
#: How long a quiet stream goes before it sends a line that keeps the connection open.
BEAT_SECONDS = 15.0


def frame(event: StoredEvent) -> str:
    """The event as a server-sent frame."""
    lines = [f"id: {event.seq}"] if event.seq is not None else []
    lines += [f"event: {event.kind}", f"data: {json.dumps(event.data, ensure_ascii=False)}"]
    return "\n".join(lines) + "\n\n"


async def stream(
    feed: ChatFeed,
    chat_id: str,
    after: int,
    disconnected: Callable[[], Awaitable[bool]],
    *,
    earlier: Sequence[StoredEvent] = (),
    poll: float = POLL_SECONDS,
    beat: float = BEAT_SECONDS,
) -> AsyncIterator[str]:
    """The chat's frames from ``after`` on, until the page goes away.

    ``earlier`` are events to send first that were never kept, such as the turns of a chat that
    began before events were kept.
    """
    last, quiet = after, 0.0
    for event in earlier:
        yield frame(event)
    async with feed.watching(chat_id) as watchers:
        while not await disconnected():
            for kept in await feed.since(chat_id, last):
                last = kept.seq if kept.seq is not None else last
                quiet = 0.0
                yield frame(kept)
            try:
                live = await asyncio.wait_for(watchers.get(), timeout=poll)
            except TimeoutError:
                quiet += poll
                if quiet >= beat:
                    quiet = 0.0
                    yield ": keep-alive\n\n"
                continue
            if live.seq is None:
                quiet = 0.0
                yield frame(live)
