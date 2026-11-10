"""Manual classwork (exit-ticket) entry schemas (FD-02).

The teacher hand-enters the lesson's real classwork as MCQ items tagged to the
frozen plan's objectives; these persist as the same ``ExitTicketItem`` rows the
LLM diagnostic writes, so the scoring pipeline consumes them unchanged. The
``option_misconceptions`` field is accepted but left empty here — FD-03 fills it
with teacher-reviewed distractor→misconception tags.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Difficulty = Literal["easy", "medium", "hard"]


class ManualClassworkItem(BaseModel):
    """One hand-entered MCQ item.

    Semantic checks (objective in plan, correct option among the entered keys) run
    in ``classwork_item_issues`` so the 422 detail is teacher-facing; only structural
    minimums are enforced here.
    """

    lesson_objective_id: str = Field(..., min_length=1)
    stem: str = Field(..., min_length=1)
    options: dict[str, str] = Field(..., min_length=2)
    correct_option: str = Field(..., min_length=1)
    knowledge_component_id: str | None = None
    difficulty: Difficulty | None = None
    # Reserved for FD-03 (teacher-reviewed distractor→misconception tags).
    option_misconceptions: dict[str, str] | None = None


class ManualClassworkCreateRequest(BaseModel):
    items: list[ManualClassworkItem] = Field(..., min_length=1)


# --- Context (form prerequisites) ---


class ManualClassworkObjective(BaseModel):
    lesson_objective_id: str
    objective_text: str | None = None
    curriculum_objective_id: str | None = None


class KnowledgeComponentOption(BaseModel):
    id: str
    kc_code: str
    description: str


class ManualClassworkExistingItem(BaseModel):
    """A persisted item, returned so the form can edit-in-place rather than start blank."""

    item_id: str
    lesson_objective_id: str | None = None
    stem: str
    options: dict[str, str]
    correct_option: str
    knowledge_component_id: str | None = None
    difficulty: str | None = None
    option_misconceptions: dict[str, str] | None = None


class ManualClassworkContextResponse(BaseModel):
    plan_version_id: str
    subject: str | None = None
    topic: str | None = None
    subtopic: str | None = None
    objectives: list[ManualClassworkObjective] = Field(default_factory=list)
    knowledge_components: list[KnowledgeComponentOption] = Field(default_factory=list)
    items: list[ManualClassworkExistingItem] = Field(default_factory=list)
    # Once the assessment is released to students it is frozen — entry locks.
    released: bool = False


# --- Coverage report ---


class ClassworkObjectiveCoverage(BaseModel):
    lesson_objective_id: str
    objective_text: str | None = None
    item_count: int
    has_items: bool


class ClassworkCoverageResponse(BaseModel):
    plan_version_id: str
    total_items: int
    objectives: list[ClassworkObjectiveCoverage] = Field(default_factory=list)
    objectives_without_items: list[str] = Field(default_factory=list)


# --- Misconception derivation (FD-03) ---


class DeriveMisconceptionsItem(BaseModel):
    """One MCQ item to derive distractor misconceptions for (from the draft being edited)."""

    stem: str = Field(..., min_length=1)
    options: dict[str, str] = Field(..., min_length=2)
    correct_option: str = Field(..., min_length=1)
    lesson_objective_id: str | None = None


class DeriveMisconceptionsRequest(BaseModel):
    items: list[DeriveMisconceptionsItem] = Field(..., min_length=1)


class DerivedItemMisconceptions(BaseModel):
    # Wrong option key -> suggested snake_case misconception code.
    option_misconceptions: dict[str, str] = Field(default_factory=dict)


class DeriveMisconceptionsResponse(BaseModel):
    # Index-aligned with the request items.
    items: list[DerivedItemMisconceptions] = Field(default_factory=list)
