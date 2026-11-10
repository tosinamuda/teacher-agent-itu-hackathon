"""Application policy for classifying recorded experiment outcomes."""

from app.domains.experiments.application.execution_outcome import completion_status_for
from app.domains.experiments.domain.types import (
    ConditionCode,
    ExecutionErrorCategory,
    ExecutionStatus,
)
from app.domains.experiments.review_pack_study.h1.outcomes import (
    AllConditionsGenerated,
    ConditionFailure,
    SomeConditionsFailed,
)
from app.domains.experiments.review_pack_study.h2.outcomes import (
    AllLearnersPersonalised,
    LearnerFailure,
    SomeLearnersFailed,
)


def test_complete_h1_is_a_successful_execution() -> None:
    completion = completion_status_for(
        AllConditionsGenerated(completed_conditions=(ConditionCode.C0, ConditionCode.C1))
    )

    assert completion.status == ExecutionStatus.SUCCEEDED
    assert completion.error is None


def test_complete_h2_is_a_successful_execution() -> None:
    completion = completion_status_for(
        AllLearnersPersonalised(
            completed_learners=("STU-1",),
            completed_conditions=(ConditionCode.P0, ConditionCode.P1),
        )
    )

    assert completion.status == ExecutionStatus.SUCCEEDED
    assert completion.error is None


def test_a_cohort_missing_one_learner_is_a_failed_execution() -> None:
    """The recorded packs survive a mid-cohort failure; the execution still fails.

    Anything else reports a cohort the analysis cannot pair as a success.
    """
    completion = completion_status_for(
        SomeLearnersFailed(
            completed_learners=("STU-1", "STU-2"),
            completed_conditions=(ConditionCode.P0, ConditionCode.P1),
            failed_learners=(LearnerFailure(focal_learner_id="STU-3", message="LLM timeout"),),
        )
    )

    assert completion.status == ExecutionStatus.FAILED
    assert completion.summary == "2 of 3 learner(s) personalised (P0/P1)"
    assert completion.error == "learners failed to personalise: STU-3"
    assert completion.error_category == ExecutionErrorCategory.GENERATION.value


def test_partial_h1_is_currently_a_failed_execution() -> None:
    completion = completion_status_for(
        SomeConditionsFailed(
            completed_conditions=(ConditionCode.C0,),
            failed_conditions=(
                ConditionFailure(
                    condition_code=ConditionCode.C1,
                    message="LLM timeout",
                ),
            ),
        )
    )

    assert completion.status == ExecutionStatus.FAILED
    assert completion.error == "conditions failed to generate: C1"
    assert completion.error_category == ExecutionErrorCategory.GENERATION.value
