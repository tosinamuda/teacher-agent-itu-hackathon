"""Shared application errors for the experiments domain."""

from __future__ import annotations

from dataclasses import dataclass


# Not frozen: Python sets __traceback__ on an exception as it passes through a context manager.
@dataclass(eq=False)
class ExperimentApplicationError(Exception):
    """A handled error from the experiments application services.

    Carries an HTTP status code + a short detail string so transport layers can
    raise an ``HTTPException`` without re-deciding the meaning.
    """

    status_code: int
    detail: str
