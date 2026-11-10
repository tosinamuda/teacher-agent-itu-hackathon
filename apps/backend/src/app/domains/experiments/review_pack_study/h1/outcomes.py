"""The pack each H1 condition ended up with, and the verdict that follows."""

from dataclasses import dataclass

from returns.pipeline import is_successful
from returns.result import Result

from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.experiments.domain.types import ConditionCode

ConditionPacks = dict[ConditionCode, Result[GeneratedReviewPack, str]]


@dataclass(frozen=True)
class ConditionFailure:
    """One condition-generation failure as reported to the application caller."""

    condition_code: ConditionCode
    message: str


@dataclass(frozen=True)
class AllConditionsGenerated:
    """Every configured H1 condition produced a pack."""

    completed_conditions: tuple[ConditionCode, ...]


@dataclass(frozen=True)
class SomeConditionsFailed:
    """H1 produced packs for some conditions and retryable failures for the rest."""

    completed_conditions: tuple[ConditionCode, ...]
    failed_conditions: tuple[ConditionFailure, ...]


H1Verdict = AllConditionsGenerated | SomeConditionsFailed


def verdict_for(packs: ConditionPacks) -> H1Verdict:
    """Judge the whole execution: every condition generated, or some left to retry."""
    completed = tuple(code for code, pack in packs.items() if is_successful(pack))
    failures = tuple(
        ConditionFailure(condition_code=code, message=pack.failure())
        for code, pack in packs.items()
        if not is_successful(pack)
    )
    if failures:
        return SomeConditionsFailed(completed_conditions=completed, failed_conditions=failures)
    return AllConditionsGenerated(completed_conditions=completed)
