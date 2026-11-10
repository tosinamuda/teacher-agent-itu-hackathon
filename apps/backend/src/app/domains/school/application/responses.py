"""DTO mappers shared by the school application services.

Built once and shared by ``SchoolApplicationService`` and
``WorkspaceProvisioningApplicationService`` so the same ORM-row -> response shape
is produced regardless of which service answers the request.
"""

from __future__ import annotations

from app.domains.school.models.core import GradeLevel, Subject
from app.domains.school.models.structure import Class, School
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.school.schemas import (
    SchoolResponse,
    SchoolWorkspaceResponse,
    TeacherOptionResponse,
)
from app.domains.teaching.models import TeacherWorkspace
from app.domains.users.models import User


def school_response(
    school: School,
    *,
    class_count: int,
    workspace_count: int,
) -> SchoolResponse:
    """Render a ``School`` ORM row + counts to the response model."""
    return SchoolResponse(
        id=school.id,
        name=school.name,
        school_code=school.code,
        default_academic_year=school.default_academic_year,
        current_term=school.current_term,
        created_at=school.created_at,
        class_count=class_count,
        workspace_count=workspace_count,
    )


def workspace_response(
    workspace: TeacherWorkspace,
    school: School,
    classroom: Class,
    grade_level: GradeLevel,
    subject: Subject,
    term_class_subject: TermClassSubject,
    teacher: User,
) -> SchoolWorkspaceResponse:
    """Render the 7-relation workspace row to the response model with a human label."""
    workspace_name = " · ".join(
        [
            school.name,
            classroom.name,
            subject.name,
            term_class_subject.term,
            teacher.full_name or teacher.email,
        ]
    )
    return SchoolWorkspaceResponse(
        workspace_id=workspace.id,
        term_class_subject_id=term_class_subject.id,
        school_id=school.id,
        school_name=school.name,
        school_code=school.code,
        class_id=classroom.id,
        class_name=classroom.name,
        grade_level=grade_level.name,
        subject_name=subject.name,
        subject_code=subject.code,
        term=term_class_subject.term,
        academic_year=term_class_subject.year,
        teacher_id=teacher.id,
        teacher_name=teacher.full_name,
        workspace_name=workspace_name,
        is_primary=workspace.is_primary,
        created_at=workspace.created_at,
    )


def teacher_option_response(teacher: User) -> TeacherOptionResponse:
    """Render a ``User`` (role='teacher') ORM row to the setup-catalog option DTO."""
    return TeacherOptionResponse(
        id=teacher.id,
        full_name=teacher.full_name,
        auth_id=teacher.auth_id,
        email=teacher.email,
    )
