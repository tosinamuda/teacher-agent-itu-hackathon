from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias, TypedDict

ValidationPathSegment: TypeAlias = str | int


class ValidationIssue(TypedDict):
    path: list[ValidationPathSegment]
    message: str


class ContextMismatch(TypedDict):
    field: str
    expected: object
    actual: object


@dataclass(frozen=True)
class ObjectiveValidationSnapshot:
    curriculum_ids: set[str]
    lesson_objective_ids: list[str]
    lesson_objective_kc_types: dict[str, str]
