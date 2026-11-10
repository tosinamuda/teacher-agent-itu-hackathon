"""What waits for the teacher's review in each lesson of a class."""

from __future__ import annotations

import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace

PLAN = "plan"


@dataclass(frozen=True)
class Waiting:
    """One thing in a lesson that waits for the teacher."""

    lesson: uuid.UUID
    kind: str
    """`plan`, or the type of the material."""
    for_a_learner: bool
    since: datetime


@dataclass(frozen=True)
class LessonReviewCounts:
    plans_to_approve: int
    materials_to_review: int
    notes_to_review: int
    oldest_kind: str
    oldest_since: datetime


def _counts(items: list[Waiting]) -> LessonReviewCounts:
    """`items` is oldest first."""
    return LessonReviewCounts(
        plans_to_approve=sum(item.kind == PLAN for item in items),
        materials_to_review=sum(item.kind != PLAN and not item.for_a_learner for item in items),
        notes_to_review=sum(item.for_a_learner for item in items),
        oldest_kind=items[0].kind,
        oldest_since=items[0].since,
    )


@dataclass(frozen=True)
class LearnerNotes:
    to_review: int = 0
    approved: int = 0


class ReviewQueueRepository:
    async def notes_by_learner(
        self, db: AsyncSession, workspace_id: uuid.UUID
    ) -> dict[str, LearnerNotes]:
        """Each learner's personalised notes for the workspace's subject, by how far they are."""
        rows = (
            await db.execute(
                self._versions_of_subject(workspace_id)
                .with_only_columns(
                    Artefact.student_id, Artefact.review_status, func.count(Artefact.id)
                )
                .join(Artefact, Artefact.plan_version_id == PlanVersion.version_id)
                .where(
                    Artefact.scope == ArtefactScope.LEARNER_LEVEL.value,
                    Artefact.student_id.is_not(None),
                    Artefact.review_status != ArtefactReviewStatus.REJECTED,
                )
                .group_by(Artefact.student_id, Artefact.review_status)
            )
        ).all()
        pending = {
            student: n for student, status, n in rows if status == ArtefactReviewStatus.PENDING
        }
        approved = {
            student: n for student, status, n in rows if status == ArtefactReviewStatus.APPROVED
        }
        return {
            student: LearnerNotes(pending.get(student, 0), approved.get(student, 0))
            for student in pending.keys() | approved.keys()
        }

    async def counts_by_lesson(
        self, db: AsyncSession, workspace_id: uuid.UUID
    ) -> dict[uuid.UUID, LessonReviewCounts]:
        """The lessons of the workspace's subject that have something to review, with what."""
        waiting = [
            *await self._draft_plans(db, workspace_id),
            *await self._pending(db, workspace_id),
        ]
        waiting.sort(key=lambda item: item.since)
        by_lesson: dict[uuid.UUID, list[Waiting]] = defaultdict(list)
        for item in waiting:
            by_lesson[item.lesson].append(item)
        return {lesson: _counts(items) for lesson, items in by_lesson.items()}

    async def _draft_plans(self, db: AsyncSession, workspace_id: uuid.UUID) -> list[Waiting]:
        rows = (
            await db.execute(
                self._versions_of_subject(workspace_id)
                .with_only_columns(LessonPeriod.id, PlanVersion.created_at)
                .where(PlanVersion.status == PlanVersionStatus.DRAFT)
            )
        ).all()
        return [Waiting(lesson, PLAN, False, since) for lesson, since in rows]

    async def _pending(self, db: AsyncSession, workspace_id: uuid.UUID) -> list[Waiting]:
        rows = (
            await db.execute(
                self._versions_of_subject(workspace_id)
                .with_only_columns(
                    LessonPeriod.id, Artefact.artefact_type, Artefact.scope, Artefact.created_at
                )
                .join(Artefact, Artefact.plan_version_id == PlanVersion.version_id)
                .where(Artefact.review_status == ArtefactReviewStatus.PENDING)
            )
        ).all()
        return [
            Waiting(lesson, kind, scope == ArtefactScope.LEARNER_LEVEL.value, since)
            for lesson, kind, scope, since in rows
        ]

    @staticmethod
    def _versions_of_subject(workspace_id: uuid.UUID) -> Select[tuple[PlanVersion]]:
        """Every plan version of the workspace's subject, joined to its lesson."""
        return (
            select(PlanVersion)
            .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
            .join(LessonPeriod, LessonPeriod.id == LessonPlan.lesson_period_id)
            .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
            .join(
                TeacherWorkspace,
                TeacherWorkspace.term_class_subject_id == SchemeOfWork.term_class_subject_id,
            )
            .where(TeacherWorkspace.id == workspace_id)
        )
