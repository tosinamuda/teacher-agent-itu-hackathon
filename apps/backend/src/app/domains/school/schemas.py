"""School domain schemas."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from app.shared.schema_base import UtcDatetime


class ClassResponse(BaseModel):
    id: uuid.UUID
    name: str
    grade: str | None = None
    school_id: uuid.UUID | None = None
    school_name: str | None = None
    school_code: str | None = None


class SchoolResponse(BaseModel):
    id: uuid.UUID
    name: str
    school_code: str
    default_academic_year: str | None = None
    current_term: str | None = None
    created_at: UtcDatetime | None = None
    class_count: int = 0
    workspace_count: int = 0


class SchoolCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    school_code: str = Field(..., min_length=2, max_length=32)
    default_academic_year: str | None = Field(default=None, min_length=4, max_length=32)
    current_term: str | None = Field(default=None, min_length=2, max_length=32)


class SchoolUpdateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    school_code: str = Field(..., min_length=2, max_length=32)
    default_academic_year: str | None = Field(default=None, min_length=4, max_length=32)
    current_term: str | None = Field(default=None, min_length=2, max_length=32)


class GradeLevelOptionResponse(BaseModel):
    id: uuid.UUID
    name: str


class SubjectOptionResponse(BaseModel):
    id: uuid.UUID
    name: str
    code: str


class TeacherOptionResponse(BaseModel):
    id: uuid.UUID
    full_name: str | None = None
    auth_id: str
    email: str


class TeacherCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    code: str = Field(..., min_length=2, description="The teacher's short login code.")


class SchoolSetupCatalogResponse(BaseModel):
    grade_levels: list[GradeLevelOptionResponse]
    subjects: list[SubjectOptionResponse]
    teachers: list[TeacherOptionResponse]
    academic_years: list[str]
    suggested_terms: list[str]


class SchoolWorkspaceCreateRequest(BaseModel):
    school_id: uuid.UUID
    class_name: str = Field(..., min_length=1, max_length=32)
    grade_level_name: str = Field(..., min_length=1, max_length=32)
    subject_code: str = Field(..., min_length=1, max_length=16)
    term: str = Field(..., min_length=2, max_length=32)
    academic_year: str = Field(..., min_length=4, max_length=32)
    teacher_id: uuid.UUID
    is_primary: bool = False


class SchoolWorkspaceResponse(BaseModel):
    workspace_id: uuid.UUID
    term_class_subject_id: uuid.UUID
    school_id: uuid.UUID
    school_name: str
    school_code: str
    class_id: uuid.UUID
    class_name: str
    grade_level: str
    subject_name: str
    subject_code: str
    term: str
    academic_year: str
    teacher_id: uuid.UUID
    teacher_name: str | None = None
    workspace_name: str
    is_primary: bool
    created_at: UtcDatetime | None = None


class SubjectSlotRulesResponse(BaseModel):
    total_subjects: int
    compulsory_subjects: int
    field_core_subjects: int
    trade_subjects: int
    notes: list[str]


class SubjectOfferingCatalogResponse(BaseModel):
    curriculum: str | None = None
    subject_slots: SubjectSlotRulesResponse
    core_compulsory_subjects: list[str]
    fields_of_study: dict[str, list[str]]
    trade_subjects: list[str]
