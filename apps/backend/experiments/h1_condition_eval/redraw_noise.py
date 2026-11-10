"""What the same inputs score when the same arm draws them again.

Every difference this study reports is a difference between cells, and a cell is three
generation draws rated twice. `final_analysis` quotes the spread *within* a cell as the
error on a difference. That understates it: two runs of the same arm over the same
inputs also disagree, and nothing in a single run can see that.

Two runs of the same arm, where only some lessons' inputs changed, can. The lessons
whose inputs did NOT change are re-draws of identical material, so whatever their cells
move is noise — floor, not finding. The lessons whose inputs DID change are read against
that floor.

    uv run python -m experiments.h1_condition_eval.redraw_noise \\
        c0c3-deepseek-native c0c3-prism-objective --changed t3-w05

A difference smaller than the floor is not a small effect. It is nothing, measured
badly.
"""

from __future__ import annotations

import argparse
import statistics

from experiments.h1_condition_eval.condition_trace.scores import DIMENSIONS, LABELS
from experiments.h1_condition_eval.final_analysis import _judged, _sign

CONDITIONS = ("C0", "C1", "C2", "C3")
ENDPOINT = "taught_lesson_alignment"


def _cells(run: str) -> dict[str, dict]:
    return {condition: _judged(run, condition)[0] for condition in CONDITIONS}


def _lessons(means: dict[str, dict]) -> list[str]:
    return sorted({lesson for lesson, _ in means["C0"]})


def _movement(before: dict, after: dict, lessons: list[str], dim: str) -> list[float]:
    """Every cell's change between the two runs, one number per lesson-condition."""
    return [
        after[condition][(lesson, dim)] - before[condition][(lesson, dim)]
        for lesson in lessons
        for condition in CONDITIONS
    ]


def _floor(moves: list[float]) -> tuple[float, float]:
    """The typical and worst movement on inputs that did not change."""
    return statistics.fmean(abs(m) for m in moves), max(abs(m) for m in moves)


def _endpoint_table(before: dict, after: dict, lessons: list[str], changed: set[str]) -> list[str]:
    out = [
        "| lesson | C1−C0 before | C1−C0 after | change | input |",
        "|---|---:|---:|---:|---|",
    ]
    for lesson in lessons:
        was = before["C1"][(lesson, ENDPOINT)] - before["C0"][(lesson, ENDPOINT)]
        now = after["C1"][(lesson, ENDPOINT)] - after["C0"][(lesson, ENDPOINT)]
        mark = "**edited**" if lesson in changed else "identical"
        out.append(f"| {lesson} | {_sign(was)} | {_sign(now)} | {_sign(now - was)} | {mark} |")
    return out


def _per_dimension(before: dict, after: dict, held: list[str]) -> list[str]:
    """The floor per rubric, since a ceilinged dimension cannot move and will look quiet."""
    out = ["| rubric | mean \\|move\\| | worst | cells that moved |", "|---|---:|---:|---:|"]
    for dim in DIMENSIONS:
        moves = _movement(before, after, held, dim)
        moved = sum(1 for m in moves if m != 0)
        mean, worst = _floor(moves)
        out.append(f"| {LABELS[dim]} | {mean:.3f} | {worst:.2f} | {moved}/{len(moves)} |")
    return out


def report(before_label: str, after_label: str, changed: set[str]) -> str:
    before, after = _cells(before_label), _cells(after_label)
    lessons = _lessons(before)
    held = [lesson for lesson in lessons if lesson not in changed]
    if not held:
        raise SystemExit("every lesson changed, so there is nothing to measure the noise on")

    moves = _movement(before, after, held, ENDPOINT)
    mean, worst = _floor(moves)
    deltas = [
        (after["C1"][(x, ENDPOINT)] - after["C0"][(x, ENDPOINT)])
        - (before["C1"][(x, ENDPOINT)] - before["C0"][(x, ENDPOINT)])
        for x in held
    ]
    pair_worst = max(abs(d) for d in deltas)

    out = [
        f"# Re-draw noise — `{before_label}` against `{after_label}`",
        "",
        f"Same arm, same judge. Inputs changed on: {', '.join(sorted(changed)) or 'nothing'}. "
        f"The other {len(held)} lessons re-drew identical material.",
        "",
        "## The floor, from the lessons whose inputs did not change",
        "",
        *_per_dimension(before, after, held),
        "",
        f"On the endpoint ({LABELS[ENDPOINT]}) a cell moved **{mean:.2f} on average, "
        f"{worst:.2f} at worst** across {len(moves)} unchanged cells, and the C1−C0 *pair* "
        f"moved up to **{pair_worst:.2f}**.",
        "",
        "The pair figure is the one that matters: it is the same quantity the study's "
        "endpoint is a signed-rank over. Any per-lesson C1−C0 smaller than it was never "
        "distinguishable from a re-draw.",
        "",
        "## The endpoint, lesson by lesson",
        "",
        *_endpoint_table(before, after, lessons, changed),
    ]
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument(
        "--changed",
        nargs="*",
        default=(),
        help="lessons whose inputs differ between the runs; the rest are the noise sample",
    )
    args = parser.parse_args()
    print(report(args.before, args.after, set(args.changed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
