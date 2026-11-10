from __future__ import annotations

import json

import dspy
from pydantic import BaseModel, Field, ValidationError

from app.domains.tutor.dspy.modules.tutor import TutorModule
from app.domains.tutor.schemas import TutorQueryResponse
from app.infra.dspy_lm import build_dspy_lm
from app.shared.json_types import JsonObject
from app.shared.review_pack_view import ReviewPackManifestView, ReviewPackStepView


class TutorResponsePayload(BaseModel):
    answer: str = Field(..., min_length=1)
    citations: list[str] = []
    refusal: bool = False
    reason: str | None = None


class TutorAnswerService:
    def __init__(self) -> None:
        self.lm = build_dspy_lm()
        self.module = TutorModule()

    async def answer_question(
        self,
        *,
        review_pack: ReviewPackManifestView,
        step: ReviewPackStepView,
        question: str,
    ) -> TutorQueryResponse:
        with dspy.settings.context(lm=self.lm):
            result = await self.module.acall(
                lesson_context=self._lesson_context(review_pack),
                step_context=json.dumps(self._step_context(step), indent=2),
                items_context=json.dumps(self._blocks_context(step), indent=2),
                question=question,
                schema_hint=self._schema_hint(),
            )

        payload = self._parse_payload(result.response_json)
        citations = self._citations(payload.citations, step)
        return TutorQueryResponse(
            answer=payload.answer,
            citations=citations,
            refusal=payload.refusal,
            reason=payload.reason,
            metadata=self._metadata(step),
        )

    def _schema_hint(self) -> str:
        return (
            'Return JSON: {"answer": string, "citations": ["ITEM_ID"], '
            '"refusal": boolean, "reason": string|null}.'
        )

    def _parse_payload(self, payload: object) -> TutorResponsePayload:
        if isinstance(payload, str):
            payload = json.loads(payload)
        if not isinstance(payload, dict):
            raise ValueError("tutor_response_invalid")
        try:
            return TutorResponsePayload.model_validate(payload)
        except ValidationError as exc:
            raise ValueError("tutor_response_invalid") from exc

    def _lesson_context(self, review_pack: ReviewPackManifestView) -> str:
        # The lesson context is a fixed subset of the pack manifest, serialised for the
        # prompt — let the model emit it directly rather than rebuilding a dict.
        return review_pack.model_dump_json(
            indent=2,
            include={
                "subject",
                "grade",
                "term",
                "week",
                "topic",
                "subtopic",
                "lesson_plan_objectives",
            },
        )

    def _step_context(self, step: ReviewPackStepView) -> JsonObject:
        return {
            "step_id": step.step_id,
            "step_kind": step.step_kind,
            "instructional_type": step.instructional_type,
            "type": step.type,
            "title": step.title,
            "estimated_minutes": step.estimated_minutes,
        }

    def _blocks_context(self, step: ReviewPackStepView) -> list[JsonObject]:
        return [
            {
                "id": payload.get("id"),
                "type": payload.get("type"),
                "content": payload.get("content"),
                "answer": payload.get("answer"),
                "hints": payload.get("hints"),
            }
            for block in step.blocks
            for payload in [block.model_dump(mode="json")]
        ]

    def _citations(
        self,
        candidate_citations: list[str],
        step: ReviewPackStepView,
    ) -> list[str]:
        valid_ids = {block.id for block in step.blocks if block.id}
        return [citation for citation in candidate_citations if citation in valid_ids]

    def _metadata(self, step: ReviewPackStepView) -> JsonObject:
        return {
            "step_id": step.step_id,
            "step_type": step.type,
        }
