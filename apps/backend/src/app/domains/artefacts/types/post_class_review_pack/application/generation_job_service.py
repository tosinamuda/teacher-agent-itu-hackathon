"""Lifecycle of the async student-pack generation job.

Owns the three transitions a generation goes through, each the student-pack analogue
of the experiment-execution lifecycle (``execution_service`` + ``experiments.tasks``):

* ``enqueue`` — create the QUEUED generation (one per (student, lesson, attempt)) and the
  job that runs it, in one commit, skipping if a generation is already in flight.
* ``claim`` — the job locks the generation and flips it RUNNING (taking over a stale
  RUNNING left by a run that was cut short), or skips a terminal one.
* ``finalize`` — the job writes the terminal status (+ produced pack id / error)
  under the lock, only if this run still owns it.
"""

from __future__ import annotations

import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.domain.types import (
    StudentPackGenerationStatus,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.repository import (
    StudentPackGenerationRepository,
)
from app.infra.jobs.kinds import GENERATE_STUDENT_PACK
from app.infra.jobs.queue import JobQueue
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.time import utc_now
from app.shared.worker_delivery import MAX_TASK_DELIVERIES

logger = logging.getLogger(__name__)


class StudentPackGenerationJobService:
    """Create/claim/finalize student-pack generation jobs."""

    def __init__(self, repository: StudentPackGenerationRepository) -> None:
        self.repository = repository

    async def enqueue(
        self, db: AsyncSession, *, student_id: str, plan_version_id: str
    ) -> StudentPackGeneration | None:
        """Queue a generation for this (student, lesson) with the job that runs it.

        Returns the new job, or ``None`` if one is already in flight (we don't
        double-generate). Completed/failed attempts do NOT block — under keep-versions
        a fresh attempt either produces a new pack version or retries a failure.
        """
        if (
            await self.repository.in_flight_for(
                db, student_id=student_id, plan_version_id=plan_version_id
            )
            is not None
        ):
            return None
        attempt = await self.repository.next_attempt_number(
            db, student_id=student_id, plan_version_id=plan_version_id
        )
        job = StudentPackGeneration(
            generation_id=new_public_id(PublicIdPrefix.STUDENT_PACK_GENERATION),
            student_id=student_id,
            plan_version_id=plan_version_id,
            attempt_number=attempt,
            status=StudentPackGenerationStatus.QUEUED,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        db.add(job)
        JobQueue(db).add(GENERATE_STUDENT_PACK, job.generation_id, subject=job.generation_id)
        try:
            await db.commit()
        except IntegrityError:
            # A concurrent dispatch won this (student, lesson, attempt) — converge: the
            # winner is queued/running, so there is nothing more to do here.
            await db.rollback()
            return None
        await db.refresh(job)
        return job

    async def latest_statuses(
        self, db: AsyncSession, *, plan_version_id: str
    ) -> list[StudentPackGeneration]:
        """The current generation attempt per student for this lesson (teacher queue)."""
        return await self.repository.latest_per_student(db, plan_version_id=plan_version_id)

    async def claim(self, db: AsyncSession, generation_id: str) -> StudentPackGeneration | None:
        """Lock + claim the job for this worker run; ``None`` if it should be skipped.

        Returns the job (flipped RUNNING, committed) when this run should proceed; ``None``
        when a terminal status means it is done. A stale RUNNING (a crashed predecessor
        left by a run that was cut short) is taken over. The RUNNING claim is what lets the
        terminal write below detect a rival that took over.
        """
        job = await self.repository.get_for_update(db, generation_id)
        if job is None:
            logger.warning("student-pack generation not found: %s", generation_id)
            return None
        if self.repository.is_terminal(job.status):
            logger.info("generation %s already %s; skipping run", generation_id, job.status)
            return None
        job.delivery_count = (job.delivery_count or 0) + 1
        if job.delivery_count > MAX_TASK_DELIVERIES:
            # A generation whose runs keep being cut short: stop running it.
            job.status = StudentPackGenerationStatus.FAILED
            job.error_message = f"exceeded {MAX_TASK_DELIVERIES} deliveries (poison message)"
            job.error_category = "poison"
            job.updated_at = utc_now()
            await db.commit()
            logger.error(
                "generation %s poison-bounded after %s deliveries; marked FAILED",
                generation_id,
                job.delivery_count,
            )
            return None
        job.status = StudentPackGenerationStatus.RUNNING
        job.updated_at = utc_now()
        await db.commit()
        return job

    async def finalize(
        self,
        db: AsyncSession,
        generation_id: str,
        *,
        status: StudentPackGenerationStatus,
        produced_artefact_id: str | None = None,
        error: str | None = None,
        error_category: str | None = None,
    ) -> None:
        """Write the terminal status under the lock — only if this run still owns it."""
        job = await self.repository.get_for_update(db, generation_id)
        if job is None or job.status != StudentPackGenerationStatus.RUNNING:
            await db.rollback()
            logger.info(
                "generation %s no longer RUNNING; discarded this run's result", generation_id
            )
            return
        job.status = status
        job.produced_artefact_id = produced_artefact_id
        job.error_message = error
        job.error_category = error_category
        job.updated_at = utc_now()
        await db.commit()
