"""Pure aggregation of structural and prose validation checks."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ValidationCheck,
)

from .schemas import CheckResult, ValidationResult


@dataclass(frozen=True)
class ValidationOutcome:
    """Aggregate validation decision with a stable, reportable reason."""

    passed: bool
    checks: tuple[CheckResult, ...]
    failed_checks: tuple[ValidationCheck, ...]
    reason: Literal["all_checks_passed", "checks_failed"]

    def as_result(self) -> ValidationResult:
        """Return the persisted Pydantic representation used by condition runs."""
        return ValidationResult(passed=self.passed, checks=list(self.checks))


def evaluate_validation(
    *,
    structural: ValidationResult,
    critiques: Sequence[CheckResult],
) -> ValidationOutcome:
    """Combine structural and prose checks under the all-must-pass rule."""
    checks = (*structural.checks, *critiques)
    failed = tuple(check.check for check in checks if not check.passed)
    return ValidationOutcome(
        passed=not failed,
        checks=checks,
        failed_checks=failed,
        reason="all_checks_passed" if not failed else "checks_failed",
    )
