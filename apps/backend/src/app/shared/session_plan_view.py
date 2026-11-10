from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.shared.json_types import JsonObject


class LessonPlanObjectiveView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    lesson_objective_id: str = Field(..., min_length=1)
    curriculum_objective_id: str | None = None
    objective_text: str | None = None


class SessionPlanStepView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    step_id: str = Field(..., min_length=1)
    step_kind: str = Field(..., min_length=1)
    instructional_type: str | None = None
    kc_type: str | None = None
    lesson_objective_id: str | None = None
    title: str | None = None
    content: str | None = None
    estimated_minutes: int | None = None
    activities: list[JsonObject] = Field(default_factory=list)
    # Field-captured plans: the teacher's note for this step, verbatim (prose, worked
    # examples, TikZ figures). Generated plans carry typed ``blocks`` instead.
    note: str | None = None
    blocks: list[JsonObject] = Field(default_factory=list)
    # The note's own parts, where the plan declares them: ``{id, title, role, body}``
    # per region, in reading order. A plan that declares none is unaffected — the note
    # stays one blob addressed by line, which is what every app-drafted plan does.
    regions: list[JsonObject] = Field(default_factory=list)


class SessionPlanView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    subject: str | None = None
    track: str | None = None
    grade: str | None = None
    term: str | None = None
    week: int | None = None
    topic: str | None = None
    subtopic: str | None = None
    # Denormalised lesson-plan title cached inside the session_plan payload by
    # the drafter. Consumers prefer this over the join on ``LessonPlan.title``
    # when it's present (consistent with how the LLM emitted it).
    title: str | None = None
    curriculum_objectives: list[JsonObject] = Field(default_factory=list)
    lesson_plan_objectives: list[LessonPlanObjectiveView] = Field(default_factory=list)
    misconceptions: list[str] = Field(default_factory=list)
    steps: list[SessionPlanStepView] = Field(default_factory=list)
    theme: str | None = None
    entry_behaviour: list[str] = Field(default_factory=list)
    instructional_materials: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
