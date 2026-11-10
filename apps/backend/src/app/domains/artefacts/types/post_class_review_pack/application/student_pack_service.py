"""Per-student review-pack generation.

When a student submits their exit assessment, the system auto-generates their
personalised pack via the product generation pipeline: ensure the approved base
exists for the lesson (generate once, cached as a class-level artefact), then
personalise it from the student's objective-indexed learner state. The result
is a learner-level artefact with review_status="pending" — a teacher must review
and approve it before the student sees it. Students never trigger this.
"""

from __future__ import annotations

from typing import TypedDict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.domain.made_from import MADE_FROM, made_from
from app.domains.artefacts.core.domain.specification import (
    ContentSpecification,
    specification_ref,
)
from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import get_plan_row
from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    StudentPackGenerationError,
)
from app.domains.artefacts.types.post_class_review_pack.application.generation_roles import (
    BaseReviewPackGenerator,
    ReviewPackPersonaliser,
)
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    ApprovedLessonNotes,
    Grounding,
    chosen_grounding,
    written_grounding,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_inputs import (
    learner_inputs,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_names import (
    learner_names,
)
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
)
from app.domains.artefacts.types.post_class_review_pack.application.pack_inputs import (
    PackInputs,
    base_pack_id,
    materialise_pack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.review_record import (
    review_record,
)
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    BASE_REVIEW_PACK_POLICY,
    PERSONALISED_REVIEW_PACK_POLICY,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_approved_class_pack,
    the_lessons_class_pack,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.generation_log.application.recorder import log_context
from app.domains.learner_state.application.service import LearnerStateService
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


class MissingPackStudent(TypedDict):
    student_id: str
    full_name: str


class StudentPackGenerationService:
    """Generates one student's pending personalised pack from their diagnostic."""

    def __init__(
        self,
        base_generator: BaseReviewPackGenerator,
        learner_personaliser: ReviewPackPersonaliser,
        lesson_notes: ApprovedLessonNotes,
        learner_state_service: LearnerStateService | None = None,
        specifications: ContentSpecifications | None = None,
        pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
    ) -> None:
        self.base_generator = base_generator
        self.learner_personaliser = learner_personaliser
        self.lesson_notes = lesson_notes
        self.learner_state_service = learner_state_service or LearnerStateService()
        self.specifications = specifications
        self.pipeline = pipeline
        self._inputs = PackInputs(lesson_notes, specifications)

    def _provenance(self, specification: ContentSpecification, grounding: Grounding) -> JsonObject:
        """What a pack records: its specification revision, pipeline, and grounding."""
        return {
            **specification_ref(specification),
            "pipeline": self.pipeline.value,
            **grounding.refs(),
        }

    def _learner_refs(
        self,
        specification: ContentSpecification,
        grounding: Grounding,
        generated: GeneratedReviewPack,
        class_pack: Artefact,
    ) -> JsonObject:
        """What a learner's note records, including the class note version it was made from."""
        return {
            **self._recorded(specification, grounding, generated),
            MADE_FROM: made_from(class_pack.artefact_id, class_pack.version),
        }

    def _recorded(
        self,
        specification: ContentSpecification,
        grounding: Grounding,
        generated: GeneratedReviewPack,
    ) -> JsonObject:
        """What a pack records, and the checks it passed and the passages it was given."""
        return {
            **self._provenance(specification, grounding),
            "review": review_record(generated.validation, generated.request),
        }

    async def _approved_class_pack(self, db: AsyncSession, plan_version_id: str) -> Artefact:
        """The class pack a learner's pack adapts; a pending one is never read."""
        class_pack = await the_lessons_approved_class_pack(db, plan_version_id)
        if class_pack is None:
            raise StudentPackGenerationError("class_pack_not_approved")
        return class_pack

    async def _learner_grounding(self, db: AsyncSession, class_pack: Artefact) -> Grounding:
        """A learner's note is grounded as the class note it adapts; else by the study's rule."""
        return await written_grounding(
            self.lesson_notes, db, class_pack.artefact_refs, class_pack.plan_version_id
        )

    async def generate_for_student(
        self, *, db: AsyncSession, student_id: str, plan_version_id: str
    ) -> Artefact:
        row = await get_plan_row(db, plan_or_version_id=plan_version_id)
        if row is None:
            raise StudentPackGenerationError("plan_version_not_found")
        plan_version, _plan = row
        class_pack = await self._approved_class_pack(db, plan_version_id)
        grounding = await self._learner_grounding(db, class_pack)
        session_plan, sources = await self._inputs.lesson_inputs(db, plan_version, grounding)
        learner = await learner_inputs(
            db, self.learner_state_service, student_id=student_id, plan_version_id=plan_version_id
        )
        specification = await self._inputs.specification(db)
        with log_context(
            kind="student_pack",
            correlation_id=f"{plan_version_id}:{student_id}",
            plan_version_id=plan_version_id,
            student_id=student_id,
        ):
            result = await self.learner_personaliser.personalise(
                session_plan=session_plan,
                base_sections=review_pack_manifest_to_sections(
                    PostClassReviewPack.model_validate(class_pack.manifest)
                ),
                learner_states=learner.states,
                marked_questions=learner.marked_questions,
                base_pack_id=base_pack_id(plan_version_id),
                focal_learner_id=student_id,
                policy=PERSONALISED_REVIEW_PACK_POLICY,
                session_signals=learner.signals,
                sources=sources,
                specification=specification,
            )

        artefact = materialise_pack(
            db=db,
            sections=result.sections,
            lesson_context=result.request.lesson_context,
            plan_version_id=plan_version_id,
            scope=ArtefactScope.LEARNER_LEVEL,
            student_id=student_id,
            review_status=ArtefactReviewStatus.PENDING,
            artefact_refs=self._learner_refs(specification, grounding, result, class_pack),
            # So the student's revision note can explain how it was pitched.
            personalisation_bands=learner.bands,
        )
        await db.commit()
        await db.refresh(artefact)
        return artefact

    async def _generate_base_artefact(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        session_plan: SessionPlanView,
        sources: LessonSources,
        grounding: Grounding,
    ) -> tuple[Artefact, list[ReviewPackSection]]:
        specification = await self._inputs.specification(db)
        base = await self.base_generator.generate(
            session_plan=session_plan,
            policy=BASE_REVIEW_PACK_POLICY,
            sources=sources,
            specification=specification,
        )
        # A new base lands as "pending": the teacher revises and approves it before any
        # learner's pack is made from it.
        artefact = materialise_pack(
            db=db,
            sections=base.sections,
            lesson_context=base.request.lesson_context,
            plan_version_id=plan_version_id,
            scope=ArtefactScope.CLASS_LEVEL,
            student_id=None,
            review_status=ArtefactReviewStatus.PENDING,
            artefact_refs=self._recorded(specification, grounding, base),
        )
        return artefact, base.sections

    async def ensure_base_artefact(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        expert: ExpertSources = ExpertSources.LESSON_NOTE,
    ) -> Artefact:
        """The lesson's class pack, generated pending from the chosen sources if it has none.

        Backs the teacher base-review screen.
        """
        existing = await the_lessons_class_pack(db, plan_version_id)
        if existing is not None:
            return existing
        row = await get_plan_row(db, plan_or_version_id=plan_version_id)
        if row is None:
            raise StudentPackGenerationError("plan_version_not_found")
        plan_version, _plan = row
        await self._inputs.lock_plan_version(db, plan_version_id)
        # Re-check under the lock with a CURRENT (locking) read: a snapshot read would
        # miss a rival's just-committed base and duplicate it (REPEATABLE READ).
        existing = await the_lessons_class_pack(db, plan_version_id, lock=True)
        if existing is not None:
            return existing
        grounding = await chosen_grounding(self.lesson_notes, db, plan_version_id, expert)
        session_plan, sources = await self._inputs.lesson_inputs(db, plan_version, grounding)
        with log_context(
            kind="study_pack_base",
            correlation_id=plan_version_id,
            plan_version_id=plan_version_id,
        ):
            artefact, _sections = await self._generate_base_artefact(
                db=db,
                plan_version_id=plan_version_id,
                session_plan=session_plan,
                sources=sources,
                grounding=grounding,
            )
        await db.commit()
        await db.refresh(artefact)
        return artefact

    async def list_students_missing_pack(
        self, *, db: AsyncSession, plan_version_id: str
    ) -> list[MissingPackStudent]:
        """Students who submitted the exit assessment for this lesson but have no.

        learner-level pack yet (generation pending or failed). Drives the teacher's
        per-student 'regenerate' action — the pack is produced by the same worker.
        """
        submitters = set(
            (
                await db.execute(
                    select(ExitTicketSubmission.student_id).where(
                        ExitTicketSubmission.plan_version_id == plan_version_id
                    )
                )
            )
            .scalars()
            .all()
        )
        have_pack = set(
            (
                await db.execute(
                    select(Artefact.student_id).where(
                        Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value,
                        Artefact.scope == ArtefactScope.LEARNER_LEVEL.value,
                        Artefact.plan_version_id == plan_version_id,
                        Artefact.student_id.isnot(None),
                    )
                )
            )
            .scalars()
            .all()
        )
        missing = sorted(submitters - have_pack)
        if not missing:
            return []
        names = await learner_names(db, missing)
        return [MissingPackStudent(student_id=sid, full_name=names[sid]) for sid in missing]
