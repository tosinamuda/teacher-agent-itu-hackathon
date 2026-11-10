"""Casbin adapter for the onboarding role-grant port."""

from __future__ import annotations

import uuid

from app.shared.authz import grant_role_to_user, revoke_role_from_user


class CasbinRoleGrants:
    async def grant(self, *, user_id: uuid.UUID, user_role: str) -> None:
        await grant_role_to_user(user_id=user_id, user_role=user_role)

    async def revoke(self, *, user_id: uuid.UUID, user_role: str) -> None:
        await revoke_role_from_user(user_id=user_id, user_role=user_role)
