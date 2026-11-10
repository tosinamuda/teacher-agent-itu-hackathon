"""Part 1 results on the measurement itself: the rating instrument's reliability, whether the
packs were suitable to rate, and how the model judge agrees with the panel."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from statistics import mean, stdev
from typing import Any

import krippendorff
import numpy as np

from .exact import icc_one_way, signed_rank
from .part1 import (
    FAMILY,
    JUDGE,
    PAIRS,
    QUALITY,
    RAW,
    favourable,
    share,
)
from .record import Printed, Result
from .sources import Row, Sources


def results(sources: Sources) -> list[Result]:
    ratings = [r for r in sources.sheet(RAW) if r["response_status"] == "answered"]
    pairs = [p for p in sources.sheet(PAIRS) if p["Answers"] == 2]
    return [
        *_instrument(sources, ratings, pairs),
        *_suitability(sources, ratings),
        *_judge(sources),
    ]


def _row(**fields: Any) -> Result:
    return Result(part="Part 1", **fields)


def _instrument(sources: Sources, ratings: list[Row], pairs: list[Row]) -> list[Result]:
    scores = [int(r["score"]) for r in ratings]
    a = np.array([p["Score A"] for p in pairs], float)
    b = np.array([p["Score B"] for p in pairs], float)
    chance = float(sum(np.mean(a == k) * np.mean(b == k) for k in range(1, 6)))
    observed = float(np.mean(a == b))
    grid = _by_rater(pairs)
    per_criterion = {
        crit: krippendorff.alpha(reliability_data=grid[:, cols], level_of_measurement="ordinal")
        for crit, cols in _columns_by(pairs, "Criterion").items()
    }
    common = {
        "question": "Rating instrument",
        "location": sources.where("sec:the-human-instrument"),
    }
    cells = {"unit": "doubly rated cell (n = 600)", "computed_from": PAIRS, **common}
    return [
        _row(
            id="P1-I1",
            quantity="Share of the 1,212 scores at 5",
            estimate=Printed("61.2%", mean(s == 5 for s in scores)),
            also=(("at 4–5", Printed("90.8%", mean(s >= 4 for s in scores))),),
            unit="rating",
            computed_from=RAW,
            **common,
        ),
        _row(
            id="P1-I2",
            quantity="Mean score",
            estimate=Printed("4.507", mean(scores)),
            also=(("SD", Printed("0.697", stdev(scores))),),
            unit="rating",
            computed_from=RAW,
            **common,
        ),
        _row(
            id="P1-I3",
            quantity="Exact agreement",
            estimate=Printed("46.0%", observed),
            also=(("expected by chance", Printed("45.5%", chance)),),
            test="chance from each rater slot's marginal distribution",
            **cells,
        ),
        _row(
            id="P1-I4",
            quantity="Cohen's kappa",
            estimate=Printed("+0.009", (observed - chance) / (1 - chance)),
            test="Cohen's kappa, unweighted",
            **cells,
        ),
        _row(
            id="P1-I5",
            quantity="Intraclass correlation",
            estimate=Printed("+0.016", icc_one_way([list(x) for x in zip(a, b, strict=True)])),
            test="ICC(1), one-way random effects",
            **cells,
        ),
        _row(
            id="P1-I6",
            quantity="Krippendorff's alpha",
            estimate=Printed(
                "-0.003", krippendorff.alpha(reliability_data=grid, level_of_measurement="ordinal")
            ),
            test="Krippendorff's alpha, ordinal metric",
            note="per criterion "
            + ", ".join(f"{k} {v:+.3f}" for k, v in sorted(per_criterion.items())),
            **cells,
        ),
    ]


def _by_rater(pairs: list[Row]) -> np.ndarray:
    raters = sorted({p["Rater A"] for p in pairs} | {p["Rater B"] for p in pairs})
    grid = np.full((len(raters), len(pairs)), np.nan)
    for column, pair in enumerate(pairs):
        grid[raters.index(pair["Rater A"]), column] = pair["Score A"]
        grid[raters.index(pair["Rater B"]), column] = pair["Score B"]
    return grid


def _columns_by(pairs: list[Row], key: str) -> dict[str, list[int]]:
    columns: dict[str, list[int]] = defaultdict(list)
    for index, pair in enumerate(pairs):
        columns[pair[key]].append(index)
    return columns


def _suitability(sources: Sources, ratings: list[Row]) -> list[Result]:
    count, rated = favourable(ratings, QUALITY, ("C3",))
    c3 = [
        int(r["score"]) for r in ratings if r["criterion_id"] == QUALITY and r["condition"] == "C3"
    ]
    common = {"question": "Suitability check", "location": sources.where("sec:rq1-suitability")}
    return [
        _row(
            id="P1-S1",
            quantity="C3 instructional-quality ratings at 4–5",
            estimate=Printed("95/101", share(count, rated)),
            also=(
                ("share", Printed("94.1%", count / rated)),
                ("at 1–2", Printed("0", sum(s <= 2 for s in c3))),
                ("raw mean", Printed("4.61", mean(c3))),
            ),
            unit="rating",
            computed_from=RAW,
            **common,
        ),
    ]


def _judge(sources: Sources) -> list[Result]:
    judge = sources.sheet(JUDGE)
    by_lesson: dict[tuple[str, str], list[int]] = defaultdict(list)
    for r in judge:
        if r["dimension"] == "taught_lesson_alignment":
            by_lesson[(r["lesson"], r["condition"])].append(int(r["score"]))
    lessons = sorted({lesson for lesson, _ in by_lesson})
    means = {key: Fraction(sum(v), len(v)) for key, v in by_lesson.items()}
    family = [
        sum((means[(lesson, c)] for c in FAMILY), Fraction(0)) / 3 - means[(lesson, "C0")]
        for lesson in lessons
    ]
    c3 = [means[(lesson, "C3")] - means[(lesson, "C0")] for lesson in lessons]
    passes: dict[tuple[str, str], dict[str, int]] = defaultdict(dict)
    for r in judge:
        passes[(r["candidate_id"], r["dimension"])][r["pass"]] = int(r["score"])
    paired = [v for v in passes.values() if {"a", "b"} <= v.keys()]
    common = {
        "question": "Model judge (supplementary)",
        "location": sources.where("sec:the-llm-judge"),
        "computed_from": JUDGE,
    }
    lesson_test = {
        "sidedness": "two-sided",
        "test": "exact Wilcoxon signed-rank",
        "unit": "lesson (n = 6)",
    }
    return [
        _row(
            id="P1-J1",
            quantity="Family − C0, judge's lesson alignment",
            estimate=Printed("+0.750", float(mean(family))),
            p=Printed(".031", 2 * signed_rank(family)[0]),
            **lesson_test,
            **common,
        ),
        _row(
            id="P1-J2",
            quantity="C3 − C0, judge's lesson alignment",
            estimate=Printed("+0.750", float(mean(c3))),
            p=Printed(".063", 2 * signed_rank(c3)[0]),
            **lesson_test,
            **common,
        ),
        _row(
            id="P1-J3",
            quantity="Judge scores identical across the two passes",
            estimate=Printed("92.4%", mean(v["a"] == v["b"] for v in paired)),
            also=(
                (
                    "mean absolute movement",
                    Printed("0.076", mean(abs(v["a"] - v["b"]) for v in paired)),
                ),
            ),
            unit=f"paired score (n = {len(paired)})",
            **common,
        ),
    ]
