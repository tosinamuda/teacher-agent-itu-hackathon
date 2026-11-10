"""GEPA prompt-optimisation of the winning generation cell (pre-registration §8).

GEPA reflectively rewrites a predictor's instructions to improve a reward. We
optimise the monolithic single-call signature (`DraftWholeLessonPlanSignature`) —
the clean, single-prompt arm — against the OPT-set deterministic reward, then
report optimised-vs-baseline on a DISJOINT test split + the blind judge (the
primary outcome GEPA never trains on).

Integrity (pre-reg §4b, §8):
  * GEPA's reward is the OPT-set checks ONLY (`opt_reward`); HELD-OUT checks and
    the rubric judge are never shown to the optimiser, so improvement on them is
    genuine generalisation.
  * train/test are disjoint subtopics drawn from S1/S2 (S3 too few), split
    deterministically and recorded before optimisation.

Usage:
    cd apps/backend
    uv run python -m experiments.strategy_bakeoff.optimize --reasoning cot --auto light
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

import dspy

import app.db.metadata  # noqa: F401  (register ORM models for standalone use)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.assembly import (
    SessionPlanAssembler,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.semantic_validation import (  # noqa: E501
    SemanticPlanValidator,
)

from .backends import build_scored_service
from .check_split import opt_reward, split_violations
from .judge import LessonPlanJudge
from .monolithic_signature import DraftWholeLessonPlanSignature, adapt_prediction
from .reasoning import build_reasoning_module
from .runner import EVAL_SET_PATH, _configure_lm, _payloads_for

DEFAULT_OUTPUT_ROOT = Path(__file__).resolve().parents[2] / ".diagnostics" / "strategy-bakeoff-gepa"
_LOGGER = logging.getLogger(__name__)
_VALIDATOR = SemanticPlanValidator(logger=_LOGGER)
_ASSEMBLER = SessionPlanAssembler()


def _signature_inputs(request) -> dict:
    """The DraftWholeLessonPlanSignature input fields for one prepared request."""
    return {
        "scope_context": request.scope_payload(),
        "curriculum_context": request.curriculum_payload(),
        "curriculum_objectives": request.curriculum_objective_payloads(),
        "textbook_records": request.textbook_record_payloads(),
        "prior_violations": [],
    }


def _score_prediction(pred: dspy.Prediction, request) -> tuple[float, list[str]]:
    """Adapt a signature prediction and score it on the OPT-set checks.

    Returns (opt_reward, opt_violations). Any structural failure -> reward 0.0.
    """
    artifacts = adapt_prediction(pred, request)
    normalized_draft = _ASSEMBLER.normalize_draft(artifacts=artifacts, inputs=request)
    violations = _VALIDATOR.collect_issues(
        lesson_plan_objectives=artifacts.lesson_plan_objectives,
        resolved_kcs=artifacts.resolved_kcs,
        step_evidence_by_objective=artifacts.step_evidence_plans,
        global_steps=normalized_draft.global_steps,
        textbook_records=request.textbook_records,
        curriculum_context=request.curriculum,
    )
    return opt_reward(violations), split_violations(violations).opt


def _gepa_metric(gold, pred, trace=None, pred_name=None, pred_trace=None):
    """Reflective GEPA metric: OPT reward + textual feedback from the violations."""
    try:
        reward, opt_violations = _score_prediction(pred, gold.request)
    except Exception as exc:  # noqa: BLE001 - a crashed draft scores 0 with feedback
        return dspy.Prediction(
            score=0.0,
            feedback=(
                "The generated plan failed structural validation with an error: "
                f"{type(exc).__name__}: {exc}. Produce schema-valid, internally "
                "consistent objects (KCs, evidence plans, steps)."
            ),
        )
    if reward >= 1.0:
        feedback = "All structural (OPT) checks passed. Keep the plan consistent."
    else:
        feedback = "Fix these structural problems in the next attempt: " + "; ".join(opt_violations)
    return dspy.Prediction(score=reward, feedback=feedback)


async def _build_examples(rows: list[dict]) -> list[dspy.Example]:
    """Build dspy.Examples (signature inputs + request for scoring) for subtopics."""
    service = build_scored_service("monolithic", reasoning="cot")
    examples: list[dspy.Example] = []
    for row in rows:
        payloads = await _payloads_for(row["lesson_period_id"])
        if payloads is None:
            continue
        session_scope, curriculum_scope, reference_context = payloads
        request = service._prepare_inputs(
            session_context=session_scope,
            curriculum_context=curriculum_scope,
            reference_context=reference_context,
            requested_strategy=None,
        )
        example = dspy.Example(
            **_signature_inputs(request),
            request=request,
            subtopic_id=row["subtopic_id"],
        ).with_inputs(
            "scope_context",
            "curriculum_context",
            "curriculum_objectives",
            "textbook_records",
            "prior_violations",
        )
        examples.append(example)
    return examples


def _train_test_split(eval_set: dict) -> tuple[list[dict], list[dict]]:
    """Deterministic disjoint split from S1/S2 only (pre-reg §5). S3 excluded."""
    s1 = list(eval_set["selected"].get("S1_grounded", []))
    s2 = list(eval_set["selected"].get("S2_partial", []))
    # Train: first 2 of each stratum; test: the remainder. Deterministic (no RNG).
    train = s1[:2] + s2[:2]
    test = s1[2:] + s2[2:]
    return train, test


def _evaluate(student: dspy.Module, examples: list[dspy.Example], judge: LessonPlanJudge) -> dict:
    """Run a student over examples; report OPT reward + blind judge (primary)."""
    rewards: list[float] = []
    judge_overalls: list[float] = []
    errors = 0
    for example in examples:
        try:
            pred = student(**example.inputs())
            reward, _ = _score_prediction(pred, example.request)
            rewards.append(reward)
            artifacts = adapt_prediction(pred, example.request)
            draft = _ASSEMBLER.normalize_draft(artifacts=artifacts, inputs=example.request)
            content = _ASSEMBLER.build_content(
                session=example.request.session,
                inputs=example.request,
                artifacts=artifacts,
                draft=draft,
            )
            session_plan = _ASSEMBLER.assemble(
                session=example.request.session, session_plan_content=content
            )
            score = judge.score(session_plan)
            if score.overall is not None:
                judge_overalls.append(score.overall)
        except Exception:  # noqa: BLE001 - a failed plan counts as reward 0 / no judge
            errors += 1
            rewards.append(0.0)
    return {
        "n": len(examples),
        "errors": errors,
        "mean_opt_reward": round(mean(rewards), 3) if rewards else 0.0,
        "mean_judge_overall": round(mean(judge_overalls), 3) if judge_overalls else None,
        "judge_scored": len(judge_overalls),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reasoning", default="cot", choices=["predict", "cot"])
    parser.add_argument("--auto", default="light", choices=["light", "medium", "heavy"])
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    model = _configure_lm(cache=False)
    reflection_model = os.getenv("GEPA_REFLECTION_MODEL") or model
    eval_set = json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))
    train_rows, test_rows = _train_test_split(eval_set)

    train = asyncio.run(_build_examples(train_rows))
    test = asyncio.run(_build_examples(test_rows))
    judge = LessonPlanJudge()
    student = build_reasoning_module(DraftWholeLessonPlanSignature, reasoning=args.reasoning)

    before = _evaluate(student, test, judge)

    gepa = dspy.GEPA(
        metric=_gepa_metric,
        auto=args.auto,
        reflection_lm=dspy.LM(model=reflection_model),
        track_stats=True,
    )
    optimized = gepa.compile(student, trainset=train, valset=train)

    after = _evaluate(optimized, test, judge)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_dir = (Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_ROOT) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_at": timestamp,
        "model": model,
        "reflection_model": reflection_model,
        "reasoning": args.reasoning,
        "auto": args.auto,
        "judge_model": judge.model,
        "train_subtopics": [r["subtopic_id"] for r in train_rows],
        "test_subtopics": [r["subtopic_id"] for r in test_rows],
        "before": before,
        "after": after,
    }
    (output_dir / "gepa_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    try:
        optimized.save(str(output_dir / "optimized_program.json"))
    except Exception as exc:  # noqa: BLE001 - saving is best-effort
        print(f"(could not save optimized program: {exc})")
    print(
        f"GEPA {args.reasoning} auto={args.auto}: "
        f"OPT reward {before['mean_opt_reward']} -> {after['mean_opt_reward']}, "
        f"judge {before['mean_judge_overall']} -> {after['mean_judge_overall']} "
        f"(test n={after['n']}). Wrote {output_dir}/gepa_report.json"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
