"""No-LLM tests for the bake-off LLM-judge plumbing.

The judge's LLM call is not exercised here (that needs a model); these tests
cover the deterministic parts: rubric mirror, clamping, overall aggregation,
blind reference/plan views, and the empty-plan path.
"""

from __future__ import annotations

from experiments.strategy_bakeoff.check_split import split_violations
from experiments.strategy_bakeoff.judge import (
    H1_CRITERIA,
    JudgeScore,
    _clamp,
    _plan_view,
    _reference_sheet,
)
from experiments.strategy_bakeoff.runner import _aggregate, _judge_aggregate
from experiments.strategy_bakeoff.strategies import StrategyResult


def _result(violations: list[str]) -> StrategyResult:
    split = split_violations(violations)
    return StrategyResult(
        strategy="baseline",
        session_plan={"ok": True},
        violations=violations,
        split=split,
        opt_reward=1.0 if not split.opt else 0.5,
        attempts=1,
        total_llm_calls=5,
        total_latency_ms=100.0,
    )


def test_rubric_mirrors_four_h1_criteria() -> None:
    ids = {cid for cid, _ in H1_CRITERIA}
    assert ids == {
        "objective_coverage",
        "scope_compliance",
        "textbook_factual_fidelity",
        "pedagogical_appropriateness",
    }


def test_clamp_bounds_and_coerces() -> None:
    assert _clamp(0) == 1
    assert _clamp(6) == 5
    assert _clamp(3) == 3
    assert _clamp("4") == 4
    assert _clamp("nonsense") == 1
    assert _clamp(None) == 1


def test_judge_score_overall_and_ok() -> None:
    full = JudgeScore(
        scores={
            "objective_coverage": 4,
            "scope_compliance": 5,
            "textbook_factual_fidelity": 3,
            "pedagogical_appropriateness": 4,
        }
    )
    assert full.ok is True
    assert full.overall == 4.0

    partial = JudgeScore(scores={"objective_coverage": 4})
    assert partial.ok is False  # not all criteria present

    errored = JudgeScore(error="boom")
    assert errored.ok is False
    assert errored.overall is None


def test_reference_sheet_is_blind_to_strategy_and_steps() -> None:
    plan = {
        "subject": "Mathematics",
        "subtopic": "Fractions",
        "curriculum_objectives": ["Convert fractions to decimals"],
        "instructional_materials": ["number cards"],
        "steps": [{"secret": "should not be in reference sheet"}],
        "strategy": "best_of_3",  # provenance must never reach the judge
    }
    ref = _reference_sheet(plan)
    assert ref["subtopic"] == "Fractions"
    assert "steps" not in ref
    assert "strategy" not in ref


def test_plan_view_excludes_provenance() -> None:
    plan = {
        "lesson_plan_objectives": [{"objective_text": "x"}],
        "steps": [{"a": 1}],
        "assessments": {"q": 1},
        "strategy": "baseline",
        "run_metadata": {"model": "x"},
    }
    view = _plan_view(plan)
    assert set(view.keys()) == {"lesson_plan_objectives", "steps", "assessments"}
    assert "strategy" not in view
    assert "run_metadata" not in view


def test_judge_aggregate_means_exclude_errored() -> None:
    scores = [
        JudgeScore(scores={cid: 4 for cid, _ in H1_CRITERIA}),
        JudgeScore(scores={cid: 2 for cid, _ in H1_CRITERIA}),
        JudgeScore(error="no_session_plan"),  # excluded from means, counted as error
    ]
    agg = _judge_aggregate(scores)
    assert agg["judge_repeats_ok"] == 2
    assert agg["judge_errors"] == 1
    assert agg["mean_overall"] == 3.0
    assert agg["stdev_overall"] > 0
    assert agg["per_criterion"]["objective_coverage"]["mean"] == 3.0


def test_judge_aggregate_all_errored_yields_none_overall() -> None:
    agg = _judge_aggregate([JudgeScore(error="boom"), JudgeScore(error="no_session_plan")])
    assert agg["judge_repeats_ok"] == 0
    assert agg["judge_errors"] == 2
    assert agg["mean_overall"] is None
    assert agg["per_criterion"]["scope_compliance"]["mean"] is None


def test_aggregate_embeds_primary_judge_block() -> None:
    results = [_result([]), _result(["reused_modeling_record: x"])]
    scores = [
        JudgeScore(scores={cid: 5 for cid, _ in H1_CRITERIA}),
        JudgeScore(error="boom"),
    ]
    agg = _aggregate(results, scores)
    assert agg["repeats"] == 2
    assert agg["judge"]["judge_repeats_ok"] == 1
    assert agg["judge"]["mean_overall"] == 5.0
    # Deterministic secondary outcome still present alongside the primary block.
    assert "held_out_pass_rate" in agg
    assert agg["opt_pass_rate"] == 0.5  # one clean, one with an OPT violation
