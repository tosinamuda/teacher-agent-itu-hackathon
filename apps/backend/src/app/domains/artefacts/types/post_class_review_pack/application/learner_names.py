"""The names a teacher knows their students by, for the screens that list their packs."""

from __future__ import annotations

from collections.abc import Collection

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.learners.models import LearnerProfile


async def learner_names(db: AsyncSession, student_ids: Collection[str]) -> dict[str, str]:
    """Each student's full name, or their ID when they have no profile."""
    wanted = set(student_ids)
    if not wanted:
        return {}
    rows = (
        await db.execute(
            select(LearnerProfile.student_id, LearnerProfile.full_name).where(
                LearnerProfile.student_id.in_(wanted)
            )
        )
    ).all()
    named = {student_id: full_name for student_id, full_name in rows if full_name}
    return {student_id: named.get(student_id, student_id) for student_id in wanted}
