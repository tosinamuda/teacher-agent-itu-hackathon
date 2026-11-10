from __future__ import annotations

from pydantic import BaseModel, Field

from app.shared.json_types import JsonObject


class TutorQueryRequest(BaseModel):
    artefact_id: str = Field(..., min_length=1)
    step_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)


class TutorQueryResponse(BaseModel):
    answer: str
    citations: list[str] = []
    refusal: bool = False
    reason: str | None = None
    metadata: JsonObject | None = None
