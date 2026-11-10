from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import (
    normalize_textbook_records,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CurriculumObjectiveRef,
)
from app.shared.json_types import JsonObject


def _stripped_str_list(value: object) -> list[str]:
    """Strip+filter on a list of strings; ``[]`` if not a list.

    Local replacement for the retired ``json_coerce.as_str_list``.
    """
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _mapping_value(payload: Mapping[str, object], key: str) -> object:
    return payload.get(key)


class LessonScope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: str
    track: str
    grade: str
    term: str
    week: int
    theme: str | None = None
    topic: str
    topic_key: str | None = None
    subtopic: str
    subtopic_id: str | None = None
    duration_minutes: int | None = None


class LessonGenerationSession(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    subject: str
    track: str
    grade: str
    term: str
    week: int
    day_index: int | None = None
    topic: str
    subtopic: str
    duration_minutes: int | None = None
    session_objectives: list[str] = Field(default_factory=list)
    theme: str | None = None
    performance_objectives: list[str] = Field(default_factory=list)
    entry_behaviour: list[str] = Field(default_factory=list)
    instructional_materials: list[str] = Field(default_factory=list)
    average_age: int | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_payload(cls, value: object) -> object:
        if not isinstance(value, Mapping):
            raise TypeError("session context must be an object")
        data = dict(value)
        for key in (
            "session_id",
            "subject",
            "track",
            "grade",
            "term",
            "topic",
            "subtopic",
        ):
            data[key] = str(data.get(key) or "").strip()
        data["week"] = int(data.get("week") or 1)
        if data.get("day_index") is not None:
            data["day_index"] = int(data["day_index"])
        if data.get("duration_minutes") is not None:
            data["duration_minutes"] = int(data["duration_minutes"])
        if data.get("average_age") is not None:
            data["average_age"] = int(data["average_age"])
        for key in (
            "session_objectives",
            "performance_objectives",
            "entry_behaviour",
            "instructional_materials",
        ):
            data[key] = _stripped_str_list(data.get(key))
        theme = str(data.get("theme") or "").strip()
        data["theme"] = theme or None
        return data


class LessonCurriculumContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: str
    track: str
    grade: str
    term: str
    week: int
    theme: str | None = None
    topic: str
    subtopic: str
    curriculum_objectives: list[CurriculumObjectiveRef] = Field(default_factory=list)
    general_objectives: list[str] = Field(default_factory=list)
    session_objectives: list[str] = Field(default_factory=list)
    performance_objectives: list[str] = Field(default_factory=list)
    teacher_activities: list[str] = Field(default_factory=list)
    student_activities: list[str] = Field(default_factory=list)
    instructional_materials: list[str] = Field(default_factory=list)
    evaluation_guide: list[str] = Field(default_factory=list)
    entry_behaviour: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _normalize_payload(cls, value: object) -> object:
        if not isinstance(value, Mapping):
            raise TypeError("curriculum context must be an object")
        data = dict(value)
        for key in ("subject", "track", "grade", "term", "topic", "subtopic"):
            data[key] = str(data.get(key) or "").strip()
        data["week"] = int(data.get("week") or 1)
        theme = str(data.get("theme") or "").strip()
        data["theme"] = theme or None
        for key in (
            "general_objectives",
            "session_objectives",
            "performance_objectives",
            "teacher_activities",
            "student_activities",
            "instructional_materials",
            "evaluation_guide",
            "entry_behaviour",
        ):
            data[key] = _stripped_str_list(data.get(key))
        objectives = data.get("curriculum_objectives") or []
        if not isinstance(objectives, list):
            data["curriculum_objectives"] = []
        return data


class TextbookRecordPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: str = "textbook_record"
    record_id: str
    title: str = ""
    section_ref: str = ""
    content: str = ""
    answer_text: str = ""
    prompt_text: str = ""
    retrieval_text: str = ""
    record_type: str | None = None
    primary_subtopic_id: str | None = None
    matched_subtopic_id: str | None = None
    source_html_path: str | None = None
    source_anchor_id: str | None = None
    asset_refs: list[JsonObject] = Field(default_factory=list)
    is_primary: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_payload(cls, value: object) -> object:
        if not isinstance(value, Mapping):
            raise TypeError("textbook record must be an object")
        data = dict(value)
        record_id = str(data.get("record_id") or data.get("section_ref") or "").strip()
        if not record_id:
            raise ValueError("textbook record requires record_id or section_ref")
        data["type"] = str(data.get("type") or "textbook_record").strip() or "textbook_record"
        data["record_id"] = record_id
        data["title"] = str(data.get("title") or "").strip()
        data["section_ref"] = str(data.get("section_ref") or record_id).strip() or record_id
        for key in ("content", "answer_text", "prompt_text", "retrieval_text"):
            data[key] = str(data.get(key) or "").strip()
        for key in (
            "record_type",
            "primary_subtopic_id",
            "matched_subtopic_id",
            "source_html_path",
            "source_anchor_id",
        ):
            data[key] = str(data.get(key) or "").strip() or None
        asset_refs = data.get("asset_refs")
        data["asset_refs"] = asset_refs if isinstance(asset_refs, list) else []
        return data

    def prompt_payload(self) -> JsonObject:
        return self.model_dump(exclude_none=True)

    def preferred_text(self) -> str:
        for candidate in (
            self.content,
            self.answer_text,
            self.prompt_text,
            self.retrieval_text,
        ):
            if candidate.strip():
                return candidate
        return ""


@dataclass(frozen=True)
class PreparedGenerationInputs:
    session: LessonGenerationSession
    scope: LessonScope
    curriculum: LessonCurriculumContext
    textbook_records: list[TextbookRecordPayload]
    evidence_selection_strategy: str
    # Two-layer routing: "manual_linkage" -> authoritative curated path;
    # "curriculum_only" -> no-linkage LLM path. curated_objectives carries the
    # per-AO curated rows (role-tagged records, assessments) for the curated path.
    grounding_mode: str = "manual_linkage"
    curated_objectives: list[JsonObject] = field(default_factory=list)
    #: The lesson-plan spec's brief, which every step writer is told to follow.
    brief: ArtefactSpec | None = None

    @property
    def curriculum_objectives(self) -> list[CurriculumObjectiveRef]:
        return list(self.curriculum.curriculum_objectives)

    @property
    def scope_context(self) -> JsonObject:
        return self.scope_payload()

    @property
    def curriculum_context(self) -> JsonObject:
        return self.curriculum_payload()

    def scope_payload(self) -> JsonObject:
        return self.scope.model_dump(exclude_none=True)

    def curriculum_payload(self) -> JsonObject:
        return self.curriculum.model_dump(exclude_none=True)

    def curriculum_objective_payloads(self) -> list[JsonObject]:
        return [objective.model_dump() for objective in self.curriculum_objectives]

    def textbook_record_payloads(self) -> list[JsonObject]:
        return [record.prompt_payload() for record in self.textbook_records]


def build_curriculum_objectives(
    session_context: Mapping[str, object],
    curriculum_context: Mapping[str, object],
) -> list[CurriculumObjectiveRef]:
    source_objectives = _mapping_value(curriculum_context, "curriculum_objectives") or []
    normalized: list[CurriculumObjectiveRef] = []

    if isinstance(source_objectives, list):
        for index, item in enumerate(source_objectives, start=1):
            if isinstance(item, Mapping):
                objective_text = str(item.get("objective_text") or "").strip()
                curriculum_objective_id = str(
                    item.get("curriculum_objective_id") or f"cur_obj{index:02d}"
                ).strip()
                objective_order = item.get("objective_order") or index
            else:
                objective_text = str(item or "").strip()
                curriculum_objective_id = f"cur_obj{index:02d}"
                objective_order = index
            if not objective_text:
                continue
            normalized.append(
                CurriculumObjectiveRef(
                    curriculum_objective_id=curriculum_objective_id,
                    objective_text=objective_text,
                    objective_order=int(objective_order),
                )
            )

    if normalized:
        return normalized

    fallback_objectives = (
        _mapping_value(curriculum_context, "performance_objectives")
        or _mapping_value(session_context, "session_objectives")
        or [f"Understand {str(_mapping_value(session_context, 'subtopic') or '').strip()}"]
    )

    if not isinstance(fallback_objectives, list):
        return []

    return [
        CurriculumObjectiveRef(
            curriculum_objective_id=f"cur_obj{index:02d}",
            objective_text=str(text).strip(),
            objective_order=index,
        )
        for index, text in enumerate(fallback_objectives, start=1)
        if str(text).strip()
    ]


COLD_START_RECORD_ID = "curriculum-only"


def _synthetic_curriculum_record(
    session: LessonGenerationSession,
    curriculum_objectives: list[CurriculumObjectiveRef],
) -> JsonObject:
    """One curriculum-derived placeholder record for cold-start (no-records) subtopics.

    Lets the no-linkage path ground generation in the curriculum alone. `type`
    must be 'textbook_record' so normalize_textbook_records keeps it; `record_type`
    'exposition' makes it a concept-style record.
    """
    objective_texts = [o.objective_text for o in curriculum_objectives if o.objective_text]
    content = "\n".join(objective_texts) or f"Curriculum objectives for {session.subtopic}."
    return {
        "type": "textbook_record",
        "record_id": COLD_START_RECORD_ID,
        "section_ref": COLD_START_RECORD_ID,
        "title": session.subtopic or "Curriculum",
        "content": content,
        "record_type": "exposition",
        "is_primary": True,
    }


def build_scope_context(session: LessonGenerationSession) -> LessonScope:
    return LessonScope(
        subject=session.subject,
        track=session.track,
        grade=session.grade,
        term=session.term,
        week=session.week,
        theme=session.theme,
        topic=session.topic,
        subtopic=session.subtopic,
        duration_minutes=session.duration_minutes,
    )


def resolve_evidence_selection_strategy(
    requested_strategy: str | None,
    default_strategy: str,
) -> str:
    strategy = (requested_strategy or default_strategy).strip() or default_strategy
    if strategy in {"per_kc_rlm", "global_rlm", "cached", "deterministic"}:
        return "cached"
    if strategy:
        raise ValueError(f"unsupported lesson plan evidence selection strategy: {strategy}")
    return "cached"


def prepare_generation_inputs(
    *,
    session_context: Mapping[str, object],
    curriculum_context: Mapping[str, object],
    reference_context: Sequence[Mapping[str, object]],
    requested_strategy: str | None,
    default_strategy: str,
    grounding_mode: str = "manual_linkage",
    curated_objectives: Sequence[JsonObject] | None = None,
    brief: ArtefactSpec | None = None,
) -> PreparedGenerationInputs:
    session = LessonGenerationSession.model_validate(session_context)
    curriculum_objectives = build_curriculum_objectives(session_context, curriculum_context)
    textbook_records = [
        TextbookRecordPayload.model_validate(record)
        for record in normalize_textbook_records(reference_context)
    ]
    if not textbook_records:
        if grounding_mode == "curriculum_only":
            # Cold-start: ground in the curriculum alone via a synthetic record.
            textbook_records = [
                TextbookRecordPayload.model_validate(
                    _synthetic_curriculum_record(session, curriculum_objectives)
                )
            ]
        else:
            raise ValueError("lesson_plan_generation_requires_textbook_records")

    curriculum = LessonCurriculumContext.model_validate(
        {
            **dict(curriculum_context),
            "subject": session.subject,
            "track": session.track,
            "grade": session.grade,
            "term": session.term,
            "week": session.week,
            "theme": session.theme,
            "topic": session.topic,
            "subtopic": session.subtopic,
            "curriculum_objectives": [
                objective.model_dump() for objective in curriculum_objectives
            ],
        }
    )

    return PreparedGenerationInputs(
        session=session,
        scope=build_scope_context(session),
        curriculum=curriculum,
        textbook_records=textbook_records,
        evidence_selection_strategy=resolve_evidence_selection_strategy(
            requested_strategy,
            default_strategy,
        ),
        grounding_mode=grounding_mode,
        # Curated objectives carry the authoritative curriculum_objective_id, and the
        # plan's curriculum_objectives now expose those same ids (see
        # SessionContextPayloadBuilder._curriculum_objective_refs), so they match by
        # construction — no id remap needed.
        curated_objectives=[dict(objective) for objective in (curated_objectives or [])],
        brief=brief,
    )


def compact_json_preview(value: object, *, max_chars: int = 4000) -> str:
    try:
        text = json.dumps(value, ensure_ascii=True)
    except TypeError:
        text = repr(value)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "...<truncated>"


class RunPromptInputs(BaseModel):
    scope_context: JsonObject
    curriculum_context: JsonObject
    textbook_records: list[JsonObject]
    evidence_selection_strategy: str
    final_writer_mode: str
    dspy_status_logging: bool


class RunMetadata(BaseModel):
    """Provenance metadata persisted alongside a generated plan (run_metadata)."""

    model: str
    generated_at: str
    prompt_inputs: RunPromptInputs


def build_run_metadata(
    *,
    model_name: str,
    generated_at: str,
    inputs: PreparedGenerationInputs,
    final_writer_mode: str,
    dspy_status_logging: bool,
) -> JsonObject:
    return RunMetadata(
        model=model_name,
        generated_at=generated_at,
        prompt_inputs=RunPromptInputs(
            scope_context=inputs.scope_payload(),
            curriculum_context=inputs.curriculum_payload(),
            textbook_records=inputs.textbook_record_payloads(),
            evidence_selection_strategy=inputs.evidence_selection_strategy,
            final_writer_mode=final_writer_mode,
            dspy_status_logging=dspy_status_logging,
        ),
    ).model_dump(mode="json")
