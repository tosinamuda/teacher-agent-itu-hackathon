"""Application-layer result DTOs for experiment summaries.

These are the result of an application computation (``ExperimentApplicationService``
builds them); the api routes expose them verbatim as ``response_model``. They live
here — not in ``api/schemas`` — because the service owns the result shape, and the
HTTP layer only serialises it. ``condition_runs`` / ``focal_cases`` / ``packets`` /
``decisions`` stay ``JsonObject`` lists: their per-row shape is genuinely open.
"""

from __future__ import annotations

from pydantic import BaseModel

from app.domains.experiments.domain.types import ExecutionStatus, Hypothesis
from app.shared.json_types import JsonObject


class ExperimentResultSummary(BaseModel):
    execution_id: str
    hypothesis: Hypothesis
    attempt_number: int
    status: ExecutionStatus
    condition_run_count: int
    focal_case_count: int
    packet_count: int
    status_counts: dict[str, int]
    condition_runs: list[JsonObject]
    focal_cases: list[JsonObject]
    packets: list[JsonObject]


class C4GovernanceSummary(BaseModel):
    experiment_id: str
    total: int
    by_decision: dict[str, int]
    by_issue_category: dict[str, int]
    approval_rate: float
    regeneration_requested_rate: float
    rejection_rate: float
    total_regenerations: int
    changed_count: int
    unchanged_count: int
    mean_review_time_seconds: float | None
    decisions: list[JsonObject]
