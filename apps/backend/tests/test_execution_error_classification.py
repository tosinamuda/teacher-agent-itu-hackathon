"""Unit tests for execution-error classification.

Classification is by exception *type* at the catch site — these tests pin
that contract so a future refactor can't silently regress the categories
the UI depends on.
"""

from __future__ import annotations

import pytest
from sqlalchemy.exc import IntegrityError, OperationalError

from app.domains.experiments.application.execution_errors import (
    classify_execution_error,
)
from app.domains.experiments.domain.types import (
    ConditionedInputsMissingError,
    ExecutionErrorCategory,
)


def test_inputs_missing_maps_to_inputs_missing() -> None:
    exc = ConditionedInputsMissingError("conditioned_execution_inputs_missing")
    assert classify_execution_error(exc) is ExecutionErrorCategory.INPUTS_MISSING


def test_integrity_error_maps_to_persistence() -> None:
    # IntegrityError is a DBAPIError subclass; the FK violation that motivated
    # this work surfaces as exactly this type.
    exc = IntegrityError("INSERT ...", params=None, orig=Exception("fk violation"))
    assert classify_execution_error(exc) is ExecutionErrorCategory.PERSISTENCE


def test_other_dbapi_error_maps_to_persistence() -> None:
    exc = OperationalError("SELECT ...", params=None, orig=Exception("connection lost"))
    assert classify_execution_error(exc) is ExecutionErrorCategory.PERSISTENCE


@pytest.mark.parametrize(
    "exc",
    [
        RuntimeError("dspy blew up"),
        ValueError("condition C0 reuses C0, which produced no result"),
        TimeoutError("llm timed out"),
    ],
)
def test_anything_else_maps_to_generation(exc: Exception) -> None:
    assert classify_execution_error(exc) is ExecutionErrorCategory.GENERATION
