"""Build the lesson note service over the live model and the database."""

from app.domains.artefacts.core.infrastructure.specifications import (
    SqlAlchemyContentSpecifications,
)
from app.domains.artefacts.lesson_note.application.draft import DraftLessonNote
from app.domains.artefacts.lesson_note.application.service import LessonNoteService
from app.domains.artefacts.lesson_note.infrastructure.dspy.write_note_step import (
    DSPyNoteStepWriter,
)
from app.domains.artefacts.lesson_note.infrastructure.repository import SqlAlchemyLessonNotes
from app.infra.dspy_lm import build_dspy_lm


def build_lesson_note_service() -> LessonNoteService:
    """The lesson note service, drafting over the configured language model."""
    return LessonNoteService(
        SqlAlchemyLessonNotes(),
        DraftLessonNote(DSPyNoteStepWriter(lm=build_dspy_lm())),
        SqlAlchemyContentSpecifications(),
    )
