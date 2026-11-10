"""Unit tests for the reusable semantic score (no LLM, no DB).

This scorer is the shared target for Refine / GEPA / ReAct-verify / bake-off, so
its invariants must hold deterministically. Inputs use the REAL
SemanticPlanValidator interface (lesson_plan_objectives + resolved_kcs +
step_evidence_by_objective + global_steps + textbook_records + curriculum_context).
"""

from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.semantic_score import (
    score_from_issues,
    score_session_plan,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonCurriculumContext,
    TextbookRecordPayload,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CandidateKC,
    LessonPlanObjective,
    StepEvidencePlan,
)

# Two distinct worked-example records so "reuse despite alternatives" can trigger.
_TEXTBOOK = [
    TextbookRecordPayload(record_id="ch04-b044", record_type="worked_example"),
    TextbookRecordPayload(record_id="ch04-b039", record_type="worked_example"),
]


def _ctx(materials: list[str] | None = None) -> LessonCurriculumContext:
    return LessonCurriculumContext.model_validate(
        {
            "subject": "Mathematics",
            "track": "General",
            "grade": "JSS1",
            "term": "First Term",
            "week": 1,
            "topic": "Fractions",
            "subtopic": "Conversion of fractions to decimals and vice versa",
            "instructional_materials": materials or [],
        }
    )


def _objective(oid: str, focus: str, target: str) -> LessonPlanObjective:
    return LessonPlanObjective.model_validate(
        {
            "lesson_objective_id": oid,
            "objective_text": focus,
            "objective_order": int(oid[-1]) if oid[-1].isdigit() else 1,
            "curriculum_objective_id": "cur-obj01",
            "curriculum_objective_text": "Convert fractions to decimals and vice versa",
            "kc_type": "procedure",
            "kc_focus": focus,
            "source_form": "fraction",
            "target_form": target,
        }
    )


def _kc(oid: str, focus: str, target: str, support: list[str]) -> CandidateKC:
    return CandidateKC.model_validate(
        {
            "kc_id": f"{oid}-kc01",
            "kc_type": "procedure",
            "objective_text": focus,
            "curriculum_objective_id": "cur-obj01",
            "kc_focus": focus,
            "source_form": "fraction",
            "target_form": target,
            "supporting_record_ids": support,
            "bloom_level": "apply",
        }
    )


def _evidence(oid: str, selected: list[str], modeling: list[str]) -> StepEvidencePlan:
    return StepEvidencePlan.model_validate(
        {
            "lesson_objective_id": oid,
            "selected_record_ids": selected,
            "modeling_record_ids": modeling,
        }
    )


def _global_steps(evaluation_text: str, covered_objective_ids: list[str]) -> dict:
    return {
        "evaluation_step": {
            "content": evaluation_text,
            "blocks": [
                {"type": "practice", "lesson_objective_id": oid} for oid in covered_objective_ids
            ],
        }
    }


def _two_distinct_objectives() -> tuple[list, list]:
    objectives = [
        _objective("lop01", "Convert fractions to decimals", "decimal"),
        _objective("lop02", "Convert decimals to fractions", "fraction"),
    ]
    kcs = [
        _kc("lop01", "Convert fractions to decimals", "decimal", ["ch04-b044"]),
        _kc("lop02", "Convert decimals to fractions", "fraction", ["ch04-b039"]),
    ]
    return objectives, kcs


def test_score_from_issues_grades_monotonically() -> None:
    assert score_from_issues([]).score == 1.0
    assert score_from_issues([]).passed is True
    one = score_from_issues(["a"]).score
    two = score_from_issues(["a", "b"]).score
    assert 0.0 <= two < one < 1.0


def test_clean_plan_scores_one_and_passes() -> None:
    objectives, kcs = _two_distinct_objectives()
    result = score_session_plan(
        lesson_plan_objectives=objectives,
        resolved_kcs=kcs,
        step_evidence_by_objective={
            "lop01": _evidence("lop01", ["ch04-b044"], ["ch04-b044"]),
            "lop02": _evidence("lop02", ["ch04-b039"], ["ch04-b039"]),
        },
        global_steps=_global_steps("Solve the exercises below.", ["lop01", "lop02"]),
        textbook_records=_TEXTBOOK,
        curriculum_context=_ctx(),
    )
    assert result.passed is True
    assert result.score == 1.0


def _n_distinct_objectives(n: int) -> tuple[list, list, dict]:
    """n internally-consistent objectives/KCs/evidence (no violations but the count)."""
    record = "ch04-b044"
    objectives, kcs, evidence = [], [], {}
    for index in range(1, n + 1):
        oid = f"lop0{index}"
        focus = f"distinct focus number {index}"
        target = f"target{index}"
        objectives.append(_objective(oid, focus, target))
        kcs.append(_kc(oid, focus, target, [record]))
        evidence[oid] = _evidence(oid, [record], [])
    return objectives, kcs, evidence


def test_more_than_four_objectives_is_flagged_for_refine() -> None:
    # The monolithic no-linkage drafter can over-decompose into >4 objectives. The
    # cap must surface as a (non-raising) semantic violation so the refine loop feeds
    # it back and self-corrects, instead of the request hard-failing with a 422.
    objectives, kcs, evidence = _n_distinct_objectives(5)
    result = score_session_plan(
        lesson_plan_objectives=objectives,
        resolved_kcs=kcs,
        step_evidence_by_objective=evidence,
        global_steps=_global_steps(
            "Solve the exercises below.", [o.lesson_objective_id for o in objectives]
        ),
        textbook_records=_TEXTBOOK,
        curriculum_context=_ctx(),
    )
    assert result.passed is False
    assert any("too_many_objectives" in v for v in result.violations)


def test_exactly_four_objectives_is_not_flagged_for_count() -> None:
    objectives, kcs, evidence = _n_distinct_objectives(4)
    result = score_session_plan(
        lesson_plan_objectives=objectives,
        resolved_kcs=kcs,
        step_evidence_by_objective=evidence,
        global_steps=_global_steps(
            "Solve the exercises below.", [o.lesson_objective_id for o in objectives]
        ),
        textbook_records=_TEXTBOOK,
        curriculum_context=_ctx(),
    )
    assert result.passed is True
    assert not any("too_many_objectives" in v for v in result.violations)


def test_objective_kc_count_mismatch_does_not_crash_and_is_flagged() -> None:
    # The monolithic no-linkage model can emit more resolved_kcs than lesson
    # objectives. The non-raising scorer must report the mismatch (so refine can
    # feed it back) rather than crash on a strict positional zip.
    objectives, kcs = _two_distinct_objectives()
    kcs = [*kcs, _kc("lop03", "Extra unmatched KC", "decimal", ["ch04-b044"])]
    result = score_session_plan(
        lesson_plan_objectives=objectives,  # 2 objectives
        resolved_kcs=kcs,  # 3 resolved KCs
        step_evidence_by_objective={
            "lop01": _evidence("lop01", ["ch04-b044"], ["ch04-b044"]),
            "lop02": _evidence("lop02", ["ch04-b039"], ["ch04-b039"]),
        },
        global_steps=_global_steps("Solve the exercises below.", ["lop01", "lop02"]),
        textbook_records=_TEXTBOOK,
        curriculum_context=_ctx(),
    )
    assert result.passed is False
    assert any("objective_kc_count_mismatch" in v for v in result.violations)


def test_reused_modeling_record_is_flagged() -> None:
    # Both objectives point modeling at ch04-b039, but each KC also supports an
    # alternative worked example -> reuse-despite-alternatives must fire.
    objectives = [
        _objective("lop01", "Convert fractions to decimals", "decimal"),
        _objective("lop02", "Convert decimals to fractions", "fraction"),
    ]
    kcs = [
        _kc("lop01", "Convert fractions to decimals", "decimal", ["ch04-b039", "ch04-b044"]),
        _kc("lop02", "Convert decimals to fractions", "fraction", ["ch04-b039", "ch04-b044"]),
    ]
    result = score_session_plan(
        lesson_plan_objectives=objectives,
        resolved_kcs=kcs,
        step_evidence_by_objective={
            "lop01": _evidence("lop01", ["ch04-b039"], ["ch04-b039"]),
            "lop02": _evidence("lop02", ["ch04-b039"], ["ch04-b039"]),
        },
        global_steps=_global_steps("Solve the exercises below.", ["lop01", "lop02"]),
        textbook_records=_TEXTBOOK,
        curriculum_context=_ctx(),
    )
    assert result.passed is False
    assert any("reused_modeling_record" in v for v in result.violations)


def test_ungrounded_evaluation_term_is_flagged() -> None:
    objectives, kcs = _two_distinct_objectives()
    result = score_session_plan(
        lesson_plan_objectives=objectives,
        resolved_kcs=kcs,
        step_evidence_by_objective={
            "lop01": _evidence("lop01", ["ch04-b044"], ["ch04-b044"]),
            "lop02": _evidence("lop02", ["ch04-b039"], ["ch04-b039"]),
        },
        global_steps=_global_steps("Hand out the worksheet and answer key.", ["lop01", "lop02"]),
        textbook_records=_TEXTBOOK,
        curriculum_context=_ctx(),
    )
    assert result.passed is False
    assert any("worksheet" in v for v in result.violations)


def test_allowed_material_is_not_flagged_for_that_term() -> None:
    objectives, kcs = _two_distinct_objectives()
    result = score_session_plan(
        lesson_plan_objectives=objectives,
        resolved_kcs=kcs,
        step_evidence_by_objective={
            "lop01": _evidence("lop01", ["ch04-b044"], ["ch04-b044"]),
            "lop02": _evidence("lop02", ["ch04-b039"], ["ch04-b039"]),
        },
        global_steps=_global_steps("Hand out the worksheet.", ["lop01", "lop02"]),
        textbook_records=_TEXTBOOK,
        curriculum_context=_ctx(materials=["worksheet"]),
    )
    assert not any("worksheet" in v for v in result.violations)
