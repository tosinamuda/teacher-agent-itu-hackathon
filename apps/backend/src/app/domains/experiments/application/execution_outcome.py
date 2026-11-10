"""Decide what an execution row ends as, given what its workflow returned."""

from dataclasses import dataclass

from app.domains.experiments.application.execution_errors import classify_execution_error
from app.domains.experiments.domain.types import ExecutionErrorCategory, ExecutionStatus
from app.domains.experiments.review_pack_study.h1.outcomes import (
    AllConditionsGenerated,
    H1Verdict,
    SomeConditionsFailed,
)
from app.domains.experiments.review_pack_study.h2.outcomes import (
    AllLearnersPersonalised,
    H2Verdict,
    SomeLearnersFailed,
)

ExperimentOutcome = H1Verdict | H2Verdict

_CANCELLED = "execution cancelled before it finished"


@dataclass(frozen=True)
class CompletionStatus:
    """The fields a finished execution is stored with, and the line it reports."""

    status: ExecutionStatus
    summary: str
    error: str | None = None
    error_category: ExecutionErrorCategory | None = None


def completion_status_for(outcome: ExperimentOutcome) -> CompletionStatus:
    """Judge a recorded workflow outcome under the current execution policy.

    Every case returns and none is a catch-all, so an outcome added to
    ``ExperimentOutcome`` fails type-check here rather than defaulting to one.
    """
    match outcome:
        case SomeConditionsFailed(failed_conditions=failures):
            failed_codes = [failure.condition_code.value for failure in failures]
            return CompletionStatus(
                status=ExecutionStatus.FAILED,
                summary=f"{len(failed_codes)} condition(s) failed — retry available",
                error=f"conditions failed to generate: {', '.join(failed_codes)}",
                error_category=ExecutionErrorCategory.GENERATION,
            )
        case AllConditionsGenerated(completed_conditions=conditions):
            return CompletionStatus(
                status=ExecutionStatus.SUCCEEDED,
                summary=f"{len(conditions)} study pack(s) generated",
            )
        case SomeLearnersFailed(completed_learners=learners, failed_learners=failures):
            failed_ids = [failure.focal_learner_id for failure in failures]
            return CompletionStatus(
                status=ExecutionStatus.FAILED,
                summary=(
                    f"{len(learners)} of {len(learners) + len(failed_ids)} "
                    "learner(s) personalised (P0/P1)"
                ),
                error=f"learners failed to personalise: {', '.join(failed_ids)}",
                error_category=ExecutionErrorCategory.GENERATION,
            )
        case AllLearnersPersonalised(completed_learners=learners):
            return CompletionStatus(
                status=ExecutionStatus.SUCCEEDED,
                summary=f"{len(learners)} learner(s) personalised (P0/P1)",
            )


def cancelled_completion() -> CompletionStatus:
    """How an interrupted attempt is stored: failed, so nothing waits on a dead claim."""
    return CompletionStatus(
        status=ExecutionStatus.FAILED,
        summary=_CANCELLED,
        error=_CANCELLED,
        error_category=ExecutionErrorCategory.CANCELLED,
    )


def failed_completion(exc: BaseException) -> CompletionStatus:
    """How a raised failure is stored, under the category its exception type implies."""
    message = str(exc)
    return CompletionStatus(
        status=ExecutionStatus.FAILED,
        summary=message,
        error=message,
        error_category=classify_execution_error(exc),
    )
