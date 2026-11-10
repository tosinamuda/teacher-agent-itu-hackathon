"""What the human scores support beyond the test that reduces them to six differences.

The declared test reduces every score to six lesson means and runs a Wilcoxon on those.
That estimator cannot see the rater variance it is drowning in; it can only be destroyed
by it. The crossed model in :mod:`.mixed_model` fits the scores as they were collected, so
the rater term is estimated rather than averaged over and a condition effect arrives with
an interval instead of a rank. This module reads that fit alongside the things only the
run record can answer: what never arrived, and whether the judge measures the same
property the panel does.

The same run was also scored by an LLM judge, twice, on the same 72 packets. That gives
two things nothing else here can: the judge's own repeat reliability, and whether judge
and human are measuring the same property at all. A judge calibrated against a human
instrument that does not rank inherits its noise, so this has to be answered before any
calibration is attempted.

Run with::

    uv run python -m experiments.human_rating.reanalysis ratings.xlsx
"""

from __future__ import annotations

import statistics as st
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import openpyxl
from scipy import stats

from . import mixed_model
from .results import JUDGE_DIMENSIONS
from .results import judge as _judge

CONDITIONS = ("C0", "C1", "C2", "C3")


def scores(path: Path) -> list[dict[str, Any]]:
    """The H1 scores sheet, as rows."""
    page = openpyxl.load_workbook(path, read_only=True, data_only=True)["H1 scores"]
    rows = list(page.iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    return [dict(zip(head, row, strict=True)) for row in rows[1:] if row[0]]


def missingness(rows: list[dict[str, Any]], expected_criteria: int = 3) -> dict[str, Any]:
    """Whether the scores that never arrived are spread evenly across the conditions."""
    seen: dict[tuple[str, str, int], set[int]] = defaultdict(set)
    condition_of = {}
    for row in rows:
        panel = (row["rater"], row["internal_packet_id"], row["objective_index"])
        seen[panel].add(row["criterion"])
        condition_of[panel] = row["condition"]
    missing: dict[str, int] = defaultdict(int)
    total: dict[str, int] = defaultdict(int)
    for row in rows:
        total[row["condition"]] += 1
    for panel, criteria in seen.items():
        if len(criteria) < expected_criteria:
            missing[condition_of[panel]] += expected_criteria - len(criteria)
    counts = [missing.get(c, 0) for c in CONDITIONS]
    result = {"missing_by_condition": dict(zip(CONDITIONS, counts, strict=True))}
    if sum(counts) and all(total.get(c) for c in CONDITIONS):
        result["chi2_p"] = float(stats.chisquare(counts).pvalue) if sum(counts) > 4 else None
    return result


def judge_repeat(run: str) -> dict[str, Any]:
    """The judge scored the same packs twice; this is how far it moved."""
    _, passes = _judge(run)
    a, b = passes["a"], passes["b"]
    shared = sorted(set(a) & set(b))
    moved, same = [], 0
    for candidate in shared:
        for dimension in JUDGE_DIMENSIONS:
            x, y = a[candidate][dimension]["score"], b[candidate][dimension]["score"]
            moved.append(abs(x - y))
            same += x == y
    return {
        "candidates": len(shared),
        "scores_compared": len(moved),
        "mean_absolute_movement": st.mean(moved),
        "identical": same / len(moved),
    }


def judge_against_human(run: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Do the two instruments rank the same packets the same way?"""
    key, passes = _judge(run)
    human = defaultdict(list)
    for row in rows:
        human[(row["lesson"], row["condition"], row["draw"])].append(row["score"])
    pairs = []
    for candidate, meta in key.items():
        cell = (meta["lesson"], meta["condition"], int(meta["repeat"]))
        if cell not in human:
            continue
        judged = [
            st.mean([passes[p][candidate][d]["score"] for d in JUDGE_DIMENSIONS])
            for p in ("a", "b")
            if candidate in passes[p]
        ]
        if judged:
            pairs.append((st.mean(judged), st.mean(human[cell])))
    if len(pairs) < 3:
        return {"packets": len(pairs)}
    x, y = zip(*pairs, strict=True)
    return {
        "packets": len(pairs),
        "pearson_r": float(stats.pearsonr(x, y)[0]),
        "pearson_p": float(stats.pearsonr(x, y)[1]),
        "spearman_r": float(stats.spearmanr(x, y)[0]),
        "judge_mean": st.mean(x),
        "human_mean": st.mean(y),
    }


def report(path: Path, run: str = "c0c3-prism-objective") -> None:
    rows = scores(path)
    print(f"═══ {len(rows)} human scores from {path.name} ═══\n")

    fit = mixed_model.fit(mixed_model.SECONDARY, mixed_model.scores(path))
    print(f"── where the score actually moves ({fit.optimiser}, llf {fit.log_likelihood:.2f}) ──")
    for name, share in sorted(fit.shares.items(), key=lambda part: -part[1]):
        print(f"   {name:22s} {share:6.1%} of total variance")

    print("\n── condition against C0, with intervals ──")
    for item in fit.contrasts:
        zero = "includes zero" if item.low <= 0 <= item.high else "excludes zero"
        print(
            f"   {item.name:4s} {item.estimate:+7.3f}   "
            f"95% CI [{item.low:+.3f}, {item.high:+.3f}]   p={item.p_value:.3f}   {zero}"
        )

    print("\n── the scores that never arrived ──")
    for name, value in missingness(rows).items():
        print(f"   {name}: {value}")

    print(f"\n── the LLM judge on the same packets ({run}) ──")
    for name, value in judge_repeat(run).items():
        print(f"   {name}: {value if isinstance(value, int) else round(value, 3)}")
    print()
    for name, value in judge_against_human(run, rows).items():
        print(f"   {name}: {value if isinstance(value, int) else round(value, 3)}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    report(Path(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
