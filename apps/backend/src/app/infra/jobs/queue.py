"""Queue background work in the caller's own transaction."""

from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.jobs.kinds import KINDS
from app.infra.jobs.models import UNFINISHED, Job, JobState
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonValue
from app.shared.time import utc_now


class JobAlreadyQueuedError(Exception):
    """A job of this kind is already unfinished for this subject."""

    def __init__(self, kind: str, subject: str | None) -> None:
        super().__init__(f"a {kind} job is already unfinished for {subject}")
        self.kind = kind
        self.subject = subject


class JobQueue:
    """Jobs, added to one session: queued when that session commits, never before."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(
        self,
        kind: str,
        *args: JsonValue,
        subject: str | None = None,
        requested_by: str | None = None,
    ) -> str:
        """Stage a job with the rest of the transaction; returns its id.

        A second unfinished job of the same kind for the same subject fails that commit.
        """
        if kind not in KINDS:
            raise ValueError(f"no job kind {kind!r}")
        job_id = new_public_id(PublicIdPrefix.JOB)
        self._session.add(
            Job(
                job_id=job_id,
                kind=kind,
                args=list(args),
                subject=subject,
                active_subject=subject,
                state=JobState.QUEUED,
                attempts=0,
                requested_by=requested_by,
                created_at=utc_now(),
            )
        )
        return job_id

    async def submit(
        self,
        kind: str,
        *args: JsonValue,
        subject: str | None = None,
        requested_by: str | None = None,
    ) -> str:
        """Queue a job that is the whole of its transaction."""
        job_id = self.add(kind, *args, subject=subject, requested_by=requested_by)
        try:
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            raise JobAlreadyQueuedError(kind, subject) from error
        return job_id

    async def ensure(
        self, kind: str, *args: JsonValue, subject: str, requested_by: str | None = None
    ) -> str:
        """The unfinished job of this kind for ``subject``, queuing it if there is none.

        Asking again while the work is under way follows the job already doing it, so a
        second click or a reloaded page never starts the same generation twice.
        """
        running = await self.unfinished(kind, subject)
        if running is not None:
            return running
        try:
            return await self.submit(kind, *args, subject=subject, requested_by=requested_by)
        except JobAlreadyQueuedError:
            # Another request queued it between the look and the insert: follow that one.
            winner = await self.unfinished(kind, subject)
            if winner is None:
                raise
            return winner

    async def unfinished(self, kind: str, subject: str) -> str | None:
        """The id of the unfinished job of this kind for ``subject``, if there is one."""
        job_id: str | None = await self._session.scalar(
            select(Job.job_id).where(Job.kind == kind, Job.active_subject == subject)
        )
        return job_id

    async def cancel(self, subject: str) -> list[str]:
        """End every unfinished job acting on ``subject``; a running one stops within a beat.

        The job's own process sees its claim gone when it next renews it, and exits.
        """
        unfinished = (
            select(Job.job_id)
            .where(Job.subject == subject, Job.state.in_(UNFINISHED))
            .with_for_update()
        )
        job_ids = list((await self._session.execute(unfinished)).scalars())
        if job_ids:
            await self._session.execute(
                update(Job)
                .where(Job.job_id.in_(job_ids))
                .values(
                    state=JobState.CANCELLED,
                    active_subject=None,
                    lease_expires_at=None,
                    finished_at=utc_now(),
                )
            )
        return job_ids
