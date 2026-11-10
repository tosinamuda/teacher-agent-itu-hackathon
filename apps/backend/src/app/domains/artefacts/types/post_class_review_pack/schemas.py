from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import ContentBlock
from app.domains.learner_state.domain.models import ObjectiveLearnerState
from app.shared.json_types import JsonObject

ReviewPackBlock = ContentBlock

ReviewPackStepKind = Literal["core", "evaluation"]
ReviewPackStepType = Literal["explain", "example", "practice", "check", "review"]
ReviewPackStepStatus = Literal["core", "review", "skip"]


class ReviewPackLearnerContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    student_id: str = Field(..., min_length=1)
    diagnostic_id: str | None = None
    field_of_study: str | None = None
    trade_subject: str | None = None
    field_core_subjects: list[str] | None = None
    language_level: str | None = None
    pace_preference: str | None = None
    time_budget_minutes: int | None = Field(default=None, ge=1)


class ReviewPackLessonContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: str | None = None
    track: str | None = None
    grade: str | None = None
    term: str | None = None
    week: int | None = None
    topic: str | None = None
    subtopic: str | None = None
    theme: str | None = None
    entry_behaviour: list[str] = Field(default_factory=list)
    instructional_materials: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    curriculum_objectives: list[JsonObject] = Field(default_factory=list)
    lesson_plan_objectives: list[JsonObject] = Field(default_factory=list)
    misconceptions: list[str] = Field(default_factory=list)


class ReviewPackStepPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(..., min_length=1)
    step_kind: ReviewPackStepKind
    instructional_type: str | None = None
    kc_type: str | None = None
    lesson_objective_id: str | None = None
    title: str | None = None
    content: str | None = None
    estimated_minutes: int | None = Field(default=None, ge=1)
    mode: str | None = None
    teacher_activities: list[str] | None = None
    student_activities: list[str] | None = None
    type: ReviewPackStepType
    status: ReviewPackStepStatus


class ClassLevelPostClassReviewPackPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artefact_plan_id: str = Field(..., min_length=1)
    artefact_type: ArtefactType = ArtefactType.POST_CLASS_REVIEW_PACK
    scope: ArtefactScope = ArtefactScope.CLASS_LEVEL
    plan_version_id: str = Field(..., min_length=1)
    created_at: datetime
    policy: str = Field(..., min_length=1)
    lesson_context: ReviewPackLessonContext
    lesson_objective_ids: list[str] = Field(..., min_length=1)
    steps: list[ReviewPackStepPlan] = Field(..., min_length=1)

    def to_json_object(self) -> JsonObject:
        return self.model_dump(mode="json", exclude_none=True)


class LearnerLevelPostClassReviewPackPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artefact_plan_id: str = Field(..., min_length=1)
    artefact_type: ArtefactType = ArtefactType.POST_CLASS_REVIEW_PACK
    scope: ArtefactScope = ArtefactScope.LEARNER_LEVEL
    plan_version_id: str = Field(..., min_length=1)
    created_at: datetime
    policy: str = Field(..., min_length=1)
    lesson_context: ReviewPackLessonContext
    lesson_objective_ids: list[str] = Field(..., min_length=1)
    steps: list[ReviewPackStepPlan] = Field(..., min_length=1)
    learner_context: ReviewPackLearnerContext
    objective_states: list[ObjectiveLearnerState] = Field(default_factory=list)

    def to_json_object(self) -> JsonObject:
        return self.model_dump(mode="json", exclude_none=True)


class ReviewPackStep(BaseModel):
    model_config = ConfigDict(extra="ignore")

    step_id: str = Field(..., min_length=1)
    step_kind: str | None = None
    instructional_type: str | None = None
    type: str | None = None
    title: str | None = None
    estimated_minutes: int | None = None
    blocks: list[ContentBlock] = Field(default_factory=list)
    status: str | None = None
    # Objective indexing and personalisation provenance.
    lesson_objective_id: str | None = None
    personalisation_band: str | None = None


class PostClassReviewPack(BaseModel):
    model_config = ConfigDict(extra="ignore")

    artefact_id: str = Field(..., min_length=1)
    artefact_type: ArtefactType = ArtefactType.POST_CLASS_REVIEW_PACK
    scope: ArtefactScope
    plan_version_id: str = Field(..., min_length=1)
    created_at: datetime
    subject: str | None = None
    track: str | None = None
    grade: str | None = None
    term: str | None = None
    week: int | None = None
    topic: str | None = None
    subtopic: str | None = None
    curriculum_objectives: list[JsonObject] = Field(default_factory=list)
    lesson_plan_objectives: list[JsonObject] = Field(default_factory=list)
    misconceptions: list[str] = Field(default_factory=list)
    steps: list[ReviewPackStep] = Field(default_factory=list)
    metadata: JsonObject = Field(default_factory=dict)
    student_id: str | None = None
    artefact_plan_id: str | None = None
    theme: str | None = None
    entry_behaviour: list[str] = Field(default_factory=list)
    instructional_materials: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)

    def to_json_object(self) -> JsonObject:
        return self.model_dump(mode="json", exclude_none=True)
