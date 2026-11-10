"""Regression: the Celery worker must survive many async tasks in one process.

Celery runs each task through its own ``asyncio.run`` — a fresh event loop per
task. The module-level async engine (``app.db.session.engine``) pools aiomysql
connections, and a pooled connection is bound to the loop that opened it. Without
disposing the pool per task, the *second* task in a worker process checks out a
connection bound to the first (now-closed) loop and dies on its first statement
with ``RuntimeError: ... attached to a different loop`` — which escapes before the
task body can mark its row ``failed`` and strands the execution in ``queued``
(diagnosed 2026-06-16: conditioned-execution dispatch was a coin-flip).

``run_in_worker`` disposes the pool inside each task's own loop, so no connection
outlives the loop that owns it. This pins that the helper is loop-safe across the
repeated dispatches a single worker process handles during a study.
"""

from __future__ import annotations

import pytest
from sqlalchemy import text
from sqlalchemy.exc import InterfaceError, OperationalError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.session import AsyncSessionLocal
from app.infra.worker_async import run_in_worker

_UNREACHABLE = (OperationalError, InterfaceError, OSError)


async def _select_one(session_factory: async_sessionmaker) -> None:
    async with session_factory() as session:
        await session.execute(text("SELECT 1"))


@pytest.fixture
def _require_async_db() -> None:
    """Skip (don't fail) when the async DB isn't reachable from this process."""
    try:
        run_in_worker(_select_one(AsyncSessionLocal))
    except _UNREACHABLE as exc:  # pragma: no cover - environment-dependent
        pytest.skip(f"async DB not reachable for loop-safety test: {exc}")


def test_run_in_worker_survives_repeated_tasks(_require_async_db: None) -> None:
    """Four sequential 'tasks' in one process — the pre-fix code died on #2.

    Pre-fix (a bare ``asyncio.run`` with no ``engine.dispose``) the second
    iteration checked out a pooled connection bound to the first iteration's
    closed loop and raised ``RuntimeError: ... attached to a different loop``.
    With ``run_in_worker`` disposing the pool inside each loop, every iteration
    starts clean and all four complete.
    """
    for _ in range(4):
        run_in_worker(_select_one(AsyncSessionLocal))
