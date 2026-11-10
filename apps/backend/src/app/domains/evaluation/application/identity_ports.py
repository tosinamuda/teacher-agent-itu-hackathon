"""Role ports for human and synthetic rater identity."""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.evaluation.domain.records import RaterIdentity


class RaterIdentityReader(Protocol):
    async def rater_identity(self, *, rater_id: str) -> RaterIdentity | None: ...

    async def rater_identity_for_user(self, *, user_id: uuid.UUID) -> RaterIdentity | None: ...


class RaterIdentities(Protocol):
    async def rater_identity_by_name(self, *, display_name: str) -> RaterIdentity | None: ...

    async def stage_rater_identity(self, identity: RaterIdentity) -> RaterIdentity: ...


class RaterRegistrationStore(Protocol):
    @property
    def rater_identities(self) -> RaterIdentities: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
