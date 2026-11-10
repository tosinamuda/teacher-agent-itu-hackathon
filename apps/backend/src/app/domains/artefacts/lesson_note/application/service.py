"""Draft a lesson note for a plan version and keep it pending until the teacher approves it."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.domain.specification import (
    ContentSpecification,
    specification_ref,
)
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.lesson_note.application.draft import DraftLessonNote
from app.domains.artefacts.lesson_note.application.store import LessonNotes, StoredLessonNote
from app.domains.artefacts.specifications.seed import seed_specification


@dataclass
class LessonNoteError(Exception):
    status_code: int
    detail: str


class LessonNoteService:
    """Draft and read lesson notes. Approval is the core artefact gate's."""

    def __init__(
        self,
        notes: LessonNotes,
        drafter: DraftLessonNote,
        specifications: ContentSpecifications | None = None,
    ) -> None:
        self._notes = notes
        self._drafter = drafter
        self._specifications = specifications

    async def _specification(self, db: AsyncSession) -> ContentSpecification:
        """The note's current stored specification; the seed when none is wired."""
        if self._specifications is None:
            return seed_specification(ArtefactType.LESSON_NOTE.value)
        return await self._specifications.current(db, ArtefactType.LESSON_NOTE.value)

    async def draft(self, *, db: AsyncSession, plan_version_id: str) -> StoredLessonNote:
        """Draft a note from the plan and store it pending. The model runs with no write open."""
        plan = await self._notes.plan(db, plan_version_id)
        if plan is None:
            raise LessonNoteError(404, "plan_version_not_found")
        specification = await self._specification(db)
        try:
            note = await self._drafter.draft(
                plan=plan, plan_version_id=plan_version_id, specification=specification
            )
        except ValueError as error:
            raise LessonNoteError(422, str(error)) from error
        stored = await self._notes.add(
            db, note, {"origin": "generated", **specification_ref(specification)}
        )
        await db.commit()
        return stored

    async def latest(self, *, db: AsyncSession, plan_version_id: str) -> StoredLessonNote | None:
        return await self._notes.latest(db, plan_version_id)

    async def get(self, *, db: AsyncSession, artefact_id: str) -> StoredLessonNote:
        note = await self._notes.get(db, artefact_id)
        if note is None:
            raise LessonNoteError(404, "lesson_note_not_found")
        return note
