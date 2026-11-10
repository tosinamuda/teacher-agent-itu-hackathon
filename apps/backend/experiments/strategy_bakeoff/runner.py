"""Bake-off runner: execute strategy cells over the frozen eval set and report.

Implements the measurement protocol from the lesson-plan strategy experiment pre-registration
(not in this repository):

  * loads the frozen eval_set.json (stratified subtopics → LessonPeriod ids);
  * builds the SAME generation payloads production uses
    (build_session_context → SessionContextPayloadBuilder);
  * runs each strategy cell k times per subtopic with the DSPy cache OFF (so
    repeats reflect real stochastic variance, not cached identical draws);
  * scores every result by the deterministic OPT/HELD-OUT split (the LLM-judge
    primary outcome is added in a later step);
  * captures cost (attempts, llm_calls, latency) and writes report.json +
    report.md.

This RUNS the LLM. Keep `--limit 1` for the first smoke pass. Use a cheap model
during iteration via `DSPY_MODEL` (e.g. a small OpenRouter model), then switch to
the production model for the measured runs.

Usage:
    cd apps/backend
    # smoke: one subtopic per stratum, both architectures x cot, baseline
    uv run python -m experiments.strategy_bakeoff.runner --limit 1 --k 1 \
      --backends staged,monolithic --reasoning cot --strategies baseline
    # architecture x reasoning grid, baseline + best_of_3, k=3
    uv run python -m experiments.strategy_bakeoff.runner --k 3 \
      --backends staged,monolithic --reasoning predict,cot,rlm \
      --strategies baseline,best_of_3
"""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev

import dspy

import app.db.metadata  # noqa: F401  (register ORM models for standalone use)
from app.db.session import AsyncSessionLocal
from app.domains.artefacts.types.lesson_plan.application.service import (
    SessionContextPayloadBuilder,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import (
    build_session_context,
)
from app.infra.dspy_lm import active_model_name

from .backends import build_scored_service
from .generation import ScoredLessonGenerationService
from .judge import H1_CRITERIA, JudgeScore, LessonPlanJudge
from .strategies import StrategyResult, run_baseline, run_best_of_n, run_refine

EVAL_SET_PATH = Path(__file__).resolve().parent / "eval_set.json"
DEFAULT_OUTPUT_ROOT = Path(__file__).resolve().parents[2] / ".diagnostics" / "strategy-bakeoff"


def _configure_lm(*, cache: bool) -> str:
    """Configure DSPy LM + cache. Returns the model id used."""
    import os

    model = os.getenv("DSPY_MODEL") or active_model_name()
    if getattr(dspy.settings, "lm", None) is None:
        dspy.configure(lm=dspy.LM(model=model))
    # Cache OFF during measurement so k repeats are genuinely independent draws.
    dspy.configure_cache(enable_disk_cache=cache, enable_memory_cache=cache)
    return model


def _load_eval_set(limit: int | None) -> list[dict]:
    data = json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))
    rows: list[dict] = []
    for stratum, members in data["selected"].items():
        for row in members:
            rows.append({**row, "stratum": stratum})
    rows.sort(key=lambda r: (r["stratum"], r["subtopic_id"]))
    if limit is not None:
        # Take up to `limit` from EACH stratum so smoke runs stay representative.
        capped: list[dict] = []
        seen: dict[str, int] = {}
        for row in rows:
            count = seen.get(row["stratum"], 0)
            if count < limit:
                capped.append(row)
                seen[row["stratum"]] = count + 1
        return capped
    return rows


async def _payloads_for(period_id: str) -> tuple | None:
    async with AsyncSessionLocal() as db:
        session_context = await build_session_context(db, period_id)
        if session_context is None:
            return None
        built = SessionContextPayloadBuilder().build(session_context)
    return (built.session_scope, built.curriculum_scope, built.reference_context)


async def _run_strategy(
    *,
    name: str,
    service: ScoredLessonGenerationService,
    payloads: tuple,
) -> StrategyResult:
    if name == "baseline":
        return await run_baseline(service=service, payloads=payloads)
    if name.startswith("best_of_"):
        n = int(name.rsplit("_", 1)[1])
        return await run_best_of_n(service=service, payloads=payloads, n=n)
    if name == "refine" or name.startswith("refine_"):
        n = int(name.rsplit("_", 1)[1]) if "_" in name else 3
        return await run_refine(service=service, payloads=payloads, n=n)
    raise ValueError(f"unknown strategy: {name}")


def _judge_aggregate(judge_scores: list[JudgeScore]) -> dict:
    """Primary-outcome block: per-criterion + overall rubric, mean ± stdev over k.

    Only judge results that scored every criterion (`ok`) feed the means; errored
    judgements (no plan, or a judge LM failure) are counted separately so a cell
    cannot look good merely because the judge failed to score it.
    """
    ok = [j for j in judge_scores if j.ok]
    overalls = [j.overall for j in ok if j.overall is not None]
    per_criterion: dict[str, dict] = {}
    for cid, _ in H1_CRITERIA:
        values = [j.scores[cid] for j in ok if cid in j.scores]
        per_criterion[cid] = {
            "mean": round(mean(values), 3) if values else None,
            "stdev": round(pstdev(values), 3) if len(values) > 1 else 0.0,
        }
    return {
        "judge_repeats_ok": len(ok),
        "judge_errors": sum(1 for j in judge_scores if j.error is not None),
        "mean_overall": round(mean(overalls), 3) if overalls else None,
        "stdev_overall": round(pstdev(overalls), 3) if len(overalls) > 1 else 0.0,
        "per_criterion": per_criterion,
    }


def _aggregate(results: list[StrategyResult], judge_scores: list[JudgeScore]) -> dict:
    """Aggregate k repeats of one (strategy, subtopic) cell."""
    opt_pass = [1.0 if r.opt_passed else 0.0 for r in results]
    held_pass = [1.0 if r.held_out_passed else 0.0 for r in results]
    full_pass = [1.0 if r.fully_passed else 0.0 for r in results]
    rewards = [r.opt_reward for r in results]
    latencies = [r.total_latency_ms for r in results]
    llm_calls = [r.total_llm_calls for r in results if r.total_llm_calls is not None]
    return {
        "repeats": len(results),
        # Primary outcome (pre-registration §4a/§6): the blind LLM-judge rubric.
        "judge": _judge_aggregate(judge_scores),
        # Secondary outcome + diagnostics: deterministic OPT/HELD-OUT split.
        "opt_pass_rate": round(mean(opt_pass), 3) if opt_pass else 0.0,
        "held_out_pass_rate": round(mean(held_pass), 3) if held_pass else 0.0,
        "full_pass_rate": round(mean(full_pass), 3) if full_pass else 0.0,
        "mean_opt_reward": round(mean(rewards), 3) if rewards else 0.0,
        "stdev_opt_reward": round(pstdev(rewards), 3) if len(rewards) > 1 else 0.0,
        "mean_latency_ms": round(mean(latencies), 1) if latencies else 0.0,
        "mean_llm_calls": round(mean(llm_calls), 1) if llm_calls else None,
        "violation_codes": sorted(
            {v.split(":", 1)[0].strip() for r in results for v in r.violations}
        ),
    }


def _judge_overall_cell(agg: dict) -> str:
    """Render `mean ±stdev` for the primary judge outcome, or `-` if unscored."""
    judge = agg.get("judge") or {}
    mean_overall = judge.get("mean_overall")
    if mean_overall is None:
        return "-"
    return f"{mean_overall} ±{judge.get('stdev_overall', 0.0)}"


def _render_markdown(report: dict) -> str:
    lines = [
        "# Strategy Bake-off Report",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Model: `{report['model']}`",
        f"- Judge model: `{report.get('judge_model', '-')}`",
        f"- Cache: `{'on' if report['cache'] else 'off'}`",
        f"- k (repeats): `{report['k']}`",
        f"- Backends: `{', '.join(report.get('backends', []))}`",
        f"- Reasoning: `{', '.join(report.get('reasoning', []))}`",
        f"- Strategies: `{', '.join(report['strategies'])}`",
        "",
        "Primary outcome = blind LLM-judge rubric (overall 1-5). Secondary = "
        "deterministic HELD-OUT pass-rate. Architecture = backend (staged=multi-"
        "signature, monolithic=single-signature).",
        "",
        "| Backend | Reasoning | Strategy | Stratum | Subtopic | judge overall | "
        "HELD-OUT pass | OPT pass | Full pass | mean reward | mean ms | mean calls "
        "| violation codes |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for cell in report["cells"]:
        agg = cell["aggregate"]
        lines.append(
            f"| {cell.get('backend', '-')} | {cell.get('reasoning', '-')} "
            f"| {cell['strategy']} | {cell['stratum']} "
            f"| {cell['subtopic_id'].replace('jss1-math-', '')} | {_judge_overall_cell(agg)} "
            f"| {agg.get('held_out_pass_rate', '-')} | {agg.get('opt_pass_rate', '-')} "
            f"| {agg.get('full_pass_rate', '-')} | {agg.get('mean_opt_reward', '-')} "
            f"| {agg.get('mean_latency_ms', '-')} | {agg.get('mean_llm_calls', '-')} "
            f"| {', '.join(agg.get('violation_codes', [])) or '-'} |"
        )
    if report.get("skipped_cells"):
        lines.append("")
        lines.append("Skipped (backend, reasoning) cells:")
        for skip in report["skipped_cells"]:
            lines.append(f"- `{skip['backend']}/{skip['reasoning']}`: {skip['reason']}")
    return "\n".join(lines) + "\n"


def _build_services(
    backends: list[str], reasonings: list[str]
) -> tuple[dict[tuple[str, str], ScoredLessonGenerationService], list[dict]]:
    """Build one scored service per (backend, reasoning) cell; skip unsupported."""
    services: dict[tuple[str, str], ScoredLessonGenerationService] = {}
    skipped: list[dict] = []
    for backend in backends:
        for reasoning in reasonings:
            try:
                services[(backend, reasoning)] = build_scored_service(backend, reasoning=reasoning)
            except (NotImplementedError, ValueError) as exc:
                # e.g. staged+rlm / staged+react are out of scope; record, don't crash.
                skipped.append({"backend": backend, "reasoning": reasoning, "reason": str(exc)})
                print(f"skip cell backend={backend} reasoning={reasoning}: {exc}")
    return services, skipped


def _write_report(
    output_dir: Path, report_meta: dict, cells: list[dict], *, complete: bool
) -> dict:
    """Write report.json + report.md from the cells gathered so far (idempotent)."""
    report = {**report_meta, "complete": complete, "cells": cells}
    (output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output_dir / "report.md").write_text(_render_markdown(report), encoding="utf-8")
    return report


async def main_async(args: argparse.Namespace) -> int:
    model = _configure_lm(cache=args.cache)
    eval_rows = _load_eval_set(args.limit)
    backends = [b.strip() for b in args.backends.split(",") if b.strip()]
    reasonings = [r.strip() for r in args.reasoning.split(",") if r.strip()]
    strategies = [s.strip() for s in args.strategies.split(",") if s.strip()]
    # PRIMARY outcome: an independent, blind LLM-judge (pre-reg §4a). Constructed
    # once; uses JUDGE_DSPY_MODEL if set so it can differ from the generation LM.
    judge = LessonPlanJudge()
    services, skipped_cells = _build_services(backends, reasonings)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_dir = (Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_ROOT) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    report_meta = {
        "generated_at": timestamp,
        "model": model,
        "judge_model": judge.model,
        "cache": args.cache,
        "k": args.k,
        "backends": backends,
        "reasoning": reasonings,
        "strategies": strategies,
        "skipped_cells": skipped_cells,
        "eval_rows": len(eval_rows),
    }

    # Prefetch ALL payloads up front so the long LLM loop never touches the DB.
    # (The DB connection dropping mid-loop — e.g. a container restart — would
    # otherwise crash the whole grid; payloads are static, so fetch once.)
    payloads_by_period: dict[str, tuple | None] = {}
    for row in eval_rows:
        period_id = row["lesson_period_id"]
        if period_id not in payloads_by_period:
            payloads_by_period[period_id] = await _payloads_for(period_id)

    cells: list[dict] = []
    for row in eval_rows:
        payloads = payloads_by_period[row["lesson_period_id"]]
        for (backend, reasoning), service in services.items():
            for strategy in strategies:
                results: list[StrategyResult] = []
                judge_scores: list[JudgeScore] = []
                if payloads is not None:
                    for _ in range(max(1, args.k)):
                        result = await _run_strategy(
                            name=strategy, service=service, payloads=payloads
                        )
                        results.append(result)
                        # Judge the chosen plan (fail-open: None plan -> JudgeScore error).
                        judge_scores.append(judge.score(result.session_plan))
                cell = {
                    "backend": backend,
                    "reasoning": reasoning,
                    "stratum": row["stratum"],
                    "subtopic_id": row["subtopic_id"],
                    "lesson_period_id": row["lesson_period_id"],
                    "strategy": strategy,
                    "payload_missing": payloads is None,
                    "aggregate": _aggregate(results, judge_scores) if results else {"repeats": 0},
                    "runs": [
                        {
                            "opt_reward": r.opt_reward,
                            "attempts": r.attempts,
                            "opt_passed": r.opt_passed,
                            "held_out_passed": r.held_out_passed,
                            "fully_passed": r.fully_passed,
                            "violations": r.violations,
                            "total_latency_ms": r.total_latency_ms,
                            "total_llm_calls": r.total_llm_calls,
                            "error": r.error,
                            "judge_overall": j.overall,
                            "judge_scores": j.scores,
                            "judge_error": j.error,
                        }
                        for r, j in zip(results, judge_scores, strict=True)
                    ],
                }
                cells.append(cell)
                agg = cell["aggregate"]
                judge_overall = (agg.get("judge") or {}).get("mean_overall", "-")
                print(
                    f"[{row['stratum']}] {row['subtopic_id'][:40]:40} "
                    f"{backend}/{reasoning}/{strategy:10} "
                    f"judge={judge_overall} held_out={agg.get('held_out_pass_rate', '-')} "
                    f"reward={agg.get('mean_opt_reward', '-')}"
                )
                # Write the report after EVERY cell so a long grid is crash-safe
                # and inspectable mid-run (not all-or-nothing at the end).
                _write_report(output_dir, report_meta, cells, complete=False)

    _write_report(output_dir, report_meta, cells, complete=True)
    print(f"\nWrote {output_dir}/report.md")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, default=1, help="Repeats per (strategy, subtopic).")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max subtopics per stratum (smoke runs). Omit for the full eval set.",
    )
    parser.add_argument(
        "--strategies",
        default="baseline",
        help="Comma-separated self-correction cells, e.g. baseline,best_of_3.",
    )
    parser.add_argument(
        "--backends",
        default="staged",
        help="Comma-separated architectures: staged,monolithic.",
    )
    parser.add_argument(
        "--reasoning",
        default="cot",
        help="Comma-separated reasoning modules: predict,cot,rlm (rlm: monolithic only).",
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Enable DSPy cache (OFF by default for honest variance).",
    )
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
