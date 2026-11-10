"""Shared application errors for the expert-content domain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExpertContentApplicationError(Exception):
    """A handled error from the expert-content application services.

    Carries an HTTP status code + a short detail string so transport layers can
    raise an ``HTTPException`` without re-deciding the meaning.
    """

    status_code: int
    detail: str
