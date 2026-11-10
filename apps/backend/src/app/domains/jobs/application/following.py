"""Who may follow a job, and what they see of it.

A job is followed by whoever asked for it; the operations roles may follow any.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.jobs.models import Job, JobState
from app.shared.auth import ROLE_ADMIN, ROLE_RESEARCH_MANAGER, Actor
from app.shared.json_types import JsonObject
from app.shared.time import as_utc

_OPERATORS = frozenset({ROLE_ADMIN, ROLE_RESEARCH_MANAGER})


@dataclass(frozen=True)
class FollowedJob:
    """A job as the caller following it sees it."""

    job_id: str
    kind: str
    subject: str | None
    state: str
    attempts: int
    error: str | None
    result: JsonObject | None
    created_at: datetime | None
    finished_at: datetime | None


def may_follow(actor: Actor, job: Job) -> bool:
    return actor.role in _OPERATORS or (
        job.requested_by is not None and job.requested_by == actor.auth_id
    )


async def followed(db: AsyncSession, actor: Actor, job_id: str) -> FollowedJob | None:
    """The job, if it exists and the caller may follow it."""
    job = await db.scalar(select(Job).where(Job.job_id == job_id))
    return _seen(job) if job is not None and may_follow(actor, job) else None


async def latest(db: AsyncSession, actor: Actor, *, kind: str, subject: str) -> FollowedJob | None:
    """The newest job of this kind for ``subject`` that the caller may follow.

    How a reloaded page picks up the generation it started before the reload.
    """
    statement = (
        select(Job).where(Job.kind == kind, Job.subject == subject).order_by(Job.created_at.desc())
    )
    if actor.role not in _OPERATORS:
        statement = statement.where(Job.requested_by == actor.auth_id)
    job = await db.scalar(statement.limit(1))
    return _seen(job) if job is not None else None


def _seen(job: Job) -> FollowedJob:
    return FollowedJob(
        job_id=job.job_id,
        kind=job.kind,
        subject=job.subject,
        state=job.state,
        attempts=job.attempts,
        error=job.last_error if job.state in (JobState.FAILED, JobState.CANCELLED) else None,
        result=job.result,
        created_at=_utc(job.created_at),
        finished_at=_utc(job.finished_at),
    )


def _utc(moment: datetime | None) -> datetime | None:
    return None if moment is None else as_utc(moment)
