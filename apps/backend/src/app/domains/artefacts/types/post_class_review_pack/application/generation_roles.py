"""Product-owned roles for creating post-class review packs."""

from collections.abc import Mapping
from typing import Protocol

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.shared.session_plan_view import SessionPlanView

from ..domain.generated_review_pack import GeneratedReviewPack
from ..domain.generation_policy import ReviewPackGenerationPolicy
from ..domain.section.schemas import ReviewPackSection
from .request.schemas import ObjectiveLearnerState, SessionSignals
from .request.sources import LessonSources


class BaseReviewPackGenerator(Protocol):
    """Generate one base review pack from a lesson and product policy."""

    async def generate(
        self,
        *,
        session_plan: SessionPlanView,
        policy: ReviewPackGenerationPolicy,
        sources: LessonSources,
        specification: ContentSpecification | None = None,
    ) -> GeneratedReviewPack: ...


class ReviewPackPersonaliser(Protocol):
    """Adapt an approved base review pack for one learner."""

    async def personalise(
        self,
        *,
        session_plan: SessionPlanView,
        policy: ReviewPackGenerationPolicy,
        sources: LessonSources,
        base_sections: list[ReviewPackSection],
        learner_states: dict[str, ObjectiveLearnerState],
        base_pack_id: str,
        focal_learner_id: str,
        session_signals: SessionSignals | None,
        marked_questions: Mapping[str, int] | None = None,
        specification: ContentSpecification | None = None,
    ) -> GeneratedReviewPack: ...
