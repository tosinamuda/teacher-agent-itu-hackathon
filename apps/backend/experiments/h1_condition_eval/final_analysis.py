"""The C1 − C0 result: every rubric dimension, every lesson, both terms.

One place for the endpoint and the three dimensions beside it, because a
conditioning study that reports only its endpoint hides what the treatment cost
elsewhere. The judge's own reason for each cell is carried through rather than
summarised, so a score can be read against what earned it.

    uv run python -m experiments.h1_condition_eval.final_analysis
    uv run python -m experiments.h1_condition_eval.final_analysis full-v3-enriched full-v7-enriched
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.h1_condition_eval.condition_trace.scores import DIMENSIONS, LABELS
from experiments.h1_condition_eval.config import RUNS_DIR

BASE = "full-v3"
FULL = "full-v7"
#: Every candidate is rated twice. The second pass is not a check on the first — it
#: measures the judge's own spread, which on this rubric moved more than half of every
#: arm's scores by about 0.45. A margin under that is not a finding, and the report
#: cannot say so unless both passes are on disk.
PASSES = ("a", "b")


def _out_path(base: str) -> Path:
    """One report per base run, so a second analysis cannot overwrite the first."""
    return RUNS_DIR / ("FINAL-ANALYSIS.md" if base == BASE else f"FINAL-ANALYSIS-{base}.md")


#: Her two terms. The cohort is one teacher across a term boundary, and the one
#: lesson that carries the effect sits on the far side of it.
TERMS = {
    "t2-w09": "Term 2",
    "t3-w02": "Term 3",
    "t3-w04": "Term 3",
    "t3-w05": "Term 3",
    "t3-w06": "Term 3",
    "t3-w09": "Term 3",
}


def _judged(run: str, condition: str) -> tuple[dict, dict, dict]:
    """Every judgment behind each cell, its mean, and every rationale the judge gave.

    The individual scores are kept, not just their mean. A cell is six judgments — three
    generation draws rated twice each — and the spread across those six is the only
    estimate of the pipeline's own variability this study can make from its own data.
    Reporting a difference without it invites reading 0.3 as a result.
    """
    rating = RUNS_DIR / run / "rating"
    key = {r["candidate_id"]: r for r in json.loads((rating / "_key.json").read_text())}
    scores: dict[tuple[str, str], list[float]] = defaultdict(list)
    reasons: dict[tuple[str, str], list[str]] = defaultdict(list)
    for suffix in PASSES:
        for j in json.loads((rating / f"judgments_pass_{suffix}.json").read_text())["judgments"]:
            row = key[j["candidate_id"]]
            if row["condition"] != condition:
                continue
            for dim in DIMENSIONS:
                scores[(row["lesson"], dim)].append(float(j[dim]["score"]))
                if text := str(j[dim].get("rationale") or "").strip():
                    reasons[(row["lesson"], dim)].append(text)
    means = {k: statistics.fmean(v) for k, v in scores.items()}
    return means, reasons, dict(scores)


def _standard_error(values: list[float]) -> float:
    return statistics.stdev(values) / math.sqrt(len(values)) if len(values) > 1 else 0.0


def _difference_error(left: list[float], right: list[float]) -> float:
    """The standard error on C1 − C0, from the spread of the draws behind each."""
    return math.sqrt(_standard_error(left) ** 2 + _standard_error(right) ** 2)


def _mean(cells: dict, dim: str, lessons: list[str]) -> float:
    return statistics.fmean(cells[(lesson, dim)] for lesson in lessons)


def _sign(value: float) -> str:
    return f"{value:+.2f}"


def _topics() -> dict[str, str]:
    """Her own topic and subtopic for each lesson, so a section names the lesson."""
    from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

    cases = json.loads(EVAL_SET_PATH.read_text())["cases"]
    return {c["lesson"]: f"{c['plan']['topic']} — {c['plan']['subtopic']}" for c in cases}


def _rubric_table(rows: list[tuple[str, float, float, float | None]]) -> list[str]:
    """One row per rubric dimension: C0, C1, their difference, and the full plan."""
    out = [
        "| rubric | C0 | C1 | **C1 − C0** | C1 with the full plan |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, a, b, f in rows:
        mark = "**" if label == LABELS["taught_lesson_alignment"] else ""
        full = "—" if f is None else f"{f:.2f}"
        out.append(f"| {mark}{label}{mark} | {a:.2f} | {b:.2f} | **{_sign(b - a)}** | {full} |")
    return out


def _verdict(delta: float, error: float) -> str:
    """Whether a difference survives the spread of the draws it was averaged from.

    Two standard errors, which is the conventional bar and a generous one at six
    judgments per cell. Nothing here is a significance test: n is six lessons and the
    study's own endpoint is a signed-rank over them, not a t-test over draws.
    """
    if error == 0.0:
        return "every draw agreed, so there is no spread to clear"
    if abs(delta) <= 2 * error:
        return f"within twice the spread of its own draws (±{2 * error:.2f}) — not separable"
    return f"clears twice the spread of its own draws (±{2 * error:.2f})"


def report(base: str = BASE, full_run: str = FULL) -> str:
    c0, c0_why, c0_raw = _judged(base, "C0")
    c1, c1_why, c1_raw = _judged(base, "C1")
    full, full_why, _ = _judged(full_run, "C1")
    lessons = sorted({lesson for lesson, _ in c0})
    topics = _topics()

    def pooled(raw: dict, dim: str) -> list[float]:
        return [score for lesson in lessons for score in raw[(lesson, dim)]]

    out = [
        "# C1 − C0, lesson by lesson",
        "",
        f"Generated by `experiments.h1_condition_eval.final_analysis`; do not edit. "
        f"Run `{base}` (C0 and C1) with `{full_run}` beside it. Six lessons, three draws per "
        "cell, two Sonnet 4.6 passes per candidate, so every figure is the mean of six "
        "judgments. Scores are 1–5.",
        "",
        "**C0** receives the objectives alone. **C1** adds her lesson plan's design — step "
        "sequence, activities, the work she set — and never her note. **C1 with the full "
        "plan** is the same condition carrying every field her plan holds, including her "
        "narration and step titles.",
        "",
        "Every difference is reported beside the spread of the draws it was averaged from. "
        "A pack is regenerated three times and each draw judged twice, and those six "
        "judgments disagree; a difference smaller than that disagreement is not a result. "
        "This is a spread, not a significance test — the study's endpoint is a signed-rank "
        "over six lessons, and no arithmetic here changes that n.",
        "",
        "Each lesson's table is followed by the judge's own reason for every cell in it, "
        "deduplicated across the six judgments, C0 first.",
        "",
        "## Across the board — all six lessons pooled",
        "",
    ]
    out += _rubric_table(
        [
            (
                LABELS[dim],
                _mean(c0, dim, lessons),
                _mean(c1, dim, lessons),
                _mean(full, dim, lessons),
            )
            for dim in DIMENSIONS
        ]
    )
    out += ["", "| rubric | C1 − C0 | reading |", "|---|---:|---|"]
    for dim in DIMENSIONS:
        delta = _mean(c1, dim, lessons) - _mean(c0, dim, lessons)
        error = _difference_error(pooled(c0_raw, dim), pooled(c1_raw, dim))
        out.append(f"| {LABELS[dim]} | {_sign(delta)} | {_verdict(delta, error)} |")
    out.append("")

    for lesson in lessons:
        out += [f"## {lesson} — {topics.get(lesson, '')}", "", f"*{TERMS[lesson]}*", ""]
        out += _rubric_table(
            [
                (LABELS[dim], c0[(lesson, dim)], c1[(lesson, dim)], full.get((lesson, dim)))
                for dim in DIMENSIONS
            ]
        )
        out.append("")
        for dim in DIMENSIONS:
            a, b = c0[(lesson, dim)], c1[(lesson, dim)]
            error = _difference_error(c0_raw[(lesson, dim)], c1_raw[(lesson, dim)])
            out += [
                f"### {LABELS[dim]} — C0 {a:.2f}, C1 {b:.2f} ({_sign(b - a)})",
                "",
                f"{_verdict(b - a, error).capitalize()}.",
                "",
            ]
            for label, why in (("C0", c0_why), ("C1", c1_why), ("full plan", full_why)):
                for text in dict.fromkeys(why[(lesson, dim)]):
                    out.append(f"- **{label}** — {text}")
            out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", nargs="?", default=BASE, help="the run holding C0 and C1")
    parser.add_argument(
        "full", nargs="?", default=FULL, help="the run holding C1 under the full plan"
    )
    args = parser.parse_args()
    out = _out_path(args.base)
    out.write_text(report(args.base, args.full), encoding="utf-8")
    print(f"  {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
