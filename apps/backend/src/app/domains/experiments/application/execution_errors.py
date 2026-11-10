"""Classify a conditioned-execution failure into a structured category.

The worker calls this at the catch site, where it still holds the actual
exception object — so classification is by exception *type*, never by
inspecting the formatted message string. The resulting
``ExecutionErrorCategory`` is persisted on the execution row; the UI reads
it directly instead of pattern-matching ``error_message``.
"""

from __future__ import annotations

from sqlalchemy.exc import DBAPIError

from app.domains.experiments.domain.types import (
    ConditionedInputsMissingError,
    ExecutionErrorCategory,
)


def classify_execution_error(exc: BaseException) -> ExecutionErrorCategory:
    """Map a worker exception to its execution-error category by type.

    - ``ConditionedInputsMissingError`` → INPUTS_MISSING (our own typed raise)
    - any ``sqlalchemy.exc.DBAPIError`` (IntegrityError, OperationalError, …)
      → PERSISTENCE (a database-layer failure while saving results)
    - everything else → GENERATION (the generation pipeline itself: an LLM
      call, validation, payload assembly, etc.)
    """
    if isinstance(exc, ConditionedInputsMissingError):
        return ExecutionErrorCategory.INPUTS_MISSING
    if isinstance(exc, DBAPIError):
        return ExecutionErrorCategory.PERSISTENCE
    return ExecutionErrorCategory.GENERATION
