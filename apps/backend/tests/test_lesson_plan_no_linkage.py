"""No-LLM tests for the no-linkage (curriculum_only) generation layer (Phase 10B).

Covers the deterministic pieces: the one-call prediction -> WholeLessonArtifacts
adapter, and cold-start synthetic-record injection in prepare_generation_inputs.
The monolithic + refine loop itself is verified by the live smoke.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import cast

import pytest

from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    LessonGenerationService,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    COLD_START_RECORD_ID,
    LessonCurriculumContext,
    LessonGenerationSession,
    PreparedGenerationInputs,
    build_scope_context,
    prepare_generation_inputs,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.whole_lesson_generator import (  # noqa: E501
    WholeLessonArtifacts,
    WholeLessonGenerationModule,
    _WholeLessonKCPlan,
    adapt_whole_plan_prediction,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CandidateKC,
    GlobalStepSet,
    LessonPlanObjective,
    PlannerPlanStep,
    StepEvidencePlan,
)

_SESSION_CTX = {
    "session_id": "s1",
    "subject": "Mathematics",
    "track": "core",
    "grade": "JSS1",
    "term": "First Term",
    "week": 1,
    "topic": "Angles",
    "subtopic": "Sum of angles of a triangle",
}
_CURRICULUM_CTX = {
    "subject": "Mathematics",
    "track": "core",
    "grade": "JSS1",
    "term": "First Term",
    "week": 1,
    "topic": "Angles",
    "subtopic": "Sum of angles of a triangle",
    "curriculum_objectives": [
        {"objective_text": "State that the angles of a triangle sum to 180 degrees"},
    ],
    "instructional_materials": ["protractor"],
}


def _request() -> PreparedGenerationInputs:
    session = LessonGenerationSession.model_validate(_SESSION_CTX)
    curriculum = LessonCurriculumContext.model_validate(
        {**_CURRICULUM_CTX, "curriculum_objectives": [], "theme": "Geometry"}
    )
    return PreparedGenerationInputs(
        session=session,
        scope=build_scope_context(session),
        curriculum=curriculum,
        textbook_records=[],
        evidence_selection_strategy="cached",
        grounding_mode="curriculum_only",
    )


def _objective(oid: str) -> LessonPlanObjective:
    return LessonPlanObjective(
        lesson_objective_id=oid,
        objective_text=f"objective {oid}",
        objective_order=1,
        curriculum_objective_id=f"co-{oid}",
        curriculum_objective_text=f"curriculum {oid}",
        kc_type="concept",
        kc_focus=f"focus {oid}",
    )


def test_adapt_whole_plan_prediction_maps_outputs() -> None:
    prediction = SimpleNamespace(
        lesson_plan_objectives=[_objective("o1")],
        resolved_kcs=["kc1"],
        step_evidence_plans=[
            StepEvidencePlan(
                lesson_objective_id="o1",
                selected_record_ids=[COLD_START_RECORD_ID],
                concept_record_ids=[COLD_START_RECORD_ID],
            )
        ],
        core_steps=["core1"],
        global_steps="global_set",
        assessments=["assess1"],
        misconceptions=["m1"],
    )
    artifacts = adapt_whole_plan_prediction(prediction, _request())
    assert isinstance(artifacts, WholeLessonArtifacts)
    assert set(artifacts.step_evidence_plans) == {"o1"}  # list -> dict by lesson_objective_id
    assert len(artifacts.evidence_summaries) == 1
    assert artifacts.kc_plan.misconceptions == ["m1"]
    assert artifacts.kc_plan.theme == "Geometry"
    assert artifacts.kc_plan.instructional_materials == ["protractor"]


def test_cold_start_injects_synthetic_record_for_curriculum_only() -> None:
    inputs = prepare_generation_inputs(
        session_context=_SESSION_CTX,
        curriculum_context=_CURRICULUM_CTX,
        reference_context=[],  # no records
        requested_strategy=None,
        default_strategy="cached",
        grounding_mode="curriculum_only",
    )
    ids = [r.record_id for r in inputs.textbook_records]
    assert ids == [COLD_START_RECORD_ID]
    # content is curriculum-derived
    assert "180" in inputs.textbook_records[0].content


def test_whole_lesson_module_defaults_to_unoptimized() -> None:
    module = WholeLessonGenerationModule()
    assert module.optimized_loaded is False


def test_whole_lesson_module_loads_bundled_gepa_program() -> None:
    baseline = WholeLessonGenerationModule().writer.predict.signature.instructions
    module = WholeLessonGenerationModule(use_optimized=True)
    assert module.optimized_loaded is True
    optimized = module.writer.predict.signature.instructions
    # Loading swaps in the GEPA-optimized (instruction-only) prompt.
    assert optimized != baseline
    assert len(optimized) > len(baseline)


def test_whole_lesson_module_missing_optimized_artifact_raises(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="GEPA-optimized program not found"):
        WholeLessonGenerationModule(
            use_optimized=True,
            optimized_program_path=str(tmp_path / "does_not_exist.json"),
        )


def test_no_records_without_curriculum_only_still_raises() -> None:
    # manual_linkage + no records is a genuine error (the guard stays).
    with pytest.raises(ValueError, match="requires_textbook_records"):
        prepare_generation_inputs(
            session_context=_SESSION_CTX,
            curriculum_context=_CURRICULUM_CTX,
            reference_context=[],
            requested_strategy=None,
            default_strategy="cached",
            grounding_mode="manual_linkage",
        )


class _SequenceResponder:
    """Stand-in generation program that returns a scripted payload per attempt.

    Records the prior_violations fed into each attempt so the refine-loop wiring
    (collect_issues -> prior_violations -> next attempt) can be asserted.
    """

    def __init__(self, payloads: list[WholeLessonArtifacts]) -> None:
        self._payloads = list(payloads)
        self.prior_violations: list[list[str] | None] = []

    def __call__(self, *, request, prior_violations=None, **_) -> WholeLessonArtifacts:
        self.prior_violations.append(prior_violations)
        return self._payloads[len(self.prior_violations) - 1]


def _concept_artifacts(n: int) -> WholeLessonArtifacts:
    """A complete, internally-consistent monolithic draft with n concept objectives.

    Everything but the objective count is clean, so collect_issues() returns exactly
    {too_many_objectives} when n > 4 and nothing when n <= 4 — isolating the cap.
    """
    oids = [f"lop{index:02d}" for index in range(1, n + 1)]
    objectives = [
        LessonPlanObjective(
            lesson_objective_id=oid,
            objective_text=f"Objective {oid}",
            objective_order=index + 1,
            curriculum_objective_id="cur_obj01",
            curriculum_objective_text="curriculum objective",
            kc_type="concept",
            kc_focus=f"distinct focus {oid}",
        )
        for index, oid in enumerate(oids)
    ]
    kcs = [
        CandidateKC.model_validate(
            {
                "kc_id": f"{oid}-kc",
                "kc_type": "concept",
                "objective_text": f"Objective {oid}",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": f"distinct focus {oid}",
                "supporting_record_ids": [COLD_START_RECORD_ID],
                "bloom_level": "understand",
            }
        )
        for oid in oids
    ]
    evidence = {
        oid: StepEvidencePlan.model_validate(
            {
                "lesson_objective_id": oid,
                "selected_record_ids": [COLD_START_RECORD_ID],
                "concept_record_ids": [COLD_START_RECORD_ID],
            }
        )
        for oid in oids
    }
    core_steps = [
        PlannerPlanStep.model_validate(
            {
                "step_id": f"step-{oid}",
                "step_kind": "core",
                "instructional_type": "explain_only",
                "kc_type": "concept",
                "lesson_objective_id": oid,
                "title": f"Teach {oid}",
                "content": f"Explain {oid}.",
                "estimated_minutes": 8,
                "activities": [],
                "blocks": [
                    {
                        "id": f"exp-{oid}",
                        "type": "explanation",
                        "content": f"Explanation for {oid}.",
                    }
                ],
            }
        )
        for oid in oids
    ]
    global_steps = GlobalStepSet.model_validate(
        {
            "intro_step": {
                "step_id": "intro",
                "step_kind": "intro",
                "instructional_type": None,
                "kc_type": None,
                "lesson_objective_id": None,
                "title": "Intro",
                "content": "Warm up.",
                "estimated_minutes": 5,
                "activities": [],
                "blocks": [],
            },
            "evaluation_step": {
                "step_id": "eval",
                "step_kind": "evaluation",
                "instructional_type": "check",
                "kc_type": None,
                "lesson_objective_id": None,
                "title": "Check",
                "content": "Quick check.",
                "estimated_minutes": 5,
                "activities": [],
                "blocks": [
                    {
                        "id": f"ev-{oid}",
                        "type": "practice",
                        "question": f"Question for {oid}.",
                        "answer": f"Answer for {oid}.",
                        "lesson_objective_id": oid,
                    }
                    for oid in oids
                ],
            },
        }
    )
    return WholeLessonArtifacts(
        lesson_plan_objectives=objectives,
        resolved_kcs=kcs,
        step_evidence_plans=evidence,
        core_steps=core_steps,
        global_steps=global_steps,
        assessment_items=[],
        kc_plan=_WholeLessonKCPlan(),
        evidence_summaries=[],
    )


def test_refine_loop_self_corrects_when_too_many_objectives() -> None:
    # First attempt over-decomposes into 5 objectives (would 422 at the safety net);
    # the loop must feed the cap violation back so the second attempt drops to 4.
    inputs = prepare_generation_inputs(
        session_context=_SESSION_CTX,
        curriculum_context=_CURRICULUM_CTX,
        reference_context=[],
        requested_strategy=None,
        default_strategy="cached",
        grounding_mode="curriculum_only",
    )
    runner = _SequenceResponder([_concept_artifacts(5), _concept_artifacts(4)])
    service = LessonGenerationService()

    best_raw, _, residual, attempts = asyncio.run(
        service._refine_attempts(
            inputs=inputs,
            runner=runner,
            stage_name="lesson_plan_no_linkage",
        )
    )
    best_artifacts = cast(WholeLessonArtifacts, best_raw)

    assert attempts == 2
    # First attempt gets no prior violations; the cap is fed into the second.
    assert runner.prior_violations[0] is None
    assert any("too_many_objectives" in v for v in runner.prior_violations[1] or [])
    # The kept (best) plan satisfies the cap, so the safety net no longer fires.
    assert len(best_artifacts.lesson_plan_objectives) == 4
    assert not any("too_many_objectives" in v for v in residual)
    assert residual == []


def test_refine_loop_keeps_best_when_cap_never_satisfied() -> None:
    # If every attempt exceeds the cap (model never complies), the loop is bounded
    # and still returns its best candidate carrying the residual violation, rather
    # than looping forever or raising — the safety net is the final backstop.
    inputs = prepare_generation_inputs(
        session_context=_SESSION_CTX,
        curriculum_context=_CURRICULUM_CTX,
        reference_context=[],
        requested_strategy=None,
        default_strategy="cached",
        grounding_mode="curriculum_only",
    )
    runner = _SequenceResponder([_concept_artifacts(5) for _ in range(5)])
    service = LessonGenerationService()

    best_raw, _, residual, attempts = asyncio.run(
        service._refine_attempts(
            inputs=inputs,
            runner=runner,
            stage_name="lesson_plan_no_linkage",
        )
    )
    best_artifacts = cast(WholeLessonArtifacts, best_raw)

    assert attempts == service.max_refine_attempts
    assert len(best_artifacts.lesson_plan_objectives) == 5
    assert any("too_many_objectives" in v for v in residual)
