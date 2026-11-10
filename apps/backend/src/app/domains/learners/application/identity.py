"""Which learner a signed-in student is."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.learners.infrastructure.repository import LearnerRepository
from app.shared.auth import Actor


async def student_id_of(actor: Actor, db: AsyncSession) -> str:
    """The public ``student_id`` of the learner the actor signed in as."""
    if actor.teacher_id is None:
        raise HTTPException(status_code=401, detail="not_authenticated")
    learner = await LearnerRepository().get_learner_by_user_id(db, actor.teacher_id)
    if learner is None:
        raise HTTPException(status_code=403, detail="no_student_identity_bound_to_this_user")
    return learner.student_id
