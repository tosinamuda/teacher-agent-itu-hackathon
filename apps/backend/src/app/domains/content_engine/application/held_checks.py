"""The checks a draft passed before it could be saved, kept with it for the teacher's review."""

from __future__ import annotations

from collections.abc import Sequence

from app.domains.artefacts.types.post_class_review_pack.application.review_record import (
    ReviewedCheck,
    ReviewRecord,
)
from app.shared.json_types import JsonObject


def held_checks_record(names: Sequence[str]) -> JsonObject:
    """A draft that failed one of these was sent back and never stored, so each one passed."""
    record = ReviewRecord(
        checks=[ReviewedCheck(check=name, passed=True) for name in names], passages=[]
    )
    return record.model_dump(mode="json")
