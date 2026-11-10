"""Appendix D results: the omnibus, the other procedures for H1c, pack length, and generation
variability. The crossed mixed models are in ``models`` and the checks on the comparative
judgements in ``judgements``."""

from __future__ import annotations

import json
from collections import defaultdict
from fractions import Fraction
from statistics import mean
from typing import Any

from scipy import stats

from . import judgements, models
from .exact import signed_rank, signed_rank_two_sided
from .part1 import CONTRASTS, LCA, PRINTED, contrast, objective_scores
from .record import Printed, Result
from .sources import Row, Sources

CONDITIONS = ("C0", "C1", "C2", "C3")
RAW = "10_P1_Raw"
DECODED = "26_P2_Decoded"


def results(sources: Sources) -> list[Result]:
    ratings = [r for r in sources.sheet(RAW) if r["response_status"] == "answered"]
    return [
        *_omnibus(sources, ratings),
        *_confirmatory_family(sources, ratings),
        *models.results(sources),
        *_procedures(sources, ratings),
        *_length(sources, ratings),
        *_replicates(sources),
        *judgements.results(sources),
    ]


def _row(**fields: Any) -> Result:
    return Result(part="Appendix D", **fields)


def _omnibus(sources: Sources, ratings: list[Row]) -> list[Result]:
    lessons = sorted({r["lesson_id"] for r in ratings})
    means = {
        (lesson, condition): Fraction(sum(scores), len(scores))
        for lesson in lessons
        for condition in CONDITIONS
        if (
            scores := [
                int(r["score"])
                for r in ratings
                if r["lesson_id"] == lesson and r["condition"] == condition
            ]
        )
    }
    friedman = stats.friedmanchisquare(
        *[[float(means[(lesson, c)]) for lesson in lessons] for c in CONDITIONS]
    )
    raw = [
        signed_rank_two_sided([means[(lesson, b)] - means[(lesson, a)] for lesson in lessons])
        for a, b in zip(CONDITIONS, CONDITIONS[1:], strict=False)
    ]
    holm = _holm(raw)
    common = {
        "question": "Omnibus and corrected family",
        "location": sources.where("app:omnibus"),
        "computed_from": RAW,
        "unit": "lesson (n = 6), secondary pooled measure",
    }
    return [
        _row(
            id="D-O1",
            quantity="Friedman chi-square across the four conditions",
            estimate=Printed("3.000", friedman.statistic),
            p=Printed(".392", friedman.pvalue),
            sidedness="omnibus",
            test="Friedman test",
            also=(("Kendall's W", Printed("0.167", friedman.statistic / (len(lessons) * 3))),),
            **common,
        ),
        _row(
            id="D-O2",
            quantity="Holm-adjusted p, three adjacent contrasts (largest raw p shown)",
            estimate=Printed("1.000", min(holm)),
            test="exact Wilcoxon signed-rank, Holm step-down",
            note="every adjusted p is " + ", ".join(f"{p:.3f}" for p in holm),
            **common,
        ),
        _row(
            id="D-O3",
            quantity="C3 − C0, pooled lesson-level mean difference",
            estimate=Printed(
                "+0.145",
                float(mean(means[(lesson, "C3")] - means[(lesson, "C0")] for lesson in lessons)),
            ),
            **common,
        ),
    ]


#: Holm-adjusted one-sided p for H1a, H1b and H1c, as Appendix D prints them.
CONFIRMATORY_HOLM = {"H1a": ".2520", "H1b": ".0700", "H1c": ".0408"}


def _confirmatory_family(sources: Sources, ratings: list[Row]) -> list[Result]:
    """Holm's correction across H1a–H1c on the primary endpoint, at the objective level."""
    scores, lesson_of = objective_scores(ratings)
    objectives = sorted(lesson_of)
    raw = [
        signed_rank([contrast(scores, o, arms) for o in objectives])[0]
        for _label, arms in CONTRASTS.values()
    ]
    unadjusted = dict(zip(CONTRASTS, raw, strict=True))
    adjusted = dict(zip(CONTRASTS, _holm(raw), strict=True))
    return [
        _row(
            id=f"D-O4-{name}",
            question="Omnibus and corrected family",
            quantity=f"{name}: {label}, one-sided p before and after Holm across H1a–H1c",
            estimate=Printed(PRINTED[name][1], unadjusted[name]),
            p=Printed(CONFIRMATORY_HOLM[name], adjusted[name]),
            sidedness="one-sided",
            test="exact Wilcoxon signed-rank, Holm step-down",
            unit=f"objective (n = {len(objectives)}), lesson-context alignment",
            location=sources.where("app:omnibus"),
            computed_from=RAW,
        )
        for name, (label, _arms) in CONTRASTS.items()
    ]


def _holm(raw: list[float]) -> list[float]:
    order = sorted(range(len(raw)), key=lambda index: raw[index])
    adjusted, running = [0.0] * len(raw), 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(raw) - rank) * raw[index]))
        adjusted[index] = running
    return adjusted


def _procedures(sources: Sources, ratings: list[Row]) -> list[Result]:
    """H1c on the six lesson means Table 6.3 tests: each lesson's ratings pooled per condition."""
    pooled: dict[tuple[str, str], list[int]] = defaultdict(list)
    for r in ratings:
        if r["criterion_id"] == LCA:
            pooled[(r["lesson_id"], r["condition"])].append(int(r["score"]))
    lessons = sorted({lesson for lesson, _ in pooled})
    lesson_level = mean(
        float(mean(pooled[(lesson, "C3")]) - mean(pooled[(lesson, "C0")])) for lesson in lessons
    )
    return [
        _row(
            id="D-H1c-lessons",
            quantity="C3 − C0 on the six lesson means",
            estimate=Printed("+0.280", lesson_level),
            unit="lesson (n = 6)",
            computed_from=RAW,
            question="RQ1, H1c under other procedures",
            location=sources.where("app:mixed-model", "tab:human-contrasts"),
        ),
    ]


def _length(sources: Sources, ratings: list[Row]) -> list[Result]:
    generation = sources.sheet("18_Generation_Raw")
    chars = [mean(g["chars"] for g in generation if g["condition"] == c) for c in CONDITIONS]
    alignment: dict[tuple[str, str, int], list[int]] = defaultdict(list)
    for r in ratings:
        if r["criterion_id"] == "lesson_context_alignment":
            alignment[(r["lesson_id"], r["condition"], r["draw"])].append(int(r["score"]))
    lengths = [g["chars"] for g in generation]
    scores = [mean(alignment[(g["lesson"], g["condition"], g["repeat"])]) for g in generation]
    common = {"question": "Pack length", "location": sources.where("app:pack-length")}
    return [
        _row(
            id="D-L1",
            quantity="Mean pack length, C0 (characters)",
            estimate=Printed("8,422", chars[0]),
            also=tuple(
                (c, Printed(t, v))
                for c, t, v in zip(
                    CONDITIONS[1:], ("6,685", "6,587", "6,203"), chars[1:], strict=True
                )
            ),
            unit="pack (n = 72)",
            computed_from="18_Generation_Raw",
            **common,
        ),
        _row(
            id="D-L2",
            quantity="Length against mean lesson-context alignment",
            estimate=Printed("-0.05", stats.spearmanr(lengths, scores).statistic),
            test="Spearman rank correlation",
            unit="pack (n = 72)",
            computed_from=f"18_Generation_Raw; {RAW}",
            **common,
        ),
        models.length(sources),
    ]


REPLICATES = {
    ("t3-w02", "lo-t3w02-01"): ("6", "-204", "+823", "-0.67", "+0.83"),
    ("t3-w05", "lo-t3w05-02"): ("4", "-1306", "-856", "-1.00", "+0.17"),
    ("t2-w09", "lo-t2w09-01"): ("3", "-949", "-463", "-0.80", "-0.50"),
    ("t3-w02", "lo-t3w02-03"): ("3", "-27", "+2672", "+0.50", "+0.67"),
}


def _replicates(sources: Sources) -> list[Result]:
    sections: dict[tuple[str, str, str, str], list[Any]] = defaultdict(list)
    groups: dict[tuple[str, str], dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for case in sources.run()["cases"]:
        for section in case["sections"]:
            sections[
                (case["lesson"], case["student"], case["condition"], section["lesson_objective_id"])
            ].append(section)
        if case["condition"] == "P1":
            for objective, state in (case.get("learner_states") or {}).items():
                groups[(case["lesson"], objective)][json.dumps(state, sort_keys=True)].append(
                    case["student"]
                )
    cells: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for r in sources.sheet(DECODED):
        if r["Status"] == "answered":
            cells[(r["Lesson"], r["Learner"], r["Objective"])].append(
                int(r["Collapsed preference"])
            )
    preference = {key: mean(values) for key, values in cells.items()}
    rows = []
    for (lesson, objective), (learners, low, high, pref_low, pref_high) in REPLICATES.items():
        members = max(groups[(lesson, objective)].values(), key=len)
        documents = {
            json.dumps(sections[(lesson, s, "P1", objective)], sort_keys=True) for s in members
        }
        lengths = [
            _characters(sections[(lesson, s, "P1", objective)])
            - _characters(sections[(lesson, s, "P0", objective)])
            for s in members
        ]
        prefs = [
            preference[(lesson, s, objective)]
            for s in members
            if (lesson, s, objective) in preference
        ]
        matched = (min(lengths), max(lengths)) == (int(low), int(high))
        run = "h2-deepseek-clean"
        rows.append(
            _row(
                id=f"D-V-{lesson}-{objective[-2:]}",
                question="Generation from identical learner states",
                quantity=f"{lesson}, objective {int(objective[-2:])}: learners sharing one state",
                estimate=Printed(learners, str(len(members))),
                also=(
                    ("distinct documents", Printed(learners, str(len(documents)))),
                    ("length change, lowest", Printed(low, min(lengths))),
                    ("highest", Printed(high, max(lengths))),
                    ("preference, lowest", Printed(pref_low, min(prefs))),
                    ("highest", Printed(pref_high, max(prefs))),
                ),
                unit="learner",
                location=sources.where("app:generation-variability", "tab:replicates"),
                computed_from=f"run record {run}; {DECODED}",
                note="length change is the characters across every text field of the "
                "objective's sections, personalised minus base, in the run the raters judged; "
                "preference is the mean of the -1/0/+1 direction over the panel's answered "
                "cells."
                + (
                    ""
                    if matched
                    else f" The run record gives {min(lengths):+d} to {max(lengths):+d}; "
                    "Table D.4 should print that range."
                ),
            )
        )
    return rows


def _characters(value: Any) -> int:
    """Characters across every string field: the measure that reproduces the printed ranges."""
    if isinstance(value, str):
        return len(value)
    if isinstance(value, dict):
        return sum(_characters(v) for v in value.values())
    if isinstance(value, list):
        return sum(_characters(v) for v in value)
    return 0
