"""Single-signature (monolithic) lesson-plan generation for the granularity axis.

The production path is MULTI-signature (staged): KC extraction, then per-objective
core-step drafting, then a global-step pass. This module is the SINGLE-signature
arm of pre-registration axis B: one DSPy call drafts the whole plan.

Design choice that keeps the comparison fair: the monolithic module emits the SAME
typed structures the staged pipeline produces (`CandidateKC`, `StepEvidencePlan`,
`PlannerPlanStep`, `GlobalStepSet`, ...), adapted into a `MonolithicArtifacts`
object whose attribute surface matches `LessonGenerationArtifacts`. The experiment's
`generate_scored` then runs the EXACT same `SessionPlanAssembler` +
`SemanticPlanValidator.collect_issues()` over both arms, so any difference is the
architecture, not the scoring. Asking one call to satisfy all the nested schema
validators is hard on purpose — its schema-validity rate is a headline finding
(pre-reg hypothesis E3).

No production code is modified; this lives entirely in the experiment package.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import dspy

from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    PreparedGenerationInputs,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.evidence_plan import (
    summarize_evidence_bundle,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.textbook_support import (
    select_textbook_records,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    CandidateKC,
    GlobalStepSet,
    LessonPlanObjective,
    PlannerPlanStep,
    StepEvidencePlan,
)
from app.shared.json_types import JsonObject

from .reasoning import REACT_MAX_ITERS, build_reasoning_module, normalize_reasoning


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
    - If textbook_records is EMPTY (cold-start), ground the plan in the curriculum
      objectives ALONE. In that case, for every KC use the single placeholder
      record id "curriculum-only" as its supporting_record_ids, and set each
      evidence plan's selected_record_ids and concept_record_ids to
      ["curriculum-only"] with modeling/practice/visual empty. Do NOT invent
      textbook page numbers, worksheets, or answer keys that are not grounded.

    Consistency rules the output MUST satisfy:
    - One LessonPlanObjective per curriculum objective; lesson_objective_id values
      are unique and reused consistently across KCs, evidence plans, and core steps.
    - resolved_kcs: distinct kc_focus per curriculum objective; at least one KC is
      new learning (is_prior_knowledge=false); supporting_record_ids non-empty.
    - step_evidence_plans: one per lesson objective; selected_record_ids ⊆ the
      matching KC's supporting_record_ids; grouped ids ⊆ selected_record_ids.
    - core_steps: one PlannerPlanStep per objective, step_kind="core", with
      lesson_objective_id and kc_type set and at least one explanation block
      (concept KCs: explanation only; procedure/representation: explanation +
      worked_example + practice).
    - global_steps: intro_step (step_kind="intro") and evaluation_step
      (step_kind="evaluation"); the evaluation step contains practice blocks that
      each carry a lesson_objective_id.
    - assessments: at least one AssessmentItem aligned to the objectives.
    """

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
        desc="Grounding evidence records (id, type, content). MAY BE EMPTY -> "
        "cold-start: ground in the curriculum only and use the 'curriculum-only' "
        "placeholder record id as described in the instructions."
    )
    prior_violations = dspy.InputField(
        desc="Structural violations from your PREVIOUS attempt (empty on the first "
        "attempt). If non-empty, FIX each one in this attempt."
    )

    lesson_plan_objectives: list[LessonPlanObjective] = dspy.OutputField(
        desc="Teacher-facing lesson objectives, one per curriculum objective, ordered."
    )
    resolved_kcs: list[CandidateKC] = dspy.OutputField(
        desc="Knowledge components; distinct kc_focus; non-empty supporting_record_ids."
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


@dataclass(frozen=True)
class _MonolithicKCPlan:
    """Minimal stand-in for CandidateKCPlan: only the fields the assembler reads."""

    misconceptions: list[str] = field(default_factory=list)
    theme: str | None = None
    entry_behaviour: list[str] = field(default_factory=list)
    instructional_materials: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MonolithicArtifacts:
    """Duck-typed twin of LessonGenerationArtifacts (only the consumed fields).

    `SessionPlanAssembler` and `SemanticPlanValidator.collect_issues()` access
    artifacts purely by attribute, so this object is scored by the exact same code
    paths as the staged backend without stubbing the heavy `KCPlanningResult`.
    """

    lesson_plan_objectives: list[LessonPlanObjective]
    resolved_kcs: list[CandidateKC]
    step_evidence_plans: dict[str, StepEvidencePlan]
    core_steps: list[PlannerPlanStep]
    global_steps: GlobalStepSet
    assessment_items: list[AssessmentItem]
    kc_plan: _MonolithicKCPlan
    evidence_summaries: list[JsonObject]


def adapt_prediction(
    prediction: dspy.Prediction,
    request: PreparedGenerationInputs,
) -> MonolithicArtifacts:
    """Map a one-call DSPy prediction into the artifacts the scorer consumes."""
    records = request.textbook_record_payloads()
    evidence_by_objective: dict[str, StepEvidencePlan] = {
        plan.lesson_objective_id: plan for plan in prediction.step_evidence_plans
    }
    evidence_summaries: list[JsonObject] = []
    for objective in prediction.lesson_plan_objectives:
        plan = evidence_by_objective.get(objective.lesson_objective_id)
        bundle = select_textbook_records(plan.selected_record_ids, records) if plan else []
        evidence_summaries.append(
            summarize_evidence_bundle(
                lesson_objective_id=objective.lesson_objective_id,
                evidence_bundle=bundle,
            )
        )
    kc_plan = _MonolithicKCPlan(
        misconceptions=list(prediction.misconceptions or []),
        theme=request.curriculum.theme,
        entry_behaviour=list(request.curriculum.entry_behaviour),
        instructional_materials=list(request.curriculum.instructional_materials),
    )
    return MonolithicArtifacts(
        lesson_plan_objectives=list(prediction.lesson_plan_objectives),
        resolved_kcs=list(prediction.resolved_kcs),
        step_evidence_plans=evidence_by_objective,
        core_steps=list(prediction.core_steps),
        global_steps=prediction.global_steps,
        assessment_items=list(prediction.assessments),
        kc_plan=kc_plan,
        evidence_summaries=evidence_summaries,
    )


def _build_react_tools(request: PreparedGenerationInputs) -> list:
    """Record-lookup tools for the ReAct drafter (grounding, no held-out leakage).

    These let the agent inspect the grounding evidence before committing to KCs
    and evidence selection, rather than producing the whole plan blind. They never
    expose the deterministic checks, so there is no metric leakage (pre-reg §4b).
    """
    records = request.textbook_record_payloads()
    by_id = {str(r.get("record_id")): r for r in records}

    def list_record_ids() -> list[str]:
        """Return the textbook record ids you may cite. Use ONLY these ids in
        supporting_record_ids / selected_record_ids. If empty, this is a
        cold-start: use the 'curriculum-only' placeholder id."""
        return list(by_id) or ["curriculum-only"]

    def record_detail(record_id: str) -> str:
        """Return the type, title, and a content snippet of one textbook record,
        so KCs and evidence selection are grounded in real material."""
        record = by_id.get(record_id)
        if record is None:
            return f"no record with id {record_id!r}; call list_record_ids first"
        return (
            f"record_type={record.get('record_type')} title={record.get('title')!r} "
            f"content={str(record.get('content'))[:500]!r}"
        )

    return [list_record_ids, record_detail]


class MonolithicLessonGenerationModule(dspy.Module):
    """Single-call lesson-plan drafter (the single-signature architecture arm).

    Reasoning modes: predict/cot/rlm are drop-in writers; `react` is a tool-using
    agent built PER REQUEST (its record-lookup tools need the request context),
    bounded at REACT_MAX_ITERS.
    """

    def __init__(
        self, *, reasoning: str = "cot", final_writer_mode: str = "chain_of_thought"
    ) -> None:
        super().__init__()
        # final_writer_mode is accepted for signature parity with the staged
        # module; the monolithic arm's reasoning is governed by `reasoning`.
        self.reasoning = normalize_reasoning(reasoning)
        # react is rebuilt per forward() (tools are request-bound); others are
        # static drop-in writers.
        self.writer = (
            None
            if self.reasoning == "react"
            else build_reasoning_module(DraftWholeLessonPlanSignature, reasoning=self.reasoning)
        )

    def _writer_for(self, request: PreparedGenerationInputs) -> dspy.Module:
        if self.reasoning == "react":
            return dspy.ReAct(
                DraftWholeLessonPlanSignature,
                tools=_build_react_tools(request),
                max_iters=REACT_MAX_ITERS,
            )
        return self.writer

    def forward(
        self,
        *,
        request: PreparedGenerationInputs,
        prior_violations: list[str] | None = None,
    ) -> MonolithicArtifacts:
        writer = self._writer_for(request)
        prediction = writer(
            scope_context=request.scope_payload(),
            curriculum_context=request.curriculum_payload(),
            curriculum_objectives=request.curriculum_objective_payloads(),
            textbook_records=request.textbook_record_payloads(),
            prior_violations=prior_violations or [],
        )
        return adapt_prediction(prediction, request)
