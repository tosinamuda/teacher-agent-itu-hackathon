from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.infrastructure.repository import UserRepository
from app.domains.users.models import User


class UserAlreadyExistsError(Exception):
    """A user with that login code or email already exists."""


class UserApplicationService:
    def __init__(self, repository: UserRepository | None = None) -> None:
        self.repository = repository or UserRepository()

    async def get_user_by_auth_id(
        self,
        *,
        db: AsyncSession,
        auth_id: str,
    ) -> User | None:
        return await self.repository.get_user_by_auth_id(db, auth_id)

    async def list_users(
        self,
        *,
        db: AsyncSession,
    ) -> list[User]:
        return await self.repository.list_users(db)

    async def create_user(
        self,
        *,
        db: AsyncSession,
        code: str,
        email: str,
        full_name: str | None,
        role: str = "teacher",
    ) -> User:
        """Onboard a user. Their login is the short ``code`` (auth_id = code|<code>)."""
        normalized_code = code.strip()
        auth_id = f"code|{normalized_code}"
        if await self.repository.get_user_by_auth_id(db, auth_id) is not None:
            raise UserAlreadyExistsError(f"login code '{normalized_code}' is taken")
        try:
            return await self.repository.create_user(
                db,
                auth_id=auth_id,
                email=email.strip(),
                full_name=(full_name or "").strip() or None,
                role=role,
            )
        except IntegrityError as exc:
            # Concurrent onboard took the same code/email (unique auth_id/email)
            # between our check and insert — surface the intended 409.
            await db.rollback()
            raise UserAlreadyExistsError(f"login code '{normalized_code}' is taken") from exc
