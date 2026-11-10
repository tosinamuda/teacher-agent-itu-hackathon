"""Rater identities are actor-bound and synthetic registration owns its UoW."""

from __future__ import annotations

import uuid
from datetime import datetime

import pytest

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.rater_identity import (
    RaterIdentityConflictError,
    ensure_synthetic_rater,
    rater_for_actor,
)
from app.domains.evaluation.domain.records import RaterIdentity


def _identity(*, user_id: uuid.UUID | None = None) -> RaterIdentity:
    now = datetime(2026, 1, 1)
    return RaterIdentity(
        id=uuid.uuid4(),
        rater_id="ERAT-1",
        display_name="Rater One",
        user_id=user_id,
        created_at=now,
        updated_at=now,
    )


class FakeIdentityStore:
    def __init__(self) -> None:
        self.by_user: dict[uuid.UUID, RaterIdentity] = {}
        self.by_name: dict[str, RaterIdentity] = {}
        self.commits = 0
        self.rollbacks = 0
        self.conflict_once = False

    @property
    def rater_identities(self) -> FakeIdentityStore:
        return self

    async def rater_identity(self, *, rater_id: str) -> RaterIdentity | None:
        return next((item for item in self.by_name.values() if item.rater_id == rater_id), None)

    async def rater_identity_for_user(self, *, user_id: uuid.UUID) -> RaterIdentity | None:
        return self.by_user.get(user_id)

    async def rater_identity_by_name(self, *, display_name: str) -> RaterIdentity | None:
        return self.by_name.get(display_name)

    async def stage_rater_identity(self, identity: RaterIdentity) -> RaterIdentity:
        if self.conflict_once:
            self.conflict_once = False
            self.by_name[identity.display_name] = _identity()
            raise RaterIdentityConflictError
        self.by_name[identity.display_name] = identity
        return identity

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1


@pytest.mark.asyncio
async def test_rater_session_resolves_only_the_actor_link() -> None:
    store = FakeIdentityStore()
    user_id = uuid.uuid4()
    expected = _identity(user_id=user_id)
    store.by_user[user_id] = expected

    assert await rater_for_actor(store, actor_user_id=user_id) == expected


@pytest.mark.asyncio
async def test_authenticated_actor_without_rater_gets_stable_403() -> None:
    with pytest.raises(EvaluationApplicationError) as caught:
        await rater_for_actor(FakeIdentityStore(), actor_user_id=uuid.uuid4())

    assert (caught.value.status_code, caught.value.detail) == (
        403,
        "no_rater_identity_bound_to_this_user",
    )


@pytest.mark.asyncio
async def test_synthetic_registration_commits_once_and_converges_after_conflict() -> None:
    store = FakeIdentityStore()
    store.conflict_once = True

    winner = await ensure_synthetic_rater(store, display_name=" Synthetic Rater ")

    assert winner.display_name == "Rater One"
    assert store.commits == 0
    assert store.rollbacks == 1
