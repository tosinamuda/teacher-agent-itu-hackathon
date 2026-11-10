from __future__ import annotations

import uuid

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.school.models import Class, GradeLevel, School, TermClassSubject

DEFAULT_SCHOOL_CODE = "DEFAULT"
DEFAULT_SCHOOL_NAME = "Plan-to-Tutor Default School"


async def ensure_default_school(
    *,
    session: AsyncSession,
) -> None:
    """Make sure the default school and its class exist, for a new or development database."""
    await _backfill_school_and_class_identity(session)


async def _backfill_school_and_class_identity(session: AsyncSession) -> None:
    school = (
        (await session.execute(select(School).where(School.code == DEFAULT_SCHOOL_CODE)))
        .scalars()
        .first()
    )
    if school is None:
        school = School(
            id=uuid.uuid4(),
            code=DEFAULT_SCHOOL_CODE,
            name=DEFAULT_SCHOOL_NAME,
        )
        session.add(school)
        await session.flush()

    await session.execute(
        text("UPDATE classes SET school_id = :school_id WHERE school_id IS NULL"),
        {"school_id": school.id},
    )

    grade_name_by_id = {
        grade_level.id: grade_level.name
        for grade_level in (await session.execute(select(GradeLevel))).scalars().all()
    }
    classes_by_grade: dict[uuid.UUID, Class] = {}
    for classroom in (
        (
            await session.execute(
                select(Class).where(Class.school_id == school.id).order_by(Class.name.asc())
            )
        )
        .scalars()
        .all()
    ):
        classes_by_grade.setdefault(classroom.grade_level_id, classroom)

    term_class_subjects = (
        (
            await session.execute(
                select(TermClassSubject)
                .options(selectinload(TermClassSubject.course))
                .where(TermClassSubject.class_id.is_(None))
            )
        )
        .scalars()
        .all()
    )
    for subject_offering in term_class_subjects:
        course = subject_offering.course
        if course is None:
            continue
        existing_class = classes_by_grade.get(course.grade_level_id)
        if existing_class is None:
            grade_name = grade_name_by_id.get(course.grade_level_id, "CLASS")
            existing_class = Class(
                id=uuid.uuid4(),
                name=grade_name,
                grade_level_id=course.grade_level_id,
                school_id=school.id,
            )
            session.add(existing_class)
            await session.flush()
            classes_by_grade[course.grade_level_id] = existing_class
        subject_offering.class_id = existing_class.id

    await session.commit()
