"""Composition roots for user-domain HTTP use cases."""

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.users.infrastructure.casbin_role_grants import CasbinRoleGrants
from app.domains.users.infrastructure.sqlalchemy_onboarding_store import (
    SqlAlchemyUserOnboardingStore,
)


async def user_onboarding_store(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[SqlAlchemyUserOnboardingStore, None]:
    store = SqlAlchemyUserOnboardingStore(db)
    try:
        yield store
    except BaseException:
        await store.rollback()
        raise


def role_grants() -> CasbinRoleGrants:
    return CasbinRoleGrants()
