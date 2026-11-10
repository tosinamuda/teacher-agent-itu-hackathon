from __future__ import annotations

from dataclasses import dataclass

import dspy
from dspy import Prediction
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.shared.json_types import JsonObject

from ....application.precompute.types import ObjectiveContext
from ....domain.textbook import textbook_record_id
from ....schemas.session_plan import CandidateKC, CandidateKCPlan
from ..signatures.kc_extraction import ExtractKCsSignature

_VALID_KC_TYPES = {"concept", "procedure", "representation"}
_KC_TYPE_ALIASES = {
    "definition": "concept",
    "fact": "concept",
    "idea": "concept",
    "principle": "concept",
    "skill": "procedure",
    "method": "procedure",
    "algorithm": "procedure",
    "process": "procedure",
    "notation": "representation",
    "diagram": "representation",
    "model": "representation",
    "visual": "representation",
}


def _coerce_kc_type(raw: str) -> str:
    """Map an LLM-produced kc_type onto the schema's allowed values.

    The extractor occasionally emits near-synonyms (e.g. 'definition') that are
    not in the CandidateKC Literal. Map known synonyms; default unknowns to
    'concept' so a single off-vocabulary token never fails the whole plan.
    """
    value = str(raw or "").strip().lower()
    if value in _VALID_KC_TYPES:
        return value
    return _KC_TYPE_ALIASES.get(value, "concept")


class _ExtractKCsView(BaseModel):
    """Typed Pydantic view of an ExtractKCs DSPy prediction.

    Replaces the previous mix of ``as_str_list`` / ``_nested_*_lists`` /
    ``getattr(prediction, ...)`` defensive narrowing scattered across the
    consumer methods. The signature itself already declares the
    OutputFields as ``list[str]`` / ``list[list[str]]`` / etc. — this view
    is the boundary-time validation that strips empties and coerces
    misshapen LLM output once, so downstream consumers read typed fields
    instead of re-narrowing per call site.

    The before-validators reproduce the exact behaviour of the old
    ``json_coerce`` helpers: filter empties on flat string lists (driver
    + positional lists), strip + filter on nested lists, integer coercion
    on the prerequisite indices. No new behaviour is introduced here; this
    is purely a structural refactor to retire ``json_coerce``.
    """

    model_config = ConfigDict(extra="ignore")

    knowledge_names: list[str] = Field(default_factory=list)
    knowledge_descriptions: list[str] = Field(default_factory=list)
    knowledge_types: list[str] = Field(default_factory=list)
    knowledge_bloom_levels: list[str] = Field(default_factory=list)
    knowledge_focuses: list[str] = Field(default_factory=list)
    exercise_record_ids: list[str] = Field(default_factory=list)
    knowledge_source_record_ids: list[list[str]] = Field(default_factory=list)
    knowledge_prerequisite_indices: list[list[int]] = Field(default_factory=list)
    knowledge_is_prior: list[bool] = Field(default_factory=list)

    @field_validator(
        "knowledge_names",
        "knowledge_descriptions",
        "knowledge_types",
        "knowledge_bloom_levels",
        "knowledge_focuses",
        "exercise_record_ids",
        mode="before",
    )
    @classmethod
    def _strip_and_drop_empty(cls, raw: object) -> list[str]:
        if not isinstance(raw, list):
            return []
        return [str(item).strip() for item in raw if str(item).strip()]

    @field_validator("knowledge_source_record_ids", mode="before")
    @classmethod
    def _nested_strip_and_drop_empty(cls, raw: object) -> list[list[str]]:
        if not isinstance(raw, list):
            return []
        nested: list[list[str]] = []
        for item in raw:
            if not isinstance(item, list):
                nested.append([])
                continue
            nested.append([str(entry).strip() for entry in item if str(entry).strip()])
        return nested

    @field_validator("knowledge_prerequisite_indices", mode="before")
    @classmethod
    def _coerce_nested_int_lists(cls, raw: object) -> list[list[int]]:
        if not isinstance(raw, list):
            return []
        nested: list[list[int]] = []
        for item in raw:
            if not isinstance(item, list):
                nested.append([])
                continue
            values: list[int] = []
            for entry in item:
                if not isinstance(entry, (int, float, str)):
                    continue
                try:
                    values.append(int(entry))
                except (TypeError, ValueError):
                    continue
            nested.append(values)
        return nested

    @field_validator("knowledge_is_prior", mode="before")
    @classmethod
    def _coerce_bool_list(cls, raw: object) -> list[bool]:
        if not isinstance(raw, list):
            return []
        return [bool(item) for item in raw]

    @classmethod
    def from_prediction(cls, prediction: Prediction) -> _ExtractKCsView:
        """Pull the OutputField values off a DSPy Prediction into the typed view."""
        return cls.model_validate(
            {field: getattr(prediction, field, None) for field in cls.model_fields}
        )


@dataclass(frozen=True)
class TextbookRecordSummary:
    record_id: str
    record_type: str
    content: str

    def to_prompt_object(self) -> JsonObject:
        return {
            "record_id": self.record_id,
            "record_type": self.record_type,
            "content": self.content,
        }


@dataclass(frozen=True)
class KCExtractionDraft:
    ordinal: int
    kc_name: str
    objective_text: str
    kc_type: str
    bloom_level: str
    kc_focus: str
    supporting_record_ids: list[str]
    prerequisite_indices: list[int]
    is_prior_knowledge: bool


class KCExtractor(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.extract = dspy.ChainOfThought(ExtractKCsSignature)
        self.last_llm_calls = 0

    def forward(self, *, objective_context: ObjectiveContext) -> CandidateKCPlan:
        self.last_llm_calls = 1
        record_summaries = self._record_summaries(objective_context.primary_records)
        prediction = self.extract(
            objective_text=objective_context.atomic_objective.objective_text,
            target_bloom_level=objective_context.atomic_objective.bloom_level,
            prior_objectives=objective_context.prior_subtopic_objectives,
            textbook_records=[summary.to_prompt_object() for summary in record_summaries],
        )
        return self._build_candidate_kc_plan(
            prediction=prediction,
            objective_context=objective_context,
        )

    def _record_summaries(
        self,
        textbook_records: list[JsonObject],
    ) -> list[TextbookRecordSummary]:
        summaries: list[TextbookRecordSummary] = []
        for record in textbook_records:
            record_id = textbook_record_id(record)
            if not record_id:
                continue
            summaries.append(
                TextbookRecordSummary(
                    record_id=record_id,
                    record_type=str(record.get("record_type") or "").strip() or "unknown",
                    content=(
                        str(record.get("content") or "").strip()
                        or str(record.get("answer_text") or "").strip()
                        or str(record.get("prompt_text") or "").strip()
                        or str(record.get("retrieval_text") or "").strip()
                    ),
                )
            )
        return summaries

    def _build_candidate_kc_plan(
        self,
        *,
        prediction: Prediction,
        objective_context: ObjectiveContext,
    ) -> CandidateKCPlan:
        view = _ExtractKCsView.from_prediction(prediction)
        available_record_ids = self._available_record_ids(objective_context.primary_records)
        exercise_record_ids = [
            record_id for record_id in view.exercise_record_ids if record_id in available_record_ids
        ]
        kc_drafts = self._read_kc_drafts(
            view=view,
            objective_context=objective_context,
            available_record_ids=available_record_ids,
            exercise_record_ids=exercise_record_ids,
        )
        if not kc_drafts:
            return self._fallback_plan(
                objective_context=objective_context,
                available_record_ids=available_record_ids,
                exercise_record_ids=exercise_record_ids,
            )

        candidate_kcs = [
            self._build_candidate_kc(
                draft=draft,
                objective_context=objective_context,
                total_kcs=len(kc_drafts),
            )
            for draft in kc_drafts
        ]
        return CandidateKCPlan.model_validate(
            {"candidate_kcs": [candidate_kc.model_dump() for candidate_kc in candidate_kcs]}
        )

    def _available_record_ids(self, textbook_records: list[JsonObject]) -> set[str]:
        return {
            record_id for record in textbook_records if (record_id := textbook_record_id(record))
        }

    def _read_kc_drafts(
        self,
        *,
        view: _ExtractKCsView,
        objective_context: ObjectiveContext,
        available_record_ids: set[str],
        exercise_record_ids: list[str],
    ) -> list[KCExtractionDraft]:
        if not view.knowledge_names:
            return []

        knowledge_names = view.knowledge_names
        knowledge_descriptions = view.knowledge_descriptions
        knowledge_types = view.knowledge_types
        knowledge_bloom_levels = view.knowledge_bloom_levels
        knowledge_source_record_ids = view.knowledge_source_record_ids
        knowledge_prerequisite_indices = view.knowledge_prerequisite_indices
        knowledge_focuses = view.knowledge_focuses
        knowledge_is_prior = view.knowledge_is_prior

        return [
            KCExtractionDraft(
                ordinal=index,
                kc_name=kc_name,
                objective_text=self._objective_text_for_kc(
                    knowledge_descriptions=knowledge_descriptions,
                    index=index,
                    objective_context=objective_context,
                ),
                kc_type=self._kc_type_for_kc(knowledge_types=knowledge_types, index=index),
                bloom_level=self._bloom_level_for_kc(
                    knowledge_bloom_levels=knowledge_bloom_levels,
                    index=index,
                    objective_context=objective_context,
                ),
                kc_focus=self._focus_for_kc(
                    knowledge_focuses=knowledge_focuses, index=index, kc_name=kc_name
                ),
                supporting_record_ids=self._supporting_record_ids_for_kc(
                    knowledge_source_record_ids=knowledge_source_record_ids,
                    index=index,
                    available_record_ids=available_record_ids,
                    exercise_record_ids=exercise_record_ids,
                ),
                prerequisite_indices=(
                    knowledge_prerequisite_indices[index - 1]
                    if index - 1 < len(knowledge_prerequisite_indices)
                    else []
                ),
                is_prior_knowledge=(
                    bool(knowledge_is_prior[index - 1])
                    if index - 1 < len(knowledge_is_prior)
                    else False
                ),
            )
            for index, kc_name in enumerate(knowledge_names, start=1)
        ]

    def _objective_text_for_kc(
        self,
        *,
        knowledge_descriptions: list[str],
        index: int,
        objective_context: ObjectiveContext,
    ) -> str:
        if index - 1 < len(knowledge_descriptions) and knowledge_descriptions[index - 1]:
            return knowledge_descriptions[index - 1]
        return objective_context.atomic_objective.objective_text

    def _kc_type_for_kc(self, *, knowledge_types: list[str], index: int) -> str:
        if index - 1 < len(knowledge_types) and knowledge_types[index - 1]:
            return _coerce_kc_type(knowledge_types[index - 1])
        return "concept"

    def _bloom_level_for_kc(
        self,
        *,
        knowledge_bloom_levels: list[str],
        index: int,
        objective_context: ObjectiveContext,
    ) -> str:
        if index - 1 < len(knowledge_bloom_levels) and knowledge_bloom_levels[index - 1]:
            return knowledge_bloom_levels[index - 1].lower()
        return objective_context.atomic_objective.bloom_level

    def _focus_for_kc(self, *, knowledge_focuses: list[str], index: int, kc_name: str) -> str:
        if index - 1 < len(knowledge_focuses) and knowledge_focuses[index - 1]:
            return knowledge_focuses[index - 1]
        return kc_name

    def _supporting_record_ids_for_kc(
        self,
        *,
        knowledge_source_record_ids: list[list[str]],
        index: int,
        available_record_ids: set[str],
        exercise_record_ids: list[str],
    ) -> list[str]:
        source_record_ids = (
            knowledge_source_record_ids[index - 1]
            if index - 1 < len(knowledge_source_record_ids)
            else []
        )
        supporting_record_ids = [
            record_id
            for record_id in [*source_record_ids, *exercise_record_ids]
            if record_id in available_record_ids
        ]
        if supporting_record_ids:
            return supporting_record_ids
        return sorted(available_record_ids)

    def _build_candidate_kc(
        self,
        *,
        draft: KCExtractionDraft,
        objective_context: ObjectiveContext,
        total_kcs: int,
    ) -> CandidateKC:
        atomic_objective = objective_context.atomic_objective
        return CandidateKC.model_validate(
            {
                "kc_id": f"{atomic_objective.atomic_objective_id}-kc{draft.ordinal:02d}",
                "kc_type": draft.kc_type,
                "objective_text": draft.objective_text,
                "curriculum_objective_id": atomic_objective.curriculum_objective_id,
                "kc_focus": draft.kc_focus,
                "supporting_record_ids": draft.supporting_record_ids,
                "bloom_level": draft.bloom_level,
                "prerequisite_kc_ids": self._prerequisite_kc_ids(
                    atomic_objective_id=atomic_objective.atomic_objective_id,
                    prerequisite_indices=draft.prerequisite_indices,
                    current_index=draft.ordinal,
                    total_kcs=total_kcs,
                ),
                "is_prior_knowledge": draft.is_prior_knowledge,
            }
        )

    def _prerequisite_kc_ids(
        self,
        *,
        atomic_objective_id: str,
        prerequisite_indices: list[int],
        current_index: int,
        total_kcs: int,
    ) -> list[str]:
        return [
            f"{atomic_objective_id}-kc{prerequisite_index:02d}"
            for prerequisite_index in prerequisite_indices
            if 0 < prerequisite_index <= total_kcs and prerequisite_index != current_index
        ]

    def _fallback_plan(
        self,
        *,
        objective_context: ObjectiveContext,
        available_record_ids: set[str],
        exercise_record_ids: list[str],
    ) -> CandidateKCPlan:
        fallback_focus = objective_context.atomic_objective.objective_text
        support_ids = sorted(available_record_ids)[:1] or exercise_record_ids[:1]
        return CandidateKCPlan.model_validate(
            {
                "candidate_kcs": [
                    {
                        "kc_id": f"{objective_context.atomic_objective.atomic_objective_id}-kc01",
                        "kc_type": "concept",
                        "objective_text": fallback_focus,
                        "curriculum_objective_id": (
                            objective_context.atomic_objective.curriculum_objective_id
                        ),
                        "kc_focus": fallback_focus,
                        "supporting_record_ids": support_ids,
                        "bloom_level": objective_context.atomic_objective.bloom_level,
                    }
                ]
            }
        )
