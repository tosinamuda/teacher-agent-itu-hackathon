"""Run a job's async handler without leaking DB connections past its event loop.

A job's process runs its handler through ``asyncio.run`` — a brand-new event loop. The
module-level async ``engine`` (``app.db.session``) pools aiomysql connections, and a pooled
connection is bound to the loop that opened it; used on another loop it raises
``RuntimeError: got Future attached to a different loop`` on the very first statement.

``run_in_worker`` disposes the pool inside the handler's own loop, so no connection ever
outlives the loop that owns it, and the process exits with its connections closed.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from typing import TypeVar

from app.db.session import engine

T = TypeVar("T")


def run_in_worker(coro: Awaitable[T]) -> T:
    """Run ``coro`` in a fresh event loop, then dispose the async engine pool."""

    async def _runner() -> T:
        try:
            return await coro
        finally:
            await engine.dispose()

    return asyncio.run(_runner())
