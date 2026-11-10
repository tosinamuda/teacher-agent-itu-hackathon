"""Typed contracts for the experiment dataset export (protocol §8 schemas).

Flat rating rows for analysis. H1 and H2 rows share the common identity columns
(``RatingRowBase``); each adds its own rubric/dimension score columns. Source-audit
rows are a separate shape. They are returned as three separate typed lists, so this
is inheritance-based polymorphism — not a discriminated union (which would only earn
its keep for a single heterogeneous list).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class _Row(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RatingRowBase(_Row):
    experiment_id: str
    lesson_id: str
    condition_code: str | None
    packet_id: str
    rater_id: str
    synthetic: bool


class H1RatingRow(RatingRowBase):
    """One expert/synthetic H1 reading-note rating, scores flattened to columns."""

    h1_composite: float
    major_issues: list[str]
    major_issue_other: str | None
    # H1_RUBRIC criteria (1-5).
    objective_curriculum_alignment: int | None = None
    taught_lesson_alignment: int | None = None
    scope_conceptual_correctness: int | None = None
    clarity_usefulness: int | None = None
    learner_state_suitability: int | None = None
    scaffolding_appropriateness: int | None = None
    challenge_calibration: int | None = None
    misconception_support: int | None = None


class H2RatingRow(RatingRowBase):
    """One H2 rating for a single section.

    Carries the candidate (P1) pack scores and — when the rater also scored the base
    pack — the paired base (P0) scores as ``base_*`` columns, so the analyst can
    compute the P0-vs-P1 contrast per section.
    """

    focal_learner_id: str | None
    section_id: str
    packet_score: float
    # H2 section dimensions — candidate (P1, personalised) pack.
    learner_state_suitability: float | None = None
    scaffolding_appropriateness: float | None = None
    challenge_calibration: float | None = None
    misconception_support: float | None = None
    objective_preservation: float | None = None
    section_score: float | None = None
    # Paired base (P0, approved class) pack — None for legacy candidate-only rows.
    base_learner_state_suitability: float | None = None
    base_scaffolding_appropriateness: float | None = None
    base_challenge_calibration: float | None = None
    base_misconception_support: float | None = None
    base_objective_preservation: float | None = None
    base_section_score: float | None = None


class SourceAuditRow(_Row):
    """One source-grounding audit rating."""

    audit_item_id: str
    lesson_id: str
    condition_code: str | None
    generated_excerpt: str | None
    source_ref: str | None
    source_excerpt: str | None
    rater_id: str
    source_relevance: int
    support_sufficiency: int
    faithfulness: int
    scope_correctness: int
    source_grounding_score: float
    synthetic: bool


class ExperimentDataset(_Row):
    experiment_id: str
    h1_ratings: list[H1RatingRow]
    h2_ratings: list[H2RatingRow]
    source_audit: list[SourceAuditRow]
