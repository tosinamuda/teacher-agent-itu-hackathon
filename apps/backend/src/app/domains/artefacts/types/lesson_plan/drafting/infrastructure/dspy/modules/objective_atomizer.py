from __future__ import annotations

from dataclasses import dataclass

import dspy
from dspy import Prediction
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.shared.json_types import JsonObject

from ....domain.bloom import extract_primary_verb, infer_bloom_level
from ....schemas.session_plan import AtomicObjective
from ..signatures.objective_atomization import AtomizeObjectiveSignature


class _AtomizeObjectiveView(BaseModel):
    """Typed Pydantic view of an AtomizeObjective DSPy prediction.

    Same role as ``_ExtractKCsView`` in ``kc_extractor.py``: boundary-time
    narrowing of the LLM-emitted parallel lists, so downstream consumers
    read typed fields instead of re-narrowing per call site. Replaces the
    previous ``as_str_list(getattr(prediction, ...))`` pair.
    """

    model_config = ConfigDict(extra="ignore")

    atomic_texts: list[str] = Field(default_factory=list)
    bloom_verbs: list[str] = Field(default_factory=list)

    @field_validator("atomic_texts", "bloom_verbs", mode="before")
    @classmethod
    def _strip_and_drop_empty(cls, raw: object) -> list[str]:
        if not isinstance(raw, list):
            return []
        return [str(item).strip() for item in raw if str(item).strip()]

    @classmethod
    def from_prediction(cls, prediction: Prediction) -> _AtomizeObjectiveView:
        return cls.model_validate(
            {field: getattr(prediction, field, None) for field in cls.model_fields}
        )


@dataclass(frozen=True)
class CurriculumObjectiveInput:
    curriculum_objective_id: str
    objective_text: str


@dataclass(frozen=True)
class AtomicObjectiveDraft:
    objective_text: str
    bloom_verb: str


class ObjectiveAtomizer(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.atomize = dspy.Predict(AtomizeObjectiveSignature)
        self.last_llm_calls = 0

    def forward(
        self,
        *,
        curriculum_objectives: list[JsonObject],
        subtopic_title: str,
        evaluation_guide: list[str],
    ) -> list[AtomicObjective]:
        self.last_llm_calls = 0
        atomic_objectives: list[AtomicObjective] = []

        for curriculum_objective in curriculum_objectives:
            parsed_objective = self._read_curriculum_objective(curriculum_objective)
            if parsed_objective is None:
                continue
            atomic_objectives.extend(
                self._atomize_curriculum_objective(
                    curriculum_objective=parsed_objective,
                    subtopic_title=subtopic_title,
                    evaluation_guide=evaluation_guide,
                    current_count=len(atomic_objectives),
                )
            )

        return atomic_objectives

    def _read_curriculum_objective(
        self,
        payload: JsonObject,
    ) -> CurriculumObjectiveInput | None:
        curriculum_objective_id = str(payload.get("curriculum_objective_id") or "").strip()
        objective_text = str(payload.get("objective_text") or "").strip()
        if not curriculum_objective_id or not objective_text:
            return None
        return CurriculumObjectiveInput(
            curriculum_objective_id=curriculum_objective_id,
            objective_text=objective_text,
        )

    def _atomize_curriculum_objective(
        self,
        *,
        curriculum_objective: CurriculumObjectiveInput,
        subtopic_title: str,
        evaluation_guide: list[str],
        current_count: int,
    ) -> list[AtomicObjective]:
        atomic_drafts = self._resolve_atomic_drafts(
            objective_text=curriculum_objective.objective_text,
            subtopic_title=subtopic_title,
            evaluation_guide=evaluation_guide,
        )
        return [
            AtomicObjective.model_validate(
                {
                    "atomic_objective_id": (
                        f"{curriculum_objective.curriculum_objective_id}-ao{index:02d}"
                    ),
                    "curriculum_objective_id": curriculum_objective.curriculum_objective_id,
                    "objective_text": draft.objective_text,
                    "bloom_verb": draft.bloom_verb,
                    "bloom_level": infer_bloom_level(draft.bloom_verb),
                    "objective_order": current_count + index,
                }
            )
            for index, draft in enumerate(atomic_drafts, start=1)
        ]

    def _resolve_atomic_drafts(
        self,
        *,
        objective_text: str,
        subtopic_title: str,
        evaluation_guide: list[str],
    ) -> list[AtomicObjectiveDraft]:
        if self._looks_atomic(objective_text):
            return [self._fallback_draft(objective_text)]

        prediction = self.atomize(
            performance_objective=objective_text,
            evaluation_guide=evaluation_guide,
            subtopic_title=subtopic_title,
        )
        self.last_llm_calls += 1

        view = _AtomizeObjectiveView.from_prediction(prediction)
        if not view.atomic_texts:
            return [self._fallback_draft(objective_text)]

        return [
            AtomicObjectiveDraft(
                objective_text=atomic_text,
                bloom_verb=self._resolve_bloom_verb(
                    atomic_text=atomic_text,
                    predicted_verbs=view.bloom_verbs,
                    index=index,
                ),
            )
            for index, atomic_text in enumerate(view.atomic_texts)
        ]

    def _resolve_bloom_verb(
        self,
        *,
        atomic_text: str,
        predicted_verbs: list[str],
        index: int,
    ) -> str:
        if index < len(predicted_verbs) and predicted_verbs[index]:
            return predicted_verbs[index]
        return extract_primary_verb(atomic_text)

    def _fallback_draft(self, objective_text: str) -> AtomicObjectiveDraft:
        return AtomicObjectiveDraft(
            objective_text=objective_text,
            bloom_verb=extract_primary_verb(objective_text),
        )

    def _looks_atomic(self, objective_text: str) -> bool:
        normalized = objective_text.lower()
        return not any(marker in normalized for marker in (" and ", " or ", " vice versa"))
