"""Pydantic contracts for the artefact-revision chat API."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.shared.json_types import JsonObject
from app.shared.schema_base import StrictRequest, UtcDatetime


class RevisionHighlight(BaseModel):
    """The part of the artefact the teacher highlighted (all anchors optional)."""

    step_id: str | None = None
    #: A unit of engine content, and the path of the field in its part, as the viewer sees them.
    unit_id: str | None = None
    path: str | None = None
    block_id: str | None = None
    lesson_objective_id: str | None = None
    selected_text: str = ""


class CreateThreadRequest(StrictRequest):
    artefact_type: str = Field(..., min_length=1)
    subject_id: str = Field(
        ..., min_length=1, description="Artefact key (plan_id for lesson_plan)."
    )


class SubmitTurnRequest(StrictRequest):
    instruction: str = Field(..., min_length=1)
    highlight: RevisionHighlight | None = None


class RevisionTurnResponse(BaseModel):
    revision_turn_id: str
    turn_number: int
    instruction: str
    highlight: RevisionHighlight | None = None
    base_version_id: str | None = None
    result_version_id: str | None = None
    summary: str | None = None
    validation_passed: bool
    created_at: UtcDatetime


class RevisionThreadResponse(BaseModel):
    """Thread metadata + turns + the current artefact (the chat seed)."""

    revision_thread_id: str
    artefact_type: str
    subject_id: str
    current_version_id: str | None = None
    current_session_plan: JsonObject | None = None
    turns: list[RevisionTurnResponse] = Field(default_factory=list)


class SubmitTurnResponse(BaseModel):
    """The new turn + the revised artefact, for immediate re-render."""

    turn: RevisionTurnResponse
    result_version_id: str
    session_plan: JsonObject
    validation_passed: bool
