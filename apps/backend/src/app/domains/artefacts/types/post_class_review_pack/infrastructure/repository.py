"""SQL for the student-pack generation job (``StudentPackGeneration``).

All the lifecycle queries the dispatch + worker need: mint the next attempt, the
in-flight guard, the FOR UPDATE claim read, and the per-student latest-status read
that backs the teacher's generation queue.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.domain.types import (
    IN_FLIGHT_GENERATION_STATUSES,
    StudentPackGenerationStatus,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)


class StudentPackGenerationRepository:
    async def next_attempt_number(
        self, db: AsyncSession, *, student_id: str, plan_version_id: str
    ) -> int:
        """MAX(attempt)+1 for this (student, lesson) — concurrent dispatch may collide here.

        Two callers reading the same MAX mint the same attempt; the unique constraint
        then lets exactly one INSERT win (the caller converges the loser).
        """
        result = await db.execute(
            select(func.max(StudentPackGeneration.attempt_number)).where(
                StudentPackGeneration.student_id == student_id,
                StudentPackGeneration.plan_version_id == plan_version_id,
            )
        )
        return (result.scalar_one_or_none() or 0) + 1

    async def save(
        self, db: AsyncSession, generation: StudentPackGeneration
    ) -> StudentPackGeneration:
        db.add(generation)
        await db.commit()
        await db.refresh(generation)
        return generation

    async def get(self, db: AsyncSession, generation_id: str) -> StudentPackGeneration | None:
        result = await db.execute(
            select(StudentPackGeneration).where(
                StudentPackGeneration.generation_id == generation_id
            )
        )
        return result.scalars().first()

    async def get_for_update(
        self, db: AsyncSession, generation_id: str
    ) -> StudentPackGeneration | None:
        """Row-lock + return the job, to serialize the worker claim/finalize.

        FOR UPDATE (+ populate_existing so a cached row refreshes to the locked DB
        state) makes the claim and the terminal write the sole serialized writers of
        ``status`` — the same pattern as ``ExperimentRepository.get_execution_for_update``.
        """
        result = await db.execute(
            select(StudentPackGeneration)
            .where(StudentPackGeneration.generation_id == generation_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return result.scalars().first()

    async def in_flight_for(
        self, db: AsyncSession, *, student_id: str, plan_version_id: str
    ) -> StudentPackGeneration | None:
        """The QUEUED/RUNNING job for this (student, lesson), if any (the dispatch guard)."""
        result = await db.execute(
            select(StudentPackGeneration)
            .where(
                StudentPackGeneration.student_id == student_id,
                StudentPackGeneration.plan_version_id == plan_version_id,
                StudentPackGeneration.status.in_(IN_FLIGHT_GENERATION_STATUSES),
            )
            .order_by(StudentPackGeneration.created_at.desc())
        )
        return result.scalars().first()

    async def latest_per_student(
        self, db: AsyncSession, *, plan_version_id: str
    ) -> list[StudentPackGeneration]:
        """The most recent generation attempt per student for this lesson.

        Backs the teacher's generation queue (generating / failed / ready). Returns
        only the newest attempt per student so an old FAILED row doesn't mask a fresh
        QUEUED retry — "current attempt", mirroring the keep-versions pack read.
        """
        rows = (
            (
                await db.execute(
                    select(StudentPackGeneration)
                    .where(StudentPackGeneration.plan_version_id == plan_version_id)
                    .order_by(
                        StudentPackGeneration.student_id,
                        StudentPackGeneration.created_at.desc(),
                        StudentPackGeneration.attempt_number.desc(),
                    )
                )
            )
            .scalars()
            .all()
        )
        latest: dict[str, StudentPackGeneration] = {}
        for row in rows:
            latest.setdefault(row.student_id, row)
        return list(latest.values())

    @staticmethod
    def is_terminal(status: StudentPackGenerationStatus) -> bool:
        return status in (
            StudentPackGenerationStatus.SUCCEEDED,
            StudentPackGenerationStatus.FAILED,
        )
