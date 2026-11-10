"""What a caller following a job reads."""

from __future__ import annotations

from pydantic import BaseModel

from app.shared.json_types import JsonObject
from app.shared.schema_base import UtcDatetime


class JobStatus(BaseModel):
    """A job's progress: ``result`` once it has succeeded, ``error`` once it has not."""

    job_id: str
    kind: str
    subject: str | None
    state: str
    attempts: int
    error: str | None
    result: JsonObject | None
    created_at: UtcDatetime | None
    finished_at: UtcDatetime | None


class JobAccepted(BaseModel):
    """The job now doing what was asked; follow it at ``/jobs/{job_id}``."""

    job_id: str
