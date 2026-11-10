"""Evaluation application error — raised by the services, caught by the api."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationApplicationError(Exception):
    status_code: int
    detail: str


def bounded_int(value: object, *, minimum: int, maximum: int, error_detail: str) -> int:
    """Validate ``value`` is an int within ``[minimum, maximum]``, else raise 422."""
    if not isinstance(value, int) or value < minimum or value > maximum:
        raise EvaluationApplicationError(422, error_detail)
    return value
