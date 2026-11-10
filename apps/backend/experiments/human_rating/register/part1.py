"""Part 1 results for RQ1: teacher alignment, the favourable shares, the criterion means and the
rungs. The instrument, suitability and the model judge are in ``instrument``."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from statistics import mean
from typing import Any

from scipy import stats

from .exact import cluster_sign_flip, icc_one_way, signed_rank
from .record import Printed, Result
from .sources import Row, Sources

LCA = "lesson_context_alignment"
QUALITY = "instructional_quality"
CURRICULUM = "curriculum_objective_alignment"
CONDITIONS = ("C0", "C1", "C2", "C3")
FAMILY = ("C1", "C2", "C3")
RAW = "10_P1_Raw"
PAIRS = "20_P1_Pairs"
GENERATION = "18_Generation_Raw"
JUDGE = "17_Judge_Raw"


def results(sources: Sources) -> list[Result]:
    ratings = [r for r in sources.sheet(RAW) if r["response_status"] == "answered"]
    return [
        *_alignment(sources, ratings),
        *_shares(sources, ratings),
        *_criterion_means(sources, ratings),
        *_rungs(sources, ratings),
    ]


def _row(**fields: Any) -> Result:
    return Result(part="Part 1", **fields)


def share(count: int, total: int) -> str:
    return f"{count}/{total}"


def favourable(ratings: list[Row], criterion: str, conditions: tuple[str, ...]) -> tuple[int, int]:
    chosen = [r for r in ratings if r["criterion_id"] == criterion and r["condition"] in conditions]
    return sum(int(r["score"]) >= 4 for r in chosen), len(chosen)


def objective_scores(ratings: list[Row]) -> tuple[dict[tuple[str, str], Fraction], dict[str, str]]:
    """Objective-by-condition lesson-context means: raters averaged within a draw, then draws."""
    cells: dict[tuple[str, str], dict[int, list[Fraction]]] = defaultdict(lambda: defaultdict(list))
    lesson_of: dict[str, str] = {}
    for r in ratings:
        if r["criterion_id"] == LCA:
            cells[(r["objective_id"], r["condition"])][r["draw"]].append(Fraction(int(r["score"])))
            lesson_of[r["objective_id"]] = r["lesson_id"]
    scores = {
        key: sum((sum(v, Fraction(0)) / len(v) for v in draws.values()), Fraction(0)) / len(draws)
        for key, draws in cells.items()
    }
    return scores, lesson_of


CONTRASTS = {
    "H1a": ("C1 − C0", ("C1",)),
    "H1b": ("plan-driven family (C1–C3) − C0", FAMILY),
    "H1c": ("C3 − C0", ("C3",)),
}
#: effect, objective-level p, cluster p, within-lesson ICC, t interval, and the objectives moved.
PRINTED = {
    "H1a": ("+0.098", ".2520", ".2188", "+.067", ("-0.13", "+0.33"), ("8", "9")),
    "H1b": ("+0.239", ".0350", ".0625", "-.162", ("+0.00", "+0.48"), None),
    "H1c": ("+0.333", ".0136", ".0313", "-.400", ("+0.07", "+0.60"), ("11", None)),
}


def contrast(
    scores: dict[tuple[str, str], Fraction], objective: str, arms: tuple[str, ...]
) -> Fraction:
    return (
        sum((scores[(objective, c)] for c in arms), Fraction(0)) / len(arms)
        - scores[(objective, "C0")]
    )


def _alignment(sources: Sources, ratings: list[Row]) -> list[Result]:
    scores, lesson_of = objective_scores(ratings)
    objectives = sorted(lesson_of)
    where = sources.where("sec:rq2-alignment", "tab:human-contrasts")
    means = [float(mean(scores[(o, c)] for o in objectives)) for c in CONDITIONS]
    rows = [
        _row(
            id="P1-A0",
            question="RQ1",
            quantity="Objective-level lesson-context mean, C0",
            estimate=Printed("4.245", means[0]),
            also=tuple(
                (c, Printed(t, m))
                for c, t, m in zip(FAMILY, ("4.343", "4.529", "4.578"), means[1:], strict=True)
            ),
            unit=f"objective (n = {len(objectives)})",
            location=where,
            computed_from=RAW,
        ),
    ]
    for name, (label, arms) in CONTRASTS.items():
        diffs = [contrast(scores, o, arms) for o in objectives]
        rows += _contrast(name, label, diffs, [lesson_of[o] for o in objectives], where)
    return rows


def _contrast(
    name: str, label: str, diffs: list[Fraction], lessons: list[str], where: str
) -> list[Result]:
    effect, p_obj, p_cluster, icc, (low, high), moved = PRINTED[name]
    p, n = signed_rank(diffs)
    by_lesson: dict[str, list[Fraction]] = defaultdict(list)
    for lesson, difference in zip(lessons, diffs, strict=True):
        by_lesson[lesson].append(difference)
    floats = [float(d) for d in diffs]
    low_t, high_t = stats.t.interval(
        0.95, len(floats) - 1, loc=mean(floats), scale=stats.sem(floats)
    )
    up, down = sum(d > 0 for d in diffs), sum(d < 0 for d in diffs)
    counts: tuple[tuple[str, Printed], ...] = ()
    if moved:
        counts = (("objectives up", Printed(moved[0], str(up))),) + (
            (("down", Printed(moved[1], str(down))),) if moved[1] else ()
        )
    common = {"question": f"RQ1, {name}", "location": where, "computed_from": RAW}
    estimate = Printed(effect, float(mean(diffs)))
    return [
        _row(
            id=f"P1-{name}",
            quantity=f"{label}, lesson-context alignment",
            estimate=estimate,
            p=Printed(p_obj, p),
            sidedness="one-sided",
            test="exact Wilcoxon signed-rank; zeros dropped, midranks, exact ties",
            unit=f"objective (n = {n} non-zero of {len(diffs)})",
            also=counts,
            note=f"two-sided {2 * p:.4f}",
            **common,
        ),
        _row(
            id=f"P1-{name}-cluster",
            quantity=f"{label}, lesson-cluster check",
            estimate=estimate,
            p=Printed(p_cluster, cluster_sign_flip(by_lesson)),
            sidedness="one-sided",
            test="sign-flip of every objective of a lesson together, 64 assignments",
            unit="lesson (n = 6)",
            **common,
        ),
        _row(
            id=f"P1-{name}-icc",
            quantity=f"{label}, within-lesson ICC of the differences",
            estimate=Printed(icc, icc_one_way([[float(x) for x in v] for v in by_lesson.values()])),
            test="ICC(1)",
            unit="objective within lesson",
            **common,
        ),
        _row(
            id=f"P1-{name}-t",
            quantity=f"{label}, 95% interval",
            estimate=estimate,
            interval=(Printed(low, low_t), Printed(high, high_t)),
            test="Student's t on the objective differences",
            unit=f"objective (n = {len(diffs)})",
            **common,
        ),
    ]


SHARES = {"C0": "81/100", "C1": "85/101", "C2": "94/102", "C3": "94/102"}


def _shares(sources: Sources, ratings: list[Row]) -> list[Result]:
    rows = []
    for condition, printed in SHARES.items():
        count, total = favourable(ratings, LCA, (condition,))
        rows.append(
            _row(
                id=f"P1-F-{condition}",
                question="RQ1, descriptive",
                quantity=f"{condition} lesson-context ratings at 4–5",
                estimate=Printed(printed, share(count, total)),
                unit="rating",
                computed_from=RAW,
                location=sources.where("sec:rq2-alignment", "tab:favourable-shares"),
            )
        )
    return rows


CRITERION_MEANS = {
    CURRICULUM: ("0.119", ("4.475", "4.495", "4.594", "4.574")),
    LCA: ("0.318", ("4.260", "4.337", "4.529", "4.578")),
    QUALITY: ("0.104", ("4.510", "4.584", "4.535", "4.614")),
    "all three pooled": ("0.174", ("4.415", "4.472", "4.553", "4.589")),
}


def _criterion_means(sources: Sources, ratings: list[Row]) -> list[Result]:
    where = sources.where("sec:rq2-alignment", "tab:criteria-means")
    rows = []
    for criterion, (spread, printed) in CRITERION_MEANS.items():
        chosen = [
            r for r in ratings if criterion.startswith("all") or r["criterion_id"] == criterion
        ]
        means = [mean(int(r["score"]) for r in chosen if r["condition"] == c) for c in CONDITIONS]
        rows.append(
            _row(
                id=f"P1-M-{criterion.split()[0]}",
                question="RQ1, every criterion",
                quantity=f"Range of condition means, {criterion}",
                estimate=Printed(spread, max(means) - min(means)),
                also=tuple(
                    (c, Printed(t, m)) for c, t, m in zip(CONDITIONS, printed, means, strict=True)
                ),
                unit="rating",
                location=where,
                computed_from=RAW,
            )
        )
    return rows


def _rungs(sources: Sources, ratings: list[Row]) -> list[Result]:
    scores, lesson_of = objective_scores(ratings)
    objectives = sorted(lesson_of)
    common = {
        "question": "Rung increments",
        "location": sources.where("sec:what-the-component-rungs-did-and-d"),
    }
    rows = [
        _row(
            id=f"P1-R{index}",
            quantity=f"{upper} − {lower}, objective level",
            estimate=Printed(
                printed, float(mean(scores[(o, upper)] - scores[(o, lower)] for o in objectives))
            ),
            test="none; not tested separately",
            unit="objective",
            computed_from=RAW,
            **common,
        )
        for index, (printed, upper, lower) in enumerate(
            (("+0.098", "C1", "C0"), ("+0.186", "C2", "C1"), ("+0.049", "C3", "C2")), start=1
        )
    ]
    generation = sources.sheet(GENERATION)
    references = {
        c: sum(g["blocks_with_source_refs"] for g in generation if g["condition"] == c)
        for c in ("C2", "C3")
    }
    c3 = [g for g in generation if g["condition"] == "C3"]
    rows += [
        _row(
            id="P1-R4",
            quantity="Blocks carrying an explicit source reference, C2",
            estimate=Printed("168", str(references["C2"])),
            also=(("C3", Printed("157", str(references["C3"]))),),
            unit="block",
            computed_from=GENERATION,
            **common,
        ),
        _row(
            id="P1-R5",
            quantity="C3 packs on which validation closed",
            estimate=Printed("6", str(sum(bool(g["passed"]) for g in c3))),
            unit=f"pack (of {len(c3)})",
            computed_from=GENERATION,
            **common,
        ),
    ]
    return rows
