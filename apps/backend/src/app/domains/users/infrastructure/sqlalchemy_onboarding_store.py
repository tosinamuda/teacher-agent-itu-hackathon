"""SQLAlchemy unit of work for cross-domain user onboarding."""

from __future__ import annotations

import uuid

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.evaluation.infrastructure.models import EvaluationRater
from app.domains.learners.models.learner import LearnerProfile
from app.domains.users.application.onboarding import (
    LearnerOnboardingTarget,
    OnboardedUser,
    UserOnboardingError,
    UserOnboardingPersistence,
)
from app.domains.users.models.user import User
from app.shared.ids import PublicIdPrefix, new_public_id


class SqlAlchemyUserOnboardingStore:
    """One session spanning the user, learner, and rater tables."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def onboarding(self) -> UserOnboardingPersistence:
        return self

    async def user_exists(self, *, auth_id: str, email: str) -> bool:
        result = await self._session.execute(
            select(User.id).where(or_(User.auth_id == auth_id, User.email == email))
        )
        return result.scalar_one_or_none() is not None

    async def learner_target(self, *, student_id: str) -> LearnerOnboardingTarget | None:
        result = await self._session.execute(
            select(LearnerProfile).where(
                or_(
                    LearnerProfile.student_id == student_id,
                    LearnerProfile.code == student_id,
                )
            )
        )
        learner = result.scalars().first()
        if learner is None:
            return None
        return LearnerOnboardingTarget(
            student_id=learner.student_id,
            already_linked=learner.user_id is not None,
        )

    async def stage_user(
        self,
        *,
        auth_id: str,
        email: str,
        full_name: str | None,
        role: str,
    ) -> OnboardedUser:
        user = User(auth_id=auth_id, email=email, full_name=full_name, role=role)
        self._session.add(user)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise UserOnboardingError(
                409, f"login code '{auth_id.removeprefix('code|')}' is taken"
            ) from exc
        return OnboardedUser(
            id=user.id,
            auth_id=user.auth_id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            created_at=user.created_at,
        )

    async def stage_rater_profile(
        self,
        *,
        user_id: uuid.UUID,
        display_name: str,
    ) -> str:
        rater_id = new_public_id(PublicIdPrefix.EVALUATION_RATER)
        self._session.add(
            EvaluationRater(
                rater_id=rater_id,
                display_name=display_name,
                user_id=user_id,
            )
        )
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise UserOnboardingError(409, "rater_display_name_taken") from exc
        return rater_id

    async def stage_learner_login(
        self,
        *,
        student_id: str,
        user_id: uuid.UUID,
        code: str,
    ) -> None:
        result = await self._session.execute(
            select(LearnerProfile).where(LearnerProfile.student_id == student_id).with_for_update()
        )
        learner = result.scalars().first()
        if learner is None:
            raise UserOnboardingError(404, "student_profile_not_found")
        if learner.user_id is not None:
            raise UserOnboardingError(409, "student_profile_already_has_login")
        learner.user_id = user_id
        learner.code = code
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise UserOnboardingError(409, "student_profile_already_has_login") from exc

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
