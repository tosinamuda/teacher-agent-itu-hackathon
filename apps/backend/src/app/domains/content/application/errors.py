"""The one error the content use cases raise, carrying its HTTP status."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContentError(Exception):
    status_code: int
    detail: str


class NoGeneratorError(ContentError):
    """The type has no generator at the level asked for."""
