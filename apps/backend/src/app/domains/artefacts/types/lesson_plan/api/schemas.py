from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import SessionPlan
from app.shared.json_types import JsonObject
from app.shared.schema_base import StrictRequest, UtcDatetime


class PlanGenerateRequest(StrictRequest):
    session_id: str = Field(..., min_length=1)
    teacher_id: str | None = Field(default=None)
    evidence_selection_strategy: Literal["per_kc_rlm", "global_rlm"] | None = Field(default=None)


class ProgressLine(BaseModel):
    """One thing the agent drafting a plan said or did, as the chat keeps it."""

    id: int
    kind: str
    data: JsonObject


class OutlineStep(BaseModel):
    title: str
    minutes: int | None = None


class PlanOutline(BaseModel):
    """What of the plan is written so far."""

    objectives: list[str]
    steps: list[OutlineStep]
    written: int
    total: int


class DraftingProgress(BaseModel):
    """What the agent has done since the caller last read, and where to read on from."""

    lines: list[ProgressLine]
    next: int
    #: The plan as written so far; none while no draft is open.
    outline: PlanOutline | None = None


class PlanGenerateResponse(BaseModel):
    artefact_type: ArtefactType = ArtefactType.LESSON_PLAN
    plan_id: str
    version_id: str
    session_plan: SessionPlan
    session_id: str | None = None
    version_status: str = "draft"
    #: Why the teacher discarded this draft or took its approval back, when they did.
    closed_reason: str | None = None
    closed_at: UtcDatetime | None = None
    status: str = "ok"
    compiled_artefact_id: str | None = None
    #: Where the plan breaks the lesson document or leaves the lesson-plan spec unmet.
    unmet_requirements: list[str] = Field(default_factory=list)


class PlanManualEditRequest(StrictRequest):
    """A teacher's hand-edited full session plan, persisted as a new draft version.

    The whole ``session_plan`` is sent back (with the teacher's text changes
    merged in); the server forces identity/scope fields from the current version
    and validates the rest against ``SessionPlan``.
    """

    session_plan: dict


class PlanManualCreateRequest(StrictRequest):
    """A teacher's hand-entered lesson plan, persisted as a new draft version.

    The teacher supplies the lesson ``session_plan`` *content*; the server forces
    lesson identity and the curriculum-objective list from the lesson's session
    context, then validates the rest against ``SessionPlan``.
    """

    session_id: str = Field(..., min_length=1)
    teacher_id: str | None = Field(default=None)
    session_plan: dict


class PlanReuseRequest(StrictRequest):
    """An existing plan to use as a lesson's plan, without writing it again.

    Give the saved plan version to reuse, or the plan's content. Where the lesson has more than
    one curriculum objective, ``curriculum_choices`` says which each lesson objective points at.
    """

    session_id: str = Field(..., min_length=1)
    source_plan_version_id: str | None = Field(default=None, min_length=1)
    session_plan: dict | None = None
    curriculum_choices: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _exactly_one_source(self) -> PlanReuseRequest:
        if (self.source_plan_version_id is None) == (self.session_plan is None):
            raise ValueError("give a plan version or the plan's content, not both or neither")
        return self


class PlanReuseResponse(BaseModel):
    """The saved draft, or the choices still to make."""

    status: Literal["reused", "needs_curriculum_choice"]
    plan: PlanGenerateResponse | None = None
    #: The lesson objectives that still need a curriculum objective chosen.
    unmapped: list[dict] = Field(default_factory=list)
    #: The curriculum objectives of the lesson, to choose from.
    choices: list[dict] = Field(default_factory=list)


class ManualCurriculumObjective(BaseModel):
    curriculum_objective_id: str
    objective_text: str
    objective_order: int


class ManualPlanContextResponse(BaseModel):
    """Lesson identity + curriculum objectives a hand-entered plan maps onto."""

    session_id: str
    subject: str
    grade: str
    term: str
    week: int
    topic: str
    subtopic: str
    curriculum_objectives: list[ManualCurriculumObjective]


class PlanApproveRequest(StrictRequest):
    approved_by: str | None = Field(default=None, min_length=1)


class PlanApproveResponse(BaseModel):
    plan_id: str
    version_id: str
    status: str
    approved_at: UtcDatetime | None
    approved_by: str | None


class PlanVersionSummary(BaseModel):
    artefact_type: ArtefactType = ArtefactType.LESSON_PLAN
    plan_id: str
    version_id: str
    session_id: str
    subject: str
    track: str
    grade: str
    term: str | None = None
    week: int | None = None
    day_index: int | None = None
    topic: str | None = None
    subtopic: str | None = None
    status: str
    #: How the version came to be: `generated`, `manual`, `revised`, `document_import`, a study's.
    source_type: str | None = None
    approved_at: UtcDatetime | None = None
    approved_by: str | None = None
    created_at: UtcDatetime | None = None
    artefact_id: str | None = None
