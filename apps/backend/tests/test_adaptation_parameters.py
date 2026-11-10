"""The settings a band and a learner's survey answers resolve to."""

from __future__ import annotations

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.adaptation_parameters import (
    resolve_parameters,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
)


def _state(band: str, **changes: str) -> ObjectiveLearnerState:
    return ObjectiveLearnerState.model_validate(
        {"lesson_objective_id": "lo1", "mastery_band": band, **changes}
    )


@pytest.mark.parametrize(
    ("band", "explanation", "worked", "practice"),
    [
        ("remediate", "smaller_steps", "every_line", "easier"),
        ("reinforce", "rule_and_reason", "key_line", "as_class"),
        ("extend", "brief_then_why", "first_and_last", "beyond_class"),
    ],
)
def test_the_band_sets_explanation_worked_support_and_where_practice_starts(
    band: str, explanation: str, worked: str, practice: str
) -> None:
    resolved = resolve_parameters(_state(band))
    assert (resolved.explanation, resolved.worked_support, resolved.practice_start) == (
        explanation,
        worked,
        practice,
    )


def test_hints_go_to_a_learner_who_needs_the_most_help_or_says_they_do() -> None:
    assert resolve_parameters(_state("remediate")).hints is True
    assert resolve_parameters(_state("reinforce")).hints is False
    assert resolve_parameters(_state("reinforce", confidence="a little sure (2/5)")).hints is True
    assert (
        resolve_parameters(_state("extend", perceived_difficulty="very difficult (5/5)")).hints
        is True
    )
    assert resolve_parameters(_state("extend", confidence="very sure (5/5)")).hints is False


def test_a_misconception_is_repaired_only_where_the_state_names_one() -> None:
    assert resolve_parameters(
        _state("reinforce", misconception="adds denominators")
    ).misconception_repair
    assert not resolve_parameters(_state("reinforce")).misconception_repair
