"""Response models for the admin ops panel."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RunnerInfo(BaseModel):
    runner: str
    online: bool
    slots: int
    running: int
    started_at: str | None
    seen_at: str | None


class OpsHealthResponse(BaseModel):
    """Whether jobs are being run: the runners seen, and what is waiting on them.

    A rising ``oldest_queued_age_seconds`` with no runner online means nothing is taking
    jobs; with one online and every slot full, it means the runners are busy.
    """

    runners: list[RunnerInfo]
    counts: dict[str, int]
    oldest_queued_age_seconds: float | None
    slots_per_runner: int


class JobRow(BaseModel):
    job_id: str
    kind: str
    subject: str | None
    state: str
    attempts: int
    runner: str | None
    last_error: str | None
    created_at: str | None
    started_at: str | None
    finished_at: str | None


class ExecutionRow(BaseModel):
    execution_id: str
    experiment_id: str
    experiment_code: str
    hypothesis: str
    status: str
    attempt_number: int
    error_category: str | None
    error_message: str | None
    created_at: str | None
    updated_at: str | None


class OpsActionResponse(BaseModel):
    ok: bool
    detail: str | None = None
    execution_id: str | None = None
    status: str | None = None
    cancelled_job_ids: list[str] = Field(default_factory=list)
