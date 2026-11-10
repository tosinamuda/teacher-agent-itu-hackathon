"""What the API does as it starts and stops."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import CONFIG
from app.db.default_school import ensure_default_school
from app.db.session import AsyncSessionLocal
from app.domains.content.infrastructure.wiring import COMMENT_DESK, LIVE_CONVERSATIONS
from app.domains.content_engine.infrastructure.harness.opencode_home import prune
from app.infra.jobs.claims import JobClaims, this_runner
from app.infra.jobs.runner import Runner


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Make sure the default school exists, then run queued jobs and MCP sessions until it stops.

    Agents kept for threads not used in a month are removed as it starts.

    The runner claims each job and runs it in a process of its own, so requests are served
    while a long generation runs.
    """
    async with AsyncSessionLocal() as db:
        await ensure_default_school(session=db)
    await asyncio.to_thread(prune)
    claims = JobClaims(
        AsyncSessionLocal, runner=this_runner(), lease_seconds=CONFIG.jobs.lease_seconds
    )
    runner = Runner(claims, CONFIG.jobs)
    running = asyncio.create_task(runner.run())
    async with app.state.content_mcp.session_manager.run():
        yield
    await COMMENT_DESK.close()
    await LIVE_CONVERSATIONS.close_all()
    runner.stop()
    await running
