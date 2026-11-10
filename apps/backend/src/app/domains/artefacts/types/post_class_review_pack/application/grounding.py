"""What a revision note is grounded in: the expert sources chosen, and the lesson note read.

Only an approved lesson note is read. A learner's note is grounded as the class note it
adapts was, so the two never disagree about what the lesson taught.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any, Protocol, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_note_input import (  # noqa: E501
    with_lesson_note,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


@dataclass(frozen=True)
class ApprovedLessonNote:
    """A lesson note its teacher approved, as generation reads it: markdown per plan step."""

    note_id: str
    version: int
    origin: str | None
    sections: Mapping[str, str]


class ApprovedLessonNotes(Protocol):
    """The approved lesson notes a revision note can be grounded in."""

    async def latest(self, db: AsyncSession, plan_version_id: str) -> ApprovedLessonNote | None:
        """The plan version's newest approved note."""
        ...

    async def get(self, db: AsyncSession, note_id: str) -> ApprovedLessonNote | None:
        """One approved note by its ID."""
        ...


@dataclass(frozen=True)
class Grounding:
    expert: ExpertSources
    lesson_note: ApprovedLessonNote | None

    def plan(self, session_plan: Mapping[str, Any]) -> SessionPlanView:
        """The plan as generation reads it, each step carrying its section of the lesson note."""
        if self.lesson_note is None:
            return SessionPlanView.model_validate(session_plan)
        return SessionPlanView.model_validate(
            with_lesson_note(session_plan, self.lesson_note.sections)
        )

    def sources(self, references: LessonSources) -> LessonSources:
        return replace(references, expert=self.expert)

    def refs(self) -> JsonObject:
        """What a revision note records of its grounding."""
        note = self.lesson_note
        return {
            "expert_sources": self.expert.value,
            "lesson_note": None
            if note is None
            else {"id": note.note_id, "version": note.version, "origin": note.origin},
        }


async def chosen_grounding(
    notes: ApprovedLessonNotes, db: AsyncSession, plan_version_id: str, expert: ExpertSources
) -> Grounding:
    """The grounding a teacher chose, over the lesson's newest approved note."""
    if expert is ExpertSources.TEXTBOOK:
        return Grounding(expert, None)
    return Grounding(expert, await notes.latest(db, plan_version_id))


async def recorded_grounding(
    notes: ApprovedLessonNotes, db: AsyncSession, refs: Mapping[str, object] | None
) -> Grounding | None:
    """The grounding a revision note records, or None where it records none."""
    recorded = (refs or {}).get("expert_sources")
    if not isinstance(recorded, str):
        return None
    note_ref = (refs or {}).get("lesson_note")
    note_id = (
        cast(Mapping[str, object], note_ref).get("id") if isinstance(note_ref, Mapping) else None
    )
    note = await notes.get(db, note_id) if isinstance(note_id, str) else None
    return Grounding(ExpertSources(recorded), note)


async def written_grounding(
    notes: ApprovedLessonNotes,
    db: AsyncSession,
    refs: Mapping[str, object] | None,
    plan_version_id: str,
) -> Grounding:
    """The grounding a revision note records; the newest approved note where it records none."""
    recorded = await recorded_grounding(notes, db, refs)
    return recorded or await chosen_grounding(notes, db, plan_version_id, ExpertSources.LESSON_NOTE)
