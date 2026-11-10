"""Learner domain schemas."""

from __future__ import annotations

import uuid

from pydantic import AliasChoices, BaseModel, Field

from app.shared.schema_base import UtcDatetime


class LearnerCreateRequest(BaseModel):
    student_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("student_id", "learner_id"),
    )
    code: str
    full_name: str = Field(..., min_length=1)
    grade: str = Field(..., min_length=1)
    track: str = Field(..., min_length=1)
    class_id: str | None = Field(default=None, min_length=1)
    field_of_study: str | None = Field(default=None, min_length=1)
    trade_subject: str | None = Field(default=None, min_length=1)
    field_core_subjects: list[str] | None = None
    language_level: str | None = Field(default=None, min_length=1)
    pace_preference: str | None = Field(default=None, min_length=1)
    time_budget_minutes: int | None = None


class LearnerUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=1)
    code: str | None = Field(default=None, min_length=1)
    grade: str | None = Field(default=None, min_length=1)
    track: str | None = Field(default=None, min_length=1)
    class_id: str | None = Field(default=None, min_length=1)
    field_of_study: str | None = Field(default=None, min_length=1)
    trade_subject: str | None = Field(default=None, min_length=1)
    field_core_subjects: list[str] | None = None
    language_level: str | None = Field(default=None, min_length=1)
    pace_preference: str | None = Field(default=None, min_length=1)
    time_budget_minutes: int | None = None


class LearnerResponse(BaseModel):
    student_id: str
    code: str | None = None
    full_name: str
    grade: str
    track: str
    class_id: uuid.UUID | str | None = None
    class_name: str | None = None
    field_of_study: str | None = None
    trade_subject: str | None = None
    field_core_subjects: list[str] | None = None
    language_level: str | None = None
    pace_preference: str | None = None
    time_budget_minutes: int | None = None
    created_at: UtcDatetime | None = None


class PaginatedLearnerResponse(BaseModel):
    data: list[LearnerResponse]
    total: int
    page: int
    page_size: int
