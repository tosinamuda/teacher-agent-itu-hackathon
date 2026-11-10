"""What a learner's revision note is adapted to: their state per objective, from their evidence."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    StudentPackGenerationError,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_state_input import (
    to_session_signals,
    to_spec_objective_state,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    SessionSignals,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.learner_state.application.service import LearnerStateService
from app.domains.learners.models import LearnerProfile


@dataclass(frozen=True)
class LearnerInputs:
    states: dict[str, ObjectiveLearnerState]
    signals: SessionSignals | None
    #: The learner's band per objective (remediate / reinforce / extend).
    bands: dict[str, str]
    #: How many of the learner's questions were marked for each objective.
    marked_questions: dict[str, int]


async def learner_inputs(
    db: AsyncSession, learner_states: LearnerStateService, *, student_id: str, plan_version_id: str
) -> LearnerInputs:
    """The learner's state from their newest exit-assessment submission for the lesson."""
    profile = (
        (await db.execute(select(LearnerProfile).where(LearnerProfile.student_id == student_id)))
        .scalars()
        .first()
    )
    if profile is None:
        raise StudentPackGenerationError("student_not_found")
    submission = (
        (
            await db.execute(
                select(ExitTicketSubmission)
                .where(ExitTicketSubmission.student_id == student_id)
                .where(ExitTicketSubmission.plan_version_id == plan_version_id)
                .order_by(ExitTicketSubmission.created_at.desc())
            )
        )
        .scalars()
        .first()
    )
    if submission is None:
        raise StudentPackGenerationError("diagnostic_not_found")
    state = learner_states.build(
        student_id=student_id,
        student_profile=profile,
        diagnostic_id=submission.diagnostic_id,
        diagnostic_results=submission.results,
    )
    objectives = state.objective_states
    return LearnerInputs(
        states={item.lesson_objective_id: to_spec_objective_state(item) for item in objectives},
        signals=to_session_signals(state),
        bands={item.lesson_objective_id: item.band for item in objectives},
        marked_questions={
            item.lesson_objective_id: item.questions_total or 0 for item in objectives
        },
    )
