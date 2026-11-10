from __future__ import annotations

from pydantic import BaseModel, Field

from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.shared.json_types import JsonObject
from app.shared.schema_base import StrictRequest, UtcDatetime


class ArtefactResponse(BaseModel):
    artefact_id: str
    artefact_type: ArtefactType
    scope: ArtefactScope
    plan_version_id: str
    artefact_plan_id: str | None = None
    learner_id: str | None = None
    #: The student's name, where a teacher reviews their pack.
    learner_name: str | None = None
    manifest: JsonObject
    artefact_refs: JsonObject | None = None
    review_status: str | None = None
    reviewed_at: UtcDatetime | None = None
    created_at: UtcDatetime | None = None
    # Optimistic-concurrency token: the client echoes this back on approve so a stale
    # approve (the pack was revised under the teacher) is rejected with 409.
    version: int | None = None


class ArtefactApproveRequest(StrictRequest):
    reviewed_by: str | None = Field(default="teacher", min_length=1)


class ApprovePackRequest(StrictRequest):
    """Approve body — the version the teacher reviewed, for the optimistic-concurrency gate.

    Optional so non-UI callers can approve without it; the teacher UI always sends the
    version it loaded so a concurrent revise can't slip an unseen manifest past approval.
    """

    expected_version: int | None = None


class MissingPackStudentResponse(BaseModel):
    student_id: str
    full_name: str


class ReviewPackStatusResponse(BaseModel):
    """Status-only view of a learner's pack — no manifest.

    Pending pack content is never exposed to the student; this surface only
    carries whether one is awaiting review or approved.
    """

    plan_version_id: str
    review_status: str


class StudentPackGenerationStatusResponse(BaseModel):
    """One student's current generation attempt for a lesson (teacher queue).

    Distinct from ``review_status``: this is the async-generation lifecycle
    (queued / running / succeeded / failed), so the teacher can see "generating…"
    or "failed → retry" before any pack exists.
    """

    student_id: str
    full_name: str
    status: str
    attempt_number: int
    error_category: str | None = None
    produced_artefact_id: str | None = None
    updated_at: UtcDatetime | None = None


class RegenerateStudentPackRequest(StrictRequest):
    plan_version_id: str = Field(..., min_length=1)
    # Omit student_id to (re)generate every student that submitted but has no pack.
    student_id: str | None = None


class RegenerateStudentPackResponse(BaseModel):
    plan_version_id: str
    queued_student_ids: list[str]


class ArtefactExportResponse(BaseModel):
    artefact_id: str
    artefact_refs: JsonObject
