"""One generator per content type, each over the service that already generates it."""

from __future__ import annotations

from enum import Enum
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.lesson_note.application.service import LessonNoteError
from app.domains.artefacts.lesson_note.infrastructure.wiring import build_lesson_note_service
from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    StudentPackGenerationError,
)
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_student_pack_service,
)
from app.domains.assessments.application.service import (
    AssessmentApplicationError,
    AssessmentApplicationService,
)
from app.domains.assessments.infrastructure.wiring import build_diagnostic_service
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords

E = TypeVar("E", bound=Enum)


def _chosen(kind: type[E], value: str | None, default: E, name: str) -> E:
    """A revision note's choice, by its value; the default when none was made."""
    try:
        return kind(value) if value else default
    except ValueError as error:
        raise ContentError(422, f"unknown_{name}:{value}") from error


def _class_level_only(level: Level, type: BuiltIn) -> None:
    if level is not Level.CLASS:
        raise ContentError(422, f"{type.value}_is_class_level_only")


class RevisionPackGenerator:
    """The class-level pack; each learner's pack is made from their submitted work."""

    def check(self, level: Level, choices: GenerationChoices) -> None:
        self._chosen(level, choices)

    def _chosen(
        self, level: Level, choices: GenerationChoices
    ) -> tuple[ReviewPackPipeline, ExpertSources]:
        if level is not Level.CLASS:
            raise ContentError(422, "learner_packs_are_made_from_a_learners_submitted_work")
        return (
            _chosen(ReviewPackPipeline, choices.pipeline, CURRENT_PIPELINE, "pipeline"),
            _chosen(ExpertSources, choices.sources, ExpertSources.LESSON_NOTE, "sources"),
        )

    async def generate(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> str:
        pipeline, expert = self._chosen(level, choices)
        try:
            artefact = await build_student_pack_service(pipeline).ensure_base_artefact(
                db=db, plan_version_id=plan_version_id, expert=expert
            )
        except StudentPackGenerationError as error:
            raise ContentError(404, str(error)) from error
        return artefact.artefact_id


class ClassTestGenerator:
    """Writes the questions for grading and the class test's record beside them."""

    def check(self, level: Level, choices: GenerationChoices) -> None:
        _class_level_only(level, BuiltIn.CLASS_TEST)

    async def generate(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> str:
        self.check(level, choices)
        service = AssessmentApplicationService(diagnostic_service=build_diagnostic_service())
        try:
            await service.generate_diagnostic(db=db, plan_version_id=plan_version_id)
        except AssessmentApplicationError as error:
            raise ContentError(error.status_code, error.detail) from error
        records = await SqlAlchemyContentRecords().find(
            db,
            plan_version_id=plan_version_id,
            type=BuiltIn.CLASS_TEST.value,
            level=None,
            student_id=None,
        )
        return records[0].content_id


class LessonNoteGenerator:
    """Drafts the lesson note from the plan, for the teacher to check."""

    def check(self, level: Level, choices: GenerationChoices) -> None:
        _class_level_only(level, BuiltIn.LESSON_NOTE)

    async def generate(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> str:
        self.check(level, choices)
        try:
            note = await build_lesson_note_service().draft(db=db, plan_version_id=plan_version_id)
        except LessonNoteError as error:
            raise ContentError(error.status_code, error.detail) from error
        return note.artefact_id
