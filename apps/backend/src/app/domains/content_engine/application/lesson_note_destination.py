"""Save a finished lesson-note draft as the lesson note: one markdown section for each step."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.part_markdown import part_as_markdown
from app.domains.artefacts.core.domain.parts import PartSchema
from app.domains.artefacts.core.domain.specification import (
    ContentSpecification,
    specification_ref,
)
from app.domains.artefacts.lesson_note.application.store import LessonNotes
from app.domains.artefacts.lesson_note.domain.note import LessonNote, NoteSection
from app.domains.content_engine.application.held_checks import held_checks_record
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.shared.json_types import JsonObject
from app.shared.llm_markup import reader_ready
from app.shared.note_text import without_record_ids

HELD_CHECKS = (
    "note_substance",
    "no_second_thoughts",
    "size_rule_correct",
    "rounding_correct",
    "distinct_questions",
    "rounding_taught",
)


def _sections(draft: Draft, schema: PartSchema) -> list[NoteSection]:
    sections = [
        NoteSection(
            step_id=unit.unit_id,
            body=without_record_ids(reader_ready(part_as_markdown(part, schema.fields))),
        )
        for unit, part in draft.written()
    ]
    if any(not section.body.strip() for section in sections):
        raise DraftError("a step's note says nothing: write at least one field of it")
    return sections


class LessonNoteDestination:
    """The note is stored as every lesson note is, so what reads notes reads this one."""

    def __init__(self, notes: LessonNotes) -> None:
        self._notes = notes

    async def issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        """The note's faults are found by the plugin's own scripts."""
        return []

    def preview(self, draft: Draft) -> JsonObject:
        return {"content_type": draft.type, "sections": draft.sections()}

    async def save(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, generator: JsonObject
    ) -> str:
        if draft.plan_version_id is None or spec.parts is None:
            raise DraftError("a lesson note is made from a plan version")
        if draft.saved_as is not None:
            raise DraftError("a lesson note is revised in its chat, not drafted again")
        note = LessonNote(
            plan_version_id=draft.plan_version_id, sections=_sections(draft, spec.parts)
        )
        stored = await self._notes.add(
            db,
            note,
            {
                **specification_ref(spec),
                "origin": "generated",
                "generator": generator,
                "engine": {"draft_id": draft.draft_id},
                "review": held_checks_record(HELD_CHECKS),
            },
        )
        await db.commit()
        return stored.artefact_id
