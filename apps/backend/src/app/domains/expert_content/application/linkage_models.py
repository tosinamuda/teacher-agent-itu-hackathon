"""Pydantic models + literal aliases for the manual AO-to-textbook linkage row.

Pure type definitions — no I/O, no validation logic, no DB. The validation
helpers in ``linkage_validation`` and the inference + loader helpers in
``linkage_inference`` both import from here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domains.expert_content.domain.types import AoTextbookLinkageStatus

# Local permissive JSON-object alias used throughout the linkage workflow.
# Distinct from ``app.shared.json_types.JsonObject`` (which is strict and
# recursive); this one stays permissive so the many cast()s in the loader path
# remain trivially typed.
JsonObject = dict[str, Any]

# ----- Literal aliases (the closed-set strings that flow through the linkage row) -----

# Row status is the domain enum (``AoTextbookLinkageStatus``), not a local literal,
# so the curated rows and the ``ao_textbook_linkage`` table share one vocabulary.
LinkageRole = Literal["foundation", "instruction", "worked_example", "exercise"]
LinkageMethod = Literal["rule_type", "rule_heading", "judgment"]
BlockType = Literal["explanation", "worked_example", "practice"]
InstructionalType = Literal[
    "explain_only",
    "explain_practice",
    "explain_example_practice",
]
ReviewCategory = Literal[
    "ambiguous_record_scope",
    "ao_no_evidence",
    "candidate_new_atomic_objective",
    "no_reused_assessment",
    "corpus_gap",
    "curriculum_textbook_mismatch",
    "prerequisite_only_evidence",
]
AOEvidenceClassification = Literal["direct", "prerequisite_only", "none"]
CandidateAtomicObjectiveKind = Literal[
    "prerequisite",
    "missing_direct_objective",
    "extension_or_enrichment",
    "curriculum_textbook_mismatch",
]
CandidateAtomicObjectiveStatus = Literal["candidate_for_expert_review"]
CandidateAtomicObjectiveReviewVerdict = Literal[
    "has_candidates",
    "no_candidate_records",
    "no_source_records",
]

# ----- Constants used by the inference + prompt-rendering helpers -----

ATOMIC_OBJECTIVE_PLACEHOLDER = "{{ATOMIC_OBJECTIVES}}"
TEXTBOOK_RECORDS_PLACEHOLDER = "{{TEXTBOOK_RECORDS}}"

# BloomLevel + BLOOM_VERB_MAP previously had a parallel copy here that diverged
# from the lesson_plan domain's copy by ~14 verbs. Now sourced from
# ``app.shared.bloom_taxonomy`` so both consumers always see the same map.
# ``as`` re-export pattern keeps the public names visible to
# ``linkage_inference.py`` without ruff flagging an unused import.
from app.shared.bloom_taxonomy import (  # noqa: E402 — kept by section heading
    BLOOM_VERB_MAP as BLOOM_VERB_MAP,
)
from app.shared.bloom_taxonomy import (  # noqa: E402
    BloomLevel as BloomLevel,
)

# ----- Pydantic models -----


class StrictModel(BaseModel):
    """Base for the linkage models — ``extra='forbid'`` so unknown keys raise."""

    model_config = ConfigDict(extra="forbid")


class RecordLink(StrictModel):
    """One reviewer-accepted textbook record → atomic-objective link."""

    record_id: str = Field(..., min_length=1)
    role: LinkageRole
    method: LinkageMethod
    rationale: str | None = None

    @model_validator(mode="after")
    def _validate_rationale(self) -> RecordLink:
        if self.method == "judgment" and not (self.rationale or "").strip():
            raise ValueError("judgment links require a rationale")
        if self.method != "judgment" and self.rationale is not None:
            raise ValueError("rule-based links must use rationale=null")
        return self


class StepBlueprint(StrictModel):
    """The derived (block_types, instructional_type) for one atomic objective."""

    block_types: list[BlockType] = Field(..., min_length=1)
    instructional_type: InstructionalType

    @model_validator(mode="after")
    def _validate_consistency(self) -> StepBlueprint:
        expected_block_types = list(dict.fromkeys(self.block_types))
        if expected_block_types != self.block_types:
            raise ValueError("block_types must not contain duplicates")
        if not self.block_types or self.block_types[0] != "explanation":
            raise ValueError("block_types must start with explanation")

        has_worked_example = "worked_example" in self.block_types
        has_practice = "practice" in self.block_types
        expected_instructional_type: InstructionalType
        if has_worked_example:
            expected_instructional_type = "explain_example_practice"
        elif has_practice:
            expected_instructional_type = "explain_practice"
        else:
            expected_instructional_type = "explain_only"
        if self.instructional_type != expected_instructional_type:
            raise ValueError("instructional_type must match the derived value from block_types")
        return self


class Assessment(StrictModel):
    """Reused or LLM-grounded assessment attached to an atomic objective."""

    question: str = Field(..., min_length=1)
    expected_answer: str = Field(..., min_length=1)
    bloom_level: BloomLevel
    source_exercise_id: str | None = None
    hints: list[str] = Field(default_factory=list)
    method: Literal["reused", "llm_grounded"]

    @model_validator(mode="after")
    def _validate_method(self) -> Assessment:
        if self.method == "reused" and not (self.source_exercise_id or "").strip():
            raise ValueError("reused assessments require source_exercise_id")
        if self.method == "llm_grounded" and self.source_exercise_id is not None:
            raise ValueError("llm_grounded assessments must set source_exercise_id=null")
        return self


class ExcludedRecord(StrictModel):
    """A textbook record the reviewer explicitly excluded with a reason."""

    record_id: str = Field(..., min_length=1)
    record_type: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)


class ReviewItem(StrictModel):
    """A textbook record flagged for expert review (cannot be auto-mapped)."""

    record_id: str = Field(..., min_length=1)
    candidate_ao_ids: list[str] = Field(default_factory=list)
    candidate_roles: list[str] = Field(default_factory=list)
    issue: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)


class CategoryReason(StrictModel):
    """Free-text reason attached to a review-category flag on the row."""

    category: ReviewCategory
    reason: str = Field(..., min_length=1)


class CandidateAtomicObjective(StrictModel):
    """A proposed new atomic objective surfaced from the textbook record(s)."""

    candidate_ao_id: str = Field(..., min_length=1)
    candidate_kind: CandidateAtomicObjectiveKind
    proposed_objective_text: str = Field(..., min_length=1)
    bloom_verb: str = Field(..., min_length=1)
    bloom_level: BloomLevel
    source_record_ids: list[str] = Field(..., min_length=1)
    evidence_quote: str = Field(..., min_length=1)
    closest_existing_ao_ids: list[str] = Field(default_factory=list)
    rationale: str = Field(..., min_length=1)
    status: CandidateAtomicObjectiveStatus


class CandidateAtomicObjectiveReview(StrictModel):
    """Reviewer's verdict on the candidate-AO set for this subtopic."""

    reviewed: bool
    verdict: CandidateAtomicObjectiveReviewVerdict
    rationale: str = Field(..., min_length=1)


class AtomicObjectiveLinkage(StrictModel):
    """One atomic objective with its accepted record links + assessment + blueprint."""

    ao_id: str = Field(..., min_length=1)
    ao_order: int = Field(..., ge=1)
    curriculum_objective_id: str = Field(..., min_length=1)
    curriculum_objective_text: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    bloom_verb: str = Field(..., min_length=1)
    bloom_level: BloomLevel
    record_links: list[RecordLink] = Field(default_factory=list)
    practice_record_ids: list[str] = Field(default_factory=list)
    step_blueprint: StepBlueprint
    assessment: Assessment | None = None
    evidence_classification: AOEvidenceClassification | None = None
    review_categories: list[ReviewCategory] = Field(default_factory=list)


class ManualSubtopicLinkageRow(StrictModel):
    """The full reviewer-curated row for one subtopic — root of the linkage record."""

    subtopic_id: str = Field(..., min_length=1)
    subtopic_title: str = Field(..., min_length=1)
    status: AoTextbookLinkageStatus
    status_reasons: list[str] = Field(default_factory=list)
    shared_foundation_record_ids: list[str] = Field(default_factory=list)
    excluded_records: list[ExcludedRecord] = Field(default_factory=list)
    review_items: list[ReviewItem] = Field(default_factory=list)
    candidate_atomic_objectives: list[CandidateAtomicObjective] = Field(default_factory=list)
    candidate_atomic_objective_review: CandidateAtomicObjectiveReview | None = None
    atomic_objectives: list[AtomicObjectiveLinkage] = Field(default_factory=list)
    review_categories: list[ReviewCategory] = Field(default_factory=list)
    category_reasons: list[CategoryReason] = Field(default_factory=list)


@dataclass(frozen=True)
class ManualLinkageValidationReport:
    """Outcome of validating a ``ManualSubtopicLinkageRow`` against its source records."""

    valid: bool
    errors: list[str]
    warnings: list[str]
    total_source_records: int
    assigned_record_count: int
    shared_foundation_count: int
    excluded_record_count: int
    review_record_count: int

    def as_json(self) -> JsonObject:
        """Render the report as a JSON-serialisable dict."""
        return asdict(self)
