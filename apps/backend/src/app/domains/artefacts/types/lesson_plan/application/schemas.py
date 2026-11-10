"""Pydantic contracts for the lesson-plan generation pipeline.

``SessionContextPayloadBuilder`` flattens the typed ``SessionContext`` into these
scope models. They are validated, structured records — not opaque dicts — and are
serialised with ``model_dump(mode="json")`` only at the DSPy generator / validator
boundary, which still takes a plain ``JsonObject``.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.shared.json_types import JsonObject


class _ScopeModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SessionScope(_ScopeModel):
    """The session metadata + objectives the generator conditions on."""

    session_id: str
    subject: str
    track: str
    grade: str
    term: str
    week: int
    day_index: int
    topic: str
    subtopic: str
    duration_minutes: int
    session_objectives: list[str]
    theme: str
    performance_objectives: list[str]
    entry_behaviour: list[str]
    instructional_materials: list[str]
    average_age: int | None


class CurriculumScope(_ScopeModel):
    """The curriculum framing (objectives, activities, materials) for generation."""

    subject: str
    track: str
    grade: str
    term: str
    week: int
    theme: str
    topic: str
    subtopic: str
    curriculum_objectives: list[JsonObject]
    general_objectives: list[str]
    session_objectives: list[str]
    performance_objectives: list[str]
    teacher_activities: list[str]
    student_activities: list[str]
    instructional_materials: list[str]
    evaluation_guide: list[str]
    entry_behaviour: list[str]


class ValidationScope(_ScopeModel):
    """The minimal context the post-generation validator checks the plan against."""

    session_id: str
    subject: str
    track: str
    grade: str
    term: str
    week: int
    topic: str
    subtopic: str
