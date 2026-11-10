"""Check a teacher's plan content against its lesson without saving it.

The manual-entry path saves only a plan that passes, and a plan a writer drafts shows it every
issue after each change, so both read their issues from here. A plan the app writes is also held
to the lesson-plan spec's requirements, which a teacher's own plan is not.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import ValidationError
from pydantic_core import ErrorDetails

from app.domains.artefacts.types.lesson_plan.application.manual_entry import (
    assemble_manual_session_plan,
    curriculum_mapping_issues,
)
from app.domains.artefacts.types.lesson_plan.application.payload_builder import (
    SessionContextPayloadBuilder,
)
from app.domains.artefacts.types.lesson_plan.domain.lesson_document import as_document, violations
from app.domains.artefacts.types.lesson_plan.domain.plan_requirements import unmet
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import SessionPlan
from app.domains.artefacts.types.lesson_plan.drafting.validation.service import (
    validate_session_plan,
    validate_session_plan_context,
)
from app.shared.json_types import JsonObject, JsonValue


@dataclass(frozen=True)
class ManualPlanCheck:
    #: The content with the lesson's identity and curriculum objectives set.
    session_plan: JsonObject
    #: What stops it being saved, by check; empty when it passes.
    issues: JsonObject = field(default_factory=dict)

    @property
    def passes(self) -> bool:
        return not self.issues


def check_manual_plan(
    session_context: SessionContext,
    content: JsonObject,
    *,
    strict: bool = False,
) -> ManualPlanCheck:
    """Every issue that stops ``content`` being saved as the lesson's plan.

    ``strict`` also holds a plan that passes to the spec's requirements: the lesson document's
    grammar, the order of the steps, the work its activities set, and its minutes.
    """
    payloads = SessionContextPayloadBuilder().build(session_context)
    curriculum = payloads.curriculum_scope.curriculum_objectives
    session_plan = assemble_manual_session_plan(session_context, curriculum, content)
    issues: JsonObject = {}
    if not curriculum:
        issues["curriculum_mapping"] = "this lesson has no curriculum objectives to map to"
    elif mapping := curriculum_mapping_issues(session_plan, curriculum):
        issues["curriculum_mapping"] = [*mapping]
    if schema_errors := validate_session_plan(session_plan):
        issues["errors"] = [
            {"path": [*issue["path"]], "message": issue["message"]} for issue in schema_errors
        ]
    if context_errors := validate_session_plan_context(
        session_plan, payloads.validation_scope.model_dump(mode="json")
    ):
        issues["context_errors"] = [
            {
                "field": found["field"],
                "expected": _scalar(found["expected"]),
                "actual": _scalar(found["actual"]),
            }
            for found in context_errors
        ]
    if model_issues := _model_issues(session_plan):
        issues["plan"] = [*model_issues]
    if strict and not issues:
        issues |= _requirement_issues(session_plan, session_context)
    return ManualPlanCheck(session_plan, issues)


def _requirement_issues(session_plan: JsonObject, context: SessionContext) -> JsonObject:
    found: JsonObject = {}
    if grammar := violations(as_document(session_plan)):
        found["lesson_document"] = [*grammar]
    if requirements := unmet(session_plan, duration_minutes=context.duration_minutes):
        found["requirements"] = [*requirements]
    if invented := _invented_references(session_plan, context):
        found["references"] = invented
    return found


def _invented_references(session_plan: JsonObject, context: SessionContext) -> list[JsonValue]:
    """The references that name no source the lesson has: its textbook, or a record of it."""
    sources = [
        str(source).lower()
        for source in (
            *(
                record.get("record_id") or record.get("section_ref")
                for record in context.textbook_references
            ),
            *(material.get("title") for material in context.reference_materials),
        )
        if source
    ]
    references = session_plan.get("references")
    return [
        f"references.{position}: {reference!r} names no source this lesson has; "
        "name a textbook record by its record id, or leave the references out"
        for position, reference in enumerate(references if isinstance(references, list) else [])
        if not any(source in str(reference).lower() for source in sources)
    ]


def _scalar(value: object) -> JsonValue:
    """A value the lesson's context holds, as JSON: itself, or its text."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _message(problem: ErrorDetails) -> str:
    """The model's own words for a check it raised, without pydantic's "Value error, " prefix."""
    raised = problem.get("ctx", {}).get("error")
    return (
        str(raised) if problem["type"] == "value_error" and raised is not None else problem["msg"]
    )


def _model_issues(session_plan: JsonObject) -> list[str]:
    """What the stored plan's own model refuses, which is checked again when it is saved."""
    try:
        SessionPlan.model_validate(session_plan)
    except ValidationError as error:
        return [
            f"{'.'.join(str(step) for step in problem['loc'])}: {_message(problem)}"
            for problem in error.errors()
        ]
    return []
