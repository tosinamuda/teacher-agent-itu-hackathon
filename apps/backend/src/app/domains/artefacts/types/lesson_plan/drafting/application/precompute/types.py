from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from hashlib import sha256

from pydantic import BaseModel

from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.kc_compression import (
    LessonStructure,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    AtomicObjective,
    CandidateKC,
    CandidateKCPlan,
    GlobalStepSet,
    PlannerPlanStep,
    StepEvidencePlan,
)
from app.shared.json_types import JsonObject

_SLUG_RE = re.compile(r"[^a-z0-9]+")


class CacheMetadata(BaseModel):
    infrastructure_version: str
    textbook_hash: str
    curriculum_hash: str
    model_name: str | None = None
    computed_at: str


@dataclass(frozen=True)
class Violation:
    code: str
    message: str
    severity: str = "error"
    atomic_objective_id: str | None = None
    kc_id: str | None = None


@dataclass(frozen=True)
class ObjectiveContext:
    atomic_objective: AtomicObjective
    subtopic_id: str
    topic_key: str
    prior_subtopic_objectives: list[str]
    primary_records: list[JsonObject]
    evaluation_guide: list[str]
    scheduled_term: str | None = None
    scheduled_week: int | None = None
    co_scheduled_subtopic_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class KCPlanningResult:
    subtopic_id: str
    topic_key: str
    atomic_objectives: list[AtomicObjective]
    kc_plans: dict[str, CandidateKCPlan]
    step_evidence_plans: dict[str, StepEvidencePlan]
    assessment_items_by_atomic_objective: dict[str, list[AssessmentItem]]
    assessment_items: dict[str, AssessmentItem]
    lesson_structure: LessonStructure
    combined_kc_plan: CandidateKCPlan
    resolved_kcs: list[CandidateKC]
    violations_by_atomic_objective: dict[str, list[Violation]] = field(default_factory=dict)
    violations: list[Violation] = field(default_factory=list)
    from_cache: bool = False
    cache_metadata: CacheMetadata | None = None
    planning_duration_ms: int = 0
    llm_calls_planning: int = 0


@dataclass(frozen=True)
class LessonDraftResult:
    core_steps: list[PlannerPlanStep]
    global_steps: GlobalStepSet
    evidence_summaries: list[JsonObject]
    step_evidence_by_objective: dict[str, StepEvidencePlan]


@dataclass(frozen=True)
class SubtopicResult:
    planning: KCPlanningResult
    drafting: LessonDraftResult
    violations: list[Violation]
    is_valid: bool
    cached_planning: bool


@dataclass(frozen=True)
class GenerationMetrics:
    subtopic_id: str
    cached_planning: bool
    llm_calls_planning: int
    llm_calls_drafting: int
    total_llm_calls: int
    planning_duration_ms: int
    drafting_duration_ms: int
    total_duration_ms: int
    violations: int
    is_valid: bool


@dataclass(frozen=True)
class PlanningQualityRow:
    subtopic_id: str
    violations: list[Violation] = field(default_factory=list)
    atomic_objectives: list[AtomicObjective] = field(default_factory=list)


def stable_payload_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=True, default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    normalized = _SLUG_RE.sub("-", value.lower()).strip("-")
    return normalized or "unknown"


def derive_scope_keys(scope_context: Mapping[str, object]) -> tuple[str, str]:
    explicit_topic_key = str(scope_context.get("topic_key") or "").strip()
    explicit_subtopic_id = str(scope_context.get("subtopic_id") or "").strip()
    if explicit_topic_key and explicit_subtopic_id:
        return explicit_topic_key, explicit_subtopic_id

    topic_key = explicit_topic_key or slugify(str(scope_context.get("topic") or "topic"))
    subject = slugify(str(scope_context.get("subject") or "subject"))
    grade = slugify(str(scope_context.get("grade") or "grade"))
    subtopic_key = explicit_subtopic_id or slugify(str(scope_context.get("subtopic") or "subtopic"))
    if explicit_topic_key:
        return topic_key, subtopic_key
    return f"{grade}-{subject}-{topic_key}", f"{grade}-{subject}-{topic_key}-{subtopic_key}"
