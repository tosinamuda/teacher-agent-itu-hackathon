"""Single-call (monolithic) whole-lesson generator for the no-linkage layer.

One DSPy call drafts the entire plan (the bake-off winner for ungrounded /
cold-start subtopics). Its output is adapted into `WholeLessonArtifacts`, whose
attribute surface matches what `SessionPlanAssembler` and
`SemanticPlanValidator.collect_issues()` read — so the no-linkage path is
assembled and scored by the same code as the staged/curated paths, without the
staged planner/drafter or a heavy `KCPlanningResult`.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import dspy

from app.shared.json_types import JsonObject

from ....domain.generation_inputs import PreparedGenerationInputs
from ....schemas.session_plan import (
    AssessmentItem,
    CandidateKC,
    GlobalStepSet,
    LessonPlanObjective,
    PlannerPlanStep,
    StepEvidencePlan,
)
from ..evidence_plan import summarize_evidence_bundle
from ..signatures.whole_lesson_drafting import DraftWholeLessonPlanSignature
from ..textbook_support import select_textbook_records


@dataclass(frozen=True)
class _WholeLessonKCPlan:
    """Minimal stand-in for CandidateKCPlan: only the fields the assembler reads."""

    misconceptions: list[str] = field(default_factory=list)
    theme: str | None = None
    entry_behaviour: list[str] = field(default_factory=list)
    instructional_materials: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WholeLessonArtifacts:
    """Duck-typed artifacts the assembler + semantic validator consume."""

    lesson_plan_objectives: list[LessonPlanObjective]
    resolved_kcs: list[CandidateKC]
    step_evidence_plans: dict[str, StepEvidencePlan]
    core_steps: list[PlannerPlanStep]
    global_steps: GlobalStepSet
    assessment_items: list[AssessmentItem]
    kc_plan: _WholeLessonKCPlan
    evidence_summaries: list[JsonObject]


def adapt_whole_plan_prediction(
    prediction: dspy.Prediction,
    request: PreparedGenerationInputs,
) -> WholeLessonArtifacts:
    """Map a one-call prediction into the artifacts the assembler/validator read."""
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
    kc_plan = _WholeLessonKCPlan(
        misconceptions=list(prediction.misconceptions or []),
        theme=request.curriculum.theme,
        entry_behaviour=list(request.curriculum.entry_behaviour),
        instructional_materials=list(request.curriculum.instructional_materials),
    )
    return WholeLessonArtifacts(
        lesson_plan_objectives=list(prediction.lesson_plan_objectives),
        resolved_kcs=list(prediction.resolved_kcs),
        step_evidence_plans=evidence_by_objective,
        core_steps=list(prediction.core_steps),
        global_steps=prediction.global_steps,
        assessment_items=list(prediction.assessments),
        kc_plan=kc_plan,
        evidence_summaries=evidence_summaries,
    )


class WholeLessonGenerationModule(dspy.Module):
    """One-call drafter (chain-of-thought — the confirmed bake-off winner).

    Optionally loads the GEPA-optimized prompt (instruction-only, no demos) in
    place of the default signature instructions. The artifact was saved from a
    bare ``ChainOfThought`` over the same signature, so its ``predict`` state
    maps directly onto ``self.writer``.
    """

    def __init__(
        self,
        *,
        final_writer_mode: str = "chain_of_thought",
        use_optimized: bool = False,
        optimized_program_path: str | None = None,
    ) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.writer = dspy.ChainOfThought(DraftWholeLessonPlanSignature)
        self.optimized_loaded = False
        if use_optimized:
            path = (
                Path(optimized_program_path)
                if optimized_program_path
                else self._default_optimized_path()
            )
            if not path.exists():
                raise FileNotFoundError(
                    f"GEPA-optimized program not found at {path}; set "
                    "lesson_plan.use_optimized_program=False or fix "
                    "optimized_program_path."
                )
            self.writer.load(str(path))
            self.optimized_loaded = True
            self.logger.info("whole_lesson_generator loaded GEPA-optimized program from %s", path)

    @staticmethod
    def _default_optimized_path() -> Path:
        # No-linkage-safe variant of the GEPA artifact: the raw GEPA prompt froze
        # a grounded worksheet demonstration that hallucinates on cold-start, so
        # the bundled default neutralises it (see build_nolinkage_optimized_program.py).
        # The raw whole_lesson_gepa.json is kept for provenance / explicit override.
        return (
            Path(__file__).resolve().parent.parent
            / "optimized"
            / "whole_lesson_gepa_nolinkage.json"
        )

    def forward(
        self,
        *,
        request: PreparedGenerationInputs,
        prior_violations: list[str] | None = None,
    ) -> WholeLessonArtifacts:
        prediction = self.writer(
            scope_context=request.scope_payload(),
            curriculum_context=request.curriculum_payload(),
            curriculum_objectives=request.curriculum_objective_payloads(),
            textbook_records=request.textbook_record_payloads(),
            prior_violations=prior_violations or [],
            artefact_spec=request.brief,
        )
        return adapt_whole_plan_prediction(prediction, request)
