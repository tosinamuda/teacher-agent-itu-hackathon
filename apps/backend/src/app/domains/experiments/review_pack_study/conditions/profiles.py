"""Condition profiles — the source of truth for what each ablation condition allows.

eval-plan §7, §9-11. Each profile declares, per condition, which lesson-plan
context is passed, whether scoped source evidence is retrieved and required,
whether deterministic validation/retry runs, and whether personalisation is
active. The request builder and validator read these; DSPy never decides what a
condition means.
"""

from app.domains.experiments.domain.types import ConditionCode, Hypothesis

from .policies import (
    ConditionProfile,
    ContextPolicy,
    PersonalisationPolicy,
    RetrievalPolicy,
    TeacherValidationPolicy,
    ValidationPolicy,
)

_FULL_LESSON_PLAN_CONTEXT = ContextPolicy(
    generation_unit="lesson_step",
    include_global_lesson_context=True,
    include_lesson_objectives=True,
    # ``instructional_type`` is derived from ``blocks``, and on a field plan those are a
    # parse of her NOTE — so it is note evidence inside the no-note condition. It is also
    # a lossy one: it collapses the SET of block types to one of three words, and on
    # `t3-w05`'s volume step the parse read her four worked examples as explanations and
    # produced "explain_only" beside instructional_events ["present_content",
    # "provide_learning_guidance"] — the two fields contradicting each other in the same
    # prompt. ``instructional_events`` says the same thing from her Presentation column,
    # ordered and in her own terms, so this is superseded rather than merely dropped.
    include_lesson_step_structure=False,
    # Her own heading for each step. The descriptor of 12 of the 17 core-step titles
    # appears verbatim on her page, so this is her text and not the transcriber's —
    # an earlier note here said the opposite and was measured wrong. What it is NOT is
    # new: 12 of 17 are half or more the objective's own words, which the unit already
    # carries in ``objective_text``, and t3-w05's two are bare "Step 1"/"Step II" with
    # no descriptor at all. The `v5-narration-titles` variant sends it; this frozen
    # definition does not.
    include_step_title=False,
    # A step's ``content`` is her Presentation narration as one paragraph — the same
    # sentences ``activities`` carries split by actor — so sending both says everything
    # twice. Where she wrote no narration (t3-w02's perimeter step, t3-w09's tallying
    # step) the researcher-supplied title stands in, and a title is not plan evidence.
    # Every sentence of all seventeen core steps' ``content`` is in her Presentation and
    # none is in her note: `experiments.h1_condition_eval.source_boundary` measures this.
    include_step_content=False,
    # Activities are who-did-what in the room, in her words — "teacher solves some
    # questions on the board", "student copy worked examples into their notes" — on 15 of
    # the 17 core steps. The artefact spec forbids writing about the lesson as an event,
    # so under this definition they reach the model only as the Gagné labels derived from
    # them (``instructional_events``), which carry a step's function and none of its
    # wording. Whether the wording adds anything the labels lost is the question the
    # `v4-activities` context variant asks, in ``variants.py``; the frozen definition here
    # is what every judged run to date was generated under.
    include_teacher_student_activities=False,
    include_assessment_points=True,
    # Lesson-level in every plan she writes — one list for the whole lesson, never per
    # step — so it travels on the lesson context. Copied onto each unit it read as
    # step-scoped evidence, and t3-w05's volume section was handed "shapes of cylinders
    # and spheres".
    include_materials=True,
    # Her Previous knowledge line. Gagné's third event is what a plan is FOR, and it
    # reached nothing until now — the intro step that would rehearse it is filtered out
    # of the generation units, so prior knowledge has to travel on the lesson context.
    include_entry_behaviour=True,
    # Every unit is a separate concurrent LM call, so without the plan's own ordering the
    # unit teaching volume cannot know the unit teaching properties ran before it. Carried
    # by ``current_step`` against the ORDERED objective list, which the core steps match
    # one-for-one on all six lessons — a separate sequence object restated it.
    include_lesson_sequence=True,
    # Her Presentation narration, Gagné-coded. The prose itself never travels: the
    # artefact spec forbids writing about the lesson as an event, and the code is the
    # part a self-study pack can act on.
    include_instructional_events=True,
    # Her in-step Student Activity questions. A learner-directed task written into a
    # lesson-plan activity field is plan evidence; the mathematics answering it is not.
    include_student_tasks=True,
)

_SCOPED_RETRIEVAL = RetrievalPolicy(
    enabled=True,
    evidence_scope="objective",
    max_evidence_items_per_unit=3,
    require_source_refs=True,
    use_only_provided_sources=True,
    restrict_to_approved_scope=True,
)

_FULL_VALIDATION = ValidationPolicy(
    enabled=True,
    checks=(
        "objective_coverage",
        "scope_compliance",
        "source_refs_present",
        "source_refs_valid",
        "practice_is_checkable",
        "content_grounding",
        "internal_consistency",
        "learner_facing_register",
    ),
    retry_on_failure=True,
    max_retries=2,
)


H1_CONDITION_PROFILES: dict[ConditionCode, ConditionProfile] = {
    ConditionCode.C0: ConditionProfile(
        hypothesis=Hypothesis.H1,
        condition_code=ConditionCode.C0,
        generated_by=ConditionCode.C0,
        description="Objective-only baseline.",
        context=ContextPolicy(generation_unit="objective"),
    ),
    ConditionCode.C1: ConditionProfile(
        hypothesis=Hypothesis.H1,
        condition_code=ConditionCode.C1,
        generated_by=ConditionCode.C1,
        description="Teacher-confirmed lesson-plan condition.",
        context=_FULL_LESSON_PLAN_CONTEXT,
    ),
    ConditionCode.C2: ConditionProfile(
        hypothesis=Hypothesis.H1,
        condition_code=ConditionCode.C2,
        generated_by=ConditionCode.C2,
        description="Lesson-plan condition with explicit scoped grounding in the lesson note.",
        context=_FULL_LESSON_PLAN_CONTEXT,
        retrieval=_SCOPED_RETRIEVAL,
    ),
    ConditionCode.C3: ConditionProfile(
        hypothesis=Hypothesis.H1,
        condition_code=ConditionCode.C3,
        generated_by=ConditionCode.C3,
        description=(
            "Full constrained condition: lesson plan, grounding, then automated "
            "validation — structural checks plus an LLM critic that reads the pack "
            "against what the teacher taught — and repair of what either one flags."
        ),
        context=_FULL_LESSON_PLAN_CONTEXT,
        retrieval=_SCOPED_RETRIEVAL,
        validation=_FULL_VALIDATION,
    ),
    ConditionCode.C4: ConditionProfile(
        hypothesis=Hypothesis.H1,
        condition_code=ConditionCode.C4,
        generated_by=ConditionCode.C3,
        description="C3's pack put through a teacher-validation gate before final acceptance.",
        context=_FULL_LESSON_PLAN_CONTEXT,
        retrieval=_SCOPED_RETRIEVAL,
        validation=_FULL_VALIDATION,
        teacher_validation=TeacherValidationPolicy(enabled=True),
    ),
}


H2_CONDITION_PROFILES: dict[ConditionCode, ConditionProfile] = {
    ConditionCode.P0: ConditionProfile(
        hypothesis=Hypothesis.H2,
        condition_code=ConditionCode.P0,
        generated_by=ConditionCode.P0,
        description="Approved base pack reused unchanged for the focal learner.",
        context=_FULL_LESSON_PLAN_CONTEXT,
        personalisation=PersonalisationPolicy(mode="reuse_base"),
    ),
    ConditionCode.P1: ConditionProfile(
        hypothesis=Hypothesis.H2,
        condition_code=ConditionCode.P1,
        generated_by=ConditionCode.P1,
        description="Personalised pack from approved base pack + objective-indexed state.",
        context=_FULL_LESSON_PLAN_CONTEXT,
        retrieval=_SCOPED_RETRIEVAL,
        validation=ValidationPolicy(
            enabled=True,
            checks=(
                "objective_preservation",
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
        ),
    ),
}


def _registry_for(hypothesis: Hypothesis) -> dict[ConditionCode, ConditionProfile]:
    return H1_CONDITION_PROFILES if hypothesis == Hypothesis.H1 else H2_CONDITION_PROFILES


def condition_codes(hypothesis: Hypothesis) -> tuple[ConditionCode, ...]:
    """Return the canonical, ordered condition codes for a hypothesis.

    Derived from the profile registry — the single source of truth. Adding or removing a
    condition is done by editing the registry (plus the ``ConditionCode`` enum and the
    frontend code list); every consumer that derives from this picks it up automatically,
    so condition counts, sort orders, statistics and study-design defaults never hardcode
    the set.
    """
    return tuple(_registry_for(hypothesis))


def h1_main_condition_codes() -> tuple[ConditionCode, ...]:
    """H1 conditions in the MAIN comparison: C0–C3.

    Excludes teacher-validation-gated conditions (C4), which are separate
    teacher-governance evidence, not part of the H1 rater comparison (June-5
    settled design). Derived from the registry's ``teacher_validation`` flag, so
    it tracks the gate automatically — H1 scale, packet export, and statistics
    all use this set; generation still runs the full ``condition_codes(H1)``.
    """
    registry = _registry_for(Hypothesis.H1)
    return tuple(
        code
        for code in condition_codes(Hypothesis.H1)
        if not registry[code].teacher_validation.enabled
    )


def profile_for(hypothesis: Hypothesis, condition_code: ConditionCode) -> ConditionProfile:
    """Look up the condition profile for a hypothesis + condition code."""
    profile = _registry_for(hypothesis).get(condition_code)
    if profile is None:
        raise KeyError(f"no condition profile for {hypothesis.value}/{condition_code.value}")
    return profile
