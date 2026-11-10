"""Shared application errors for the school domain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SchoolApplicationError(Exception):
    """A handled error from the school application services.

    Carries an HTTP status code + a short detail string so transport layers can
    raise an ``HTTPException`` without re-deciding the meaning.
    """

    status_code: int
    detail: str
