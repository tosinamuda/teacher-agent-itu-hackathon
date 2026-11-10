"""Persistable outcomes from structural and model-backed validation checks."""

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ValidationCheck,
)


class CheckResult(BaseModel):
    """Outcome of a single validation check."""

    model_config = ConfigDict(extra="forbid")

    check: ValidationCheck
    passed: bool
    message: str | None = None
    details: dict = Field(default_factory=dict)


class ValidationResult(BaseModel):
    """Aggregate validation outcome for a generated or personalised pack."""

    model_config = ConfigDict(extra="forbid")

    passed: bool
    checks: list[CheckResult]
