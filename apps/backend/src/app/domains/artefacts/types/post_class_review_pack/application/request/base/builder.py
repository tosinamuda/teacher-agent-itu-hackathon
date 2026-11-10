"""Build base review-pack generation requests."""

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.shared.session_plan_view import SessionPlanView

from ..evidence import FigureSource
from ..projection import project_condition_request_fields
from ..schemas import BaseReviewPackRequest
from ..sources import LessonSources


class BaseReviewPackRequestBuilder:
    """Construct a request for base review-pack generation."""

    def __init__(self, *, figures: FigureSource = "reference") -> None:
        self._figures = figures

    def build(
        self,
        *,
        session_plan: SessionPlanView,
        policy: ReviewPackGenerationPolicy,
        sources: LessonSources,
        specification: ContentSpecification | None = None,
    ) -> BaseReviewPackRequest:
        return BaseReviewPackRequest(
            **project_condition_request_fields(
                session_plan=session_plan,
                policy=policy,
                learner_states={},
                sources=sources,
                figures=self._figures,
                specification=specification,
            )
        )
