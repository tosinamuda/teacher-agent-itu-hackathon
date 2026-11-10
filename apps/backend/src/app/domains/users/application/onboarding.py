"""Atomic user onboarding across identity and role-profile persistence."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.shared.auth import ROLE_RATER, ROLE_STUDENT


class UserOnboardingError(Exception):
    """A stable onboarding failure that the transport maps to HTTP."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


@dataclass(frozen=True)
class UserOnboardingCommand:
    code: str
    email: str
    full_name: str | None
    role: str
    student_id: str | None = None


@dataclass(frozen=True)
class OnboardedUser:
    id: uuid.UUID
    auth_id: str
    email: str
    full_name: str | None
    role: str
    created_at: datetime | None
    rater_id: str | None = None
    student_id: str | None = None


@dataclass(frozen=True)
class LearnerOnboardingTarget:
    student_id: str
    already_linked: bool


class UserOnboardingPersistence(Protocol):
    async def user_exists(self, *, auth_id: str, email: str) -> bool: ...

    async def learner_target(self, *, student_id: str) -> LearnerOnboardingTarget | None: ...

    async def stage_user(
        self,
        *,
        auth_id: str,
        email: str,
        full_name: str | None,
        role: str,
    ) -> OnboardedUser: ...

    async def stage_rater_profile(
        self,
        *,
        user_id: uuid.UUID,
        display_name: str,
    ) -> str: ...

    async def stage_learner_login(
        self,
        *,
        student_id: str,
        user_id: uuid.UUID,
        code: str,
    ) -> None: ...


class UserOnboardingStore(Protocol):
    @property
    def onboarding(self) -> UserOnboardingPersistence: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class RoleGrantPort(Protocol):
    async def grant(self, *, user_id: uuid.UUID, user_role: str) -> None: ...

    async def revoke(self, *, user_id: uuid.UUID, user_role: str) -> None: ...


async def onboard_user(
    command: UserOnboardingCommand,
    *,
    store: UserOnboardingStore,
    role_grants: RoleGrantPort,
) -> OnboardedUser:
    """Persist a login and its role profile, then make its policy grant durable."""
    code = command.code.strip()
    auth_id = f"code|{code}"
    email = command.email.strip()
    full_name = (command.full_name or "").strip() or None

    learner = await _validated_learner_target(command, store.onboarding)
    if await store.onboarding.user_exists(auth_id=auth_id, email=email):
        raise UserOnboardingError(409, f"login code '{code}' is taken")

    try:
        user = await store.onboarding.stage_user(
            auth_id=auth_id,
            email=email,
            full_name=full_name,
            role=command.role,
        )
        rater_id = await _stage_role_profile(
            command,
            user=user,
            learner=learner,
            store=store.onboarding,
        )
    except Exception:
        await store.rollback()
        raise

    try:
        await role_grants.grant(user_id=user.id, user_role=user.role)
    except Exception:
        await store.rollback()
        raise

    try:
        await store.commit()
    except Exception:
        await store.rollback()
        await role_grants.revoke(user_id=user.id, user_role=user.role)
        raise

    return OnboardedUser(
        id=user.id,
        auth_id=user.auth_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        created_at=user.created_at,
        rater_id=rater_id,
        student_id=learner.student_id if learner is not None else None,
    )


async def _validated_learner_target(
    command: UserOnboardingCommand,
    persistence: UserOnboardingPersistence,
) -> LearnerOnboardingTarget | None:
    if command.role != ROLE_STUDENT:
        return None
    if not command.student_id:
        raise UserOnboardingError(422, "student_id_required_for_student")
    learner = await persistence.learner_target(student_id=command.student_id)
    if learner is None:
        raise UserOnboardingError(404, "student_profile_not_found")
    if learner.already_linked:
        raise UserOnboardingError(409, "student_profile_already_has_login")
    return learner


async def _stage_role_profile(
    command: UserOnboardingCommand,
    *,
    user: OnboardedUser,
    learner: LearnerOnboardingTarget | None,
    store: UserOnboardingPersistence,
) -> str | None:
    if command.role == ROLE_RATER:
        return await store.stage_rater_profile(
            user_id=user.id,
            display_name=user.full_name or user.email,
        )
    if learner is not None:
        await store.stage_learner_login(
            student_id=learner.student_id,
            user_id=user.id,
            code=command.code.strip(),
        )
    return None
