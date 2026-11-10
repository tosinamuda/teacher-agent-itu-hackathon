"""The lesson a draft is for: its plan version, its approved note, and whether it is closed."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.concluded_record import is_concluded
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.lesson_note.domain.note import LessonNote
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.shared.session_plan_view import SessionPlanView


class SqlAlchemyLessons:
    async def plan(self, db: AsyncSession, plan_version_id: str) -> SessionPlanView | None:
        session_plan = await db.scalar(
            select(PlanVersion.session_plan).where(PlanVersion.version_id == plan_version_id)
        )
        return SessionPlanView.model_validate(session_plan) if session_plan is not None else None

    async def approved_note_sections(
        self, db: AsyncSession, plan_version_id: str
    ) -> dict[str, str]:
        manifest = await db.scalar(
            select(Artefact.manifest)
            .where(Artefact.artefact_type == ArtefactType.LESSON_NOTE.value)
            .where(Artefact.review_status == ArtefactReviewStatus.APPROVED)
            .where(Artefact.plan_version_id == plan_version_id)
            .order_by(Artefact.reviewed_at.desc(), Artefact.id.desc())
            .limit(1)
        )
        if manifest is None:
            return {}
        note = LessonNote.model_validate(manifest)
        return {section.step_id: section.body for section in note.sections}

    async def concluded(self, db: AsyncSession, plan_version_id: str) -> bool:
        return await is_concluded(db, plan_version_id)
