"""The packs each H2 learner ended up with, and the verdict that follows."""

from dataclasses import dataclass

from returns.pipeline import is_successful
from returns.result import Result

from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis

from ..conditions.profiles import condition_codes
from .execution import FocalLearner

LearnerPacks = dict[ConditionCode, GeneratedReviewPack]
CohortPacks = list[tuple[FocalLearner, Result[LearnerPacks, str]]]


@dataclass(frozen=True)
class LearnerFailure:
    """One learner whose P0/P1 pair was not produced, as reported to the caller."""

    focal_learner_id: str
    message: str


@dataclass(frozen=True)
class AllLearnersPersonalised:
    """P0/P1 were recorded for every selected focal learner."""

    completed_learners: tuple[str, ...]
    completed_conditions: tuple[ConditionCode, ...]


@dataclass(frozen=True)
class SomeLearnersFailed:
    """H2 recorded the pair for some learners and a failure for each of the rest."""

    completed_learners: tuple[str, ...]
    completed_conditions: tuple[ConditionCode, ...]
    failed_learners: tuple[LearnerFailure, ...]


H2Verdict = AllLearnersPersonalised | SomeLearnersFailed


def verdict_for(cohort: CohortPacks) -> H2Verdict:
    """Judge the whole cohort: every learner personalised, or some left unrecorded."""
    completed = tuple(learner.focal_learner_id for learner, packs in cohort if is_successful(packs))
    failures = tuple(
        LearnerFailure(focal_learner_id=learner.focal_learner_id, message=packs.failure())
        for learner, packs in cohort
        if not is_successful(packs)
    )
    conditions = condition_codes(Hypothesis.H2) if completed else ()
    if failures:
        return SomeLearnersFailed(
            completed_learners=completed,
            completed_conditions=conditions,
            failed_learners=failures,
        )
    return AllLearnersPersonalised(
        completed_learners=completed,
        completed_conditions=conditions,
    )
