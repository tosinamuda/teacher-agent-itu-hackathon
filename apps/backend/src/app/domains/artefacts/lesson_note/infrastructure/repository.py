"""Lesson notes in the artefacts table, and the plan versions they are written for."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.lesson_note.domain.note import LessonNote
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView

_KIND = ArtefactType.LESSON_NOTE.value


class SqlAlchemyLessonNotes:
    """Stores each note as a class-level artefact, pending the teacher's review."""

    async def plan(self, db: AsyncSession, plan_version_id: str) -> SessionPlanView | None:
        session_plan = (
            await db.execute(
                select(PlanVersion.session_plan).where(PlanVersion.version_id == plan_version_id)
            )
        ).scalar_one_or_none()
        if session_plan is None:
            return None
        return SessionPlanView.model_validate(session_plan)

    async def add(self, db: AsyncSession, note: LessonNote, artefact_refs: JsonObject) -> Artefact:
        artefact = Artefact(
            artefact_id=new_public_id(PublicIdPrefix.ARTEFACT),
            artefact_type=_KIND,
            scope=ArtefactScope.CLASS_LEVEL.value,
            plan_version_id=note.plan_version_id,
            manifest=note.model_dump(mode="json"),
            artefact_refs=artefact_refs,
            review_status=ArtefactReviewStatus.PENDING,
        )
        db.add(artefact)
        await db.flush()
        return artefact

    async def latest(self, db: AsyncSession, plan_version_id: str) -> Artefact | None:
        return (
            await db.execute(
                select(Artefact)
                .where(Artefact.artefact_type == _KIND)
                .where(Artefact.plan_version_id == plan_version_id)
                .order_by(Artefact.created_at.desc(), Artefact.id.desc())
                .limit(1)
            )
        ).scalar_one_or_none()

    async def get(self, db: AsyncSession, artefact_id: str) -> Artefact | None:
        return (
            await db.execute(
                select(Artefact)
                .where(Artefact.artefact_id == artefact_id)
                .where(Artefact.artefact_type == _KIND)
            )
        ).scalar_one_or_none()

    async def get_for_update(self, db: AsyncSession, artefact_id: str) -> Artefact | None:
        return (
            await db.execute(
                select(Artefact)
                .where(Artefact.artefact_id == artefact_id)
                .where(Artefact.artefact_type == _KIND)
                .with_for_update()
                .execution_options(populate_existing=True)
            )
        ).scalar_one_or_none()
