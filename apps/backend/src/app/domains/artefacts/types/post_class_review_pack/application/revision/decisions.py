"""Pure decisions governing validation and revision of generated review packs."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    section_cited_refs,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)

RevisionAction = Literal["accept", "revise", "stop"]
RepairStrategy = Literal["preserve", "edit", "repair", "regenerate"]


@dataclass(frozen=True)
class RevisionDecision:
    """Whether the revision loop accepts, retries, or stops with a failed pack."""

    action: RevisionAction
    reason: Literal[
        "validation_passed",
        "retry_disabled",
        "retry_budget_exhausted",
        "validation_failed_with_retry_available",
    ]


@dataclass(frozen=True)
class RepairDecision:
    """How one generated section should respond to its validation findings."""

    strategy: RepairStrategy
    reason: Literal[
        "section_not_implicated",
        "generation_unit_missing",
        "finding_threshold_exceeded",
        "targeted_reviser_available",
        "packed_repair_required",
    ]


def evaluate_revision(
    *,
    validation_passed: bool,
    retry_on_failure: bool,
    retries_completed: int,
    max_retries: int,
) -> RevisionDecision:
    """Decide whether another revision round is permitted and warranted."""
    if validation_passed:
        return RevisionDecision(action="accept", reason="validation_passed")
    if not retry_on_failure:
        return RevisionDecision(action="stop", reason="retry_disabled")
    if retries_completed >= max_retries:
        return RevisionDecision(action="stop", reason="retry_budget_exhausted")
    return RevisionDecision(
        action="revise",
        reason="validation_failed_with_retry_available",
    )


def select_repair_strategy(
    *,
    implicated: bool,
    finding_count: int,
    max_patchable_findings: int,
    has_unit: bool,
    has_reviser: bool,
) -> RepairDecision:
    """Choose the least destructive repair strategy supported by the evidence."""
    if not implicated:
        return RepairDecision(strategy="preserve", reason="section_not_implicated")
    if not has_unit:
        return RepairDecision(strategy="preserve", reason="generation_unit_missing")
    if finding_count > max_patchable_findings:
        return RepairDecision(strategy="regenerate", reason="finding_threshold_exceeded")
    if has_reviser:
        return RepairDecision(strategy="edit", reason="targeted_reviser_available")
    return RepairDecision(strategy="repair", reason="packed_repair_required")


def issue_messages(validation: ValidationResult) -> list[str]:
    """Flatten failed checks into section-addressable repair instructions."""
    messages: list[str] = []
    for check in validation.checks:
        if check.passed:
            continue
        findings = (check.details or {}).get("findings")
        if findings:
            messages.extend(f"{check.check}: {finding}" for finding in findings)
        elif check.message:
            messages.append(f"{check.check}: {check.message}")
    return messages


def implicated_objectives(
    validation: ValidationResult,
    sections: Sequence[ReviewPackSection],
) -> set[str] | None:
    """Return targeted objectives, or ``None`` when every section is implicated."""
    implicated: set[str] = set()
    for check in validation.checks:
        if check.passed:
            continue
        details = check.details or {}
        if check.check == "scope_compliance":
            implicated.update(details.get("out_of_scope", []))
        elif check.check == "source_refs_present":
            implicated.update(details.get("sections_without_refs", []))
        elif check.check == "source_refs_valid":
            invalid = set(details.get("invalid_refs", []))
            implicated.update(
                section.lesson_objective_id
                for section in sections
                if section_cited_refs(section) & invalid
            )
        elif check.check in ("objective_preservation", "objective_coverage"):
            continue
        elif "sections_with_findings" in details:
            implicated.update(details["sections_with_findings"])
        else:
            return None
    return implicated or None


def finding_counts(validation: ValidationResult) -> dict[str, int]:
    """Count findings attributed to each objective across all failed checks."""
    counts: dict[str, int] = {}
    for check in validation.checks:
        if check.passed:
            continue
        details = check.details or {}
        for objective_id in details.get("sections_with_findings", []):
            counts[objective_id] = counts.get(objective_id, 0) + len(details.get("findings", []))
    return counts


def issues_for_section(
    section_id: str,
    all_section_ids: Sequence[str],
    issues: Sequence[str],
) -> list[str]:
    """Return this section's findings plus findings with no section attribution."""
    other_ids = [other for other in all_section_ids if other != section_id]
    return [
        issue
        for issue in issues
        if section_id in issue or not any(other in issue for other in other_ids)
    ]
