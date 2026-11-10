"""Use a lesson note that exists for another plan as the note of this plan.

The note is copied, section by section, in the order of this plan's steps. It is a new pending
note, so the teacher reads it through and approves it as any note. It can be copied only where the
plan has the same steps as the note, which is where the plan itself was reused. The note may
leave out the plan's evaluation step, which has nothing to teach.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.lesson_note.application.store import LessonNotes
from app.domains.artefacts.lesson_note.domain.note import LessonNote, NoteSection
from app.domains.content.application.errors import ContentError
from app.domains.content.application.records import ContentRecords
from app.shared.concluded import ConcludedLessonError
from app.shared.json_types import JsonObject

#: The kind of a plan step that has no teaching content, so a note may have no section for it.
EVALUATION = "evaluation"

#: What a copy keeps of the source's record of how it was made: its specification, which says
#: what the note is, and nothing about the run that wrote it.
_KEPT = ("specification",)


class NoteReuse:
    def __init__(self, notes: LessonNotes, records: ContentRecords) -> None:
        self._notes = notes
        self._records = records

    async def __call__(self, db: AsyncSession, *, source_id: str, plan_version_id: str) -> str:
        """The id of the new note, copied from the note `source_id` for the plan version."""
        source = await self._notes.get(db, source_id)
        if source is None:
            raise ContentError(404, "source_note_not_found")
        plan = await self._notes.plan(db, plan_version_id)
        if plan is None:
            raise ContentError(404, "plan_version_not_found")
        await self._refuse(db, plan_version_id)
        sections = _sections_of(source.manifest)
        missing = [
            step.step_id
            for step in plan.steps
            if step.step_id not in sections and step.step_kind != EVALUATION
        ]
        if missing:
            raise ContentError(422, f"the_note_has_no_section_for:{','.join(missing)}")
        copy = LessonNote(
            plan_version_id=plan_version_id,
            sections=[
                NoteSection(step_id=s.step_id, body=sections[s.step_id])
                for s in plan.steps
                if s.step_id in sections
            ],
        )
        refs: JsonObject = {
            key: value for key, value in (source.artefact_refs or {}).items() if key in _KEPT
        }
        stored = await self._notes.add(
            db, copy, {**refs, "origin": "reused", "reused_from": source_id}
        )
        await db.commit()
        return stored.artefact_id

    async def _refuse(self, db: AsyncSession, plan_version_id: str) -> None:
        if await self._records.concluded(db, plan_version_id):
            raise ContentError(409, ConcludedLessonError.detail)
        refusal = await self._records.plan_refusal(db, plan_version_id)
        if refusal is not None:
            raise ContentError(409, refusal)
        if await self._notes.latest(db, plan_version_id) is not None:
            raise ContentError(409, "the_plan_already_has_a_lesson_note")


def _sections_of(manifest: JsonObject) -> dict[str, str]:
    found = manifest.get("sections")
    return {
        str(section["step_id"]): str(section["body"])
        for section in (found if isinstance(found, list) else [])
        if isinstance(section, dict) and section.get("step_id") and section.get("body")
    }
