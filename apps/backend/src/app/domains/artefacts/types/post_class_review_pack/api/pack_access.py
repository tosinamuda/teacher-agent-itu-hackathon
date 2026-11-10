"""Who may read a revision note, and which ones.

A teacher reads the notes of the classes they teach, a researcher or admin any, and a learner
only their own that stand approved at the class note's current version. Anyone else is refused;
a learner asking for a note they may not read is told it does not exist.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.wiring import build_lifecycle_manager
from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owns_plan_version,
)
from app.domains.learners.application.identity import student_id_of
from app.shared.auth import ROLE_ADMIN, ROLE_RESEARCH_MANAGER, ROLE_STUDENT, ROLE_TEACHER, Actor

if TYPE_CHECKING:
    # Type-annotation-only — see ``api ↛ models`` rule.
    from app.domains.artefacts.core.infrastructure.models import Artefact

_ANY_NOTE = {ROLE_RESEARCH_MANAGER, ROLE_ADMIN}


async def require_class(actor: Actor, db: AsyncSession, plan_version_id: str | None) -> None:
    """The notes of a lesson are for the teacher of its class, and for researchers and admins."""
    if actor.role in _ANY_NOTE:
        return
    if (
        actor.role == ROLE_TEACHER
        and actor.teacher_id is not None
        and plan_version_id is not None
        and await teacher_owns_plan_version(
            db, teacher_id=actor.teacher_id, plan_version_id=plan_version_id
        )
    ):
        return
    raise HTTPException(status_code=403, detail="You can only read notes of a class you teach.")


async def require_teaching_role(actor: Actor) -> None:
    if actor.role not in _ANY_NOTE | {ROLE_TEACHER}:
        raise HTTPException(status_code=403, detail="Only a teacher can do this.")


async def require_readable(
    actor: Actor, db: AsyncSession, artefact: Artefact, *, learner_may: bool = True
) -> None:
    """Refuse the note unless this caller may read it."""
    if actor.role == ROLE_STUDENT and learner_may:
        student_id = await student_id_of(actor, db)
        released = await build_lifecycle_manager().list_learner_artefacts(
            db=db,
            learner_id=student_id,
            plan_version_id=artefact.plan_version_id,
            limit=200,
            review_status=ArtefactReviewStatus.APPROVED.value,
        )
        if artefact.student_id != student_id or artefact.artefact_id not in {
            a.artefact_id for a in released
        }:
            raise HTTPException(status_code=404, detail="artefact_not_found")
        return
    await require_class(actor, db, artefact.plan_version_id)
