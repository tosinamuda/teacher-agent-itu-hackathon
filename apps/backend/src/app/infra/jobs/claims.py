"""What a runner does to the jobs table: claim a job, give back one that was cut short.

A claim is ``FOR UPDATE SKIP LOCKED`` and commits at once, so two runners never take the
same job and no lock is held while a job runs. A RUNNING job whose lease has passed is
claimable again: its process died without finishing it.
"""

from __future__ import annotations

import os
import socket
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.retry import run_with_deadlock_retry
from app.infra.jobs.kinds import KINDS
from app.infra.jobs.models import Job, JobRunner, JobState
from app.shared.json_types import JsonValue
from app.shared.time import utc_now

#: A runner not seen for this long is gone; its row is only history.
_FORGET_RUNNERS_AFTER = timedelta(days=1)


@dataclass(frozen=True)
class ClaimedJob:
    """One run of one job, as the process running it is handed it."""

    id: uuid.UUID
    job_id: str
    kind: str
    args: list[JsonValue]
    attempt: int

    @property
    def rerun(self) -> bool:
        """Whether an earlier run of this job was cut short."""
        return self.attempt > 1


def this_runner() -> str:
    """How the runner in this process is known: host and process id."""
    return f"{socket.gethostname()}:{os.getpid()}"


def finish(job: Job, state: JobState, error: str | None) -> None:
    """End a job: it no longer holds its subject, a lease or a runner."""
    job.state = state
    job.last_error = error
    job.active_subject = None
    job.lease_expires_at = None
    job.finished_at = utc_now()


class JobClaims:
    """The runner's reads and writes, each in a session of its own."""

    def __init__(
        self, sessions: Callable[[], AsyncSession], *, runner: str, lease_seconds: int
    ) -> None:
        self._sessions = sessions
        self._runner = runner
        self._lease = timedelta(seconds=lease_seconds)

    async def claim(self) -> ClaimedJob | None:
        """The oldest job ready to run, now held by this runner; None when there is none."""
        async with self._sessions() as session:
            return await run_with_deadlock_retry(session, lambda: self._claim_in(session))

    async def _claim_in(self, session: AsyncSession) -> ClaimedJob | None:
        # READ COMMITTED takes no gap locks, so moving a claimed row out of the queued range
        # of the index cannot deadlock against another runner's claim beside it.
        await session.connection(execution_options={"isolation_level": "READ COMMITTED"})
        while (job := await self._next(session)) is not None:
            kind = KINDS.get(job.kind)
            if kind is None:
                finish(job, JobState.FAILED, f"no job kind {job.kind!r}")
            elif job.attempts >= kind.runs:
                finish(job, JobState.FAILED, _gave_up(job))
            else:
                claimed = self._hold(job)
                await session.commit()
                return claimed
            await session.commit()
        return None

    async def give_back(self, claimed: ClaimedJob, reason: str) -> None:
        """Return a run that ended without recording an outcome, to run again or to fail.

        Only while this run still holds it: a job its process finished, or that was
        cancelled or claimed again since, is left as it is.
        """
        async with self._sessions() as session:
            job = await session.get(Job, claimed.id, with_for_update=True)
            if job is None or job.state != JobState.RUNNING or job.attempts != claimed.attempt:
                return
            job.last_error = reason
            if job.attempts >= KINDS[job.kind].runs:
                finish(job, JobState.FAILED, f"{reason}; {_gave_up(job)}")
            else:
                job.state = JobState.QUEUED
                job.runner = None
                job.lease_expires_at = None
            await session.commit()

    async def seen(self, *, slots: int, running: int) -> None:
        """Record that this runner is alive, and forget runners long gone."""
        now = utc_now()
        async with self._sessions() as session:
            statement = insert(JobRunner).values(
                runner=self._runner, slots=slots, running=running, started_at=now, seen_at=now
            )
            await session.execute(
                statement.on_duplicate_key_update(running=running, slots=slots, seen_at=now)
            )
            await session.execute(
                delete(JobRunner).where(JobRunner.seen_at < now - _FORGET_RUNNERS_AFTER)
            )
            await session.commit()

    async def _next(self, session: AsyncSession) -> Job | None:
        """A job whose run died first, then the oldest queued one.

        Two queries rather than one ``OR``: each walks its own index and locks only the row
        it returns, which is what lets runners claim side by side.
        """
        lapsed = (
            select(Job)
            .where(Job.state == JobState.RUNNING, Job.lease_expires_at < utc_now())
            .order_by(Job.lease_expires_at)
        )
        queued = select(Job).where(Job.state == JobState.QUEUED).order_by(Job.created_at)
        for statement in (lapsed, queued):
            job = (
                await session.execute(statement.limit(1).with_for_update(skip_locked=True))
            ).scalar_one_or_none()
            if job is not None:
                return job
        return None

    def _hold(self, job: Job) -> ClaimedJob:
        now = utc_now()
        if job.state == JobState.RUNNING:
            job.last_error = f"run {job.attempts} stopped renewing its claim"
        job.state = JobState.RUNNING
        job.attempts += 1
        job.runner = self._runner
        job.lease_expires_at = now + self._lease
        job.started_at = now
        return ClaimedJob(
            id=job.id, job_id=job.job_id, kind=job.kind, args=list(job.args), attempt=job.attempts
        )


def _gave_up(job: Job) -> str:
    return f"stopped after {job.attempts} interrupted run(s)"
