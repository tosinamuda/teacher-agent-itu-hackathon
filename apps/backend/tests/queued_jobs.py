"""Run a queued job's own handler in the test, on the test's session.

The runner would run it in a process of its own against a session of its own; here the
handler's session is the test's, so what it writes is inside the test's transaction.
"""

from __future__ import annotations

import importlib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.jobs.kinds import KINDS
from app.infra.jobs.models import Job
from app.shared.json_types import JsonObject


async def run_queued_job(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch, job_id: str
) -> JsonObject | None:
    """Run the job's handler with its queued arguments; what it returned."""
    job = (await db.execute(select(Job).where(Job.job_id == job_id))).scalar_one()
    module_path, function = KINDS[job.kind].handler.split(":")
    module = importlib.import_module(module_path)

    @asynccontextmanager
    async def _session() -> AsyncIterator[AsyncSession]:
        yield db

    monkeypatch.setattr(module, "AsyncSessionLocal", _session)
    result: JsonObject | None = await getattr(module, function)(*job.args)
    return result
