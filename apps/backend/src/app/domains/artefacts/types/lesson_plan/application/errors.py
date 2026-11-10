"""What the lesson-plan use cases refuse, and why."""

from __future__ import annotations

from dataclasses import dataclass


class SessionNotFoundError(Exception):
    pass


# Not frozen: Python sets __traceback__ on an exception as it passes through a context manager.
@dataclass(eq=False)
class PlanValidationError(Exception):
    detail: object


class PlanVersionNotFoundError(Exception):
    pass


class PlanNotOwnedByTeacherError(Exception):
    """The approving teacher does not teach this plan's class + subject + term."""


class PlanLookupNotFoundError(Exception):
    pass


class GenerationFailedError(Exception):
    pass
