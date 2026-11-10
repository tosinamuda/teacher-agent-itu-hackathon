"""Approved lesson notes, read from the artefacts table for generation."""

from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.lesson_note.domain.note import LessonNote
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    ApprovedLessonNote,
)


def _approved() -> Select[tuple[Artefact]]:
    return (
        select(Artefact)
        .where(Artefact.artefact_type == ArtefactType.LESSON_NOTE.value)
        .where(Artefact.review_status == ArtefactReviewStatus.APPROVED)
    )


def _as_read(artefact: Artefact | None) -> ApprovedLessonNote | None:
    if artefact is None:
        return None
    note = LessonNote.model_validate(artefact.manifest)
    origin = (artefact.artefact_refs or {}).get("origin")
    return ApprovedLessonNote(
        note_id=artefact.artefact_id,
        version=artefact.version,
        origin=origin if isinstance(origin, str) else None,
        sections={section.step_id: section.body for section in note.sections},
    )


class SqlAlchemyApprovedLessonNotes:
    async def latest(self, db: AsyncSession, plan_version_id: str) -> ApprovedLessonNote | None:
        query = (
            _approved()
            .where(Artefact.plan_version_id == plan_version_id)
            .order_by(Artefact.reviewed_at.desc(), Artefact.id.desc())
            .limit(1)
        )
        return _as_read((await db.execute(query)).scalar_one_or_none())

    async def get(self, db: AsyncSession, note_id: str) -> ApprovedLessonNote | None:
        query = _approved().where(Artefact.artefact_id == note_id)
        return _as_read((await db.execute(query)).scalar_one_or_none())
