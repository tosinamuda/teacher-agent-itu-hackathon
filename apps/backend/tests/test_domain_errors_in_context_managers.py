"""A domain error comes out of a context manager as itself.

Python sets ``__traceback__`` on an exception as it passes through a ``contextlib`` context
manager; a frozen dataclass error refused that, and the caller got ``FrozenInstanceError``
instead of the 409 it was meant to answer with.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import pytest

from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefacts.types.lesson_plan.application.errors import PlanValidationError
from app.domains.assessments.application.service import AssessmentApplicationError
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.learners.application.service import LearnerApplicationError


@asynccontextmanager
async def _around() -> AsyncIterator[None]:
    yield


@pytest.mark.parametrize(
    "error",
    [
        ExperimentApplicationError(409, "experiment_lesson_missing"),
        AssessmentApplicationError(409, "not_released"),
        ArtefactRevisionError(409, "stale"),
        LearnerApplicationError(404, "learner_not_found"),
        PlanValidationError({"errors": []}),
    ],
    ids=lambda error: type(error).__name__,
)
def test_a_domain_error_passes_through_a_context_manager_as_itself(error: Exception) -> None:
    async def _raise() -> None:
        async with _around():
            raise error

    with pytest.raises(type(error)) as raised:
        asyncio.run(_raise())

    assert raised.value is error
