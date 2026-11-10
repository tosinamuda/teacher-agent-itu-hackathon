"""The ops panel reads the job queue straight from its tables.

Whether jobs are being run has two causes an operator must tell apart: no runner is taking
them, or every runner is busy. The runners' last-seen times and the oldest wait say which.
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.ops.application import job_ops
from app.infra.jobs.kinds import RUN_CONDITIONED_EXECUTION, SYNTHETIC_RATE
from app.infra.jobs.models import Job, JobRunner, JobState
from app.infra.jobs.queue import JobQueue
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from app.shared.time import utc_now

pytestmark = pytest.mark.asyncio

_ADMIN = Actor(role="admin", auth_id="code|admin-1", full_name="Admin One")


async def _runner(db: AsyncSession, name: str, *, silent_for: timedelta) -> None:
    seen = utc_now() - silent_for
    db.add(JobRunner(runner=name, slots=4, running=1, started_at=seen, seen_at=seen))
    await db.flush()


async def _jobs(db: AsyncSession, *states: JobState) -> None:
    """One job per state given, the first the oldest, a minute apart."""
    for index, state in enumerate(states):
        subject = f"EXE-{index}"
        JobQueue(db).add(RUN_CONDITIONED_EXECUTION, subject, subject=subject)
        await db.flush()
        await db.execute(
            update(Job)
            .where(Job.subject == subject)
            .values(state=state, created_at=utc_now() - timedelta(minutes=10 - index))
        )


async def test_a_runner_seen_just_now_is_online_and_a_silent_one_is_not(db: AsyncSession) -> None:
    await _runner(db, "api:1", silent_for=timedelta(seconds=5))
    await _runner(db, "api:0", silent_for=timedelta(minutes=5))

    runners = {
        runner["runner"]: runner["online"] for runner in (await job_ops.job_health(db))["runners"]
    }

    assert runners == {"api:1": True, "api:0": False}


async def test_health_counts_jobs_by_state_and_ages_the_oldest_waiting(db: AsyncSession) -> None:
    await _jobs(db, JobState.QUEUED, JobState.QUEUED, JobState.RUNNING, JobState.FAILED)

    health = await job_ops.job_health(db)

    assert health["counts"] == {
        "queued": 2,
        "running": 1,
        "succeeded": 0,
        "failed": 1,
        "cancelled": 0,
    }
    assert health["oldest_queued_age_seconds"] == pytest.approx(600, abs=5)


async def test_unfinished_jobs_are_listed_first(db: AsyncSession) -> None:
    await _jobs(db, JobState.FAILED, JobState.QUEUED, JobState.SUCCEEDED, JobState.RUNNING)

    listed = [job["state"] for job in await job_ops.recent_jobs(db)]

    assert listed == ["running", "queued", "succeeded", "failed"]


async def test_cancelling_a_job_ends_it_once(db: AsyncSession) -> None:
    job_id = JobQueue(db).add(SYNTHETIC_RATE, "EXP-1", subject="EXP-1")
    await db.flush()

    assert await job_ops.cancel_job(db, job_id) == {"ok": True, "detail": JobState.CANCELLED}
    assert await job_ops.cancel_job(db, job_id) == {"ok": True, "detail": JobState.CANCELLED}
    assert await job_ops.cancel_job(db, "JOB-none") == {"ok": False, "detail": "job_not_found"}


async def test_the_health_route_reports_the_runners(db: AsyncSession, monkeypatch) -> None:
    async def _allow(*_args, **_kwargs) -> None:
        """The Casbin layer has its own tests in ``test_authz.py``."""

    async def _db():  # type: ignore[no-untyped-def]
        yield db

    monkeypatch.setattr(authz, "enforce", _allow)
    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_actor] = lambda: _ADMIN
    await _runner(db, "api:1", silent_for=timedelta(seconds=1))
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            health = (await client.get("/ops/health")).json()
    finally:
        app.dependency_overrides.clear()

    assert [runner["runner"] for runner in health["runners"]] == ["api:1"]
    assert health["slots_per_runner"] == 4
