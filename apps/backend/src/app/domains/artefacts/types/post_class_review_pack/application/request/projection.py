"""Assemble fields shared by base and personalised requests."""

from typing import TypedDict

from app.domains.artefacts.core.domain.specification import ArtefactSpec, ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.shared.session_plan_view import SessionPlanView

from .artefact import revision_pack_spec
from .evidence import FigureSource, SourceEvidenceProjector
from .lesson import project_lesson_context
from .policy import build_generation_policy
from .schemas import (
    GenerationPolicyContext,
    LessonContextForGeneration,
    ObjectiveLearnerState,
    SectionGenerationUnit,
)
from .sources import LessonSources
from .units import SectionGenerationUnitProjector


class ConditionRequestFields(TypedDict):
    """Fields required by both concrete review-pack request contracts."""

    generation_policy: ReviewPackGenerationPolicy
    artefact_spec: ArtefactSpec
    policy: GenerationPolicyContext
    lesson_context: LessonContextForGeneration
    units: list[SectionGenerationUnit]


def project_condition_request_fields(
    *,
    session_plan: SessionPlanView,
    policy: ReviewPackGenerationPolicy,
    learner_states: dict[str, ObjectiveLearnerState],
    sources: LessonSources,
    figures: FigureSource = "reference",
    specification: ContentSpecification | None = None,
) -> ConditionRequestFields:
    """Assemble common fields without choosing a concrete request type."""
    policy = ReviewPackGenerationPolicy.model_validate(policy, from_attributes=True)
    units = SectionGenerationUnitProjector(
        SourceEvidenceProjector(figures=figures), sources.expert
    ).project(
        plan=session_plan,
        policy=policy,
        learner_states=learner_states,
        sources=sources,
    )
    return {
        "generation_policy": policy,
        "artefact_spec": revision_pack_spec(session_plan.grade or "", specification),
        "policy": build_generation_policy(policy),
        "lesson_context": project_lesson_context(session_plan, policy),
        "units": units,
    }
