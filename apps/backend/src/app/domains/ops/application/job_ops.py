"""The job queue as the admin ops panel sees it: who is running jobs, what is waiting, what failed.

Everything is one query on the jobs tables, so the panel's poll is cheap.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import CONFIG
from app.infra.jobs.claims import finish
from app.infra.jobs.models import UNFINISHED, Job, JobRunner, JobState
from app.shared.time import as_utc, utc_now

#: A runner reports every ten seconds; one silent for three reports is taken to be gone.
_RUNNER_SILENCE = timedelta(seconds=30)


def _aware(moment: datetime | None) -> datetime | None:
    return None if moment is None else as_utc(moment)


def _iso(moment: datetime | None) -> str | None:
    aware = _aware(moment)
    return aware.isoformat() if aware else None


async def job_health(db: AsyncSession) -> dict[str, Any]:
    """The runners, how many jobs are in each state, and how long the oldest has waited."""
    now = utc_now()
    runners = (await db.execute(select(JobRunner).order_by(JobRunner.seen_at.desc()))).scalars()
    counts = dict(
        (await db.execute(select(Job.state, func.count()).group_by(Job.state))).tuples().all()
    )
    oldest = await db.scalar(select(func.min(Job.created_at)).where(Job.state == JobState.QUEUED))
    oldest_aware = _aware(oldest)
    return {
        "runners": [_runner(runner, now) for runner in runners],
        "counts": {state.value: counts.get(state.value, 0) for state in JobState},
        "oldest_queued_age_seconds": (
            None if oldest_aware is None else max((now - oldest_aware).total_seconds(), 0.0)
        ),
        "slots_per_runner": CONFIG.jobs.slots,
    }


def _runner(runner: JobRunner, now: datetime) -> dict[str, Any]:
    seen = _aware(runner.seen_at)
    return {
        "runner": runner.runner,
        "online": seen is not None and now - seen < _RUNNER_SILENCE,
        "slots": runner.slots,
        "running": runner.running,
        "started_at": _iso(runner.started_at),
        "seen_at": _iso(seen),
    }


async def recent_jobs(
    db: AsyncSession, *, state: str | None = None, limit: int = 50
) -> list[dict[str, Any]]:
    """Unfinished jobs first, then the most recent, newest first within each."""
    unfinished_first = Job.state.in_(UNFINISHED).desc()
    statement = select(Job).order_by(unfinished_first, Job.created_at.desc()).limit(limit)
    if state:
        statement = statement.where(Job.state == state)
    return [_job(job) for job in (await db.execute(statement)).scalars()]


def _job(job: Job) -> dict[str, Any]:
    return {
        "job_id": job.job_id,
        "kind": job.kind,
        "subject": job.subject,
        "state": job.state,
        "attempts": job.attempts,
        "runner": job.runner,
        "last_error": job.last_error,
        "created_at": _iso(job.created_at),
        "started_at": _iso(job.started_at),
        "finished_at": _iso(job.finished_at),
    }


async def cancel_job(db: AsyncSession, job_id: str) -> dict[str, Any]:
    """Cancel one unfinished job; its process sees the claim gone and stops within a beat."""
    job = await db.scalar(select(Job).where(Job.job_id == job_id).with_for_update())
    if job is None:
        return {"ok": False, "detail": "job_not_found"}
    if job.state in UNFINISHED:
        finish(job, JobState.CANCELLED, "Cancelled by admin from the ops panel.")
        await db.commit()
    return {"ok": True, "detail": job.state}
