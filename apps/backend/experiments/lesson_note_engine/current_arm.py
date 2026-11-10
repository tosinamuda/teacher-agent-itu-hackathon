"""Arm A: the lesson note's own generator, one chain-of-thought call per plan step."""

from __future__ import annotations

import dspy

from app.domains.artefacts.lesson_note.application.draft import DraftLessonNote
from app.domains.artefacts.lesson_note.infrastructure.dspy.write_note_step import (
    DSPyNoteStepWriter,
)
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.generation_log.application.recorder import log_context
from app.shared.session_plan_view import SessionPlanView

LESSON_NOTE = "lesson_note"


async def current_notes(
    plan: SessionPlanView, plan_version_id: str, lm: dspy.BaseLM
) -> dict[str, str]:
    """Each step's note as markdown, by step ID."""
    with log_context(
        kind="lesson_note_comparison", arm="current", correlation_id=plan_version_id
    ):
        note = await DraftLessonNote(DSPyNoteStepWriter(lm=lm)).draft(
            plan=plan,
            plan_version_id=plan_version_id,
            specification=seed_specification(LESSON_NOTE),
        )
    return {section.step_id: section.body for section in note.sections}
