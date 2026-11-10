"""Composition root for artefact revision.

Each executor owns a language model, so building the service builds four. That
cost is why the executors are passed in rather than defaulted: a caller that
only reads a thread never comes through here.
"""

from __future__ import annotations

from app.domains.artefact_revision.application.diagnostic_executor import (
    DiagnosticRevisionExecutor,
)
from app.domains.artefact_revision.application.executor import RevisionExecutor
from app.domains.artefact_revision.application.lesson_note_executor import (
    LessonNoteRevisionExecutor,
)
from app.domains.artefact_revision.application.review_pack_executor import (
    ReviewPackRevisionExecutor,
)
from app.domains.artefact_revision.application.service import ArtefactRevisionService
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.artefacts.core.infrastructure.specifications import (
    SqlAlchemyContentSpecifications,
)
from app.domains.artefacts.lesson_note.infrastructure.dspy.write_note_step import (
    DSPyLessonNoteReviser,
)
from app.domains.artefacts.lesson_note.infrastructure.repository import SqlAlchemyLessonNotes
from app.infra.dspy_lm import build_dspy_lm


def build_artefact_revision_service(
    fallback: RevisionExecutor | None = None, plans: RevisionExecutor | None = None
) -> ArtefactRevisionService:
    """The revision conversation: one executor per built-in type, ``fallback`` for the rest.

    The content engine revises engine content, and a lesson plan, which it drafts too. Its
    wiring passes those executors in as ``fallback`` and ``plans``, so this root builds no
    content engine of its own.
    """
    return ArtefactRevisionService(
        (
            *((plans,) if plans is not None else ()),
            ReviewPackRevisionExecutor(ArtefactRepository()),
            DiagnosticRevisionExecutor(),
            LessonNoteRevisionExecutor(
                SqlAlchemyLessonNotes(),
                DSPyLessonNoteReviser(lm=build_dspy_lm()),
                SqlAlchemyContentSpecifications(),
            ),
        ),
        fallback=fallback,
    )
