"""Revise a lesson note in place from the teacher's instruction.

The revised note goes back to pending with its version bumped, so an approval of the text
the teacher saw before this turn is refused rather than applied to text they never read.
"""

from __future__ import annotations

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.executor import RevisionExecutionOutcome
from app.domains.artefact_revision.application.highlight import format_highlight
from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.domain.specification import ArtefactSpec, ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.lesson_note.application.errors import UnreadableReplyError
from app.domains.artefacts.lesson_note.application.store import LessonNotes
from app.domains.artefacts.lesson_note.domain.note import LessonNote, NoteSection
from app.domains.artefacts.specifications.seed import seed_specification
from app.shared.json_types import JsonObject
from app.shared.readers import reader_for


class LessonNoteReviser(Protocol):
    """Applies one instruction to the whole note."""

    async def revise(
        self,
        *,
        brief: ArtefactSpec,
        current_sections: list[NoteSection],
        highlighted_section: str,
        instruction: str,
    ) -> tuple[list[NoteSection], str]: ...


class LessonNoteRevisionExecutor:
    """The revision conversation's executor for lesson notes."""

    artefact_type = ArtefactType.LESSON_NOTE.value

    def __init__(
        self,
        notes: LessonNotes,
        reviser: LessonNoteReviser,
        specifications: ContentSpecifications | None = None,
    ) -> None:
        self._notes = notes
        self._reviser = reviser
        self._specifications = specifications

    async def _specification(
        self, db: AsyncSession, refs: JsonObject | None
    ) -> ContentSpecification:
        """The revision a generated note was written against; the current one otherwise."""
        kind = ArtefactType.LESSON_NOTE.value
        recorded = (refs or {}).get("specification")
        revision = recorded.get("revision") if isinstance(recorded, dict) else None
        if self._specifications is None:
            return seed_specification(kind)
        if isinstance(revision, int):
            return await self._specifications.revision(db, kind, revision)
        return await self._specifications.current(db, kind)

    async def current_artefact(
        self, *, db: AsyncSession, subject_id: str
    ) -> tuple[str | None, JsonObject | None]:
        note = await self._notes.get(db, subject_id)
        if note is None:
            return None, None
        return note.artefact_id, note.manifest

    async def revise(
        self,
        *,
        db: AsyncSession,
        subject_id: str,
        thread_id: str,
        instruction: str,
        highlight: JsonObject | None,
        conversation_summary: str,
    ) -> RevisionExecutionOutcome:
        stored = await self._notes.get(db, subject_id)
        if stored is None:
            raise LookupError("artefact_not_found")
        note = LessonNote.model_validate(stored.manifest)
        plan = await self._notes.plan(db, note.plan_version_id)
        reader = reader_for((plan.grade if plan is not None else None) or "")
        brief = (await self._specification(db, stored.artefact_refs)).brief(reader)
        try:
            sections, change_summary = await self._reviser.revise(
                brief=brief,
                current_sections=note.sections,
                highlighted_section=format_highlight(highlight, ("step_id",)),
                instruction=instruction,
            )
        except UnreadableReplyError as error:
            raise ArtefactRevisionError(502, "the_model_reply_could_not_be_read") from error
        if [section.step_id for section in sections] != [s.step_id for s in note.sections]:
            raise ValueError("revision_changed_the_note_s_sections")
        manifest = note.model_copy(update={"sections": sections}).model_dump(mode="json")
        locked = await self._notes.get_for_update(db, stored.artefact_id)
        target = locked if locked is not None else stored
        target.manifest = manifest
        target.review_status = ArtefactReviewStatus.PENDING
        target.version = target.version + 1
        return RevisionExecutionOutcome(
            base_version_id=stored.artefact_id,
            result_version_id=stored.artefact_id,
            session_plan=manifest,
            change_summary=change_summary,
            validation_passed=True,
        )
