"""The study's school: its teacher, its JSS1 class, and one lesson period per studied lesson.

The school is not named in the release, and it is not named here. The study's teacher has no
access code, so no one can sign in as her: the study is read, not taught, in the app. The
JSS1 Mathematics course is the curriculum's own, seeded before any import.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.school.models.core import GradeLevel
from app.domains.school.models.structure import Class, Course, School
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace
from app.domains.users.models import User
from experiments.study_import.dataset import StudyLesson

GRADE, COURSE = "JSS1", "JSS1 Mathematics"
#: The school year the lessons were taught in (the lesson-plans dataset card).
SCHOOL_YEAR = "2025/2026"
TEACHER_NAME = "The study teacher"
Row = TypeVar("Row")


class CurriculumNotSeededError(RuntimeError):
    """The JSS1 Mathematics course the study was taught from is not in the database."""


@dataclass(frozen=True)
class LessonPlace:
    """Where one studied lesson sits: its period, and the teacher's workspace for its term."""

    lesson_period_id: uuid.UUID
    workspace_id: uuid.UUID


async def _one(db: AsyncSession, query: Select[tuple[Row]]) -> Row | None:
    return (await db.execute(query)).scalar_one_or_none()


async def _course_and_grade(db: AsyncSession) -> tuple[Course, GradeLevel]:
    grade = await _one(db, select(GradeLevel).where(GradeLevel.name == GRADE))
    course = await _one(db, select(Course).where(Course.name == COURSE))
    if grade is None or course is None:
        raise CurriculumNotSeededError(f"seed the {COURSE} curriculum before importing the study")
    return course, grade


async def _teacher(db: AsyncSession) -> User:
    teacher = await _one(db, select(User).where(User.auth_id == "study|teacher"))
    if teacher is None:
        teacher = User(
            auth_id="study|teacher",
            email="study-teacher@study.invalid",
            full_name=TEACHER_NAME,
            role="teacher",
        )
        db.add(teacher)
    return teacher


async def study_class(db: AsyncSession) -> Class:
    """The study's JSS1 class, in a school the app names only as the study's."""
    _, grade = await _course_and_grade(db)
    school = await _one(db, select(School).where(School.code == "STUDY"))
    if school is None:
        school = School(name="The study school", code="STUDY", default_academic_year=SCHOOL_YEAR)
        db.add(school)
        await db.flush()
    klass = await _one(db, select(Class).where(Class.school_id == school.id))
    if klass is None:
        klass = Class(name=f"{GRADE} (study)", school_id=school.id, grade_level_id=grade.id)
        db.add(klass)
        await db.flush()
    return klass


async def _workspace(
    db: AsyncSession, teacher: User, course: Course, klass: Class, term: str
) -> TeacherWorkspace:
    """The study teacher's workspace for the class's Mathematics in one term."""
    offering = await _one(
        db,
        select(TermClassSubject).where(
            TermClassSubject.class_id == klass.id,
            TermClassSubject.course_id == course.id,
            TermClassSubject.term == term,
        ),
    )
    if offering is None:
        offering = TermClassSubject(
            course_id=course.id, class_id=klass.id, term=term, year=SCHOOL_YEAR
        )
        db.add(offering)
        await db.flush()
    workspace = await _one(
        db, select(TeacherWorkspace).where(TeacherWorkspace.term_class_subject_id == offering.id)
    )
    if workspace is None:
        workspace = TeacherWorkspace(
            teacher_id=teacher.id, term_class_subject_id=offering.id, is_primary=True
        )
        db.add(workspace)
        await db.flush()
    return workspace


async def place_lessons(db: AsyncSession, lessons: list[StudyLesson]) -> dict[str, LessonPlace]:
    """A term offering, a scheme-of-work week and a period for each lesson, and the workspaces."""
    course, _ = await _course_and_grade(db)
    klass = await study_class(db)
    teacher = await _teacher(db)
    await db.flush()
    places: dict[str, LessonPlace] = {}
    workspaces: dict[str, TeacherWorkspace] = {}
    for lesson in lessons:
        if lesson.term not in workspaces:
            workspaces[lesson.term] = await _workspace(db, teacher, course, klass, lesson.term)
        workspace = workspaces[lesson.term]
        week = SchemeOfWork(
            term_class_subject_id=workspace.term_class_subject_id,
            week_number=lesson.week,
            title=str(lesson.plan.get("topic") or lesson.lesson),
        )
        db.add(week)
        await db.flush()
        period = LessonPeriod(
            scheme_of_work_id=week.id, period_number=1, title=lesson.plan.get("subtopic")
        )
        db.add(period)
        await db.flush()
        places[lesson.lesson] = LessonPlace(lesson_period_id=period.id, workspace_id=workspace.id)
    return places
