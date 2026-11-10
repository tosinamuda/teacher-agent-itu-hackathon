"""Persistence-neutral records crossing evaluation application boundaries."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from app.domains.evaluation.domain.types import AuditItemStatus
from app.shared.experiment_enums import PacketStatus
from app.shared.json_types import JsonObject, JsonValue


@dataclass(frozen=True)
class RaterIdentity:
    id: uuid.UUID
    rater_id: str
    display_name: str
    user_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class EvaluationPacketRecord:
    id: uuid.UUID
    evaluation_packet_id: str
    execution_db_id: uuid.UUID
    packet_code: str
    hypothesis: str
    status: PacketStatus
    primary_condition_run_id: str
    experiment_focal_case_id: str | None
    export_refs: JsonObject | None
    condition_run_ids: tuple[str, ...]
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class RatingRecord:
    id: uuid.UUID
    rating_id: str
    evaluation_packet_db_id: uuid.UUID
    rater_db_id: uuid.UUID
    hypothesis: str
    overall_score: float
    rubric_scores: dict[str, float | None]
    section_scores: JsonValue | None
    diagnostic_scores: JsonObject | None
    notes: JsonObject | None
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None


@dataclass(frozen=True)
class AssignmentRecord:
    id: uuid.UUID
    assignment_id: str
    experiment_db_id: uuid.UUID
    rater_db_id: uuid.UUID
    hypothesis: str
    scope_id: str
    is_adjudicator: bool
    assigned_by: str | None
    created_at: datetime


@dataclass(frozen=True)
class AuditItemRecord:
    id: uuid.UUID
    audit_item_id: str
    execution_db_id: uuid.UUID
    condition_run_id: str
    condition_code: str
    lesson_id: str | None
    lesson_objective_id: str | None
    objective_text: str | None
    generated_excerpt: str
    source_ref: str | None
    source_record_id: str | None
    source_excerpt: str | None
    figure_url: str | None
    figure_caption: str | None
    scope_boundary: str | None
    status: AuditItemStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class AuditRatingRecord:
    id: uuid.UUID
    rating_id: str
    audit_item_db_id: uuid.UUID
    rater_db_id: uuid.UUID
    source_relevance: int
    support_sufficiency: int
    faithfulness: int
    scope_correctness: int
    source_grounding_score: float
    notes: JsonObject | None
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None
