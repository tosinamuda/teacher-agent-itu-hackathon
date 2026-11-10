"""Persistence layer for the school domain — own every SQL query the services need.

Until now ``school/application/service.py`` issued raw ``select()``/``db.execute()``
inline (39 sites) — a baseline-rule breach (``application/`` orchestrates,
``infrastructure/`` persists). This repository centralises every query the school
+ workspace-provisioning services need and follows the repo-commits-per-save
convention used by ``experiments``/``evaluation``.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.school.models.core import AcademicYear, GradeLevel, Subject
from app.domains.school.models.structure import Class, Course, School
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models import TeacherWorkspace
from app.domains.users.models import User

# ----- Composite-row aliases (the join shapes returned by the join queries below) -----

ClassWithSchoolRow = tuple[Class, str, uuid.UUID, str, str]
"""(Class, grade_name, school_id, school_name, school_code)"""

SchoolWithCountsRow = tuple[School, int, int]
"""(School, class_count, workspace_count)"""

WorkspaceWithRelationsRow = tuple[
    TeacherWorkspace, School, Class, GradeLevel, Subject, TermClassSubject, User
]


class SchoolRepository:
    """SQLAlchemy implementation of the school domain's persistence surface."""

    # ===== Class reads =====

    async def list_classes_with_school(
        self,
        db: AsyncSession,
        *,
        grade: str | None,
        school_id: uuid.UUID | None,
    ) -> list[ClassWithSchoolRow]:
        """List classes joined with their grade + school for the dashboard."""
        stmt = (
            select(
                Class,
                GradeLevel.name.label("grade_name"),
                School.id.label("school_id"),
                School.name.label("school_name"),
                School.code.label("school_code"),
            )
            .join(GradeLevel, Class.grade_level_id == GradeLevel.id)
            .join(School, Class.school_id == School.id)
            .order_by(School.name.asc(), GradeLevel.sequence.asc(), Class.name.asc())
        )
        if grade:
            stmt = stmt.where(GradeLevel.name == grade)
        if school_id is not None:
            stmt = stmt.where(School.id == school_id)
        result = await db.execute(stmt)
        return [tuple(row) for row in result.all()]

    # ===== School CRUD =====

    async def list_schools_with_counts(self, db: AsyncSession) -> list[SchoolWithCountsRow]:
        """List schools with derived class + workspace counts."""
        class_count = func.count(func.distinct(Class.id))
        workspace_count = func.count(func.distinct(TeacherWorkspace.id))
        stmt = (
            select(
                School,
                class_count.label("class_count"),
                workspace_count.label("workspace_count"),
            )
            .outerjoin(Class, Class.school_id == School.id)
            .outerjoin(TermClassSubject, TermClassSubject.class_id == Class.id)
            .outerjoin(
                TeacherWorkspace,
                TeacherWorkspace.term_class_subject_id == TermClassSubject.id,
            )
            .group_by(School.id)
            .order_by(School.created_at.desc(), School.name.asc())
        )
        result = await db.execute(stmt)
        return [tuple(row) for row in result.all()]

    async def find_school_conflict(
        self,
        db: AsyncSession,
        *,
        school_code: str,
        name: str,
        exclude_id: uuid.UUID | None = None,
    ) -> School | None:
        """Find an existing school with the same code or name (optionally excluding one)."""
        stmt = select(School).where((School.code == school_code) | (School.name == name))
        if exclude_id is not None:
            stmt = stmt.where(School.id != exclude_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_school(self, db: AsyncSession, school_id: uuid.UUID) -> School | None:
        """Fetch a school by primary key (``None`` if absent)."""
        return await db.get(School, school_id)

    async def save_school(self, db: AsyncSession, school: School) -> School:
        """Persist a school (insert or update) and refresh from the DB."""
        db.add(school)
        await db.commit()
        await db.refresh(school)
        return school

    async def school_counts(
        self,
        db: AsyncSession,
        *,
        school_id: uuid.UUID,
    ) -> tuple[int, int]:
        """Return ``(class_count, workspace_count)`` for one school."""
        class_stmt = select(func.count(func.distinct(Class.id))).where(Class.school_id == school_id)
        workspace_stmt = (
            select(func.count(func.distinct(TeacherWorkspace.id)))
            .select_from(TeacherWorkspace)
            .join(TermClassSubject, TeacherWorkspace.term_class_subject_id == TermClassSubject.id)
            .join(Class, TermClassSubject.class_id == Class.id)
            .where(Class.school_id == school_id)
        )
        class_total = (await db.execute(class_stmt)).scalar_one()
        workspace_total = (await db.execute(workspace_stmt)).scalar_one()
        return int(class_total), int(workspace_total)

    # ===== Setup-catalog reads =====

    async def list_grade_levels(self, db: AsyncSession) -> Sequence[GradeLevel]:
        """List grade levels in sequence order."""
        result = await db.execute(select(GradeLevel).order_by(GradeLevel.sequence.asc()))
        return list(result.scalars().all())

    async def list_subjects(self, db: AsyncSession) -> Sequence[Subject]:
        """List subjects in name order."""
        result = await db.execute(select(Subject).order_by(Subject.name.asc()))
        return list(result.scalars().all())

    async def list_academic_year_names(self, db: AsyncSession) -> list[str]:
        """Return academic year names, most recent first."""
        result = await db.execute(select(AcademicYear).order_by(AcademicYear.start_date.desc()))
        return [year.name for year in result.scalars().all()]

    # ===== Workspace reads =====

    async def list_workspaces_with_relations(
        self,
        db: AsyncSession,
        *,
        school_id: uuid.UUID | None,
    ) -> list[WorkspaceWithRelationsRow]:
        """Workspaces joined with their full school -> class -> course -> teacher chain."""
        stmt = (
            select(
                TeacherWorkspace,
                School,
                Class,
                GradeLevel,
                Subject,
                TermClassSubject,
                User,
            )
            .join(TermClassSubject, TeacherWorkspace.term_class_subject_id == TermClassSubject.id)
            .join(Class, TermClassSubject.class_id == Class.id)
            .join(School, Class.school_id == School.id)
            .join(Course, TermClassSubject.course_id == Course.id)
            .join(GradeLevel, Course.grade_level_id == GradeLevel.id)
            .join(Subject, Course.subject_id == Subject.id)
            .join(User, TeacherWorkspace.teacher_id == User.id)
            .order_by(
                School.name.asc(),
                GradeLevel.sequence.asc(),
                Subject.name.asc(),
                TermClassSubject.term.asc(),
                User.full_name.asc(),
            )
        )
        if school_id is not None:
            stmt = stmt.where(School.id == school_id)
        result = await db.execute(stmt)
        return [tuple(row) for row in result.all()]

    # ===== Provisioning-cascade lookups =====

    async def get_teacher(self, db: AsyncSession, teacher_id: uuid.UUID) -> User | None:
        """Fetch a teacher user by primary key (``None`` if absent)."""
        return await db.get(User, teacher_id)

    async def grade_level_by_name(self, db: AsyncSession, name: str) -> GradeLevel | None:
        """Look up a grade level by display name (``None`` if absent)."""
        result = await db.execute(select(GradeLevel).where(GradeLevel.name == name.strip()))
        return result.scalars().first()

    async def subject_by_code(self, db: AsyncSession, code: str) -> Subject | None:
        """Look up a subject by code (``None`` if absent). Codes are normalised upper-case."""
        result = await db.execute(select(Subject).where(Subject.code == code.strip().upper()))
        return result.scalars().first()

    async def find_class(
        self,
        db: AsyncSession,
        *,
        school_id: uuid.UUID,
        name: str,
    ) -> Class | None:
        """Find a class within a school by name (``None`` if absent)."""
        result = await db.execute(
            select(Class).where(Class.school_id == school_id, Class.name == name)
        )
        return result.scalars().first()

    async def save_class(self, db: AsyncSession, classroom: Class) -> Class:
        """Persist a class and refresh from the DB."""
        db.add(classroom)
        await db.commit()
        await db.refresh(classroom)
        return classroom

    async def find_course(
        self,
        db: AsyncSession,
        *,
        grade_level_id: uuid.UUID,
        subject_id: uuid.UUID,
    ) -> Course | None:
        """Find the unique course for a (grade, subject) pair (``None`` if absent)."""
        result = await db.execute(
            select(Course).where(
                Course.grade_level_id == grade_level_id,
                Course.subject_id == subject_id,
            )
        )
        return result.scalars().first()

    async def save_course(self, db: AsyncSession, course: Course) -> Course:
        """Persist a course and refresh from the DB."""
        db.add(course)
        await db.commit()
        await db.refresh(course)
        return course

    async def find_term_class_subject(
        self,
        db: AsyncSession,
        *,
        class_id: uuid.UUID,
        course_id: uuid.UUID,
        term: str,
        year: str,
    ) -> TermClassSubject | None:
        """Find the unique TCS for one (class, course, term, year) (``None`` if absent)."""
        result = await db.execute(
            select(TermClassSubject).where(
                TermClassSubject.class_id == class_id,
                TermClassSubject.course_id == course_id,
                TermClassSubject.term == term,
                TermClassSubject.year == year,
            )
        )
        return result.scalars().first()

    async def save_term_class_subject(
        self, db: AsyncSession, tcs: TermClassSubject
    ) -> TermClassSubject:
        """Persist a TermClassSubject row and refresh from the DB."""
        db.add(tcs)
        await db.commit()
        await db.refresh(tcs)
        return tcs

    async def find_workspace(
        self,
        db: AsyncSession,
        *,
        teacher_id: uuid.UUID,
        term_class_subject_id: uuid.UUID,
    ) -> TeacherWorkspace | None:
        """Find a teacher workspace by (teacher, TCS) (``None`` if absent)."""
        result = await db.execute(
            select(TeacherWorkspace).where(
                TeacherWorkspace.teacher_id == teacher_id,
                TeacherWorkspace.term_class_subject_id == term_class_subject_id,
            )
        )
        return result.scalars().first()

    async def save_workspace(
        self, db: AsyncSession, workspace: TeacherWorkspace
    ) -> TeacherWorkspace:
        """Persist a TeacherWorkspace (insert or update) and refresh from the DB."""
        db.add(workspace)
        await db.commit()
        await db.refresh(workspace)
        return workspace
