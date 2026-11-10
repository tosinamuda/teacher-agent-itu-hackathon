"""Generate, read, revise and approve content of every type through one interface."""

from __future__ import annotations

from collections.abc import Mapping

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.service import ChatRecord, RevisionRecord
from app.domains.artefacts.core.application.ports import Approval
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content.application.errors import ContentError, NoGeneratorError
from app.domains.content.application.generation import ContentGenerator, GenerationChoices
from app.domains.content.application.kinds import ContentKind
from app.domains.content.application.records import ContentItem, ContentRecord, ContentRecords
from app.domains.content.application.review import Revisions
from app.domains.content.domain.generators import (
    GeneratorBinding,
    GeneratorKind,
)
from app.domains.content.domain.types import BuiltIn, ContentTypeDefinition, Engine, Level
from app.shared.concluded import ConcludedLessonError
from app.shared.json_types import JsonObject


class ContentService:
    """One interface over every content type; each type's handler does what differs.

    A built-in type has handlers of its own. Every engine type shares ``engine_kind`` and
    ``engine_generator``, so registering one needs no code.
    """

    def __init__(
        self,
        *,
        catalogue: ContentCatalogue,
        records: ContentRecords,
        kinds: Mapping[str, ContentKind],
        generators: Mapping[str, ContentGenerator],
        engine_kind: ContentKind,
        engine_generator: ContentGenerator,
        revisions: Revisions,
    ) -> None:
        self._catalogue = catalogue
        self._records = records
        self._kinds = kinds
        self._generators = generators
        self._engine_kind = engine_kind
        self._engine_generator = engine_generator
        self._revisions = revisions

    def _kind(self, record: ContentRecord) -> ContentKind:
        return self._kinds.get(record.type, self._engine_kind)

    def _generator(
        self, definition: ContentTypeDefinition, binding: GeneratorBinding
    ) -> ContentGenerator | None:
        """The engine builds what its generator is, and any engine type; else the type's own."""
        if definition.engine is Engine.MCP or binding.harness is GeneratorKind.ENGINE:
            return self._engine_generator
        return self._generators.get(definition.slug)

    async def _refuse_if_concluded(self, db: AsyncSession, plan_version_id: str) -> None:
        if await self._records.concluded(db, plan_version_id):
            raise ContentError(409, ConcludedLessonError.detail)

    async def _refuse_a_plan_that_is_not_current(
        self, db: AsyncSession, plan_version_id: str
    ) -> None:
        refusal = await self._records.plan_refusal(db, plan_version_id)
        if refusal is not None:
            raise ContentError(409, refusal)

    async def _refuse_a_second_class_pack(
        self, db: AsyncSession, plan_version_id: str, type: ContentTypeDefinition, level: Level
    ) -> None:
        if not type.is_(BuiltIn.REVISION_NOTE) or level is not Level.CLASS:
            return
        if await self._records.class_pack_awaits_its_experiment(db, plan_version_id):
            raise ContentError(409, "class_revision_note_is_made_by_the_lessons_experiment")

    async def _refuse_a_second_class_note_from_the_engine(
        self,
        db: AsyncSession,
        plan_version_id: str,
        type: ContentTypeDefinition,
        level: Level,
        binding: GeneratorBinding,
    ) -> None:
        """The engine stores one class revision note a lesson, so it says so before it writes."""
        if (
            type.is_(BuiltIn.REVISION_NOTE)
            and level is Level.CLASS
            and binding.harness is GeneratorKind.ENGINE
            and await self._records.has_class_revision_note(db, plan_version_id)
        ):
            raise ContentError(409, "lesson_already_has_a_class_revision_note")

    async def _refuse_a_class_test_students_have_answered(
        self, db: AsyncSession, plan_version_id: str, type: ContentTypeDefinition
    ) -> None:
        """A class test that students have answered is the record of what they were asked."""
        if type.is_(BuiltIn.CLASS_TEST) and await self._records.class_test_answered(
            db, plan_version_id
        ):
            raise ContentError(409, "class_test_has_student_answers")

    async def find_record(self, db: AsyncSession, content_id: str) -> ContentRecord | None:
        """The content's record, or none where the id is not content, such as a lesson plan."""
        return await self._records.get(db, content_id)

    async def record(self, db: AsyncSession, content_id: str) -> ContentRecord:
        found = await self.find_record(db, content_id)
        if found is None:
            raise ContentError(404, "content_not_found")
        return found

    async def get(self, db: AsyncSession, content_id: str) -> ContentItem:
        record = await self.record(db, content_id)
        return ContentItem(record=record, content=await self._kind(record).body(db, record))

    async def find(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str | None = None,
        type: str | None = None,
        level: Level | None = None,
        student_id: str | None = None,
    ) -> list[ContentRecord]:
        return await self._records.find(
            db, plan_version_id=plan_version_id, type=type, level=level, student_id=student_id
        )

    async def generate(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> ContentItem:
        generator, binding = await self._generator_for(
            db, plan_version_id=plan_version_id, type=type, level=level, choices=choices
        )
        content_id = await generator.generate(
            db,
            plan_version_id=plan_version_id,
            type=type,
            level=level,
            choices=choices,
        )
        await self._records.record_generator(db, content_id, binding.provenance())
        return await self.get(db, content_id)

    async def check_generation(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> None:
        """Refuse now what generation would refuse before its first model call."""
        await self._generator_for(
            db, plan_version_id=plan_version_id, type=type, level=level, choices=choices
        )

    def _refuse_what_the_type_never_makes(
        self, definition: ContentTypeDefinition, level: Level, choices: GenerationChoices
    ) -> None:
        """Say what the type's own generator says about a level it has no generator for."""
        native = self._generators.get(definition.slug)
        if native is not None:
            native.check(level, choices)

    async def _generator_for(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> tuple[ContentGenerator, GeneratorBinding]:
        definition = await self._catalogue.type(db, type)
        if choices.sources and not definition.is_(BuiltIn.REVISION_NOTE):
            raise ContentError(422, "sources_apply_to_the_revision_note_only")
        await self._refuse_if_concluded(db, plan_version_id)
        await self._refuse_a_second_class_pack(db, plan_version_id, definition, level)
        await self._refuse_a_class_test_students_have_answered(db, plan_version_id, definition)
        try:
            binding = await self._catalogue.generator(db, definition, level, choices.pipeline)
        except NoGeneratorError:
            self._refuse_what_the_type_never_makes(definition, level, choices)
            raise
        if choices.instructions and binding.harness is not GeneratorKind.ENGINE:
            raise ContentError(422, "instructions_apply_to_engine_types_only")
        if (
            choices.sources not in (None, ExpertSources.LESSON_NOTE.value)
            and binding.harness is GeneratorKind.ENGINE
        ):
            # An engine writer grounds a revision note in the lesson note, which is the default.
            raise ContentError(422, "sources_apply_to_the_pipeline_only")
        await self._refuse_a_second_class_note_from_the_engine(
            db, plan_version_id, definition, level, binding
        )
        generator = self._generator(definition, binding)
        if generator is None or not definition.made_from_a_plan_version:
            raise ContentError(422, f"{definition.slug}_is_not_generated_from_a_plan_version")
        await self._refuse_a_plan_that_is_not_current(db, plan_version_id)
        generator.check(level, choices)
        return generator, binding

    async def approve(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        expected_version: int | None,
        approved_by: str,
    ) -> ContentItem:
        record = await self.record(db, content_id)
        await self._refuse_if_concluded(db, record.plan_version_id)
        await self._kind(record).approve(
            db, record, expected_version=expected_version, approved_by=approved_by
        )
        return await self.get(db, content_id)

    async def reject(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        expected_version: int | None,
        rejected_by: str,
        reason: str,
    ) -> ContentItem:
        """Reject a pending version, or withdraw an approved one, and say why."""
        record = await self.record(db, content_id)
        await self._refuse_if_concluded(db, record.plan_version_id)
        await self._kind(record).reject(
            db,
            record,
            expected_version=expected_version,
            rejected_by=rejected_by,
            reason=reason,
        )
        return await self.get(db, content_id)

    async def approvals(self, db: AsyncSession, content_id: str) -> list[Approval]:
        record = await self.record(db, content_id)
        return await self._kind(record).approvals(db, record)

    async def revise(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        feedback: str,
        requested_by: str | None,
        highlight: JsonObject | None = None,
        chat_id: str | None = None,
    ) -> RevisionRecord:
        record = await self.record(db, content_id)
        await self._refuse_if_concluded(db, record.plan_version_id)
        kind = self._kind(record)
        kind.refuse_revision(record)
        revision = await self._revisions.revise(
            db,
            stored_type=record.kind,
            subject_id=kind.revision_subject(record),
            feedback=feedback,
            requested_by=requested_by,
            highlight=highlight,
            chat_id=chat_id,
        )
        await kind.revised(db, record)
        return revision

    async def chats(self, db: AsyncSession, content_id: str) -> list[ChatRecord]:
        record = await self.record(db, content_id)
        return await self._revisions.chats(
            db, stored_type=record.kind, subject_id=self._kind(record).revision_subject(record)
        )

    async def new_chat(
        self, db: AsyncSession, *, content_id: str, requested_by: str | None, title: str | None
    ) -> ChatRecord:
        record = await self.record(db, content_id)
        await self._refuse_if_concluded(db, record.plan_version_id)
        kind = self._kind(record)
        kind.refuse_revision(record)
        return await self._revisions.new_chat(
            db,
            stored_type=record.kind,
            subject_id=kind.revision_subject(record),
            requested_by=requested_by,
            title=title,
        )

    async def chat(self, db: AsyncSession, content_id: str, chat_id: str) -> ChatRecord:
        record = await self.record(db, content_id)
        return await self._revisions.chat(
            db,
            stored_type=record.kind,
            subject_id=self._kind(record).revision_subject(record),
            chat_id=chat_id,
        )

    async def revisions(self, db: AsyncSession, content_id: str) -> list[RevisionRecord]:
        record = await self.record(db, content_id)
        return await self._revisions.history(
            db,
            stored_type=record.kind,
            subject_id=self._kind(record).revision_subject(record),
        )
