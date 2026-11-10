"""Application-layer result DTOs for the evaluation read endpoints.

The evaluation dashboard endpoints (``experiment_statistics``,
``experiment_ratings_summary``, ``investigation_results_rollup``) return these;
the api routes expose them verbatim via ``response_model``. Computed stats
sub-structures keyed dynamically (per-condition / per-criterion / per-hypothesis)
stay ``JsonObject`` fields — genuinely dynamic JSON inside a typed envelope.
"""

from __future__ import annotations

from pydantic import BaseModel

from app.shared.json_types import JsonObject


class SourceAuditDescriptives(BaseModel):
    """Pass/partial/fail counts per criterion + mean over the audit ratings."""

    n_items: int
    n_ratings: int
    mean_score: float | None
    criteria: JsonObject


class ExperimentStatistics(BaseModel):
    """H1/H2 hypothesis test + inter-rater reliability (statistics endpoint)."""

    experiment_id: str
    synthetic: bool
    h1: JsonObject
    h2: JsonObject
    source_audit: SourceAuditDescriptives
    inter_rater: JsonObject
    notes: list[str]


class ExperimentRatingsSummary(BaseModel):
    """Rater-rating progress for one experiment (results dashboard)."""

    experiment_id: str
    packet_count: int
    rated_packet_count: int
    total_ratings: int
    distinct_raters: int
    mean_overall: float | None
    by_hypothesis: JsonObject
    synthetic: JsonObject | None


class RatingImportResult(BaseModel):
    """Outcome of a bulk offline-rating import (research-manager action)."""

    imported: int
    updated: int
    skipped: int
    errors: list[str]


class InvestigationResultsRollup(BaseModel):
    """Rater results rolled up across an investigation's experiments."""

    investigation_id: str
    experiment_count: int
    packet_count: int
    rated_packet_count: int
    total_ratings: int
    distinct_raters: int
    mean_overall: float | None
    per_experiment: list[JsonObject]
