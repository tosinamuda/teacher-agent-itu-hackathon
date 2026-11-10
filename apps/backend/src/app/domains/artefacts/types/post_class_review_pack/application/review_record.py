"""What a teacher is shown beside a note: the checks it passed and the passages it cites."""

from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.shared.json_types import JsonObject


class ReviewedCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    check: str
    passed: bool
    message: str | None = None


class CitedPassage(BaseModel):
    """A passage the note was given to cite, by the reference its sections use."""

    model_config = ConfigDict(extra="forbid")

    source_ref: str
    title: str | None = None
    excerpt: str


class ReviewRecord(BaseModel):
    """The checks run on a version of a note and the passages it was given, kept with it."""

    model_config = ConfigDict(extra="forbid")

    #: The version of the note the checks ran on.
    version: int = 1
    checks: list[ReviewedCheck]
    passages: list[CitedPassage]


def review_record(
    validation: ValidationResult | None,
    request: ReviewPackRequest,
    *,
    held_to: Sequence[str] = (),
) -> JsonObject:
    """The record of a generated note: its checks, and each passage once by its reference.

    ``held_to`` names checks the note passed before it could be saved, which the validator does
    not run: a draft that failed one was sent back and never stored.
    """
    passages: dict[str, CitedPassage] = {}
    for unit in request.units:
        for item in unit.source_evidence:
            if item.source_ref and item.source_ref not in passages:
                passages[item.source_ref] = CitedPassage(
                    source_ref=item.source_ref, title=item.title, excerpt=item.excerpt
                )
    ran = [
        ReviewedCheck(check=c.check, passed=c.passed, message=c.message)
        for c in (validation.checks if validation else [])
    ]
    seen = {c.check for c in ran}
    record = ReviewRecord(
        checks=ran
        + [ReviewedCheck(check=name, passed=True) for name in held_to if name not in seen],
        passages=list(passages.values()),
    )
    return record.model_dump(mode="json")
