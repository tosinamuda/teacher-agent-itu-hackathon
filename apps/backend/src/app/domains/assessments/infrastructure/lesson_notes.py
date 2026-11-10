"""The lesson's approved note, as the text a class-test reader checks items against."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.lesson_note.domain.note import LessonNote


class ApprovedLessonNoteText:
    async def text(self, db: AsyncSession, plan_version_id: str) -> str | None:
        artefact = (
            await db.execute(
                select(Artefact)
                .where(Artefact.artefact_type == ArtefactType.LESSON_NOTE.value)
                .where(Artefact.review_status == ArtefactReviewStatus.APPROVED)
                .where(Artefact.plan_version_id == plan_version_id)
                .order_by(Artefact.reviewed_at.desc(), Artefact.id.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        if artefact is None:
            return None
        note = LessonNote.model_validate(artefact.manifest)
        return "\n\n".join(section.body for section in note.sections) or None
