from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.teaching.application.service import TeachingWorkspaceApplicationService
from app.domains.teaching.infrastructure.repository import TeachingRepository
from app.domains.users.application import UserApplicationService


def _workspace_stub(
    *,
    teacher_id: uuid.UUID,
    term: str,
    is_primary: bool,
) -> SimpleNamespace:
    school = SimpleNamespace(
        id=uuid.uuid4(),
        name="Plan-to-Tutor Research School",
        code="PTRS",
    )
    classroom = SimpleNamespace(id=uuid.uuid4(), name="JSS1", school=school)
    subject = SimpleNamespace(name="Mathematics", code="MATH")
    grade_level = SimpleNamespace(name="JSS1")
    course = SimpleNamespace(
        id=uuid.uuid4(),
        name="JSS1 Mathematics",
        subject=subject,
        grade_level=grade_level,
    )
    term_class_subject = SimpleNamespace(
        id=uuid.uuid4(),
        course_id=course.id,
        course=course,
        classroom=classroom,
        term=term,
    )
    return SimpleNamespace(
        id=uuid.uuid4(),
        term_class_subject=term_class_subject,
        is_primary=is_primary,
        teacher_id=teacher_id,
        settings=None,
        created_at=datetime.now(timezone.utc),
    )


class FakeUsersService:
    def __init__(self, teacher_id: uuid.UUID | None) -> None:
        self.teacher_id = teacher_id
        self.auth_ids: list[str] = []

    async def get_user_by_auth_id(
        self,
        *,
        db: AsyncSession,
        auth_id: str,
    ) -> SimpleNamespace | None:
        self.auth_ids.append(auth_id)
        if self.teacher_id is None:
            return None
        return SimpleNamespace(id=self.teacher_id)


class FakeTeachingRepository:
    def __init__(self, workspaces: list[SimpleNamespace]) -> None:
        self.workspaces = workspaces
        self.canonical_only_flags: list[bool] = []

    async def list_workspaces_for_teacher(
        self,
        db: AsyncSession,
        teacher_id: uuid.UUID,
        *,
        canonical_only: bool = True,
    ) -> list[SimpleNamespace]:
        self.canonical_only_flags.append(canonical_only)
        return self.workspaces


@pytest.mark.asyncio
async def test_list_workspaces_returns_canonical_term_order() -> None:
    teacher_id = uuid.uuid4()
    repository = FakeTeachingRepository(
        [
            _workspace_stub(teacher_id=teacher_id, term="Third Term", is_primary=False),
            _workspace_stub(teacher_id=teacher_id, term="Second Term", is_primary=False),
            _workspace_stub(teacher_id=teacher_id, term="First Term", is_primary=True),
        ]
    )
    users = FakeUsersService(teacher_id)
    service = TeachingWorkspaceApplicationService(
        users=cast(UserApplicationService, users),
        repository=cast(TeachingRepository, repository),
    )

    workspaces = await service.list_workspaces(
        db=cast(AsyncSession, object()),
        teacher_code="uncle-tosin",
    )

    assert users.auth_ids == ["code|uncle-tosin"]
    assert repository.canonical_only_flags == [True]
    assert [workspace.term for workspace in workspaces] == [
        "First Term",
        "Second Term",
        "Third Term",
    ]
    assert workspaces[0].teacher_id == str(teacher_id)
    assert workspaces[0].school_name == "Plan-to-Tutor Research School"
    assert workspaces[0].class_name == "JSS1"


@pytest.mark.asyncio
async def test_list_workspaces_returns_empty_when_teacher_is_unknown() -> None:
    repository = FakeTeachingRepository([])
    users = FakeUsersService(None)
    service = TeachingWorkspaceApplicationService(
        users=cast(UserApplicationService, users),
        repository=cast(TeachingRepository, repository),
    )

    workspaces = await service.list_workspaces(
        db=cast(AsyncSession, object()),
        teacher_code="missing-teacher",
    )

    assert workspaces == []
    assert repository.canonical_only_flags == []
