"""C1 − C0 per rubric dimension, for one lesson, across generator models.

The study's endpoint is a six-lesson paired test. This is not that: one lesson
gives one pair per dimension, so there is nothing to test and the number stands
or falls on its own. What it is for is comparing two models on the same lesson,
the same conditions and the same rating protocol, where the model is the only
thing that differs — and reporting the judge's own repeat spread beside the
delta, so a reader can see which differences the instrument can resolve.

    uv run python -m experiments.h1_condition_eval.model_contrast t3w02-dspy t3w02-deepseek
"""

from __future__ import annotations

import argparse
import json
import statistics

from experiments.h1_condition_eval.condition_trace.scores import DIMENSIONS, LABELS, load_scores
from experiments.h1_condition_eval.config import RUNS_DIR


def _arm(label: str) -> tuple[str, dict[str, dict[str, float]], dict[str, float]]:
    """Per-condition means over draws, and the judge's own spread between passes."""
    run = json.loads((RUNS_DIR / label / "run.json").read_text())
    scores = load_scores(RUNS_DIR / label)
    if scores is None:
        raise SystemExit(f"{label}: no archived judge passes")
    means = {
        condition: {
            dim: statistics.fmean(
                v[dim] for (les, cond, _), v in scores.by_draw.items() if cond == condition
            )
            for dim in DIMENSIONS
        }
        for condition in ("C0", "C1")
    }
    key = {
        r["candidate_id"]: r
        for r in json.loads((RUNS_DIR / label / "rating" / "_key.json").read_text())
    }
    passes = sorted((RUNS_DIR / label / "rating").glob("judgments_pass_*.json"))
    per_pass = []
    for path in passes:
        rows = json.loads(path.read_text())["judgments"]
        per_pass.append(
            {j["candidate_id"]: {d: float(j[d]["score"]) for d in DIMENSIONS} for j in rows}
        )
    spread = {
        dim: statistics.fmean(
            abs(per_pass[0][c][dim] - per_pass[1][c][dim]) for c in key if len(per_pass) > 1
        )
        if len(per_pass) > 1
        else 0.0
        for dim in DIMENSIONS
    }
    return str(run["arm"].get("model") or "config-default"), means, spread


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labels", nargs="+")
    args = parser.parse_args()

    arms = {label: _arm(label) for label in args.labels}
    width = max(len(LABELS[d]) for d in DIMENSIONS)
    for label, (model, means, spread) in arms.items():
        print(f"\n  {label}  —  {model}")
        print(f"    {'rubric':<{width}} {'C0':>6} {'C1':>6} {'C1−C0':>7} {'judge spread':>13}")
        for dim in DIMENSIONS:
            delta = means["C1"][dim] - means["C0"][dim]
            resolved = "" if abs(delta) > spread[dim] else "  (within it)"
            print(
                f"    {LABELS[dim]:<{width}} {means['C0'][dim]:>6.2f} {means['C1'][dim]:>6.2f} "
                f"{delta:>+7.2f} {spread[dim]:>13.2f}{resolved}"
            )
    if len(arms) > 1:
        first, second = args.labels[0], args.labels[1]
        print(f"\n  Same conditions, same lesson: {second} minus {first}, per condition")
        print(f"    {'rubric':<{width}} {'C0':>7} {'C1':>7}")
        for dim in DIMENSIONS:
            a, b = arms[first][1], arms[second][1]
            print(
                f"    {LABELS[dim]:<{width}} {b['C0'][dim] - a['C0'][dim]:>+7.2f} "
                f"{b['C1'][dim] - a['C1'][dim]:>+7.2f}"
            )
    print("\n  One lesson, three draws, two judge passes. No test is run: n = 1 pair.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
