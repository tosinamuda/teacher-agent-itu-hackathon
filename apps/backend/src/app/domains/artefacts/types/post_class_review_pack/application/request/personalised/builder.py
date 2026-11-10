"""Build learner-scoped review-pack requests."""

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.shared.session_plan_view import SessionPlanView

from ..evidence import FigureSource
from ..projection import project_condition_request_fields
from ..schemas import (
    ObjectiveLearnerState,
    PersonalisedReviewPackRequest,
    SessionSignals,
)
from ..sources import LessonSources


class PersonalisedReviewPackRequestBuilder:
    """Construct a request for learner personalisation or base reuse."""

    def __init__(self, *, figures: FigureSource = "reference") -> None:
        self._figures = figures

    def build(
        self,
        *,
        session_plan: SessionPlanView,
        base_pack_id: str,
        focal_learner_id: str,
        learner_states: dict[str, ObjectiveLearnerState],
        policy: ReviewPackGenerationPolicy,
        session_signals: SessionSignals | None = None,
        sources: LessonSources,
        specification: ContentSpecification | None = None,
    ) -> PersonalisedReviewPackRequest:
        return PersonalisedReviewPackRequest(
            **project_condition_request_fields(
                session_plan=session_plan,
                policy=policy,
                learner_states=learner_states,
                sources=sources,
                figures=self._figures,
                specification=specification,
            ),
            base_pack_id=base_pack_id,
            focal_learner_id=focal_learner_id,
            session_signals=session_signals,
        )
