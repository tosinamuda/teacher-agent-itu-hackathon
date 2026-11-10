"""Write the input/output trace for every lesson and condition.

Two documents, from the same assembler:

    # one PDF per lesson × condition, with the layer analysis (default run: clean-six)
    uv run python -m experiments.h1_condition_eval.condition_trace

    # one PDF per lesson: C0 input → output, C1 input → output, then the rubric
    uv run python -m experiments.h1_condition_eval.condition_trace --per-lesson --run diag-v3
"""

from __future__ import annotations

import argparse
from pathlib import Path

from app.shared.session_plan_view import SessionPlanView

from .assemble import build, load_outputs, load_plans
from .lesson_report import lesson_html, scoreboard_html
from .render import condition_html, to_pdf
from .scores import load_scores
from .summary import summary_html

HERE = Path(__file__).resolve().parent.parent
RUNS = HERE / "runs"
DEFAULT_OUT = HERE / "input-output"


def _title(plan: SessionPlanView) -> str:
    return f"{plan.topic or ''} — {plan.subtopic or ''}".strip(" —")


def _last_repeat(run: Path) -> int:
    import json

    return max(int(c.get("repeat", 1)) for c in json.loads(run.read_text())["cases"])


def per_condition(args: argparse.Namespace) -> int:
    plans = load_plans()
    outputs = load_outputs(args.run, repeat=args.repeat or 1)
    wanted = args.lesson or sorted(plans)
    everything = []
    for lesson in wanted:
        for item in build(lesson, plans[lesson], outputs):
            path = args.out / f"{lesson}-{item.condition}.pdf"
            to_pdf(condition_html(item, _title(plans[lesson])), path)
            print(f"  {path.relative_to(HERE)}")
            everything.append(item)
    analysis = args.out / "LAYER-ANALYSIS.pdf"
    to_pdf(summary_html(everything, len(wanted)), analysis)
    print(f"  {analysis.relative_to(HERE)}")
    return 0


def per_lesson(args: argparse.Namespace) -> int:
    plans = load_plans()
    repeat = args.repeat or _last_repeat(args.run)
    outputs = load_outputs(args.run, repeat=repeat)
    scores = load_scores(args.run.parent)
    conditions = tuple(args.conditions.split(",")) if args.conditions else ("C0", "C1")
    out = args.out / args.run.parent.name
    for lesson in args.lesson or sorted(plans):
        traces = build(lesson, plans[lesson], outputs)
        path = out / f"{lesson}.pdf"
        to_pdf(
            lesson_html(
                lesson,
                _title(plans[lesson]),
                traces,
                scores,
                repeat=repeat,
                conditions=conditions,
                plan=plans[lesson],
            ),
            path,
        )
        print(f"  {path.relative_to(HERE)}")
    if scores:
        path = out / "SUMMARY.pdf"
        to_pdf(scoreboard_html(sorted(plans), plans, scores, conditions), path)
        print(f"  {path.relative_to(HERE)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=RUNS / "clean-six" / "run.json")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--lesson", action="append", help="restrict to these lessons")
    parser.add_argument(
        "--repeat", type=int, help="which draw to show; per-lesson defaults to the last"
    )
    parser.add_argument(
        "--per-lesson", action="store_true", help="one document per lesson with scores"
    )
    parser.add_argument("--conditions", help="comma-separated, in ladder order, e.g. C0,C1,C2,C3")
    args = parser.parse_args()
    if args.run.is_dir():
        args.run = args.run / "run.json"
    return per_lesson(args) if args.per_lesson else per_condition(args)


if __name__ == "__main__":
    raise SystemExit(main())
