from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

import dspy

from app.shared.json_types import JsonObject

from ....schemas.session_plan import AssessmentItem, CandidateKC
from ..signatures.assessment_design import DesignAssessmentSignature


class AssessmentPromptPayload(TypedDict):
    knowledge_name: str
    knowledge_description: str
    knowledge_type: str
    bloom_level: str
    source_content: str
    existing_exercises: list[JsonObject]


@dataclass(frozen=True)
class AssessmentPromptInputs:
    kc_name: str
    kc_description: str
    kc_type: str
    bloom_level: str
    source_content: str
    existing_exercises: list[JsonObject]

    def to_prompt_payload(self) -> AssessmentPromptPayload:
        return {
            "knowledge_name": self.kc_name,
            "knowledge_description": self.kc_description,
            "knowledge_type": self.kc_type,
            "bloom_level": self.bloom_level,
            "source_content": self.source_content,
            "existing_exercises": self.existing_exercises,
        }


class AssessmentDesigner(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.design = dspy.ChainOfThought(DesignAssessmentSignature)
        self.last_llm_calls = 0

    def forward(
        self,
        *,
        kc: CandidateKC,
        source_records: list[JsonObject],
        exercise_records: list[JsonObject],
        lesson_objective_id: str | None = None,
    ) -> AssessmentItem:
        self.last_llm_calls = 1
        prompt_inputs = self._prompt_inputs(
            kc=kc,
            source_records=source_records,
            exercise_records=exercise_records,
        )
        prediction = self.design(**prompt_inputs.to_prompt_payload())
        return AssessmentItem.model_validate(
            {
                "kc_id": kc.kc_id,
                "lesson_objective_id": lesson_objective_id,
                "question": str(getattr(prediction, "question", "") or "").strip(),
                "expected_answer": str(getattr(prediction, "expected_answer", "") or "").strip(),
                "bloom_justification": str(
                    getattr(prediction, "bloom_justification", "") or ""
                ).strip(),
            }
        )

    def _prompt_inputs(
        self,
        *,
        kc: CandidateKC,
        source_records: list[JsonObject],
        exercise_records: list[JsonObject],
    ) -> AssessmentPromptInputs:
        return AssessmentPromptInputs(
            kc_name=kc.kc_focus,
            kc_description=kc.objective_text,
            kc_type=kc.kc_type,
            bloom_level=kc.bloom_level,
            source_content=self._source_content(source_records),
            existing_exercises=self._exercise_payloads(exercise_records),
        )

    def _source_content(self, source_records: list[JsonObject]) -> str:
        return "\n\n".join(
            str(
                record.get("content")
                or record.get("answer_text")
                or record.get("prompt_text")
                or record.get("retrieval_text")
                or ""
            ).strip()
            for record in source_records
            if isinstance(record, dict)
        ).strip()

    def _exercise_payloads(self, exercise_records: list[JsonObject]) -> list[JsonObject]:
        return [
            {
                "prompt": str(record.get("prompt_text") or record.get("content") or "").strip(),
                "answer": str(record.get("answer_text") or "").strip(),
            }
            for record in exercise_records
            if isinstance(record, dict)
        ]
