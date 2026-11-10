from __future__ import annotations

import uuid
from typing import cast

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.learners.models.learner import LearnerProfile
from app.domains.school.models.structure import Class


class LearnerRepository:
    async def get_learner_by_code(
        self,
        db: AsyncSession,
        code: str,
    ) -> LearnerProfile | None:
        result = await db.execute(select(LearnerProfile).filter(LearnerProfile.code == code))
        return result.scalars().first()

    async def get_learner_by_user_id(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> LearnerProfile | None:
        """The student profile bound to this login user (None for pure research data)."""
        result = await db.execute(select(LearnerProfile).filter(LearnerProfile.user_id == user_id))
        return result.scalars().first()

    async def save_learner(
        self,
        db: AsyncSession,
        learner: LearnerProfile,
    ) -> LearnerProfile:
        db.add(learner)
        await db.commit()
        await db.refresh(learner)
        return learner

    async def list_learners(
        self,
        db: AsyncSession,
        *,
        grade: str | None,
        track: str | None,
        class_id: uuid.UUID | None,
        field_of_study: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[tuple[LearnerProfile, str | None]], int]:
        stmt = select(LearnerProfile, Class.name.label("class_name")).outerjoin(
            Class,
            LearnerProfile.class_id == Class.id,
        )
        if grade:
            stmt = stmt.filter(LearnerProfile.grade == grade)
        if track:
            stmt = stmt.filter(LearnerProfile.track == track)
        if class_id:
            stmt = stmt.filter(LearnerProfile.class_id == class_id)
        if field_of_study:
            stmt = stmt.filter(LearnerProfile.field_of_study == field_of_study)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt) or 0

        paginated_stmt = (
            stmt.order_by(LearnerProfile.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await db.execute(paginated_stmt)
        return cast(list[tuple[LearnerProfile, str | None]], list(result.all())), int(total)

    async def get_learner_by_id_or_code(
        self,
        db: AsyncSession,
        learner_id: str,
    ) -> tuple[LearnerProfile, str | None] | None:
        stmt = (
            select(LearnerProfile, Class.name.label("class_name"))
            .outerjoin(
                Class,
                LearnerProfile.class_id == Class.id,
            )
            .filter(
                or_(
                    LearnerProfile.student_id == learner_id,
                    LearnerProfile.code == learner_id,
                )
            )
        )
        result = await db.execute(stmt)
        return cast(tuple[LearnerProfile, str | None] | None, result.first())

    async def get_learner_by_id(
        self,
        db: AsyncSession,
        learner_id: str,
    ) -> LearnerProfile | None:
        result = await db.execute(
            select(LearnerProfile).filter(LearnerProfile.student_id == learner_id)
        )
        return result.scalars().first()

    async def list_user_ids_for_student_ids(
        self,
        db: AsyncSession,
        student_ids: set[str],
    ) -> set[uuid.UUID]:
        """The login user ids paired with these student profiles.

        Drops rows whose ``user_id`` is null (pure research data with no login).
        """
        if not student_ids:
            return set()
        result = await db.execute(
            select(LearnerProfile.user_id).filter(
                LearnerProfile.student_id.in_(student_ids),
                LearnerProfile.user_id.is_not(None),
            )
        )
        return {user_id for user_id in result.scalars().all() if user_id is not None}

    async def list_names_by_student_ids(
        self,
        db: AsyncSession,
        student_ids: set[str],
    ) -> dict[str, str | None]:
        """Map ``student_id`` → ``full_name`` for surfacing learner names in the UI."""
        if not student_ids:
            return {}
        result = await db.execute(
            select(LearnerProfile.student_id, LearnerProfile.full_name).filter(
                LearnerProfile.student_id.in_(student_ids)
            )
        )
        return {student_id: full_name for student_id, full_name in result.all()}
