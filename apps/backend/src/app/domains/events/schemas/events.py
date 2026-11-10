"""Pydantic schemas for event ingestion."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.json_types import JsonObject


class EventIn(BaseModel):
    event_id: str | None = None
    student_id: str | None = None
    artefact_id: str | None = None
    event_type: str = Field(..., min_length=1)
    payload: JsonObject = Field(default_factory=dict)
    event_timestamp: datetime | None = None


class EventOut(BaseModel):
    event_id: str
    status: str
