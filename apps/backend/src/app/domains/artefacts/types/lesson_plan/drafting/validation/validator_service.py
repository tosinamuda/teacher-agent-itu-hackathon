from __future__ import annotations

from dataclasses import dataclass

from app.domains.artefacts.types.lesson_plan.drafting.validation.service import (
    validate_session_plan,
    validate_session_plan_context,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.types import (
    ContextMismatch,
    ValidationIssue,
)
from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class SessionPlanValidationResult:
    schema_errors: list[ValidationIssue]
    context_errors: list[ContextMismatch]


class SessionPlanValidatorService:
    def validate(
        self, session_plan: JsonObject, session_context: JsonObject
    ) -> SessionPlanValidationResult:
        schema_errors = validate_session_plan(session_plan)
        context_errors = validate_session_plan_context(session_plan, session_context)
        return SessionPlanValidationResult(
            schema_errors=schema_errors,
            context_errors=context_errors,
        )
