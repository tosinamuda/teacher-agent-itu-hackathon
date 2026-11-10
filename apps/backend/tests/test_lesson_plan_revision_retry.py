"""The revision reviser must turn a model output-validation failure into a
fed-back retry, not a 500.

DSPy validates the ``revised_session_plan`` OutputField against the strict
``SessionPlan`` model and raises ``pydantic.ValidationError`` when the LM emits
an invalid plan. That throw happens inside the reviser's refine loop; before the
fix it escaped the loop and surfaced as an unhandled 500. These tests pin the
two behaviours: a transient failure is retried (with the violations fed back),
and an always-failing model gives up as ``LessonPlanRevisionError`` (which the
executor maps to a clean 422), never letting the raw error escape.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.domains.artefacts.types.lesson_plan.drafting.application.revision import (
    LessonPlanReviser,
    LessonPlanRevisionError,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import SessionPlan


def _a_validation_error() -> ValidationError:
    """A real pydantic ValidationError, exactly what DSPy raises on a bad plan."""
    try:
        SessionPlan.model_validate({"plan_id": "LP-x"})  # missing required fields
    except ValidationError as error:
        return error
    raise AssertionError("expected a ValidationError")  # pragma: no cover


class _StubResult:
    def __init__(self, session_plan: dict) -> None:
        self.revised_session_plan = session_plan
        self.change_summary = "stub change"


class _FakeRevise:
    """Stands in for ``dspy.ChainOfThought`` — scripted to raise then (maybe) pass."""

    def __init__(self, *, fail_times: int, then_plan: dict | None) -> None:
        self._fail_times = fail_times
        self._then_plan = then_plan
        self.calls = 0
        self.seen_prior_violations: list[list[str]] = []

    async def acall(self, **kwargs: object):
        self.calls += 1
        self.seen_prior_violations.append(list(kwargs.get("prior_violations") or []))
        if self.calls <= self._fail_times:
            raise _a_validation_error()
        if self._then_plan is None:  # pragma: no cover - guarded by callers
            raise AssertionError("no success plan scripted")
        return _StubResult(self._then_plan)


class _PassThroughValidator:
    """Treats any plan as valid — isolates the test to the parse-failure path."""

    def validate(self, _session_plan: object, _scope: object):
        class _Result:
            schema_errors: list[str] = []
            context_errors: list[str] = []

        return _Result()


def _reviser(fake_revise: _FakeRevise) -> LessonPlanReviser:
    reviser = LessonPlanReviser.__new__(LessonPlanReviser)
    reviser.lm = None  # dspy.settings.context(lm=None) is a harmless no-op here
    reviser.revise = fake_revise
    reviser.validator = _PassThroughValidator()
    return reviser


_VALID_PLAN = {"plan_id": "LP-x", "subtopic": "fractions"}


@pytest.mark.asyncio
async def test_parse_failure_is_retried_with_violations_fed_back() -> None:
    fake = _FakeRevise(fail_times=1, then_plan=_VALID_PLAN)
    reviser = _reviser(fake)

    result = await reviser.revise_plan(
        current_session_plan={"plan_id": "LP-x", "subtopic": "fractions"},
        highlighted_part="",
        instruction="tidy the first objective",
        conversation_summary="",
        plan_id="LP-x",
        thread_id="RVT-x",
    )

    assert fake.calls == 2  # first threw, second succeeded
    assert result.validation_passed is True
    # The first attempt sent no violations; the retry was told what broke.
    assert fake.seen_prior_violations[0] == []
    assert fake.seen_prior_violations[1], "retry must receive the prior violations"


@pytest.mark.asyncio
async def test_all_attempts_failing_raises_revision_error_not_a_raw_500() -> None:
    fake = _FakeRevise(fail_times=99, then_plan=None)
    reviser = _reviser(fake)

    with pytest.raises(LessonPlanRevisionError):
        await reviser.revise_plan(
            current_session_plan={"plan_id": "LP-x", "subtopic": "fractions"},
            highlighted_part="",
            instruction="do something impossible",
            conversation_summary="",
            plan_id="LP-x",
            thread_id="RVT-x",
        )

    # Exhausted the configured refine budget rather than giving up after one throw.
    assert fake.calls >= 2
