"""Lesson-plan reviser — one focused, validated edit per human-feedback turn.

Runs ``ReviseLessonPlanSignature``, normalises the output, validates it with the
same ``SessionPlanValidatorService`` the generate path uses, and retries with the
violations fed back (the established refine pattern). Identity + scope fields are
forced from the original so a wording tweak can never silently change the lesson's
subject/grade/objectives coverage. Each LM call is tagged for the generation log.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass

import dspy
from dspy.utils.exceptions import AdapterParseError
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from app.config import CONFIG
from app.domains.artefacts.types.lesson_plan.application.ports import (
    SessionPlanValidatorPort,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    normalize_session_plan_payload,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.signatures.lesson_plan_revision import (  # noqa: E501
    ReviseLessonPlanSignature,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.validator_service import (
    SessionPlanValidatorService,
)
from app.domains.generation_log.application.recorder import log_context
from app.infra.dspy_lm import build_dspy_lm
from app.shared.json_types import JsonObject

logger = logging.getLogger(__name__)

# Identity + scope fields a revision must never drift — forced from the original.
_PRESERVED_FIELDS = (
    "plan_id",
    "session_id",
    "subject",
    "track",
    "grade",
    "term",
    "week",
    "topic",
    "subtopic",
)


class LessonPlanRevisionError(Exception):
    """Raised when a revision turn cannot produce any plan at all."""


@dataclass(frozen=True)
class RevisionResult:
    """The outcome of one revision turn."""

    session_plan: JsonObject
    change_summary: str
    validation_passed: bool
    violations: list[str]


def _validation_scope(session_plan: JsonObject) -> JsonObject:
    return {field: session_plan.get(field) for field in _PRESERVED_FIELDS if field != "plan_id"}


def _parse_failure_messages(exc: Exception) -> list[str]:
    """Turn a DSPy/pydantic output-parse failure into human-readable violations.

    These feed the ``prior_violations`` self-correction channel so the next
    attempt is told exactly what its previous output got wrong.
    """
    if isinstance(exc, PydanticValidationError):
        return [str(error.get("msg", error)) for error in exc.errors()] or [str(exc)]
    return [str(exc)]


class LessonPlanReviser:
    """Produce a new, validated SessionPlan from the current plan + one instruction."""

    def __init__(self, validator: SessionPlanValidatorPort | None = None) -> None:
        self.lm = build_dspy_lm()
        self.revise = dspy.ChainOfThought(ReviseLessonPlanSignature)
        self.validator = validator or SessionPlanValidatorService()

    async def revise_plan(
        self,
        *,
        current_session_plan: JsonObject,
        highlighted_part: str,
        instruction: str,
        conversation_summary: str,
        plan_id: str,
        thread_id: str,
    ) -> RevisionResult:
        scope = _validation_scope(current_session_plan)
        prior_violations: list[str] = []
        last: RevisionResult | None = None
        attempts = max(1, CONFIG.lesson_plan.max_refine_attempts)

        for attempt in range(1, attempts + 1):
            try:
                with log_context(
                    kind="lesson_plan_revision",
                    correlation_id=plan_id,
                    thread_id=thread_id,
                    attempt=attempt,
                ):
                    with dspy.settings.context(lm=self.lm):
                        result = await self.revise.acall(
                            current_session_plan=current_session_plan,
                            highlighted_part=highlighted_part or "(none — whole-plan instruction)",
                            revision_instruction=instruction,
                            conversation_summary=conversation_summary or "(first turn)",
                            prior_violations=prior_violations,
                        )
            except (PydanticValidationError, AdapterParseError) as exc:
                # The model emitted output our SessionPlan schema rejected (DSPy
                # validates the OutputField against the strict model and raises).
                # Feed the violations back as the next attempt's prior_violations
                # and retry, instead of letting a raw 500 escape the refine loop.
                # NB: rate-limit / network errors are neither of these types, so
                # they propagate untouched (we never silently retry those).
                prior_violations = _parse_failure_messages(exc)
                logger.info(
                    "revision attempt %s could not parse/validate (%s issue(s)); retrying",
                    attempt,
                    len(prior_violations),
                )
                continue
            payload = self._coerce(result.revised_session_plan, current_session_plan)
            normalized = normalize_session_plan_payload(payload)
            validation = self.validator.validate(normalized, scope)
            violations = [str(error) for error in validation.schema_errors] + [
                str(mismatch) for mismatch in validation.context_errors
            ]
            summary = str(getattr(result, "change_summary", "") or "Revised the lesson plan.")
            last = RevisionResult(
                session_plan=normalized,
                change_summary=summary,
                validation_passed=not violations,
                violations=violations,
            )
            if not violations:
                return last
            prior_violations = violations
            logger.info("revision attempt %s had %s issue(s); retrying", attempt, len(violations))

        if last is None:
            # Every attempt failed to even parse into a valid plan. Surface the
            # last set of violations so the caller can render a clear message
            # ("the assistant couldn't apply that cleanly") instead of a 500.
            detail = "; ".join(prior_violations) or "revision_produced_no_plan"
            raise LessonPlanRevisionError(detail)
        # Best-effort: return the last attempt with violations recorded rather than
        # hard-failing the chat (consistent with the generate-path failure policy).
        return last

    def _coerce(self, revised: object, original: JsonObject) -> JsonObject:
        if isinstance(revised, BaseModel):
            payload: JsonObject = revised.model_dump(mode="json", exclude_none=True)
        elif isinstance(revised, Mapping):
            payload = dict(revised)
        else:
            raise LessonPlanRevisionError("revision_payload_invalid")
        for field in _PRESERVED_FIELDS:
            if field in original:
                payload[field] = original[field]
        return payload
