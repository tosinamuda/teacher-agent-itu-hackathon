"""Workspace provisioning — the school -> class -> course -> TCS -> workspace upsert cascade.

One distinct concern: given a teacher + a (school, grade, subject, class name,
term, academic_year, is_primary) payload, idempotently ensure the full graph
exists and return the resolved workspace. School, grade level and subject are
looked up; the four get-or-create steps that follow each own a separate identity
policy (and a separate persistence commit), so the cascade is a real
orchestration, not a delegating wrapper.

Concurrency: each natural key has a composite unique constraint, so two callers
provisioning the same graph at once can't duplicate it — the loser's insert fails
at commit. The whole cascade is retried (``create_workspace``): a fresh attempt
re-loads its rows and finds the winner's, so it converges instead of 500ing. The
retry re-loads from scratch deliberately — a mid-cascade ``rollback`` expires every
ORM object in the session, so reusing them would raise ``MissingGreenlet``.

Distinct from the read/CRUD/setup-catalog surface (kept in
``SchoolApplicationService``). Depends on ``SchoolRepository`` for all SQL —
no raw ``select()``/``db.execute()`` in this layer.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.school.application.errors import SchoolApplicationError
from app.domains.school.application.responses import workspace_response
from app.domains.school.infrastructure.repository import SchoolRepository
from app.domains.school.models.core import GradeLevel, Subject
from app.domains.school.models.structure import Class, Course, School
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.school.schemas import (
    SchoolWorkspaceCreateRequest,
    SchoolWorkspaceResponse,
)
from app.domains.teaching.models import TeacherWorkspace
from app.domains.users.models import User

# class, course, term-class-subject, workspace — each commits on its own, so a
# caller that loses a race at every step in turn spends one whole attempt per step
# before the last one can commit. The budget has to clear that step count with room
# for a step lost more than once, or a loaded machine exhausts it at the final step.
_PROVISION_COMMIT_STEPS = 4
_MAX_PROVISION_ATTEMPTS = _PROVISION_COMMIT_STEPS + 2


class WorkspaceProvisioningApplicationService:
    """Own the get-or-create cascade from a payload to a resolved teacher workspace."""

    def __init__(self, repository: SchoolRepository | None = None) -> None:
        self.repository = repository or SchoolRepository()

    async def create_workspace(
        self,
        *,
        db: AsyncSession,
        payload: SchoolWorkspaceCreateRequest,
    ) -> SchoolWorkspaceResponse:
        """Provision the school -> class -> course -> TCS -> workspace graph, idempotently.

        Retries the whole cascade on a concurrent insert race: the loser's commit
        trips a unique constraint, we roll back, and a fresh attempt finds the
        winner's rows. Re-loading from scratch each attempt is required because the
        rollback expires the session's ORM objects.
        """
        for attempt in range(1, _MAX_PROVISION_ATTEMPTS + 1):
            try:
                return await self._provision(db=db, payload=payload)
            except IntegrityError:
                await db.rollback()
                if attempt == _MAX_PROVISION_ATTEMPTS:
                    raise
        raise AssertionError("unreachable: loop returns or raises")

    async def _provision(
        self,
        *,
        db: AsyncSession,
        payload: SchoolWorkspaceCreateRequest,
    ) -> SchoolWorkspaceResponse:
        school = await self.repository.get_school(db, payload.school_id)
        if school is None:
            raise SchoolApplicationError(404, "school_not_found")

        teacher = await self.repository.get_teacher(db, payload.teacher_id)
        if teacher is None:
            raise SchoolApplicationError(404, "teacher_not_found")

        grade_level = await self._grade_level_or_error(db, payload.grade_level_name)
        subject = await self._subject_or_error(db, payload.subject_code)

        classroom = await self._get_or_create_class(
            db=db, school=school, grade_level=grade_level, class_name=payload.class_name
        )
        course = await self._get_or_create_course(db=db, grade_level=grade_level, subject=subject)
        term_class_subject = await self._get_or_create_term_class_subject(
            db=db,
            classroom=classroom,
            course=course,
            term=payload.term,
            academic_year=payload.academic_year,
        )
        workspace = await self._get_or_create_workspace(
            db=db,
            teacher=teacher,
            term_class_subject=term_class_subject,
            is_primary=payload.is_primary,
        )
        return workspace_response(
            workspace,
            school,
            classroom,
            grade_level,
            subject,
            term_class_subject,
            teacher,
        )

    async def _grade_level_or_error(self, db: AsyncSession, name: str) -> GradeLevel:
        grade_level = await self.repository.grade_level_by_name(db, name)
        if grade_level is None:
            raise SchoolApplicationError(404, "grade_level_not_found")
        return grade_level

    async def _subject_or_error(self, db: AsyncSession, code: str) -> Subject:
        subject = await self.repository.subject_by_code(db, code)
        if subject is None:
            raise SchoolApplicationError(404, "subject_not_found")
        return subject

    async def _get_or_create_class(
        self,
        *,
        db: AsyncSession,
        school: School,
        grade_level: GradeLevel,
        class_name: str,
    ) -> Class:
        normalized_name = class_name.strip()
        existing = await self.repository.find_class(db, school_id=school.id, name=normalized_name)
        if existing is not None:
            return existing
        return await self.repository.save_class(
            db,
            Class(
                name=normalized_name,
                school_id=school.id,
                grade_level_id=grade_level.id,
            ),
        )

    async def _get_or_create_course(
        self,
        *,
        db: AsyncSession,
        grade_level: GradeLevel,
        subject: Subject,
    ) -> Course:
        existing = await self.repository.find_course(
            db, grade_level_id=grade_level.id, subject_id=subject.id
        )
        if existing is not None:
            return existing
        return await self.repository.save_course(
            db,
            Course(
                name=f"{grade_level.name} {subject.name}",
                description=None,
                subject_id=subject.id,
                grade_level_id=grade_level.id,
            ),
        )

    async def _get_or_create_term_class_subject(
        self,
        *,
        db: AsyncSession,
        classroom: Class,
        course: Course,
        term: str,
        academic_year: str,
    ) -> TermClassSubject:
        normalized_term = term.strip()
        normalized_year = academic_year.strip()
        existing = await self.repository.find_term_class_subject(
            db,
            class_id=classroom.id,
            course_id=course.id,
            term=normalized_term,
            year=normalized_year,
        )
        if existing is not None:
            return existing
        return await self.repository.save_term_class_subject(
            db,
            TermClassSubject(
                class_id=classroom.id,
                course_id=course.id,
                term=normalized_term,
                year=normalized_year,
            ),
        )

    async def _get_or_create_workspace(
        self,
        *,
        db: AsyncSession,
        teacher: User,
        term_class_subject: TermClassSubject,
        is_primary: bool,
    ) -> TeacherWorkspace:
        existing = await self.repository.find_workspace(
            db, teacher_id=teacher.id, term_class_subject_id=term_class_subject.id
        )
        if existing is None:
            return await self.repository.save_workspace(
                db,
                TeacherWorkspace(
                    teacher_id=teacher.id,
                    term_class_subject_id=term_class_subject.id,
                    is_primary=is_primary,
                ),
            )
        if is_primary and not existing.is_primary:
            existing.is_primary = True
            return await self.repository.save_workspace(db, existing)
        return existing
