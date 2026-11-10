from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ContentBase(StrictModel):
    id: str = Field(..., description="Unique identifier for React keys.")
    type: Literal["explanation", "visual", "worked_example", "practice"]


class ExplanationBlock(ContentBase):
    type: Literal["explanation"]
    content: str = Field(..., description="Markdown explanation text.")
    # Provenance travels beside the prose, not inside it. It used to be appended
    # as a "_Sources: REF-1_" footer and read back with a regex — the only
    # channel this schema offered — which put citation markers in the text a
    # rater reads and made the renderer's strip the thing protecting blinding.
    # Defaulted, so packs stored before the field validate unchanged.
    source_refs: list[str] = Field(
        default_factory=list,
        description="Source refs this block is grounded in. Never rendered to a reader.",
    )


# ``image`` is a figure lifted from an ingested textbook record and so must be traceable
# to it. ``diagram_tikz`` is one the teacher drew herself, carrying its own source — she
# has no record to cite, which is why such figures previously had nowhere to live and
# survived only as raw LaTeX inside explanation prose.
VisualVariant = Literal["image", "diagram_clock", "diagram_number_line", "diagram_tikz"]


class VisualBlock(ContentBase):
    type: Literal["visual"]
    variant: VisualVariant
    caption: str | None = None
    url: str | None = None
    data: dict | None = None
    source_record_id: str | None = None
    source_html_path: str | None = None
    source_anchor_id: str | None = None
    # The note's own name for the figure ("fig-01"), where it labels one. This is what
    # the prose points at, so it is what a reference has to resolve against.
    figure_ref: str | None = None
    # The drawing itself, as the teacher wrote it. Never shown to a learner or a model;
    # it exists so the figure can be rendered without going back to the source document.
    source_tikz: str | None = None

    @model_validator(mode="after")
    def _validate_grounded_image(self) -> VisualBlock:
        if self.variant == "image":
            if not self.url:
                raise ValueError("image visuals require grounded url")
            if not self.source_record_id:
                raise ValueError("image visuals require source_record_id")
        if self.variant == "diagram_tikz" and not self.source_tikz:
            raise ValueError("tikz diagrams require source_tikz")
        return self


class PlannerExplanationBlock(ContentBase):
    # A plan records its grounding per step, in its evidence plans, so the planner is not
    # offered ``source_refs``: shown on one block kind, a model extends it to the others,
    # which the strict schema then rejects.
    type: Literal["explanation"]
    content: str = Field(..., description="Markdown explanation text.")


class PlannerVisualBlock(ContentBase):
    type: Literal["visual"]
    variant: Literal["image", "diagram_clock", "diagram_number_line"]
    caption: str | None = None
    url: str | None = None
    data: dict | None = None
    source_record_id: str | None = None
    source_html_path: str | None = None
    source_anchor_id: str | None = None


class WorkedExampleStep(StrictModel):
    label: str = Field(..., description="Step label (e.g., 'Step 1').")
    content: str = Field(..., description="Markdown content for the step.")


class WorkedExampleBlock(ContentBase):
    type: Literal["worked_example"]
    problem: str = Field(..., description="The problem statement.")
    steps: list[WorkedExampleStep]
    final_answer: str


class PracticeBlock(ContentBase):
    type: Literal["practice"]
    question: str = Field(..., description="The practice question.")
    answer: str = Field(..., description="The correct answer (hidden initially).")
    hints: list[str] | None = None
    lesson_objective_id: str | None = Field(
        default=None,
        description="Linked lesson objective for evaluation coverage tracking.",
    )


ContentBlock = Annotated[
    ExplanationBlock | VisualBlock | WorkedExampleBlock | PracticeBlock,
    Field(discriminator="type"),
]
PlannerContentBlock = Annotated[
    PlannerExplanationBlock | PlannerVisualBlock | WorkedExampleBlock | PracticeBlock,
    Field(discriminator="type"),
]

BlockType = Literal["explanation", "worked_example", "practice"]
BloomLevel = Literal["remember", "understand", "apply", "analyze"]
CoreInstructionalType = Literal[
    "explain_only",
    "explain_practice",
    "explain_example_practice",
]
InstructionalType = Literal[
    "explain",
    "example",
    "practice",
    "check",
    "explain_only",
    "explain_practice",
    "explain_example_practice",
]


class CurriculumObjectiveRef(StrictModel):
    curriculum_objective_id: str = Field(..., min_length=1)
    objective_text: str = Field(..., min_length=1)
    objective_order: int = Field(..., ge=1)


class LessonPlanObjective(StrictModel):
    # LM-facing aliases (see PlanStep) — canonical kc_* keys preserved in storage.
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    lesson_objective_id: str = Field(..., min_length=1)
    objective_text: str = Field(..., min_length=1)
    objective_order: int = Field(..., ge=1)
    curriculum_objective_id: str = Field(..., min_length=1)
    curriculum_objective_text: str = Field(..., min_length=1)
    kc_type: Literal["concept", "procedure", "representation"] = Field(
        ...,
        alias="knowledge_type",
        description=(
            "What kind of knowledge this objective is: 'concept' = a definition or "
            "idea; 'procedure' = a step-by-step method; 'representation' = reading or "
            "drawing a form (diagram, number line, table)."
        ),
    )
    kc_focus: str = Field(
        ...,
        min_length=1,
        alias="knowledge_focus",
        description="The specific skill or idea this objective focuses on.",
    )
    source_form: str | None = None
    target_form: str | None = None


class AtomicObjective(StrictModel):
    atomic_objective_id: str = Field(..., min_length=1)
    curriculum_objective_id: str = Field(..., min_length=1)
    objective_text: str = Field(..., min_length=1)
    bloom_verb: str = Field(..., min_length=1)
    bloom_level: BloomLevel = Field(...)
    objective_order: int = Field(..., ge=1)


def required_block_types_for_kc(
    kc_type: Literal["concept", "procedure", "representation"],
) -> list[BlockType]:
    if kc_type == "concept":
        return ["explanation"]
    return ["explanation", "worked_example", "practice"]


class CoreStepBlueprint(StrictModel):
    # LM-facing alias (see PlanStep) — canonical kc_type preserved internally.
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    step_id: str = Field(..., min_length=1)
    lesson_objective_id: str = Field(..., min_length=1)
    kc_type: Literal["concept", "procedure", "representation"] = Field(
        ...,
        alias="knowledge_type",
        description=(
            "What kind of knowledge this step teaches: 'concept' = a definition or "
            "idea; 'procedure' = a step-by-step method; 'representation' = reading or "
            "drawing a form (diagram, number line, table)."
        ),
    )
    required_block_types: list[BlockType] = Field(..., min_length=1)

    @model_validator(mode="after")
    def _validate_required_block_types(self) -> CoreStepBlueprint:
        expected = required_block_types_for_kc(self.kc_type)
        if list(self.required_block_types) != expected:
            raise ValueError(f"{self.kc_type} core steps must use required_block_types={expected}")
        return self


class CandidateKC(StrictModel):
    # LM-facing aliases (see PlanStep) — canonical kc_* keys preserved internally.
    # This is an intermediate planner artefact (not persisted), but aliasing keeps
    # the vocabulary the model sees consistent across every drafting stage.
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    kc_id: str = Field(
        ...,
        min_length=1,
        alias="knowledge_id",
        description="A short unique id for this knowledge item, referenced by prerequisites.",
    )
    kc_type: Literal["concept", "procedure", "representation"] = Field(
        ...,
        alias="knowledge_type",
        description=(
            "What kind of knowledge this is: 'concept' = a definition or idea; "
            "'procedure' = a step-by-step method; 'representation' = reading or "
            "drawing a form (diagram, number line, table)."
        ),
    )
    objective_text: str = Field(..., min_length=1)
    curriculum_objective_id: str = Field(..., min_length=1)
    kc_focus: str = Field(
        ...,
        min_length=1,
        alias="knowledge_focus",
        description="The specific skill or idea this knowledge item focuses on.",
    )
    source_form: str | None = None
    target_form: str | None = None
    supporting_record_ids: list[str] = Field(..., min_length=1)
    ordering_notes: str | None = None
    bloom_level: BloomLevel = Field(
        default="apply",
        description=(
            "Cognitive process level from Bloom's revised taxonomy. "
            "Determines the instructional strategy and assessment depth."
        ),
    )
    prerequisite_kc_ids: list[str] = Field(
        default_factory=list,
        alias="prerequisite_knowledge_ids",
        description=(
            "knowledge_id values of other items in this plan that must be taught "
            "first. Forms a DAG. Empty list means no prerequisites."
        ),
    )
    is_prior_knowledge: bool = Field(
        default=False,
        description=(
            "True if this item covers content from a prior subtopic. "
            "Activated in the intro rather than taught from scratch."
        ),
    )


def _normalize_key(value: str | None) -> str:
    return " ".join(str(value or "").strip().lower().split())


class CandidateKCPlan(StrictModel):
    candidate_kcs: list[CandidateKC] = Field(..., min_length=1)
    misconceptions: list[str] = Field(default_factory=list)
    theme: str | None = None
    entry_behaviour: list[str] = Field(default_factory=list)
    instructional_materials: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_candidate_kc_distinctness(self) -> CandidateKCPlan:
        seen_kc_ids: set[str] = set()
        grouped: dict[str, list[tuple[str, tuple[str, str], str]]] = {}

        for candidate_kc in self.candidate_kcs:
            if candidate_kc.kc_id in seen_kc_ids:
                raise ValueError(
                    f"candidate_kcs must contain unique kc_id values: {candidate_kc.kc_id}"
                )
            seen_kc_ids.add(candidate_kc.kc_id)

            grouped.setdefault(candidate_kc.curriculum_objective_id, []).append(
                (
                    _normalize_key(candidate_kc.kc_focus),
                    (
                        _normalize_key(candidate_kc.source_form),
                        _normalize_key(candidate_kc.target_form),
                    ),
                    _normalize_key(candidate_kc.objective_text),
                )
            )

        for curriculum_objective_id, siblings in grouped.items():
            for index, (focus, form_pair, objective_text) in enumerate(siblings):
                for other_focus, other_form_pair, other_objective_text in siblings[index + 1 :]:
                    if focus and focus == other_focus and form_pair == other_form_pair:
                        raise ValueError(
                            "sibling candidate_kcs for curriculum objective "
                            f"{curriculum_objective_id} must differ in kc_focus or "
                            "(source_form, target_form)"
                        )
                    if focus and focus == other_focus and objective_text == other_objective_text:
                        raise ValueError(
                            "split candidate_kcs may not keep the same broad objective_text and "
                            f"kc_focus for curriculum objective {curriculum_objective_id}"
                        )

        return self

    @model_validator(mode="after")
    def _validate_prerequisite_graph(self) -> CandidateKCPlan:
        kc_ids = {candidate_kc.kc_id for candidate_kc in self.candidate_kcs}
        for candidate_kc in self.candidate_kcs:
            for prerequisite_kc_id in candidate_kc.prerequisite_kc_ids:
                if prerequisite_kc_id not in kc_ids:
                    raise ValueError(
                        f"KC '{candidate_kc.kc_id}' references prerequisite "
                        f"'{prerequisite_kc_id}' which does not exist."
                    )
            if candidate_kc.kc_id in candidate_kc.prerequisite_kc_ids:
                raise ValueError(f"KC '{candidate_kc.kc_id}' lists itself as a prerequisite.")
        return self

    @model_validator(mode="after")
    def _validate_bloom_coverage(self) -> CandidateKCPlan:
        if not any(not candidate_kc.is_prior_knowledge for candidate_kc in self.candidate_kcs):
            raise ValueError("At least one KC must be new learning, not prior knowledge.")
        return self


class AssessmentItem(StrictModel):
    # LM-facing alias (see PlanStep) — canonical kc_id preserved internally.
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    kc_id: str = Field(
        ...,
        min_length=1,
        alias="knowledge_id",
        description="The knowledge_id this assessment item checks.",
    )
    lesson_objective_id: str | None = Field(default=None, min_length=1)
    question: str = Field(..., min_length=1)
    expected_answer: str = Field(..., min_length=1)
    bloom_justification: str = Field(..., min_length=1)


class StepEvidencePlan(StrictModel):
    lesson_objective_id: str = Field(..., min_length=1)
    selected_record_ids: list[str] = Field(..., min_length=1)
    concept_record_ids: list[str] = Field(default_factory=list)
    modeling_record_ids: list[str] = Field(default_factory=list)
    practice_record_ids: list[str] = Field(default_factory=list)
    visual_record_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_record_groups(self) -> StepEvidencePlan:
        selected_ids = set(self.selected_record_ids)
        for group_name in (
            "concept_record_ids",
            "modeling_record_ids",
            "practice_record_ids",
            "visual_record_ids",
        ):
            for record_id in getattr(self, group_name):
                if record_id not in selected_ids:
                    raise ValueError(f"{group_name} must be a subset of selected_record_ids")
        return self


def _block_types(
    blocks: list[ContentBlock] | list[PlannerContentBlock],
) -> set[str]:
    return {block.type for block in blocks}


def derive_core_instructional_type(
    blocks: list[ContentBlock] | list[PlannerContentBlock],
) -> CoreInstructionalType:
    block_types = _block_types(blocks)
    if "worked_example" in block_types:
        return "explain_example_practice"
    if "practice" in block_types:
        return "explain_practice"
    return "explain_only"


#: The validation context under which a stored plan is read back. Which blocks a step of each
#: knowledge type must carry is asked of a plan being written; a plan already stored, a
#: teacher's or a study's, is read as it was kept.
READING_A_STORED_PLAN = {"reading_a_stored_plan": True}


def reading_a_stored_plan(info: ValidationInfo) -> bool:
    return bool((info.context or {}).get("reading_a_stored_plan"))


def _validate_core_blocks_for_kc(
    kc_type: Literal["concept", "procedure", "representation"],
    blocks: list[ContentBlock] | list[PlannerContentBlock],
) -> None:
    block_types = _block_types(blocks)
    if "explanation" not in block_types:
        raise ValueError("core steps require at least one explanation block")

    if kc_type == "concept":
        if "worked_example" in block_types:
            raise ValueError("concept core steps must not include worked_example blocks")
        return

    required_types = {"explanation", "worked_example", "practice"}
    missing = sorted(required_types - block_types)
    if missing:
        raise ValueError(f"{kc_type} core steps require blocks: {', '.join(missing)}")


def activities_of(step: object, who: str) -> list[str]:
    """The ``what`` of a step's activities for one actor, in order.

    For consumers that only want the text — diagnostics, the semantic validator, the
    lesson-plan renderer. Accepts a ``PlanStep`` or the raw stored mapping.
    """
    if isinstance(step, Mapping):
        raw = cast(Mapping[str, Any], step).get("activities")
    else:
        raw = getattr(step, "activities", None)
    out: list[str] = []
    for item in raw or []:
        actor = item.get("who") if isinstance(item, Mapping) else getattr(item, "who", None)
        what = item.get("what") if isinstance(item, Mapping) else getattr(item, "what", None)
        if actor == who and what:
            out.append(str(what))
    return out


# Replaces the parallel ``teacher_activities`` / ``student_activities`` lists, which
# could not express the ordering: a step runs "teacher demonstrates, then students
# attempt, then teacher circulates and marks", and two lists reduce that to two
# unordered piles. Models the NERDC lesson-plan form, which pairs Teacher's Activities
# with Student's/Pupil's Activities step by step; other national formats differ.
#
# Kept OUT of the docstring deliberately — model docstrings serialize into the JSON
# schema and reach the prompt, so they carry only what the model must act on.
class StepActivity(StrictModel):
    """One action in a lesson-plan sequence."""

    model_config = ConfigDict(extra="forbid")

    who: Literal["teacher", "student"] = Field(
        ..., description="Is this an activity performed by the teacher or the student?"
    )
    what: str = Field(..., min_length=1, description="The action itself.")
    sets_work: bool | None = Field(
        default=None,
        exclude_if=lambda value: value is None,
        description=(
            "Students only: true when the activity gives the students work to do on their "
            "own (questions to answer, a task to complete), false when it is taking part in "
            "the teaching (listening, copying, answering the teacher). Leave out for the teacher."
        ),
    )

    @model_validator(mode="after")
    def _only_students_set_work(self) -> StepActivity:
        if self.who == "teacher" and self.sets_work is not None:
            raise ValueError("only a student activity says whether it sets work")
        return self


class PlanStep(StrictModel):
    # ``populate_by_name`` keeps the canonical keys (kc_type, step_kind) valid for
    # stored plans + all internal code, while the LM-facing aliases below give the
    # model clearer names in the generated JSON schema. Storage dumps by field
    # name (default), so persisted JSON stays canonical.
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    step_id: str = Field(..., min_length=1, description="Unique identifier for the step.")
    step_kind: Literal["intro", "core", "evaluation"] = Field(
        ...,
        alias="step_role",
        description=(
            "Structural role of the step: 'intro' activates prior knowledge, 'core' "
            "teaches one lesson objective (carries knowledge_type + lesson_objective_id "
            "+ blocks), 'evaluation' checks mastery with practice blocks only."
        ),
    )
    instructional_type: InstructionalType | None = Field(
        default=None,
        description="Derived instructional pattern for rendered plan steps.",
    )
    kc_type: Literal["concept", "procedure", "representation"] | None = Field(
        default=None,
        alias="knowledge_type",
        description=(
            "What kind of knowledge a core step teaches (null for intro/evaluation). "
            "'concept' = a definition or idea, taught with an explanation only; "
            "'procedure' = a step-by-step method to carry out; 'representation' = "
            "reading or drawing a form such as a diagram, number line or table. "
            "'procedure' and 'representation' steps must include a worked_example and "
            "a practice block alongside the explanation."
        ),
    )
    lesson_objective_id: str | None = Field(
        default=None,
        description="Parent lesson-plan objective for core steps only.",
    )
    title: str = Field(..., min_length=1, description="Short label for the step.")
    content: str = Field(..., min_length=1, description="Teacher-facing summary of the step.")
    blocks: list[ContentBlock] = Field(
        default_factory=list,
        description=(
            "Structured content blocks. The required block types depend on the step: "
            "a 'core' step with knowledge_type='concept' must include at least one 'explanation' "
            "block and NO 'worked_example' block; a 'core' step with knowledge_type='procedure' or "
            "'representation' must include ALL THREE of 'explanation', 'worked_example' and "
            "'practice'; an 'evaluation' step must contain only 'practice' blocks (each with a "
            "lesson_objective_id). Honour these when adding or editing a step."
        ),
    )
    estimated_minutes: int = Field(..., ge=1, description="Estimated time for the step in minutes.")
    activities: list[StepActivity] = Field(
        default_factory=list,
        description=(
            "What happens in this step, in the order it runs, each attributed to the "
            "teacher or the students."
        ),
    )

    @model_validator(mode="after")
    def _validate_structure(self, info: ValidationInfo) -> PlanStep:
        if self.step_kind == "core":
            if not self.lesson_objective_id:
                raise ValueError("core steps require lesson_objective_id")
            if self.kc_type is None:
                raise ValueError("core steps require knowledge_type")
            if not self.blocks:
                raise ValueError("core steps require at least one structured block")
            if not reading_a_stored_plan(info):
                _validate_core_blocks_for_kc(self.kc_type, self.blocks)
            self.instructional_type = derive_core_instructional_type(self.blocks)
            return self

        if self.lesson_objective_id is not None:
            raise ValueError("only core steps may define lesson_objective_id")
        if self.kc_type is not None:
            raise ValueError("only core steps may define knowledge_type")

        if self.step_kind == "evaluation":
            self.instructional_type = "check"
            if not self.blocks:
                raise ValueError("evaluation steps require at least one practice block")
            for block in self.blocks:
                if not isinstance(block, PracticeBlock):
                    raise ValueError("evaluation steps may only contain practice blocks")
                if not block.lesson_objective_id:
                    raise ValueError("evaluation practice blocks require lesson_objective_id")
            return self

        self.instructional_type = None

        return self


class PlannerPlanStep(StrictModel):
    # See ``PlanStep`` — same LM-facing aliases, canonical storage keys.
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    step_id: str = Field(..., min_length=1, description="Unique identifier for the step.")
    step_kind: Literal["intro", "core", "evaluation"] = Field(
        ...,
        alias="step_role",
        description=(
            "Structural role of the step: 'intro' activates prior knowledge, 'core' "
            "teaches one lesson objective (carries knowledge_type + lesson_objective_id "
            "+ blocks), 'evaluation' checks mastery with practice blocks only."
        ),
    )
    instructional_type: InstructionalType | None = Field(
        default=None,
        description="Derived instructional pattern for rendered plan steps.",
    )
    kc_type: Literal["concept", "procedure", "representation"] | None = Field(
        default=None,
        alias="knowledge_type",
        description=(
            "What kind of knowledge a core step teaches (null for intro/evaluation). "
            "'concept' = a definition or idea, taught with an explanation only; "
            "'procedure' = a step-by-step method to carry out; 'representation' = "
            "reading or drawing a form such as a diagram, number line or table. "
            "'procedure' and 'representation' steps must include a worked_example and "
            "a practice block alongside the explanation."
        ),
    )
    lesson_objective_id: str | None = Field(
        default=None,
        description="Parent lesson-plan objective for core steps only.",
    )
    title: str = Field(..., min_length=1, description="Short label for the step.")
    content: str = Field(..., min_length=1, description="Teacher-facing summary of the step.")
    blocks: list[PlannerContentBlock] = Field(
        default_factory=list,
        description=(
            "Structured content blocks. The required block types depend on the step: "
            "a 'core' step with knowledge_type='concept' must include at least one 'explanation' "
            "block and NO 'worked_example' block; a 'core' step with knowledge_type='procedure' or "
            "'representation' must include ALL THREE of 'explanation', 'worked_example' and "
            "'practice'; an 'evaluation' step must contain only 'practice' blocks (each with a "
            "lesson_objective_id). Honour these when adding or editing a step."
        ),
    )
    estimated_minutes: int = Field(..., ge=1, description="Estimated time for the step in minutes.")
    activities: list[StepActivity] = Field(
        default_factory=list,
        description=(
            "What happens in this step, in the order it runs, each attributed to the "
            "teacher or the students."
        ),
    )

    @model_validator(mode="after")
    def _validate_structure(self) -> PlannerPlanStep:
        if self.step_kind == "core":
            if not self.lesson_objective_id:
                raise ValueError("core steps require lesson_objective_id")
            if self.kc_type is None:
                raise ValueError("core steps require knowledge_type")
            if not self.blocks:
                raise ValueError("core steps require at least one structured block")
            _validate_core_blocks_for_kc(self.kc_type, self.blocks)
            self.instructional_type = derive_core_instructional_type(self.blocks)
            return self

        if self.lesson_objective_id is not None:
            raise ValueError("only core steps may define lesson_objective_id")
        if self.kc_type is not None:
            raise ValueError("only core steps may define knowledge_type")

        if self.step_kind == "evaluation":
            self.instructional_type = "check"
            if not self.blocks:
                raise ValueError("evaluation steps require at least one practice block")
            for block in self.blocks:
                if not isinstance(block, PracticeBlock):
                    raise ValueError("evaluation steps may only contain practice blocks")
                if not block.lesson_objective_id:
                    raise ValueError("evaluation practice blocks require lesson_objective_id")
            return self

        self.instructional_type = None

        return self


class PlanAssessment(StrictModel):
    question: str = Field(..., min_length=1, description="Assessment prompt or question.")
    answer: str = Field(..., min_length=1, description="Expected answer or solution.")
    rubric: str | None = Field(
        default=None,
        description="Optional scoring guidance for the assessment.",
    )


class SessionPlan(StrictModel):
    plan_id: str = Field(..., min_length=1, description="Unique identifier for the plan.")
    session_id: str = Field(..., min_length=1, description="Curriculum session identifier.")
    subject: str = Field(..., min_length=1, description="Subject name for the lesson.")
    track: str = Field(..., min_length=1, description="Track or stream within the subject.")
    grade: str = Field(..., min_length=1, description="Grade level.")
    term: str = Field(..., min_length=1, description="Academic term name.")
    week: int = Field(..., ge=1, description="Week number in the term.")
    topic: str = Field(..., min_length=1, description="Curriculum topic title.")
    subtopic: str = Field(..., min_length=1, description="Curriculum subtopic title.")
    curriculum_objectives: list[CurriculumObjectiveRef] = Field(
        ...,
        min_length=1,
        description="Curriculum objectives that constrain the lesson plan.",
    )
    lesson_plan_objectives: list[LessonPlanObjective] = Field(
        ...,
        min_length=1,
        description="Teacher-facing lesson-plan objectives.",
    )
    misconceptions: list[str] = Field(
        default_factory=list,
        description="Common misconceptions to address during instruction.",
    )
    steps: list[PlanStep] = Field(..., min_length=1, description="Sequenced instructional steps.")
    assessments: list[PlanAssessment] = Field(
        default_factory=list,
        description="Optional checks or assessments aligned to objectives.",
    )
    theme: str | None = Field(default=None, description="NERDC curriculum theme.")
    entry_behaviour: list[str] = Field(
        default_factory=list,
        description="Expected prior knowledge from the previous lesson.",
    )
    instructional_materials: list[str] = Field(
        default_factory=list,
        description="Teaching/learning materials and resources.",
    )
    references: list[str] = Field(
        default_factory=list,
        description="Textbook and reference citations derived from the selected evidence.",
    )


class SessionPlanContent(StrictModel):
    curriculum_objectives: list[CurriculumObjectiveRef] = Field(
        ...,
        min_length=1,
        description="Curriculum objectives available to the planner.",
    )
    lesson_plan_objectives: list[LessonPlanObjective] = Field(
        ...,
        min_length=1,
        description="Teacher-facing lesson-plan objectives.",
    )
    misconceptions: list[str] = Field(
        default_factory=list,
        description="Common misconceptions to address during instruction.",
    )
    steps: list[PlanStep] = Field(..., min_length=1, description="Sequenced instructional steps.")
    assessments: list[PlanAssessment] = Field(
        default_factory=list,
        description="Optional checks or assessments aligned to objectives.",
    )
    theme: str | None = Field(default=None, description="NERDC curriculum theme.")
    entry_behaviour: list[str] = Field(
        default_factory=list,
        description="Expected prior knowledge from the previous lesson.",
    )
    instructional_materials: list[str] = Field(
        default_factory=list,
        description="Teaching/learning materials and resources.",
    )
    references: list[str] = Field(
        default_factory=list,
        description="Textbook and reference citations derived from the selected evidence.",
    )


class GlobalStepSet(StrictModel):
    intro_step: PlannerPlanStep
    evaluation_step: PlannerPlanStep
