"""The onboarding command owns one database transaction and Casbin compensation."""

from __future__ import annotations

import uuid
from datetime import datetime

import pytest

from app.domains.users.application.onboarding import (
    LearnerOnboardingTarget,
    OnboardedUser,
    UserOnboardingCommand,
    UserOnboardingError,
    onboard_user,
)


class FakeOnboardingStore:
    def __init__(self) -> None:
        self.events: list[str] = []
        self.existing = False
        self.learner: LearnerOnboardingTarget | None = None
        self.fail_commit = False
        self.user = OnboardedUser(
            id=uuid.uuid4(),
            auth_id="code|new-user",
            email="new@example.test",
            full_name="New User",
            role="rater",
            created_at=datetime(2026, 1, 1),
        )

    @property
    def onboarding(self) -> FakeOnboardingStore:
        return self

    async def user_exists(self, *, auth_id: str, email: str) -> bool:
        self.events.append("check_user")
        return self.existing

    async def learner_target(self, *, student_id: str) -> LearnerOnboardingTarget | None:
        self.events.append("check_learner")
        return self.learner

    async def stage_user(self, **_values: object) -> OnboardedUser:
        self.events.append("stage_user")
        return self.user

    async def stage_rater_profile(self, **_values: object) -> str:
        self.events.append("stage_rater")
        return "ERAT-1"

    async def stage_learner_login(self, **_values: object) -> None:
        self.events.append("stage_learner")

    async def commit(self) -> None:
        self.events.append("commit")
        if self.fail_commit:
            raise RuntimeError("commit failed")

    async def rollback(self) -> None:
        self.events.append("rollback")


class FakeRoleGrants:
    def __init__(self, events: list[str]) -> None:
        self.events = events
        self.fail_grant = False

    async def grant(self, **_values: object) -> None:
        self.events.append("grant")
        if self.fail_grant:
            raise RuntimeError("grant failed")

    async def revoke(self, **_values: object) -> None:
        self.events.append("revoke")


def _rater_command() -> UserOnboardingCommand:
    return UserOnboardingCommand(
        code=" new-user ",
        email=" new@example.test ",
        full_name=" New User ",
        role="rater",
    )


@pytest.mark.asyncio
async def test_onboarding_grants_before_one_database_commit() -> None:
    store = FakeOnboardingStore()
    result = await onboard_user(
        _rater_command(),
        store=store,
        role_grants=FakeRoleGrants(store.events),
    )

    assert result.rater_id == "ERAT-1"
    assert store.events == ["check_user", "stage_user", "stage_rater", "grant", "commit"]


@pytest.mark.asyncio
async def test_grant_failure_rolls_back_database_without_committing() -> None:
    store = FakeOnboardingStore()
    grants = FakeRoleGrants(store.events)
    grants.fail_grant = True

    with pytest.raises(RuntimeError, match="grant failed"):
        await onboard_user(_rater_command(), store=store, role_grants=grants)

    assert store.events[-2:] == ["grant", "rollback"]
    assert "commit" not in store.events


@pytest.mark.asyncio
async def test_commit_failure_rolls_back_and_revokes_grant() -> None:
    store = FakeOnboardingStore()
    store.fail_commit = True

    with pytest.raises(RuntimeError, match="commit failed"):
        await onboard_user(
            _rater_command(),
            store=store,
            role_grants=FakeRoleGrants(store.events),
        )

    assert store.events[-4:] == ["grant", "commit", "rollback", "revoke"]


@pytest.mark.asyncio
async def test_student_profile_is_validated_before_user_is_staged() -> None:
    store = FakeOnboardingStore()
    command = UserOnboardingCommand(
        code="student",
        email="student@example.test",
        full_name="Student",
        role="student",
        student_id="STU-missing",
    )

    with pytest.raises(UserOnboardingError, match="student_profile_not_found"):
        await onboard_user(
            command,
            store=store,
            role_grants=FakeRoleGrants(store.events),
        )

    assert store.events == ["check_learner"]
