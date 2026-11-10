from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import TypedDict

import dspy

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.shared.json_types import JsonObject

from ....application.precompute import (
    InfrastructurePlanningPipeline,
    KCPlanningResult,
    LessonDraftResult,
)
from ....application.precompute.curated_planning import build_curated_planning
from ....application.precompute.curated_planning_adapter import (
    curated_artifacts_to_kc_planning_result,
)
from ....domain.evaluation_step import build_evaluation_step
from ....domain.generation_inputs import PreparedGenerationInputs
from ....schemas.session_plan import (
    AssessmentItem,
    CandidateKC,
    CandidateKCPlan,
    CoreStepBlueprint,
    GlobalStepSet,
    LessonPlanObjective,
    PlannerPlanStep,
    StepEvidencePlan,
)
from ..evidence_plan import (
    build_supported_evidence_plan,
    ensure_evidence_matches_objective,
    summarize_evidence_bundle,
)
from ..kc_compression import LessonStructure
from ..model_io import read_validated_model
from ..signatures.core_step_drafting import GenerateCoreStepSignature
from ..signatures.global_step_drafting import GenerateGlobalStepsSignature
from ..textbook_support import PRACTICE_SUPPORT_TYPES, select_textbook_records
from .assessment_designer import AssessmentDesigner

FINAL_WRITER_MODES = {"predict", "chain_of_thought"}


class _CoreStepInputs(TypedDict):
    """LLM input bundle for one core step, spread as kwargs into the DSPy signature."""

    scope_context: JsonObject
    curriculum_context: JsonObject
    lesson_objective: JsonObject
    knowledge_component: JsonObject
    step_blueprint: JsonObject
    step_evidence_plan: JsonObject
    evidence_bundle: dict[str, list[JsonObject]]
    target_assessment: JsonObject
    prior_violations: list[str]
    artefact_spec: ArtefactSpec | None


class _GlobalStepInputs(TypedDict):
    """LLM input bundle for the global (intro/evaluation) steps."""

    scope_context: JsonObject
    curriculum_context: JsonObject
    lesson_objectives: list[JsonObject]
    core_steps: dict[str, list[JsonObject]]
    evidence_summaries: dict[str, list[JsonObject]]
    prior_violations: list[str]
    artefact_spec: ArtefactSpec | None


@dataclass(frozen=True)
class LessonGenerationArtifacts:
    planning_result: KCPlanningResult
    kc_plan: CandidateKCPlan
    resolved_kcs: list[CandidateKC]
    lesson_plan_objectives: list[LessonPlanObjective]
    core_step_blueprints: list[CoreStepBlueprint]
    assessment_items: list[AssessmentItem]
    step_evidence_plans: dict[str, StepEvidencePlan]
    core_steps: list[PlannerPlanStep]
    global_steps: GlobalStepSet
    evidence_summaries: list[JsonObject]
    planning_duration_ms: int
    drafting_duration_ms: int
    drafting_llm_call_estimate: int


def _build_final_writer(signature: type[dspy.Signature], *, mode: str) -> dspy.Module:
    normalized_mode = str(mode or "").strip().lower()
    if normalized_mode == "predict":
        return dspy.Predict(signature)
    if normalized_mode == "chain_of_thought":
        return dspy.ChainOfThought(signature)
    raise ValueError(f"unsupported lesson plan final writer mode: {mode}")


class InfrastructurePlanningModule(dspy.Module):
    """Build lesson infrastructure from one validated lesson-generation request."""

    def __init__(self, *, model_name: str | None = None) -> None:
        super().__init__()
        # Propagate the LLM model name to the planning pipeline so the
        # InfrastructureArtifactCache's model_name invalidation dimension
        # has something to compare against — switching models must miss
        # cache entries computed under the previous one.
        self.infrastructure_builder = InfrastructurePlanningPipeline(model_name=model_name)

    def forward(self, *, request: PreparedGenerationInputs) -> KCPlanningResult:
        return self.infrastructure_builder.build_infrastructure(
            scope_context=request.scope_payload(),
            curriculum_context=request.curriculum_payload(),
            curriculum_objectives=request.curriculum_objective_payloads(),
            textbook_records=request.textbook_record_payloads(),
        )


class LessonDraftWriter(dspy.Module):
    """Draft lesson steps from cached planning infrastructure and grounded evidence."""

    def __init__(self, *, final_writer_mode: str) -> None:
        super().__init__()
        self.final_writer_mode = str(final_writer_mode or "").strip().lower()
        self.core_step_writer = _build_final_writer(
            GenerateCoreStepSignature,
            mode=self.final_writer_mode,
        )
        self.global_step_writer = _build_final_writer(
            GenerateGlobalStepsSignature,
            mode=self.final_writer_mode,
        )
        self.assessment_designer = AssessmentDesigner()

    def _core_step_inputs(
        self,
        *,
        lesson_structure: LessonStructure,
        lesson_objective_id: str,
        request: PreparedGenerationInputs,
        evidence_plan: StepEvidencePlan,
        evidence_bundle: list[JsonObject],
        target_assessment: AssessmentItem | None,
        prior_violations: list[str] | None = None,
    ) -> _CoreStepInputs:
        lesson_objective = lesson_structure.objectives_by_id[lesson_objective_id]
        blueprint = next(
            item
            for item in lesson_structure.blueprints
            if item.lesson_objective_id == lesson_objective_id
        )
        knowledge_component = lesson_structure.kcs_by_objective_id[lesson_objective_id]
        # by_alias=True throughout: these are LM-facing inputs, so they must use
        # the same field vocabulary (knowledge_type / step_role) the output schema
        # asks for. Harmless for models without aliases.
        return {
            "scope_context": request.scope_payload(),
            "curriculum_context": request.curriculum_payload(),
            "lesson_objective": lesson_objective.model_dump(by_alias=True),
            "knowledge_component": knowledge_component.model_dump(by_alias=True),
            "step_blueprint": blueprint.model_dump(by_alias=True),
            "step_evidence_plan": evidence_plan.model_dump(by_alias=True),
            "evidence_bundle": {"evidence": evidence_bundle},
            "target_assessment": (
                target_assessment.model_dump(by_alias=True) if target_assessment is not None else {}
            ),
            "prior_violations": prior_violations or [],
            "artefact_spec": request.brief,
        }

    def _global_step_inputs(
        self,
        *,
        lesson_structure: LessonStructure,
        core_steps: list[PlannerPlanStep],
        evidence_summaries: list[JsonObject],
        request: PreparedGenerationInputs,
        prior_violations: list[str] | None = None,
    ) -> _GlobalStepInputs:
        return {
            "scope_context": request.scope_payload(),
            "curriculum_context": request.curriculum_payload(),
            "lesson_objectives": [
                item.model_dump(by_alias=True) for item in lesson_structure.objectives
            ],
            "core_steps": {"core_steps": [item.model_dump(by_alias=True) for item in core_steps]},
            "evidence_summaries": {"evidence_summaries": evidence_summaries},
            "prior_violations": prior_violations or [],
            "artefact_spec": request.brief,
        }

    def _draft_core_steps(
        self,
        *,
        lesson_structure: LessonStructure,
        evidence_by_objective: dict[str, StepEvidencePlan],
        assessment_by_objective: dict[str, AssessmentItem],
        request: PreparedGenerationInputs,
        prior_violations: list[str] | None = None,
    ) -> tuple[list[PlannerPlanStep], list[JsonObject]]:
        textbook_records = request.textbook_record_payloads()
        drafted_steps: list[PlannerPlanStep] = []
        evidence_summaries: list[JsonObject] = []

        for blueprint in lesson_structure.blueprints:
            lesson_objective_id = blueprint.lesson_objective_id
            evidence_plan = evidence_by_objective[lesson_objective_id]
            evidence_bundle = select_textbook_records(
                evidence_plan.selected_record_ids,
                textbook_records,
            )
            evidence_summaries.append(
                summarize_evidence_bundle(
                    lesson_objective_id=lesson_objective_id,
                    evidence_bundle=evidence_bundle,
                )
            )
            step_result = self.core_step_writer(
                **self._core_step_inputs(
                    lesson_structure=lesson_structure,
                    lesson_objective_id=lesson_objective_id,
                    request=request,
                    evidence_plan=evidence_plan,
                    evidence_bundle=evidence_bundle,
                    target_assessment=assessment_by_objective.get(lesson_objective_id),
                    prior_violations=prior_violations,
                )
            )
            drafted_steps.append(
                read_validated_model(
                    step_result.core_step,
                    label="core_step",
                    model_type=PlannerPlanStep,
                )
            )

        return drafted_steps, evidence_summaries

    def _ensure_assessment_items(
        self,
        *,
        lesson_structure: LessonStructure,
        existing: dict[str, AssessmentItem],
        request: PreparedGenerationInputs,
    ) -> dict[str, AssessmentItem]:
        """Guarantee one assessment item per objective for deterministic eval assembly.

        Curated linkage rows do not always carry an ``assessment``, so the manual_linkage
        planner can yield an incomplete (or empty) assessment set. Design the missing ones
        with the same ``AssessmentDesigner`` the curriculum_only path uses, so the
        evaluation step can always be assembled deterministically from real, grounded items
        rather than authored (and dropped) by the LLM in the global-step pass.
        """
        textbook_records = request.textbook_record_payloads()
        assessment_by_objective = dict(existing)
        for lesson_objective in lesson_structure.objectives:
            lesson_objective_id = lesson_objective.lesson_objective_id
            if lesson_objective_id in assessment_by_objective:
                continue
            candidate_kc = lesson_structure.kcs_by_objective_id[lesson_objective_id]
            source_records = select_textbook_records(
                candidate_kc.supporting_record_ids,
                textbook_records,
            )
            exercise_records = [
                record
                for record in source_records
                if str(record.get("record_type") or "").strip() in PRACTICE_SUPPORT_TYPES
            ]
            assessment_by_objective[lesson_objective_id] = self.assessment_designer(
                kc=candidate_kc,
                source_records=source_records,
                exercise_records=exercise_records,
                lesson_objective_id=lesson_objective_id,
            )
        return assessment_by_objective

    def _draft_global_steps(
        self,
        *,
        lesson_structure: LessonStructure,
        core_steps: list[PlannerPlanStep],
        evidence_summaries: list[JsonObject],
        request: PreparedGenerationInputs,
        assessment_by_objective: dict[str, AssessmentItem],
        prior_violations: list[str] | None = None,
    ) -> GlobalStepSet:
        global_result = self.global_step_writer(
            **self._global_step_inputs(
                lesson_structure=lesson_structure,
                core_steps=core_steps,
                evidence_summaries=evidence_summaries,
                request=request,
                prior_violations=prior_violations,
            )
        )
        intro_step = read_validated_model(
            global_result.intro_step,
            label="intro_step",
            model_type=PlannerPlanStep,
        )
        # The evaluation step is assembled deterministically from the curated assessment
        # items (no LLM) — the model only authors the intro. This removes the stochastic
        # "evaluation steps require at least one practice block" crash entirely.
        evaluation_step = build_evaluation_step(assessment_by_objective)
        return GlobalStepSet(intro_step=intro_step, evaluation_step=evaluation_step)


class CachedLessonDraftingModule(LessonDraftWriter):
    """Draft a lesson from cached evidence plans, falling back only to deterministic support."""

    def forward(
        self,
        *,
        request: PreparedGenerationInputs,
        planning_result: KCPlanningResult,
        prior_violations: list[str] | None = None,
    ) -> LessonDraftResult:
        lesson_structure = planning_result.lesson_structure
        evidence_by_objective = self._resolve_evidence_plans(
            lesson_structure=lesson_structure,
            planning_result=planning_result,
            textbook_records=request.textbook_record_payloads(),
            authoritative=request.grounding_mode == "manual_linkage",
        )
        core_steps, evidence_summaries = self._draft_core_steps(
            lesson_structure=lesson_structure,
            evidence_by_objective=evidence_by_objective,
            assessment_by_objective=planning_result.assessment_items,
            request=request,
            prior_violations=prior_violations,
        )
        assessment_by_objective = self._ensure_assessment_items(
            lesson_structure=lesson_structure,
            existing=planning_result.assessment_items,
            request=request,
        )
        global_steps = self._draft_global_steps(
            lesson_structure=lesson_structure,
            core_steps=core_steps,
            evidence_summaries=evidence_summaries,
            request=request,
            assessment_by_objective=assessment_by_objective,
            prior_violations=prior_violations,
        )
        return LessonDraftResult(
            core_steps=core_steps,
            global_steps=global_steps,
            evidence_summaries=evidence_summaries,
            step_evidence_by_objective=evidence_by_objective,
        )

    def _resolve_evidence_plans(
        self,
        *,
        lesson_structure: LessonStructure,
        planning_result: KCPlanningResult,
        textbook_records: list[JsonObject],
        authoritative: bool = False,
    ) -> dict[str, StepEvidencePlan]:
        evidence_by_objective = dict(planning_result.step_evidence_plans)
        for lesson_objective in lesson_structure.objectives:
            lesson_objective_id = lesson_objective.lesson_objective_id
            candidate_kc = lesson_structure.kcs_by_objective_id[lesson_objective_id]
            cached_plan = evidence_by_objective.get(lesson_objective_id)
            freshly_built = cached_plan is None
            if cached_plan is None:
                evidence_plan = build_supported_evidence_plan(
                    lesson_objective=lesson_objective,
                    candidate_kc=candidate_kc,
                    textbook_records=textbook_records,
                )
                if evidence_plan is None:
                    raise ValueError(
                        f"missing cached evidence plan for lesson objective: {lesson_objective_id}"
                    )
            else:
                evidence_plan = cached_plan
            # Validate freshly-built plans, and re-validate cached plans on the LLM
            # path. The authoritative curated path is trusted as-is: the expert
            # curation decided the per-objective roles, which need not satisfy the
            # LLM pipeline's record-type contract (e.g. a curated objective may be
            # taught from a worked example with no separate concept-type record).
            if freshly_built or not authoritative:
                ensure_evidence_matches_objective(
                    evidence_plan,
                    lesson_objective=lesson_objective,
                    textbook_records=textbook_records,
                    candidate_kc=candidate_kc,
                )
            evidence_by_objective[lesson_objective_id] = evidence_plan
        return evidence_by_objective


class LessonGenerationModule(dspy.Module):
    """Plan the infrastructure first, then draft the lesson from saved evidence."""

    def __init__(
        self,
        *,
        final_writer_mode: str = "chain_of_thought",
        model_name: str | None = None,
    ) -> None:
        super().__init__()
        self.final_writer_mode = str(final_writer_mode or "").strip().lower()
        if self.final_writer_mode not in FINAL_WRITER_MODES:
            raise ValueError(f"unsupported lesson plan final writer mode: {final_writer_mode}")
        self.infrastructure_planner = InfrastructurePlanningModule(model_name=model_name)
        self.draft_builder = CachedLessonDraftingModule(final_writer_mode=self.final_writer_mode)

    def _llm_plan(self, request: PreparedGenerationInputs) -> KCPlanningResult:
        """Run the LLM infrastructure-planning stage (the untyped dspy boundary)."""
        result: KCPlanningResult = self.infrastructure_planner(request=request)
        return result

    def _plan(self, request: PreparedGenerationInputs) -> KCPlanningResult:
        """Authoritative curated planning for the manual-linkage path; otherwise.

        the LLM planning stage. Falls back to LLM planning if the curated rows
        carry no usable textbook evidence.
        """
        if request.grounding_mode == "manual_linkage" and request.curated_objectives:
            try:
                curated = build_curated_planning(
                    curated_objectives=request.curated_objectives,
                    theme=request.curriculum.theme,
                    entry_behaviour=request.curriculum.entry_behaviour,
                    instructional_materials=request.curriculum.instructional_materials,
                    curriculum_objectives=request.curriculum_objective_payloads(),
                )
            except ValueError:
                # No grounded curated objective -> fall back to LLM planning.
                return self._llm_plan(request)
            return curated_artifacts_to_kc_planning_result(
                curated,
                scope_context=request.scope_payload(),
                curriculum_objectives=request.curriculum_objective_payloads(),
            )
        return self._llm_plan(request)

    def forward(
        self,
        *,
        request: PreparedGenerationInputs,
        prior_violations: list[str] | None = None,
    ) -> LessonGenerationArtifacts:
        planning_started_at = perf_counter()
        planning_result = self._plan(request)
        planning_duration_ms = getattr(
            planning_result,
            "planning_duration_ms",
            int(round((perf_counter() - planning_started_at) * 1000)),
        )

        drafting_started_at = perf_counter()
        draft_result = self.draft_builder(
            request=request,
            planning_result=planning_result,
            prior_violations=prior_violations,
        )
        drafting_duration_ms = int(round((perf_counter() - drafting_started_at) * 1000))

        return LessonGenerationArtifacts(
            planning_result=planning_result,
            kc_plan=planning_result.combined_kc_plan,
            resolved_kcs=planning_result.resolved_kcs,
            lesson_plan_objectives=planning_result.lesson_structure.objectives,
            core_step_blueprints=planning_result.lesson_structure.blueprints,
            assessment_items=list(planning_result.assessment_items.values()),
            step_evidence_plans=draft_result.step_evidence_by_objective,
            core_steps=draft_result.core_steps,
            global_steps=draft_result.global_steps,
            evidence_summaries=draft_result.evidence_summaries,
            planning_duration_ms=planning_duration_ms,
            drafting_duration_ms=drafting_duration_ms,
            drafting_llm_call_estimate=len(planning_result.lesson_structure.objectives) + 1,
        )
