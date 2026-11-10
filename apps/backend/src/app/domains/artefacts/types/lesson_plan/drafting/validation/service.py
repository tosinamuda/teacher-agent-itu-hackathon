from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.domain.schema import schema_issues
from app.domains.artefacts.types.lesson_plan.drafting.validation.session_plan_rules import (
    validate_lesson_objective_step_alignment,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.types import (
    ContextMismatch,
    ValidationIssue,
)
from app.shared.json_types import JsonObject


def validate_session_plan(session_plan: JsonObject) -> list[ValidationIssue]:
    """A drafted plan: the lesson plan schema, then the rules a draft must also meet."""
    issues: list[ValidationIssue] = [
        {"path": path, "message": message} for path, message in schema_issues(session_plan)
    ]
    issues.extend(validate_lesson_objective_step_alignment(session_plan))
    return issues


def validate_session_plan_context(
    session_plan: JsonObject,
    session_context: JsonObject,
) -> list[ContextMismatch]:
    mismatches: list[ContextMismatch] = []
    for field in (
        "session_id",
        "subject",
        "track",
        "grade",
        "term",
        "week",
        "topic",
        "subtopic",
    ):
        expected = session_context.get(field)
        actual = session_plan.get(field)
        if expected is not None and actual != expected:
            mismatches.append(
                {
                    "field": field,
                    "expected": expected,
                    "actual": actual,
                }
            )
    return mismatches
