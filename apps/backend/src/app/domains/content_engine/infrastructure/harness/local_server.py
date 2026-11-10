"""An ASGI app served on a free port of localhost, in this process's event loop."""

from __future__ import annotations

import asyncio
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from starlette.types import ASGIApp


@asynccontextmanager
async def served_locally(app: ASGIApp) -> AsyncIterator[int]:
    """The port ``app`` answers on, for the length of the block."""
    listening = socket.socket()
    listening.bind(("127.0.0.1", 0))
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning"))
    serving = asyncio.create_task(server.serve(sockets=[listening]))
    while not server.started and not serving.done():
        await asyncio.sleep(0.01)
    try:
        yield int(listening.getsockname()[1])
    finally:
        server.should_exit = True
        await serving
