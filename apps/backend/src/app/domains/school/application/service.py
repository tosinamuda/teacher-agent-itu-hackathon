"""School CRUD + setup catalog + read-side listings.

The workspace provisioning cascade lives in its own service
(``workspace_provisioning_service``); all SQL lives in ``SchoolRepository``;
the response mappers live in ``responses``. This service is now pure
orchestration over the repo: listings, school CRUD, and the setup-catalog
read.
"""

from __future__ import annotations

import re
import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.curriculum.domain.subject_offerings import SubjectCatalog
from app.domains.school.application.errors import SchoolApplicationError
from app.domains.school.application.responses import (
    school_response,
    teacher_option_response,
    workspace_response,
)
from app.domains.school.infrastructure.repository import SchoolRepository
from app.domains.school.models.structure import School
from app.domains.school.schemas import (
    ClassResponse,
    GradeLevelOptionResponse,
    SchoolCreateRequest,
    SchoolResponse,
    SchoolSetupCatalogResponse,
    SchoolUpdateRequest,
    SchoolWorkspaceResponse,
    SubjectOptionResponse,
)
from app.domains.users.application import UserApplicationService

DEFAULT_TERMS = ["First Term", "Second Term", "Third Term"]
DEFAULT_ACADEMIC_YEARS = ["2025/2026", "2024/2025"]


def _normalize_school_code(value: str) -> str:
    """Normalise a school code to uppercase + ``-`` separators (raise on empty)."""
    normalized = re.sub(r"[^A-Z0-9]+", "-", value.upper()).strip("-")
    if not normalized:
        raise SchoolApplicationError(422, "school_code_invalid")
    return normalized


def _strip_or_none(value: str | None) -> str | None:
    """Strip ``value``; return ``None`` for empty/whitespace-only/``None`` input."""
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class SchoolApplicationService:
    """Own school CRUD + the setup-catalog read + the workspace listing."""

    def __init__(
        self,
        repository: SchoolRepository | None = None,
        users: UserApplicationService | None = None,
    ) -> None:
        self.repository = repository or SchoolRepository()
        self.users = users or UserApplicationService()

    async def list_classes(
        self,
        *,
        db: AsyncSession,
        grade: str | None,
        school_id: uuid.UUID | None,
    ) -> list[ClassResponse]:
        """List classes with their grade + school join, ordered for the dashboard."""
        rows = await self.repository.list_classes_with_school(db, grade=grade, school_id=school_id)
        return [
            ClassResponse(
                id=classroom.id,
                name=classroom.name,
                grade=grade_name,
                school_id=row_school_id,
                school_name=school_name,
                school_code=school_code,
            )
            for classroom, grade_name, row_school_id, school_name, school_code in rows
        ]

    async def list_schools(self, *, db: AsyncSession) -> list[SchoolResponse]:
        """List schools with their class + workspace counts."""
        rows = await self.repository.list_schools_with_counts(db)
        return [
            school_response(school, class_count=class_total, workspace_count=workspace_total)
            for school, class_total, workspace_total in rows
        ]

    async def create_school(
        self,
        *,
        db: AsyncSession,
        payload: SchoolCreateRequest,
    ) -> SchoolResponse:
        """Create a school after the unique-code-or-name conflict check."""
        school_code = _normalize_school_code(payload.school_code)
        name = payload.name.strip()
        if (
            await self.repository.find_school_conflict(db, school_code=school_code, name=name)
            is not None
        ):
            raise SchoolApplicationError(409, "school_exists")
        try:
            saved = await self.repository.save_school(
                db,
                School(
                    name=name,
                    code=school_code,
                    default_academic_year=_strip_or_none(payload.default_academic_year),
                    current_term=_strip_or_none(payload.current_term),
                ),
            )
        except IntegrityError as exc:
            # Concurrent create took the same name/code (unique) between the
            # conflict check and the insert — surface the intended 409.
            await db.rollback()
            raise SchoolApplicationError(409, "school_exists") from exc
        return school_response(saved, class_count=0, workspace_count=0)

    async def get_school(
        self,
        *,
        db: AsyncSession,
        school_id: uuid.UUID,
    ) -> SchoolResponse:
        """Fetch one school with its derived counts."""
        school = await self._school_or_error(db=db, school_id=school_id)
        class_total, workspace_total = await self.repository.school_counts(db, school_id=school.id)
        return school_response(school, class_count=class_total, workspace_count=workspace_total)

    async def update_school(
        self,
        *,
        db: AsyncSession,
        school_id: uuid.UUID,
        payload: SchoolUpdateRequest,
    ) -> SchoolResponse:
        """Update a school after the conflict check (excluding itself)."""
        school = await self._school_or_error(db=db, school_id=school_id)
        school_code = _normalize_school_code(payload.school_code)
        name = payload.name.strip()
        if (
            await self.repository.find_school_conflict(
                db, school_code=school_code, name=name, exclude_id=school.id
            )
            is not None
        ):
            raise SchoolApplicationError(409, "school_exists")
        school.name = name
        school.code = school_code
        school.default_academic_year = _strip_or_none(payload.default_academic_year)
        school.current_term = _strip_or_none(payload.current_term)
        try:
            saved = await self.repository.save_school(db, school)
        except IntegrityError as exc:
            # A concurrent rename to the same code/name slipped past the find_school_conflict
            # check above (TOCTOU) and hit the unique at commit — surface the intended 409, not
            # a raw 500 (the create_school path already converges this way).
            await db.rollback()
            raise SchoolApplicationError(409, "school_exists") from exc
        class_total, workspace_total = await self.repository.school_counts(db, school_id=saved.id)
        return school_response(saved, class_count=class_total, workspace_count=workspace_total)

    def subject_offering_catalog(self) -> SubjectCatalog:
        """Return the curriculum-published subject-offering catalog (slots + fields + trades).

        Wraps ``curriculum.domain.subject_offerings.load_subject_catalog`` so
        the school transport layer doesn't import the curriculum domain
        directly (``api ↛ peer-domain``). Pure read — no DB; the catalog
        ships as a JSON file the curriculum domain validates on load.
        """
        from app.domains.curriculum.domain.subject_offerings import load_subject_catalog

        return load_subject_catalog()

    async def list_setup_catalog(self, *, db: AsyncSession) -> SchoolSetupCatalogResponse:
        """Return the dropdown choices for the school-setup workflow."""
        grade_levels = await self.repository.list_grade_levels(db)
        subjects = await self.repository.list_subjects(db)
        academic_years = await self.repository.list_academic_year_names(db)
        teachers = await self.users.list_users(db=db)
        return SchoolSetupCatalogResponse(
            grade_levels=[
                GradeLevelOptionResponse(id=grade.id, name=grade.name) for grade in grade_levels
            ],
            subjects=[
                SubjectOptionResponse(id=subject.id, name=subject.name, code=subject.code)
                for subject in subjects
            ],
            teachers=[teacher_option_response(teacher) for teacher in teachers],
            academic_years=academic_years or list(DEFAULT_ACADEMIC_YEARS),
            suggested_terms=list(DEFAULT_TERMS),
        )

    async def list_workspaces(
        self,
        *,
        db: AsyncSession,
        school_id: uuid.UUID | None,
    ) -> list[SchoolWorkspaceResponse]:
        """List teacher workspaces with their full school/class/course/teacher graph."""
        rows = await self.repository.list_workspaces_with_relations(db, school_id=school_id)
        return [workspace_response(*row) for row in rows]

    async def _school_or_error(
        self,
        *,
        db: AsyncSession,
        school_id: uuid.UUID,
    ) -> School:
        school = await self.repository.get_school(db, school_id)
        if school is None:
            raise SchoolApplicationError(404, "school_not_found")
        return school
