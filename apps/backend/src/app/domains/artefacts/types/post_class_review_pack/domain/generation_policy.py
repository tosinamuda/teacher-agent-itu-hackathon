"""Product-owned controls for generating and validating review packs."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GenerationUnit = Literal["objective", "lesson_step"]
EvidenceScope = Literal["none", "unit", "objective", "step"]
PersonalisationMode = Literal["none", "reuse_base", "objective_indexed"]
ValidationCheck = Literal[
    "objective_coverage",
    "scope_compliance",
    "source_refs_present",
    "source_refs_valid",
    "objective_preservation",
    "content_grounding",
    "internal_consistency",
    "learner_facing_register",
    "practice_is_checkable",
    "explanation_present",
    "no_added_objectives",
]

#: The least explanation a section holds, in characters of text across its explanation blocks.
#: A section below it states the idea in a line and teaches nothing a learner can revise from.
MIN_EXPLANATION_CHARS = 300

STRUCTURAL_CHECKS: tuple[ValidationCheck, ...] = (
    "objective_coverage",
    "scope_compliance",
    "source_refs_present",
    "source_refs_valid",
    "objective_preservation",
    "practice_is_checkable",
    "explanation_present",
    "no_added_objectives",
)
PROSE_CHECKS: tuple[ValidationCheck, ...] = (
    "content_grounding",
    "internal_consistency",
    "learner_facing_register",
)


class ContextPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    generation_unit: GenerationUnit
    include_global_lesson_context: bool = True
    include_lesson_objectives: bool = True
    include_lesson_step_structure: bool = False
    include_step_title: bool = False
    include_step_content: bool = False
    include_teacher_student_activities: bool = False
    include_assessment_points: bool = False
    include_materials: bool = False
    include_entry_behaviour: bool = False
    include_lesson_sequence: bool = False
    include_instructional_events: bool = False
    include_student_tasks: bool = False
    #: Carry the drawing with an assessment question that depends on one. The model
    #: reads TikZ; the label summary it is otherwise given is not the same question.
    include_assessment_figures: bool = False


class RetrievalPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = False
    evidence_scope: EvidenceScope = "none"
    max_evidence_items_per_unit: int = 0
    require_source_refs: bool = False
    use_only_provided_sources: bool = False
    restrict_to_approved_scope: bool = True

    @property
    def provides_evidence(self) -> bool:
        return self.enabled and self.evidence_scope != "none"


class ValidationPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = False
    checks: tuple[ValidationCheck, ...] = ()
    retry_on_failure: bool = False
    max_retries: int = 0


class GenerationExecutionPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_patchable_findings: int = Field(default=3, ge=0)
    agent_max_iterations: int = Field(default=8, ge=1)


class PersonalisationPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    mode: PersonalisationMode = "none"
    use_objective_indexed_state: bool = False
    preserve_base_objectives: bool = True
    allow_section_dropping: bool = False
    #: The fewest marked questions an objective needs before its band adapts a section; below
    #: it the base section stays. Zero adapts on any evidence, as the study did.
    min_marked_questions: int = Field(default=0, ge=0)

    @property
    def reuses_base_sections(self) -> bool:
        return self.mode == "reuse_base"

    @property
    def adapts_to_learner_state(self) -> bool:
        return self.mode == "objective_indexed"


class ReviewPackGenerationPolicy(BaseModel):
    """Everything the review-pack product needs to generate and validate a pack."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    context: ContextPolicy
    retrieval: RetrievalPolicy = Field(default_factory=RetrievalPolicy)
    validation: ValidationPolicy = Field(default_factory=ValidationPolicy)
    personalisation: PersonalisationPolicy = Field(default_factory=PersonalisationPolicy)
    execution: GenerationExecutionPolicy = Field(default_factory=GenerationExecutionPolicy)


FULL_LESSON_CONTEXT = ContextPolicy(
    generation_unit="lesson_step",
    include_assessment_points=True,
    include_materials=True,
    include_entry_behaviour=True,
    include_lesson_sequence=True,
    include_instructional_events=True,
    include_student_tasks=True,
)
SCOPED_RETRIEVAL = RetrievalPolicy(
    enabled=True,
    evidence_scope="objective",
    max_evidence_items_per_unit=3,
    require_source_refs=True,
    use_only_provided_sources=True,
    restrict_to_approved_scope=True,
)
FULL_VALIDATION = ValidationPolicy(
    enabled=True,
    checks=(
        "objective_coverage",
        "scope_compliance",
        "source_refs_present",
        "source_refs_valid",
        "practice_is_checkable",
        "explanation_present",
        "content_grounding",
        "internal_consistency",
        "learner_facing_register",
    ),
    retry_on_failure=True,
    max_retries=2,
)
#: The class revision note is written with the context the rated Part 1 notes were: the
#: teacher's activities, narration and step titles, and the assessment's figures, on top of
#: the full lesson context. Personalisation keeps the full lesson context, as Part 2 did.
EVALUATED_CLASS_NOTE_CONTEXT = FULL_LESSON_CONTEXT.model_copy(
    update={
        "include_teacher_student_activities": True,
        "include_step_content": True,
        "include_step_title": True,
        "include_assessment_figures": True,
    }
)
BASE_REVIEW_PACK_POLICY = ReviewPackGenerationPolicy(
    context=EVALUATED_CLASS_NOTE_CONTEXT,
    retrieval=SCOPED_RETRIEVAL,
    validation=FULL_VALIDATION,
)
PERSONALISED_REVIEW_PACK_POLICY = ReviewPackGenerationPolicy(
    context=FULL_LESSON_CONTEXT,
    retrieval=SCOPED_RETRIEVAL,
    validation=ValidationPolicy(
        enabled=True,
        checks=(
            "objective_preservation",
            "no_added_objectives",
            "explanation_present",
            "source_refs_valid",
            "learner_facing_register",
        ),
        retry_on_failure=True,
        max_retries=1,
    ),
    personalisation=PersonalisationPolicy(
        mode="objective_indexed",
        use_objective_indexed_state=True,
        preserve_base_objectives=True,
        min_marked_questions=2,
    ),
)

#: The checks the product runs beyond the ones the study's rated notes passed.
CHECKS_ADDED_AFTER_THE_STUDY = frozenset({"explanation_present", "no_added_objectives"})


def as_the_study_ran_it(policy: ReviewPackGenerationPolicy) -> ReviewPackGenerationPolicy:
    """The policy without what the product added after the study, to compare with the rated one."""
    kept = tuple(
        check for check in policy.validation.checks if check not in CHECKS_ADDED_AFTER_THE_STUDY
    )
    return policy.model_copy(
        update={
            "validation": policy.validation.model_copy(update={"checks": kept}),
            "personalisation": policy.personalisation.model_copy(
                update={"min_marked_questions": 0}
            ),
        }
    )
