from __future__ import annotations

import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.models import User


class UserRepository:
    async def get_user_by_auth_id(
        self,
        db: AsyncSession,
        auth_id: str,
    ) -> User | None:
        result = await db.execute(select(User).where(User.auth_id == auth_id))
        return result.scalars().first()

    async def list_users(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User).order_by(User.full_name.asc(), User.email.asc()))
        return list(result.scalars().all())

    async def create_user(
        self,
        db: AsyncSession,
        *,
        auth_id: str,
        email: str,
        full_name: str | None,
        role: str,
    ) -> User:
        user = User(auth_id=auth_id, email=email, full_name=full_name, role=role)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def delete_user(self, db: AsyncSession, user_id: uuid.UUID) -> None:
        """Delete a user row — onboarding compensation when a later step fails."""
        await db.execute(delete(User).where(User.id == user_id))
        await db.commit()
