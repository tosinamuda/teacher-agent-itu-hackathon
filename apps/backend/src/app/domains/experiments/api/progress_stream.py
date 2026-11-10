"""Relay a progress channel to a WebSocket, as a job's process reports on it.

Both experiment progress streams (synthetic-test flows, generation) are server→client: a
job writes events to a channel in the ``progress_events`` table, and this sends each one to
the browser as it appears, reading what is new every half second.

A send-only loop would leak the handler coroutine: ``WebSocketDisconnect`` is only surfaced
when the handler *receives* from the socket, so it would never see a client close or a
server shutdown (uvicorn ``--reload`` delivers a ``websocket.disconnect`` the same way) and
would block graceful shutdown. So the forwarder and a disconnect-watcher run concurrently,
and everything is torn down as soon as either finishes.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging

from fastapi import WebSocket, WebSocketDisconnect

from app.db.session import AsyncSessionLocal
from app.infra import progress

logger = logging.getLogger(__name__)

#: How often the relay reads what is new on its channel.
_POLL_SECONDS = 0.5


async def _forward(websocket: WebSocket, channel: str) -> None:
    """Send every event written to ``channel`` after the socket opened, until cancelled."""
    async with AsyncSessionLocal() as session:
        await progress.forget_old(session)
        seen = await progress.latest(session, channel)
        await session.commit()
    while True:
        await asyncio.sleep(_POLL_SECONDS)
        async with AsyncSessionLocal() as session:
            events = await progress.after(session, channel, seen)
        for event_id, payload in events:
            await websocket.send_text(json.dumps(payload))
            seen = event_id


async def _wait_for_disconnect(websocket: WebSocket) -> None:
    """Resolve when the peer goes away.

    These are server→client streams; the client never sends data frames, so
    the first inbound message is always the disconnect. Reading is the only
    way Starlette surfaces a client close — or a server-shutdown disconnect —
    to the handler, so this is what lets graceful shutdown actually complete.
    """
    with contextlib.suppress(WebSocketDisconnect):
        while True:
            await websocket.receive()


async def stream_channel_to_websocket(websocket: WebSocket, channel: str) -> None:
    """Accept the socket and relay ``channel`` to it until either side closes.

    Cancels both the forwarder and the disconnect-watcher the moment one of them finishes,
    so no coroutine is left running after the connection ends.
    """
    await websocket.accept()
    forward = asyncio.ensure_future(_forward(websocket, channel))
    watch = asyncio.ensure_future(_wait_for_disconnect(websocket))
    try:
        done, _pending = await asyncio.wait({forward, watch}, return_when=asyncio.FIRST_COMPLETED)
        # Surface a genuine forwarder error (not a normal disconnect) to the
        # log so a broken stream isn't swallowed by the teardown below.
        for task in done:
            if task is forward and not task.cancelled():
                exc = task.exception()
                if exc is not None and not isinstance(exc, WebSocketDisconnect):
                    logger.warning("progress stream forwarder failed: %s", exc)
    finally:
        forward.cancel()
        watch.cancel()
