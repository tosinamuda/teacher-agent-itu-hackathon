"""Composition root for class-test generation."""

from app.domains.artefacts.core.infrastructure.specifications import (
    SqlAlchemyContentSpecifications,
)
from app.domains.assessments.application.diagnostic_service import DiagnosticGenerationService
from app.domains.assessments.application.item_reader import DspyItemReader
from app.domains.assessments.infrastructure.lesson_notes import ApprovedLessonNoteText
from app.domains.assessments.infrastructure.repository import ClassTestMaterials


def build_diagnostic_service() -> DiagnosticGenerationService:
    """The class-test generator, reading the class test's stored specification.

    Every item is answered by a second reader against the lesson before it is kept.
    """
    return DiagnosticGenerationService(
        specifications=SqlAlchemyContentSpecifications(),
        materials=ClassTestMaterials(),
        reader=DspyItemReader(),
        lesson_notes=ApprovedLessonNoteText(),
    )
