"""The lesson-context alignment contrast, under every resampling unit the design allows.

The pooled model averages three criteria, one of which sits near ceiling for every
condition, and the dilution hides the criterion with headroom. Read on lesson-context
alignment alone — the criterion literally named "Reflects the teacher-planned mathematics
lesson" — the C3-C0 contrast separates. That is a different quantity from the pooled one,
not a correction of it, and both are reported here so neither can be mistaken for the
other.

Three resampling units, because the choice is the whole argument. Resampling *packets*
within condition ignores that three packets share a lesson. Resampling *lessons*, carrying
every condition's packets together, keeps a lesson's C0 and C3 in or out as a pair. The
paired form is narrower, not wider: pairing removes between-lesson variance from the
contrast, which is the point of having generated all four conditions from every lesson.

None of these model the raters. Raters are crossed and balanced, so their main effect
cancels from a contrast, but a rater-by-condition interaction would not — the intervals
describe packet and lesson sampling only, and say so.

Run with::

    uv run python -m experiments.human_rating.alignment_contrast "<delivered folder>"
"""

from __future__ import annotations

import random
import statistics as st
import sys
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .absolute_quality import CONDITIONS, ratings

LESSON_CONTEXT = 2
REPLICATES = 20_000
SEED = 20260909


def packet_means(rows: list[dict[str, Any]], criterion: int) -> dict[tuple[str, str, str], float]:
    """One mean per generated pack: the unit a condition actually produced."""
    packs: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for row in rows:
        if row["criterion"] == criterion:
            packs[(row["lesson"], row["condition"], row["packet"])].append(row["score"])
    return {key: st.mean(scores) for key, scores in packs.items()}


def _by_condition(means: dict[tuple[str, str, str], float]) -> dict[str, list[float]]:
    out: dict[str, list[float]] = defaultdict(list)
    for (_, condition, _), value in means.items():
        out[condition].append(value)
    return out


def _by_lesson(means: dict[tuple[str, str, str], float]) -> dict[str, dict[str, list[float]]]:
    out: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for (lesson, condition, _), value in means.items():
        out[lesson][condition].append(value)
    return out


def _percentile(values: list[float]) -> tuple[float, float]:
    values = sorted(values)
    return values[int(0.025 * len(values))], values[int(0.975 * len(values))]


def _resample(draw: Callable[[], dict[str, list[float]]], condition: str) -> tuple[float, float]:
    rng = random.Random(SEED)
    reps = []
    for _ in range(REPLICATES):
        groups = draw(rng)
        reps.append(st.mean(groups[condition]) - st.mean(groups["C0"]))
    return _percentile(reps)


def by_packet(means: dict, condition: str) -> tuple[float, float]:
    """Packets resampled within condition. Ignores that packets share a lesson."""
    groups = _by_condition(means)

    def draw(rng: random.Random) -> dict[str, list[float]]:
        return {c: [rng.choice(groups[c]) for _ in groups[c]] for c in groups}

    return _resample(draw, condition)


def by_lesson(means: dict, condition: str) -> tuple[float, float]:
    """Lessons resampled whole, so a lesson's conditions travel together."""
    per = _by_lesson(means)
    lessons = sorted(per)

    def draw(rng: random.Random) -> dict[str, list[float]]:
        groups: dict[str, list[float]] = defaultdict(list)
        for lesson in (rng.choice(lessons) for _ in lessons):
            for condition_, values in per[lesson].items():
                groups[condition_].extend(values)
        return groups

    return _resample(draw, condition)


def paired_differences(means: dict, condition: str) -> list[float]:
    """One difference per lesson — the estimator the pre-registration reduces to."""
    per = _by_lesson(means)
    return [
        st.mean(per[lesson][condition]) - st.mean(per[lesson]["C0"])
        for lesson in sorted(per)
        if per[lesson][condition] and per[lesson]["C0"]
    ]


def report(folder: Path, criterion: int = LESSON_CONTEXT) -> None:
    rows = ratings(folder)
    means = packet_means(rows, criterion)
    groups = _by_condition(means)
    print(f"═══ criterion {criterion} — {len(means)} packets, {len(rows)} ratings ═══\n")
    print(
        f"  {'contrast':12s} {'estimate':>9s}  {'packets':>18s}  "
        f"{'lessons paired':>18s}  lessons +ve"
    )
    for condition in CONDITIONS[1:]:
        effect = st.mean(groups[condition]) - st.mean(groups["C0"])
        pk = by_packet(means, condition)
        ls = by_lesson(means, condition)
        diffs = paired_differences(means, condition)
        positive = sum(1 for d in diffs if d > 0)
        print(
            f"  {condition} vs C0     {effect:+9.3f}  [{pk[0]:+.3f}, {pk[1]:+.3f}]  "
            f"[{ls[0]:+.3f}, {ls[1]:+.3f}]  {positive}/{len(diffs)}"
        )
    print("\n  per-lesson differences:")
    for condition in CONDITIONS[1:]:
        diffs = paired_differences(means, condition)
        print(f"    {condition} - C0  {[round(d, 3) for d in diffs]}")
    print(
        "\n  Intervals are percentile bootstrap, "
        f"{REPLICATES:,} replicates, seed {SEED}. They describe packet and lesson\n"
        "  sampling. Raters are crossed and balanced and are not modelled here."
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    report(Path(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
