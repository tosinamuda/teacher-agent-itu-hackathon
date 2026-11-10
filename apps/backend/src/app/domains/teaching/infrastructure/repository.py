from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domains.school.models.core import Subject
from app.domains.school.models.structure import Class, Course
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.domain import (
    CANONICAL_GRADE_NAME,
    CANONICAL_SCHOOL_CODE,
    CANONICAL_SUBJECT_CODE,
)
from app.domains.teaching.models import TeacherWorkspace


class TeachingRepository:
    async def list_workspaces_for_teacher(
        self,
        db: AsyncSession,
        teacher_id: uuid.UUID,
        *,
        canonical_only: bool = True,
    ) -> Sequence[TeacherWorkspace]:
        stmt = (
            select(TeacherWorkspace)
            .join(TeacherWorkspace.term_class_subject)
            .join(TermClassSubject.classroom)
            .join(Class.school)
            .join(TermClassSubject.course)
            .join(Course.subject)
            .where(TeacherWorkspace.teacher_id == teacher_id)
            .options(
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.subject),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.grade_level),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.classroom)
                .joinedload(Class.school),
            )
        )
        if canonical_only:
            stmt = stmt.where(
                Class.name == CANONICAL_GRADE_NAME,
                Subject.code == CANONICAL_SUBJECT_CODE,
                Class.school.has(code=CANONICAL_SCHOOL_CODE),
            )
        stmt = stmt.order_by(TeacherWorkspace.created_at.desc())
        result = await db.execute(stmt)
        return result.scalars().unique().all()
