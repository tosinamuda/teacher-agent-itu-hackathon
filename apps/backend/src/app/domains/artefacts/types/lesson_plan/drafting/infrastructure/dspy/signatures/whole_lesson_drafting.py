"""Single-call (monolithic) whole-lesson-plan drafting signature.

Used by the no-linkage generation layer (grounding_mode == "curriculum_only"):
one DSPy call drafts the entire plan — knowledge components, per-objective
evidence selection, core steps, intro/evaluation steps, assessments. This was the
bake-off winner (monolithic + refine) for ungrounded / cold-start subtopics where
no expert curated linkage exists.

`prior_violations` is the self-correction channel: on a retry it carries the
deterministic semantic violations of the previous attempt (the FULL check set in
production — there is no held-out split to protect here) so the model fixes them.
"""

from __future__ import annotations

import dspy

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    CandidateKC,
    GlobalStepSet,
    LessonPlanObjective,
    PlannerPlanStep,
    StepEvidencePlan,
)


class DraftWholeLessonPlanSignature(dspy.Signature):
    """Draft a complete, curriculum-faithful JSS1 mathematics lesson plan in one pass.

    You are an expert teacher. Produce every part of the plan together so it is
    internally consistent: the knowledge components, the per-objective evidence
    selection, the core teaching steps, the intro/evaluation steps, and the
    assessments.

    Grounding:
    - Use the provided textbook_records as the evidence base. Each KC's
      supporting_record_ids and each evidence plan's selected_record_ids MUST be
      real record_ids drawn from textbook_records.
    - When the only record is the curriculum placeholder (id "curriculum-only"),
      this is a cold-start: ground the plan in the curriculum objectives ALONE.
      Use "curriculum-only" as each KC's supporting_record_ids and each evidence
      plan's selected_record_ids/concept_record_ids, with modeling/practice/visual
      empty. Do NOT invent textbook pages, worksheets, or answer keys.

    Consistency rules the output MUST satisfy:
    - One LessonPlanObjective per curriculum objective, but AT MOST 4 in total. If
      there are more than four curriculum objectives, merge the most closely related
      ones so the plan defines no more than four core lesson objectives (a single
      40-minute lesson cannot teach more). lesson_objective_id values are unique and
      reused consistently across KCs, evidence plans, and core steps.
    - resolved_kcs: distinct knowledge_focus per curriculum objective; at least one KC is
      new learning (is_prior_knowledge=false); supporting_record_ids non-empty.
    - step_evidence_plans: one per lesson objective; selected_record_ids subset of
      the matching KC's supporting_record_ids; grouped ids subset of selected.
    - core_steps: one PlannerPlanStep per objective, step_role="core", with
      lesson_objective_id and knowledge_type set and at least one explanation block
      (concept KCs: explanation only; procedure/representation: explanation +
      worked_example + practice).
    - global_steps: intro_step (step_role="intro") and evaluation_step
      (step_role="evaluation"); the evaluation step contains practice blocks that
      each carry a lesson_objective_id. Do NOT mention ungrounded materials such as
      'worksheet', 'answer key', or 'response cards'.
    - assessments: at least one AssessmentItem aligned to the objectives.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(
        desc="The lesson-plan specification: what the plan is, who it is for, and the "
        "requirements it must meet. Follow every requirement exactly."
    )
    scope_context = dspy.InputField(
        desc="Subject/track/grade/term/week/topic/subtopic of the lesson."
    )
    curriculum_context = dspy.InputField(
        desc="Curriculum constraints: objectives, themes, materials, evaluation guide."
    )
    curriculum_objectives = dspy.InputField(
        desc="The ordered curriculum objectives the plan must fully and only cover."
    )
    textbook_records = dspy.InputField(
        desc="Grounding evidence records (id, type, content). For cold-start this is "
        "a single 'curriculum-only' placeholder record -> ground in the curriculum."
    )
    prior_violations = dspy.InputField(
        desc="Semantic violations from your PREVIOUS attempt (empty on the first "
        "attempt). If non-empty, FIX every one in this attempt."
    )

    lesson_plan_objectives: list[LessonPlanObjective] = dspy.OutputField(
        desc="Teacher-facing lesson objectives, one per curriculum objective "
        "(at most four; merge related ones if there are more), ordered."
    )
    resolved_kcs: list[CandidateKC] = dspy.OutputField(
        desc="Knowledge components; distinct knowledge_focus; non-empty supporting_record_ids."
    )
    step_evidence_plans: list[StepEvidencePlan] = dspy.OutputField(
        desc="One evidence plan per lesson objective; ids consistent with the KCs and records."
    )
    core_steps: list[PlannerPlanStep] = dspy.OutputField(
        desc="One core teaching step per objective, with structured content blocks."
    )
    global_steps: GlobalStepSet = dspy.OutputField(
        desc="The intro_step and evaluation_step bracketing the core steps."
    )
    assessments: list[AssessmentItem] = dspy.OutputField(
        desc="Assessment items aligned to the lesson objectives."
    )
    misconceptions: list[str] = dspy.OutputField(
        desc="Common misconceptions to address during instruction."
    )
