"""The teacher's arm: the teacher's own approved lesson note, the benchmark for both generators."""

from __future__ import annotations

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.lesson_note.domain.note import LessonNote

#: Where a note the teacher wrote is recorded as coming from.
TEACHER_ORIGINS = ("teacher", "study_record")


async def teacher_notes(plan_version_id: str) -> dict[str, str]:
    """Each step's section of the teacher's approved note, by step ID; empty when there is none."""
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                select(Artefact.manifest, Artefact.artefact_refs)
                .where(Artefact.artefact_type == ArtefactType.LESSON_NOTE.value)
                .where(Artefact.review_status == ArtefactReviewStatus.APPROVED)
                .where(Artefact.plan_version_id == plan_version_id)
            )
        ).all()
    for manifest, refs in rows:
        if (refs or {}).get("origin") in TEACHER_ORIGINS:
            note = LessonNote.model_validate(manifest)
            return {section.step_id: section.body for section in note.sections}
    return {}
