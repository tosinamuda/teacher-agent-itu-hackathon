from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from app.shared.experiment_enums import FocalCaseType, Hypothesis, PacketStatus
from app.shared.json_types import JsonObject
from app.shared.schema_base import AuditScore, LikertScore, StrictRequest, UtcDatetime


class EvaluationRaterSessionRequest(StrictRequest):
    display_name: str = Field(..., min_length=2, max_length=128)


class EvaluationRaterResponse(BaseModel):
    rater_id: str
    display_name: str
    created_at: UtcDatetime | None = None
    updated_at: UtcDatetime | None = None


class EvaluationRubricCriterionResponse(BaseModel):
    criterion_id: str
    label: str
    # Teacher-friendly alias shown to raters; falls back to ``label``.
    display_label: str = ""
    description: str
    scale_min: int
    scale_max: int


class EvaluationMetaResponse(BaseModel):
    institution_name: str
    study_title: str
    textbook_name: str


class EvaluationMajorIssueFlagResponse(BaseModel):
    key: str
    label: str
    description: str = ""


class EvaluationObjectiveResponse(BaseModel):
    lesson_objective_id: str
    objective_text: str | None = None


class EvaluationReferenceSheetResponse(BaseModel):
    subject: str | None = None
    grade: str | None = None
    term: str | None = None
    week: int | None = None
    topic: str | None = None
    subtopic: str | None = None
    theme: str | None = None
    curriculum_objectives: list[str] = Field(default_factory=list)
    # Her previous-knowledge line, so the rater can see what the lesson assumed.
    entry_behaviour: list[str] = Field(default_factory=list)
    # One line per core step: the objective it taught, her activities in her own
    # words, and the work it set — so the rater can judge the pack against the
    # taught arc, not against a list of titles.
    lesson_sequence: list[str] = Field(default_factory=list)
    instructional_materials: list[str] = Field(default_factory=list)
    # The questions she assessed the lesson with. Rated against for assessment
    # congruence; the rubric says that reproducing them alone is not alignment.
    evaluation: list[str] = Field(default_factory=list)
    # Textbook references are intentionally absent from the rater-facing sheet
    # (Final Evaluation Protocol) — they live in the source-grounding audit.


class EvaluationReviewPackResponse(BaseModel):
    scope: str
    manifest: JsonObject


class EvaluationLearnerStateCardResponse(BaseModel):
    focal_case_type: FocalCaseType
    curriculum_profile: JsonObject | None = None
    preferences: JsonObject | None = None
    mastered_sections: list[JsonObject] = Field(default_factory=list)
    objective_states: list[JsonObject] = Field(default_factory=list)
    # Session-level Interest/Affect (1-5) from the post-class survey.
    session_survey: JsonObject | None = None
    selection_metadata: JsonObject | None = None


class EvaluationBlindedPackResponse(BaseModel):
    """One anonymous candidate's pack content — manifest only, no scope/role labels."""

    manifest: JsonObject


class EvaluationBlindedCandidateResponse(BaseModel):
    """An anonymous rateable candidate: stable id + blinded label, no condition."""

    candidate_id: str
    label: str
    display_order: int
    pack: EvaluationBlindedPackResponse


class EvaluationH2SectionContextResponse(BaseModel):
    section_id: str
    step_id: str
    title: str | None = None
    step_kind: str | None = None
    instructional_type: str | None = None
    lesson_objective_id: str
    objective_text: str | None = None
    # Per-candidate step content keyed by candidate_id; None when that candidate
    # has no section for this objective (the rater penalises the lesson-goal score).
    candidate_steps: dict[str, JsonObject | None] = Field(default_factory=dict)


class EvaluationRatingResponse(BaseModel):
    rating_id: str
    evaluation_packet_id: str
    rater_id: str
    hypothesis: Hypothesis
    overall_score: float
    rubric_scores: dict[str, float | None] = Field(default_factory=dict)
    section_scores: JsonObject | None = None
    diagnostic_scores: JsonObject | None = None
    notes: JsonObject | None = None
    created_at: UtcDatetime | None = None
    updated_at: UtcDatetime | None = None
    submitted_at: UtcDatetime | None = None


class EvaluationPacketQueueItemResponse(BaseModel):
    evaluation_packet_id: str
    packet_code: str
    hypothesis: Hypothesis
    status: PacketStatus
    created_at: UtcDatetime | None = None
    rating: EvaluationRatingResponse | None = None
    # H1 blinding: the anonymous per-lesson label ("Candidate A…D") and an opaque
    # lesson-group key so the queue can render lesson blocks. None for H2.
    candidate_label: str | None = None
    group_key: str | None = None


class H1PacketDetailResponse(BaseModel):
    evaluation_packet_id: str
    packet_code: str
    hypothesis: Hypothesis
    status: PacketStatus
    # Blinded position in the lesson block ("Candidate B" of candidate_count).
    candidate_label: str | None = None
    candidate_count: int = 0
    lesson_title: str | None = None
    lesson_subtitle: str | None = None
    objectives: list[EvaluationObjectiveResponse] = Field(default_factory=list)
    reference_sheet: EvaluationReferenceSheetResponse
    candidate_pack: EvaluationReviewPackResponse
    rubric: list[EvaluationRubricCriterionResponse] = Field(default_factory=list)
    # Shown beside the rubric, on every H1 rating surface alike (see constants).
    rating_guidance: list[str] = Field(default_factory=list)
    major_issue_flags: list[EvaluationMajorIssueFlagResponse] = Field(default_factory=list)
    existing_rating: EvaluationRatingResponse | None = None


class H2PacketDetailResponse(BaseModel):
    """Blinded H2 detail: anonymous candidates in randomised per-rater order.

    No P0/P1/base/personalised labels anywhere — the candidate -> condition mapping
    stays server-side (Protocol §4 blinding).
    """

    evaluation_packet_id: str
    packet_code: str
    hypothesis: Hypothesis
    status: PacketStatus
    lesson_title: str | None = None
    lesson_subtitle: str | None = None
    objectives: list[EvaluationObjectiveResponse] = Field(default_factory=list)
    focal_learner: EvaluationLearnerStateCardResponse
    candidates: list[EvaluationBlindedCandidateResponse] = Field(default_factory=list)
    sections: list[EvaluationH2SectionContextResponse] = Field(default_factory=list)
    rubric: list[EvaluationRubricCriterionResponse] = Field(default_factory=list)
    existing_rating: EvaluationRatingResponse | None = None


class H1PacketRatingSaveRequest(StrictRequest):
    rubric_scores: dict[str, int] = Field(default_factory=dict)
    notes: JsonObject | None = None


class H2SectionRatingSaveRequest(StrictRequest):
    section_id: str = Field(..., min_length=1)
    learner_state_suitability: LikertScore
    scaffolding_appropriateness: LikertScore
    challenge_calibration: LikertScore
    misconception_support: LikertScore | None = None
    objective_preservation: LikertScore


class H2CandidateScoresSaveRequest(StrictRequest):
    """One anonymous candidate's full set of section scores (blinded save path)."""

    candidate_id: str = Field(..., min_length=1)
    section_scores: list[H2SectionRatingSaveRequest] = Field(..., min_length=1)


class H2PacketRatingSaveRequest(StrictRequest):
    # Blinded save path: scores keyed by anonymous candidate_id — must cover every
    # candidate in the packet; the backend de-anonymises to P0/P1 server-side.
    candidate_section_scores: list[H2CandidateScoresSaveRequest] | None = None
    # Legacy path (old clients / archived payloads): candidate (P1) section scores...
    section_scores: list[H2SectionRatingSaveRequest] | None = None
    # ...and optional base (P0) scores covering the same sections.
    base_section_scores: list[H2SectionRatingSaveRequest] | None = None
    notes: JsonObject | None = None


class BlindingKeyRowResponse(BaseModel):
    """RESEARCHER-ONLY: one candidate-label -> condition fact for one rater's view."""

    rater_id: str
    rater_name: str
    hypothesis: str
    group: str
    packet_code: str
    evaluation_packet_id: str
    candidate_label: str
    condition_code: str


# --- Offline (bulk) rating import ---


class RatingImportRow(BaseModel):
    packet_code: str = Field(..., min_length=1)
    rater_name: str = Field(..., min_length=2)
    overall_score: float = Field(..., ge=0)
    rubric_scores: dict[str, float] = Field(default_factory=dict)
    notes: str | None = None


class RatingImportRequest(StrictRequest):
    ratings: list[RatingImportRow] = Field(..., min_length=1)


# --- Source-grounding audit (C2-C4) ---


class SourceAuditBuildResponse(BaseModel):
    created: int
    dropped: int
    skipped_executions: int


class SourceAuditQueueItemResponse(BaseModel):
    audit_item_id: str
    condition_code: str
    lesson_objective_id: str | None = None
    objective_text: str | None = None
    source_ref: str | None = None
    status: str
    rated: bool = False


class SourceAuditRatingResponse(BaseModel):
    rating_id: str
    source_relevance: int
    support_sufficiency: int
    faithfulness: int
    scope_correctness: int
    source_grounding_score: float
    submitted_at: UtcDatetime | None = None


class SourceAuditItemDetailResponse(BaseModel):
    audit_item_id: str
    condition_code: str
    lesson_objective_id: str | None = None
    objective_text: str | None = None
    generated_excerpt: str
    source_ref: str | None = None
    source_record_id: str | None = None
    source_excerpt: str | None = None
    scope_boundary: str | None = None
    criteria: list[EvaluationRubricCriterionResponse] = Field(default_factory=list)
    existing_rating: SourceAuditRatingResponse | None = None


class SourceAuditRatingSaveRequest(StrictRequest):
    source_relevance: AuditScore
    support_sufficiency: AuditScore
    faithfulness: AuditScore
    scope_correctness: AuditScore
    notes: JsonObject | None = None


# --- Rater assignments (Phase H) ---


class RaterAssignmentH1Request(StrictRequest):
    """Assign one rater to one H1 lesson — expands to all C0–C3 packets."""

    rater_id: str = Field(..., min_length=1)
    lesson_period_id: uuid.UUID


class RaterAssignmentH2Request(StrictRequest):
    """Assign one rater to one H2 focal learner — expands to P0+P1 packets."""

    rater_id: str = Field(..., min_length=1)
    focal_case_id: str = Field(..., min_length=1)


class RaterAssignmentBundleRequest(StrictRequest):
    """Assign one rater to the experiment's whole scope (lesson + all focal cases)."""

    rater_id: str = Field(..., min_length=1)
    # Also assign them as a primary auditor on every audit item (caps permitting).
    include_audit: bool = False


class RaterAssignmentBundleResponse(BaseModel):
    experiment_id: str
    rater_id: str
    h1_assigned: int
    h2_assigned: int
    audit_assigned: int


class RaterAssignmentAuditRequest(StrictRequest):
    """Assign one rater to one source-audit item; ``is_adjudicator`` sets the slot."""

    rater_id: str = Field(..., min_length=1)
    is_adjudicator: bool = False


class RaterAssignmentResponse(BaseModel):
    assignment_id: str
    experiment_id: str
    rater_id: str
    hypothesis: str
    scope_id: str
    is_adjudicator: bool


class MyQueueLineResponse(BaseModel):
    assignment_id: str
    hypothesis: str
    scope_id: str
    is_adjudicator: bool


class MyQueueResponse(BaseModel):
    rater_id: str
    h1: list[MyQueueLineResponse] = Field(default_factory=list)
    h2: list[MyQueueLineResponse] = Field(default_factory=list)
    audit: list[MyQueueLineResponse] = Field(default_factory=list)


# --- Per-experiment assignment picker (Phase J) ---


class AssignedRaterResponse(BaseModel):
    """One rater currently holding a slot.

    The assignment id is carried so the UI can later add a remove action
    without re-resolving the (rater, scope) pair.
    """

    assignment_id: str
    rater_id: str
    display_name: str
    is_adjudicator: bool = False


class H1AssignmentSlotResponse(BaseModel):
    """The single H1 slot for an experiment — one lesson, up to 3 raters."""

    lesson_period_id: str
    lesson_title: str | None = None
    raters: list[AssignedRaterResponse] = Field(default_factory=list)
    capacity: int


class H2AssignmentSlotResponse(BaseModel):
    """One H2 focal case — up to 3 raters cover its P0+P1 pair."""

    focal_case_id: str
    student_id: str
    student_full_name: str | None = None
    focal_case_type: str
    raters: list[AssignedRaterResponse] = Field(default_factory=list)
    capacity: int


class AuditAssignmentSlotResponse(BaseModel):
    """One source-audit item — 2 raters + 1 optional adjudicator."""

    audit_item_id: str
    raters: list[AssignedRaterResponse] = Field(default_factory=list)
    adjudicators: list[AssignedRaterResponse] = Field(default_factory=list)
    capacity: int
    adjudicator_capacity: int


class ExperimentAssignmentsResponse(BaseModel):
    """Every assignment slot for one experiment, grouped by hypothesis."""

    experiment_id: str
    h1: H1AssignmentSlotResponse | None = None
    h2: list[H2AssignmentSlotResponse] = Field(default_factory=list)
    audit: list[AuditAssignmentSlotResponse] = Field(default_factory=list)
