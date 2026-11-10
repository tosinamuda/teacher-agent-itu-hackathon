from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.types import (
    KCPlanningResult,
    PlanningQualityRow,
)


@dataclass(frozen=True)
class _ReportTally:
    valid: int
    warnings: int
    errors: int
    violation_counts: dict[str, int]
    invalid_entries: list[tuple[str, str | None]]


def _tally(results: Sequence[KCPlanningResult | PlanningQualityRow]) -> _ReportTally:
    valid = sum(1 for result in results if not result.violations)
    warnings = sum(
        1
        for result in results
        if result.violations
        and all(violation.severity != "error" for violation in result.violations)
    )
    violation_counts: dict[str, int] = {}
    invalid_entries: list[tuple[str, str | None]] = []
    for result in results:
        if result.violations:
            invalid_entries.append(
                (
                    getattr(result, "subtopic_id", "unknown"),
                    result.violations[0].message if result.violations else None,
                )
            )
        for violation in result.violations:
            violation_counts[violation.code] = violation_counts.get(violation.code, 0) + 1
    return _ReportTally(
        valid=valid,
        warnings=warnings,
        errors=len(results) - valid - warnings,
        violation_counts=violation_counts,
        invalid_entries=invalid_entries,
    )


def _violation_lines(violation_counts: dict[str, int]) -> list[str]:
    if not violation_counts:
        return ["  - none"]
    return [
        f"  - {code}: {count}"
        for code, count in sorted(violation_counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def _review_lines(invalid_entries: list[tuple[str, str | None]]) -> list[str]:
    if not invalid_entries:
        return []
    lines = ["", "Subtopics needing review:"]
    for subtopic_id, reason in invalid_entries:
        lines.append(f"  - {subtopic_id}")
        if reason:
            lines.append(f"    Reason: {reason}")
    return lines


def render_infrastructure_quality_report(
    results: Sequence[KCPlanningResult | PlanningQualityRow],
) -> str:
    tally = _tally(results)
    lines = [
        "Infrastructure Quality Report",
        "=============================",
        f"Subtopics processed:     {len(results)}",
        f"  Valid:                {tally.valid}",
        f"  With warnings:        {tally.warnings}",
        f"  With errors:          {tally.errors}",
        "",
        "Common violations:",
        *_violation_lines(tally.violation_counts),
    ]
    lines.extend(_review_lines(tally.invalid_entries))
    return "\n".join(lines)
