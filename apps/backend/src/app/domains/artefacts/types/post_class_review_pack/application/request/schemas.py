"""Pydantic contracts for condition-filtered generation inputs.

The DSPy module never sees raw database objects. It receives a
``BaseReviewPackRequest`` or ``PersonalisedReviewPackRequest`` whose contents
have already been filtered by the product policy.
"""

from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)

LearnerStatus = Literal["remediate", "reinforce", "extend"]
SignalLevel = Literal["low", "medium", "high"]


class SourceRegion(BaseModel):
    """One named part of an evidence item, addressable on its own."""

    model_config = ConfigDict(extra="forbid")

    region_id: str
    title: str
    excerpt: str


class SourceEvidenceItem(BaseModel):
    """Approved source evidence passed in for retrieval-grounded conditions."""

    model_config = ConfigDict(extra="forbid")

    source_ref: str
    excerpt: str
    title: str | None = None
    section_ref: str | None = None
    lesson_objective_id: str | None = None
    curriculum_objective_id: str | None = None
    #: The item's own parts, where the plan declares them. A reading tool can then
    #: address "the properties of a cylinder" rather than lines 12 to 28 — an address
    #: that does not move when someone edits a word above it. Empty for a plan that
    #: declares none, which is every plan the app drafts today.
    regions: list[SourceRegion] = Field(default_factory=list)


class SourceFigure(BaseModel):
    """A source-derived figure carried into one section-generation request."""

    model_config = ConfigDict(extra="forbid")

    figure_id: str
    variant: Literal["image", "diagram_tikz"]
    url: str | None = None
    caption: str | None = None
    figure_ref: str | None = None
    source_tikz: str | None = None
    source_record_id: str | None = None


# Boundary translation: the canonical assessment vocabulary (stem /
# chosen_option / misconception_code) stays in the domain models; these field
# names are chosen for the LM.
class AnswerEvidenceItem(BaseModel):
    """One diagnostic question the learner got wrong, with the chosen distractor."""

    model_config = ConfigDict(extra="forbid")

    question: str
    options: dict[str, str] = Field(default_factory=dict)
    correct_option: str = ""
    student_choice: str = ""
    chosen_option_misconception: str | None = Field(
        default=None,
        description="The misconception the chosen distractor was authored to reveal.",
    )


# Shape chosen by the prompt-evidence experiment (experiments/p1_evidence_prompt):
# raw answer evidence beat the distilled label card decisively on remediation.
#
# Field names ARE prompt text (they serialize with the values). Pydantic Field
# descriptions on this INPUT model are NOT — verified by rendering the real
# ChatAdapter prompt — so every semantic (band meanings, 1-5 scale anchors,
# small-denominator caveat) lives in the personalise signature docstring, the
# one channel that provably reaches the model.
class ObjectiveLearnerState(BaseModel):
    """One objective's learner state as the personalisation model receives it.

    Survey values are rendered as SELF-DESCRIBING phrases ("a little sure
    (2/5)") rather than bare numbers: three differently-scaled "scores" with
    opposite polarities in one object invite misreading, and a phrase carries
    its own anchor wherever the model reads it. The mapper owns the rendering.
    """

    model_config = ConfigDict(extra="forbid")

    lesson_objective_id: str
    # remediate / reinforce / extend — what each band prescribes is spelled out
    # in the signature docstring.
    mastery_band: LearnerStatus
    # e.g. "1 of 2 diagnostic questions correct" — counts over a bare fraction,
    # so thin evidence reads as thin.
    mastery: str | None = None
    # The learner's own survey answers, e.g. "a little sure (2/5)",
    # "very difficult (5/5)".
    confidence: str | None = None
    perceived_difficulty: str | None = None
    misconception: str | None = None
    evidence_items: list[AnswerEvidenceItem] = Field(default_factory=list)


class SessionSignals(BaseModel):
    """Session-level survey answers, asked once for the whole lesson (tone/depth).

    Same self-describing rendering as the per-objective survey answers,
    e.g. "very interested (5/5)", "confused (2/5)".
    """

    model_config = ConfigDict(extra="forbid")

    interest: str | None = None
    end_of_lesson_feeling: str | None = None


class LessonContextForGeneration(BaseModel):
    """Global lesson context shared by every unit in a request."""

    model_config = ConfigDict(extra="forbid")

    subject: str
    grade_level: str
    topic: str
    subtopic: str | None = None
    term: str | None = None
    week: int | None = None
    curriculum_scope: str | None = None
    lesson_objectives: list[str]
    # What the teacher's plan records as already taught, from its Previous knowledge
    # list. Lesson-level, and withheld from the baseline condition.
    entry_behaviour: list[str] = Field(default_factory=list)
    # Teaching/learning materials the plan lists. Lesson-level in every field plan —
    # one list for the whole lesson, never per step.
    instructional_materials: list[str] = Field(default_factory=list)


class GenerationPolicyContext(BaseModel):
    """The product-policy rules the generator must follow, in-band.

    LM-facing: this model serializes INTO the prompt, so it carries only rules
    the model can act on and no caller bookkeeping.
    """

    model_config = ConfigDict(extra="forbid")

    require_source_refs: bool
    use_only_provided_sources: bool
    preserve_lesson_objective: bool

    instruction_summary: str


class StepActivityView(BaseModel):
    """One action in a lesson step, who performs it, and whether it is work set.

    ``sets_work`` is the read verdict on a student line — performance the lesson
    set, as against participation inside the teacher's exposition — and it is kept
    here because dropping it leaves "identify their properties" and "construct
    angle 90 degrees" looking like the same kind of line.
    """

    model_config = ConfigDict(extra="ignore")

    who: str
    what: str
    sets_work: bool | None = None


class SectionGenerationUnit(BaseModel):
    """Policy-filtered input from which exactly one generated section is produced."""

    model_config = ConfigDict(extra="forbid")

    unit_id: str

    lesson_objective_id: str
    objective_text: str

    source_step_id: str | None = None
    step_title: str | None = None
    step_content: str | None = None
    instructional_type: str | None = None
    estimated_minutes: int | None = None
    # This step's position against the ordered lesson objectives. Sections are generated
    # by independent concurrent calls, so without it a unit cannot know what precedes it.
    current_step: int | None = None
    # The step's Teacher/Student activity narration, Gagne-coded. The raw narration never
    # travels: the artefact spec forbids writing about the lesson as an event.
    instructional_events: list[str] = Field(default_factory=list)
    # The Student Activity questions this step sets, as statements. No answers.
    student_tasks: list[str] = Field(default_factory=list)

    activities: list[StepActivityView] = Field(default_factory=list)
    assessment_points: list[str] = Field(default_factory=list)

    source_evidence: list[SourceEvidenceItem] = Field(default_factory=list)
    # Grounded figures carried from the lesson-plan step (textbook-grounded conditions only).
    source_figures: list[SourceFigure] = Field(default_factory=list)
    objective_learner_state: ObjectiveLearnerState | None = None


class _ReviewPackRequestBase(BaseModel):
    """Fields shared by base-generation and personalisation requests."""

    model_config = ConfigDict(extra="forbid")

    generation_policy: ReviewPackGenerationPolicy

    artefact_spec: ArtefactSpec
    policy: GenerationPolicyContext
    lesson_context: LessonContextForGeneration
    units: list[SectionGenerationUnit]


class BaseReviewPackRequest(_ReviewPackRequestBase):
    """A base review-pack generation request."""


class PersonalisedReviewPackRequest(_ReviewPackRequestBase):
    """A learner-scoped personalisation or base-reuse request."""

    model_config = ConfigDict(extra="forbid")

    base_pack_id: str
    focal_learner_id: str
    # Focal learner's session-level survey, used as tone and depth modifiers.
    session_signals: SessionSignals | None = None


ReviewPackRequest: TypeAlias = BaseReviewPackRequest | PersonalisedReviewPackRequest
