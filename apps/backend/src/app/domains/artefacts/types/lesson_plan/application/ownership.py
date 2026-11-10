"""Does a teacher own a given lesson plan?

A teacher owns a plan when they have a workspace on the plan's exact
class + subject + term — i.e. the workspace's ``term_class_subject`` matches the
plan's lesson's scheme-of-work. Used to gate plan approval so a teacher can only
freeze *their own* lesson (a research-manager bypasses the check).

This is a read-only ownership query that spans the lesson-plan + teaching models;
it deliberately joins across them rather than threading several cross-domain
service calls for one boolean.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.teaching.models.syllabus import LessonPeriod, SchemeOfWork
from app.domains.teaching.models.workspace import TeacherWorkspace


async def teacher_owns_plan_version(
    db: AsyncSession,
    *,
    teacher_id: uuid.UUID,
    plan_version_id: str,
) -> bool:
    """True if the teacher has a workspace on the plan's class + subject + term.

    plan version → plan → lesson period → scheme of work → term-class-subject,
    matched against the teacher's workspaces' term-class-subject.
    """
    stmt = (
        select(TeacherWorkspace.id)
        .join(
            SchemeOfWork,
            SchemeOfWork.term_class_subject_id == TeacherWorkspace.term_class_subject_id,
        )
        .join(LessonPeriod, LessonPeriod.scheme_of_work_id == SchemeOfWork.id)
        .join(LessonPlan, LessonPlan.lesson_period_id == LessonPeriod.id)
        .join(PlanVersion, PlanVersion.plan_id == LessonPlan.plan_id)
        .where(
            PlanVersion.version_id == plan_version_id,
            TeacherWorkspace.teacher_id == teacher_id,
        )
        .limit(1)
    )
    return (await db.execute(stmt)).scalars().first() is not None


async def teacher_owns_lesson_period(
    db: AsyncSession,
    *,
    teacher_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
) -> bool:
    """True if the teacher has a workspace on the lesson's class + subject + term.

    The plan-less counterpart of :func:`teacher_owns_plan_version` — used to gate
    authoring an experiment's plan before any plan_version exists yet.
    """
    stmt = (
        select(TeacherWorkspace.id)
        .join(
            SchemeOfWork,
            SchemeOfWork.term_class_subject_id == TeacherWorkspace.term_class_subject_id,
        )
        .join(LessonPeriod, LessonPeriod.scheme_of_work_id == SchemeOfWork.id)
        .where(
            LessonPeriod.id == lesson_period_id,
            TeacherWorkspace.teacher_id == teacher_id,
        )
        .limit(1)
    )
    return (await db.execute(stmt)).scalars().first() is not None


async def teacher_owned_plan_version_ids(
    db: AsyncSession,
    *,
    teacher_id: uuid.UUID,
) -> list[str]:
    """Every plan-version id whose class + subject + term the teacher owns.

    The listing counterpart of :func:`teacher_owns_plan_version` — used to scope a
    teacher's pack-review queue to their own classes (so the filter applies inside
    the query, before any limit, rather than after fetching).
    """
    stmt = (
        select(PlanVersion.version_id)
        .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
        .join(LessonPeriod, LessonPeriod.id == LessonPlan.lesson_period_id)
        .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
        .join(
            TeacherWorkspace,
            TeacherWorkspace.term_class_subject_id == SchemeOfWork.term_class_subject_id,
        )
        .where(TeacherWorkspace.teacher_id == teacher_id)
    )
    return list((await db.execute(stmt)).scalars().all())
