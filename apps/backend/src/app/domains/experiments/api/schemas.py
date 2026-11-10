from __future__ import annotations

import uuid
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.domains.experiments.application.result_schemas import ExperimentResultSummary
from app.domains.experiments.domain.types import (
    ConditionCode,
    ConditionRunStatus,
    ExecutionStatus,
    ExperimentLifecycleStatus,
    FocalCaseType,
    Hypothesis,
    PacketStatus,
)
from app.shared.json_types import JsonObject
from app.shared.schema_base import StrictRequest, UtcDatetime


class ExperimentCreateRequest(StrictRequest):
    # The parent study — every experiment belongs to one (one-offs use a default).
    investigation_id: str = Field(..., min_length=1)
    teacher_workspace_id: uuid.UUID
    # The experiment is created against a lesson; its own plan is authored after.
    lesson_period_id: uuid.UUID


class ExperimentReadinessResponse(BaseModel):
    lesson_approved: bool
    baseline_selected: bool
    h1_ready: bool
    base_pack_ready: bool
    base_pack_approved: bool = False
    # The C4 condition-run artefact id the teacher reviews + approves (the lesson's
    # class pack). Null before H1 has generated it. The teacher UI links to this id.
    base_pack_artefact_id: str | None = None
    # H2's base: the first draw's C3 pack, approved programmatically in C4's place.
    h2_base_pack_artefact_id: str | None = None
    h2_base_approved: bool = False
    # The lesson's newest lesson note, and whether the teacher has approved it.
    lesson_note_artefact_id: str | None = None
    lesson_note_approved: bool = False
    learner_evidence_ready: bool
    h2_ready: bool


class ExperimentHypothesisSummaryResponse(BaseModel):
    ready: bool
    execution_count: int = 0
    latest_execution_id: str | None = None
    latest_execution_status: str | None = None
    latest_attempt_number: int | None = None


class ExperimentResponse(BaseModel):
    experiment_id: str
    experiment_code: str
    teacher_workspace_id: uuid.UUID
    workspace_name: str | None = None
    teacher_id: uuid.UUID | None = None
    teacher_name: str | None = None
    school_id: uuid.UUID | None = None
    school_name: str | None = None
    school_code: str | None = None
    class_id: uuid.UUID | None = None
    class_name: str | None = None
    subject_name: str | None = None
    subject_code: str | None = None
    grade_level: str | None = None
    term: str | None = None
    academic_year: str | None = None
    # None while the experiment awaits its own teacher-authored plan.
    plan_version_id: str | None = None
    baseline_version_label: str | None = None
    baseline_approved_by: str | None = None
    lesson_period_id: uuid.UUID | None = None
    lesson_title: str | None = None
    lesson_subtitle: str | None = None
    learner_count: int = 0
    diagnostic_count: int = 0
    focal_learner_count: int = 0
    readiness: ExperimentReadinessResponse
    h1_summary: ExperimentHypothesisSummaryResponse
    h2_summary: ExperimentHypothesisSummaryResponse
    hypothesis: Hypothesis | None = None
    status: str = "created"
    lifecycle_status: ExperimentLifecycleStatus = ExperimentLifecycleStatus.ACTIVE
    ended_at: UtcDatetime | None = None
    ended_by: str | None = None
    is_sandbox: bool = False
    execution_count: int | None = None
    latest_execution_status: str | None = None
    created_at: UtcDatetime | None = None
    # Derived from the experiment's ratings: "synthetic" | "live" | "mixed" | None
    # (None = not yet evaluated). Surfaced on the experiments list.
    evaluation_mode: str | None = None
    # The parent study this experiment's lesson belongs to (containment breadcrumb).
    # None when the lesson is not scoped by any investigation.
    investigation_id: str | None = None
    investigation_code: str | None = None


class ExperimentEndRequest(StrictRequest):
    ended_by: str | None = Field(default="researcher", min_length=1)


class ExperimentSandboxRequest(StrictRequest):
    is_sandbox: bool


class ExperimentPlanFreezeRequest(StrictRequest):
    """Optional body for freezing an experiment plan.

    ``accepted_version_id`` carries the head version when the teacher ran the
    feedback-revision loop, so freeze binds the revised plan rather than the
    one bound at author time. Omitted (or null) freezes the currently-bound
    version unchanged.
    """

    accepted_version_id: str | None = Field(default=None, min_length=1)


class ExperimentManualPlanRequest(StrictRequest):
    """A teacher's hand-entered plan content for an experiment's lesson (FD-01).

    Identity + curriculum objectives are forced from the experiment's lesson; the
    ``session_plan`` carries only the entered content.
    """

    session_plan: dict
    # Optional photo of the teacher's original paper plan (provenance).
    original_document_attachment_id: str | None = None


class ExperimentPlanReuseRequest(StrictRequest):
    """An existing plan to reuse as an experiment's plan, without writing it again.

    Give the saved plan version to reuse, or the plan's content. Where the lesson has more
    than one curriculum objective, ``curriculum_choices`` names the one for each lesson
    objective, by lesson objective id.
    """

    source_plan_version_id: str | None = Field(default=None, min_length=1)
    session_plan: dict | None = None
    curriculum_choices: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _exactly_one_source(self) -> ExperimentPlanReuseRequest:
        if (self.source_plan_version_id is None) == (self.session_plan is None):
            raise ValueError("give exactly one of source_plan_version_id or session_plan")
        return self


class UnmappedObjectiveResponse(BaseModel):
    lesson_objective_id: str
    objective_text: str


class CurriculumChoiceResponse(BaseModel):
    curriculum_objective_id: str
    objective_text: str = ""


class ExperimentPlanReuseResponse(BaseModel):
    """The experiment once the plan is reused, or the choices still to make."""

    status: Literal["reused", "needs_curriculum_choice"]
    experiment: ExperimentResponse | None = None
    unmapped: list[UnmappedObjectiveResponse] = Field(default_factory=list)
    choices: list[CurriculumChoiceResponse] = Field(default_factory=list)


class ExperimentWorkspaceOptionResponse(BaseModel):
    teacher_workspace_id: uuid.UUID
    term_class_subject_id: uuid.UUID
    school_id: uuid.UUID
    school_name: str
    school_code: str
    class_id: uuid.UUID
    class_name: str
    subject_name: str
    subject_code: str
    grade_level: str
    term: str
    academic_year: str
    teacher_id: uuid.UUID
    teacher_name: str | None = None
    workspace_name: str
    is_primary: bool


class ExperimentLessonOptionResponse(BaseModel):
    lesson_period_id: uuid.UUID
    week_number: int
    period_number: int
    lesson_title: str
    lesson_subtitle: str | None = None
    approved_version_count: int = 0
    latest_approved_version_id: str | None = None
    latest_approved_version_label: str | None = None
    under_research_study: bool = False


class ExperimentApprovedVersionResponse(BaseModel):
    plan_id: str
    plan_version_id: str
    lesson_period_id: uuid.UUID | None = None
    lesson_title: str
    lesson_subtitle: str | None = None
    version_label: str
    approved_at: UtcDatetime | None = None
    approved_by: str | None = None


class ExperimentFocalLearnerOptionResponse(BaseModel):
    learner_id: str
    learner_name: str
    latest_diagnostic_id: str | None = None
    has_evidence: bool
    latest_submitted_at: UtcDatetime | None = None


class ExperimentFocalLearnerUpdateRequest(StrictRequest):
    learner_ids: list[str] = Field(..., min_length=1, max_length=8)


class ExperimentFocalLearnerSelectionResponse(BaseModel):
    experiment_id: str
    learner_ids: list[str]
    candidates: list[ExperimentFocalLearnerOptionResponse] = Field(default_factory=list)


class ExperimentConditionRunResponse(BaseModel):
    experiment_condition_run_id: str
    hypothesis: Hypothesis
    condition_code: ConditionCode
    learner_id: str | None = None
    artefact_plan_id: str | None = None
    artefact_build_job_id: str | None = None
    artefact_id: str | None = None
    status: ConditionRunStatus
    error_message: str | None = None


class ExperimentFocalCaseResponse(BaseModel):
    experiment_focal_case_id: str
    learner_id: str
    focal_case_type: FocalCaseType
    # The band (above) and the misconceptions (here) are separate tags: a learner can
    # sit in the ``extend`` band yet still carry a misconception.
    misconception_codes: list[str] = []
    learner_state_snapshot: JsonObject
    selection_metadata: JsonObject | None = None


class EvaluationPacketResponse(BaseModel):
    evaluation_packet_id: str
    packet_code: str
    hypothesis: Hypothesis
    status: PacketStatus
    primary_condition_run_id: str
    experiment_focal_case_id: str | None = None
    export_refs: JsonObject | None = None
    condition_run_ids: list[str]


class EvaluationPacketExportResponse(BaseModel):
    execution_id: str
    hypothesis: Hypothesis
    packet_count: int
    packets: list[EvaluationPacketResponse] = Field(default_factory=list)


class ExperimentExecutionCreateRequest(StrictRequest):
    hypothesis: Hypothesis
    runtime_snapshot: JsonObject | None = None


class ExperimentExecutionResponse(BaseModel):
    execution_id: str
    experiment_id: str
    hypothesis: Hypothesis
    attempt_number: int
    status: ExecutionStatus
    runtime_snapshot: JsonObject | None = None
    error_message: str | None = None
    # Structured failure category (inputs_missing / persistence / generation),
    # set by the worker. Null unless the execution failed. The UI maps this to
    # a friendly message instead of parsing ``error_message``.
    error_category: str | None = None
    created_at: UtcDatetime | None = None
    updated_at: UtcDatetime | None = None
    condition_runs: list[ExperimentConditionRunResponse] = Field(default_factory=list)
    focal_cases: list[ExperimentFocalCaseResponse] = Field(default_factory=list)
    packets: list[EvaluationPacketResponse] = Field(default_factory=list)


class ExperimentDetailResponse(BaseModel):
    experiment: ExperimentResponse
    executions: list[ExperimentExecutionResponse]
    focal_learner_candidates: list[ExperimentFocalLearnerOptionResponse] = Field(
        default_factory=list
    )
    selected_focal_learners: list[ExperimentFocalLearnerOptionResponse] = Field(
        default_factory=list
    )
    latest_summary: ExperimentResultSummary | None = None


# --- Experiment Story (pipeline reconstructed from the generation log) ---


class ExperimentStoryStage(BaseModel):
    """One pipeline step of an experiment, with its generation-log trace (if any)."""

    key: str
    title: str
    llm: bool
    correlation_ids: list[str] = Field(default_factory=list)
    event_count: int = 0
    note: str | None = None


class ExperimentStoryCurriculum(BaseModel):
    """The scheme-of-work context a lesson sits in (the teacher's starting point)."""

    subject: str | None = None
    grade: str | None = None
    term: str | None = None
    week: str | int | None = None
    topic: str | None = None
    subtopic: str | None = None


class ExperimentStoryResponse(BaseModel):
    """An experiment's pipeline as an ordered, log-traceable story."""

    experiment_id: str
    plan_version_id: str
    lesson_title: str | None = None
    curriculum: ExperimentStoryCurriculum | None = None
    lesson_plan: JsonObject | None = None
    stages: list[ExperimentStoryStage]


# --- Investigations (the study: explicit parent of its experiments) ---


class InvestigationCreateRequest(StrictRequest):
    title: str = Field(..., min_length=1)
    description: str | None = None


class InvestigationEndRequest(StrictRequest):
    ended_by: str | None = Field(default="researcher", min_length=1)


class InvestigationSummaryResponse(BaseModel):
    investigation_id: str
    investigation_code: str
    title: str
    description: str | None = None
    status: str
    experiment_count: int = 0
    ended_at: UtcDatetime | None = None
    ended_by: str | None = None
    created_at: UtcDatetime | None = None


class InvestigationExperimentRow(BaseModel):
    """One member experiment of a study, projected for the study dashboard."""

    experiment_id: str
    experiment_code: str
    lesson_period_id: uuid.UUID | None = None
    lesson_title: str | None = None
    lesson_subtitle: str | None = None
    week_number: int | None = None
    period_number: int | None = None
    school_name: str | None = None
    class_name: str | None = None
    subject_name: str | None = None
    grade_level: str | None = None
    term: str | None = None
    plan_version_id: str | None = None
    status: str = "created"
    lifecycle_status: str = "active"
    is_sandbox: bool = False


class InvestigationDetailResponse(InvestigationSummaryResponse):
    experiments: list[InvestigationExperimentRow] = Field(default_factory=list)
