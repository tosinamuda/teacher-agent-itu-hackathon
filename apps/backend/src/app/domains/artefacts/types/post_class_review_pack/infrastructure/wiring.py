"""Composition root for the review-pack surface.

Generation opens a language model, so the pack service is built only where one
is actually wanted — never as a constructor default on a use case that might
only be listing rows.
"""

from __future__ import annotations

from app.domains.artefacts.core.infrastructure.specifications import (
    SqlAlchemyContentSpecifications,
)
from app.domains.artefacts.core.infrastructure.wiring import build_lifecycle_manager
from app.domains.artefacts.types.post_class_review_pack.application.engine_base_pack import (
    EngineBasePack,
)
from app.domains.artefacts.types.post_class_review_pack.application.engine_learner_pack import (
    EngineLearnerPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.generation_job_service import (
    StudentPackGenerationJobService,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_pack_gate import (
    LearnerPackGate,
)
from app.domains.artefacts.types.post_class_review_pack.application.pack_inputs import PackInputs
from app.domains.artefacts.types.post_class_review_pack.application.review_pack_workflow_service import (  # noqa: E501
    ReviewPackWorkflowService,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.revised_pack_checks import (  # noqa: E501
    RevisedPackChecks,
)
from app.domains.artefacts.types.post_class_review_pack.application.student_pack_service import (
    StudentPackGenerationService,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
    build_review_pack_personaliser,
    class_note_requests,
    live_finalise,
    live_section_collaborators,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.learner_pack_readiness import (  # noqa: E501
    SqlAlchemyLearnerPackReadiness,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_notes import (
    SqlAlchemyApprovedLessonNotes,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.repository import (
    StudentPackGenerationRepository,
)


def build_generation_job_service() -> StudentPackGenerationJobService:
    """The queue behind per-student pack generation."""
    return StudentPackGenerationJobService(StudentPackGenerationRepository())


def build_learner_pack_gate() -> LearnerPackGate:
    """The one way a learner's pack is queued: class pack approved and evidence in."""
    return LearnerPackGate(SqlAlchemyLearnerPackReadiness(), build_generation_job_service())


def build_student_pack_service(
    pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
) -> StudentPackGenerationService:
    """Generation itself, on one pipeline version — constructing this opens a language model."""
    collaborators = live_section_collaborators(pipeline)
    return StudentPackGenerationService(
        base_generator=build_base_review_pack_generator(collaborators),
        learner_personaliser=build_review_pack_personaliser(collaborators),
        lesson_notes=SqlAlchemyApprovedLessonNotes(),
        specifications=SqlAlchemyContentSpecifications(),
        pipeline=pipeline,
    )


def build_engine_base_pack() -> EngineBasePack:
    """Stores the class pack the engine wrote. It opens no language model."""
    return EngineBasePack(
        PackInputs(SqlAlchemyApprovedLessonNotes(), SqlAlchemyContentSpecifications())
    )


def build_engine_learner_pack() -> EngineLearnerPack:
    """Stores the learner's note the engine wrote. It opens no language model."""
    return EngineLearnerPack(
        PackInputs(SqlAlchemyApprovedLessonNotes(), SqlAlchemyContentSpecifications())
    )


def build_revised_pack_checks() -> RevisedPackChecks:
    """The checks a teacher's revision is put through; constructing this opens no model."""
    return RevisedPackChecks(
        inputs=PackInputs(SqlAlchemyApprovedLessonNotes(), SqlAlchemyContentSpecifications()),
        finalise_for=live_finalise,
        class_requests=class_note_requests(),
    )


def build_review_pack_workflow() -> ReviewPackWorkflowService:
    """The learner-pack visibility policy and the regenerate workflow."""
    return ReviewPackWorkflowService(
        build_lifecycle_manager(),
        build_student_pack_service(),
        build_learner_pack_gate(),
    )
