"""Pure decision contracts for conditioned study-pack generation."""

from dataclasses import FrozenInstanceError

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.prompt_provenance import (
    PromptTrace,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.policy import (
    build_generation_policy,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.decisions import (
    evaluate_revision,
    select_repair_strategy,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.outcome import (
    evaluate_validation,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    CheckResult,
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.repair_section import (  # noqa: E501
    RepairSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_fingerprint import (  # noqa: E501
    fingerprint_signature,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for


def _validation(*checks: CheckResult) -> ValidationResult:
    return ValidationResult(
        passed=all(check.passed for check in checks),
        checks=list(checks),
    )


def test_validation_outcome_aggregates_structural_and_prose_checks() -> None:
    structural = _validation(CheckResult(check="scope_compliance", passed=True))
    critique = CheckResult(
        check="content_grounding",
        passed=False,
        message="unsupported claim",
    )

    outcome = evaluate_validation(structural=structural, critiques=[critique])

    assert not outcome.passed
    assert outcome.reason == "checks_failed"
    assert outcome.failed_checks == ("content_grounding",)
    assert [check.check for check in outcome.checks] == [
        "scope_compliance",
        "content_grounding",
    ]
    with pytest.raises(FrozenInstanceError):
        outcome.reason = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("passed", "retry_on_failure", "retries_completed", "max_retries", "action", "reason"),
    [
        (True, True, 0, 2, "accept", "validation_passed"),
        (False, False, 0, 2, "stop", "retry_disabled"),
        (False, True, 2, 2, "stop", "retry_budget_exhausted"),
        (False, True, 1, 2, "revise", "validation_failed_with_retry_available"),
    ],
)
def test_revision_decision_records_why_the_loop_continues_or_stops(
    passed: bool,
    retry_on_failure: bool,
    retries_completed: int,
    max_retries: int,
    action: str,
    reason: str,
) -> None:
    decision = evaluate_revision(
        validation_passed=passed,
        retry_on_failure=retry_on_failure,
        retries_completed=retries_completed,
        max_retries=max_retries,
    )

    assert decision.action == action
    assert decision.reason == reason


@pytest.mark.parametrize(
    ("implicated", "finding_count", "has_unit", "has_reviser", "strategy", "reason"),
    [
        (False, 9, True, True, "preserve", "section_not_implicated"),
        (True, 9, False, True, "preserve", "generation_unit_missing"),
        (True, 4, True, True, "regenerate", "finding_threshold_exceeded"),
        (True, 3, True, True, "edit", "targeted_reviser_available"),
        (True, 3, True, False, "repair", "packed_repair_required"),
    ],
)
def test_repair_strategy_is_a_pure_threshold_decision(
    implicated: bool,
    finding_count: int,
    has_unit: bool,
    has_reviser: bool,
    strategy: str,
    reason: str,
) -> None:
    decision = select_repair_strategy(
        implicated=implicated,
        finding_count=finding_count,
        max_patchable_findings=3,
        has_unit=has_unit,
        has_reviser=has_reviser,
    )

    assert decision.strategy == strategy
    assert decision.reason == reason


def test_execution_controls_are_persistable_but_absent_from_model_policy() -> None:
    profile = profile_for(Hypothesis.H1, ConditionCode.C3)

    assert profile.execution.max_patchable_findings == 3
    assert profile.execution.agent_max_iterations == 8
    assert profile.model_dump(mode="json")["execution"] == {
        "max_patchable_findings": 3,
        "agent_max_iterations": 8,
    }
    assert "max_patchable_findings" not in build_generation_policy(profile).model_dump()
    assert "agent_max_iterations" not in build_generation_policy(profile).model_dump()


def test_prompt_trace_fingerprints_only_signatures_that_were_actually_invoked() -> None:
    trace = PromptTrace()

    trace.record("base_generation", fingerprint_signature(WriteSection))
    generated = trace.snapshot()
    trace.record("section_repair", fingerprint_signature(RepairSection))
    repaired = trace.snapshot()

    assert generated.components == {"base_generation": fingerprint_signature(WriteSection)}
    assert "section_repair" not in generated.components
    assert repaired.components["section_repair"] == fingerprint_signature(RepairSection)
    assert repaired.composite_fingerprint != generated.composite_fingerprint
