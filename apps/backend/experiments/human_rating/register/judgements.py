"""Appendix D's checks on the comparative judgements: consistency within a panel, the side a
material was shown on, and how the raters' cases fell across the attainment groups."""

from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
from typing import Any

from .record import Printed, Result
from .sources import Sources

DECODED = "26_P2_Decoded"
P2_RAW = "12_P2_Raw"


def results(sources: Sources) -> list[Result]:
    return [*_consistency(sources), *_side(sources), *_allocation(sources)]


def _row(**fields: Any) -> Result:
    return Result(part="Appendix D", **fields)


CONSISTENCY = {
    "learner_evidence_alignment": ("32", "8", "14", "12", "6"),
    "adaptive_calibration": ("32", "8", "14", "7", "11"),
    "instructional_integrity": ("30", "8", "11", "16", "3"),
}


def _consistency(sources: Sources) -> list[Result]:
    panels: dict[tuple[str, str], list[int]] = defaultdict(list)
    for r in sources.sheet(DECODED):
        if r["Status"] == "answered":
            panels[(r["Criterion"], r["Panel"])].append(int(r["Signed preference"]))
    rows = []
    for criterion, (n, identical, agree, one_equal, opposite) in CONSISTENCY.items():
        pairs = [v for (c, _), v in panels.items() if c == criterion and len(v) == 2]
        signs = [(_sign(a), _sign(b)) for a, b in pairs]
        rows.append(
            _row(
                id=f"D-C-{criterion.split('_')[0]}",
                question="Checks on the comparative judgements",
                quantity=f"{criterion}: panels both raters answered",
                estimate=Printed(n, str(len(pairs))),
                also=(
                    ("identical", Printed(identical, str(sum(a == b for a, b in pairs)))),
                    ("same direction", Printed(agree, str(sum(x == y for x, y in signs)))),
                    (
                        "one judged equal",
                        Printed(one_equal, str(sum((x == 0) != (y == 0) for x, y in signs))),
                    ),
                    ("opposite", Printed(opposite, str(sum(x * y < 0 for x, y in signs)))),
                ),
                unit="doubly answered panel",
                computed_from=DECODED,
                location=sources.where("app:comparative-checks", "tab:comparative-consistency"),
            )
        )
    return rows


def _sign(value: int) -> int:
    return (value > 0) - (value < 0)


def _side(sources: Sources) -> list[Result]:
    decoded = {r["Judgement ID"]: r for r in sources.sheet(DECODED)}
    answered = [r for r in sources.sheet(P2_RAW) if r["response_status"] == "answered"]
    side = {r["judgement_id"]: "A" if r["condition_a"] == "P1" else "B" for r in answered}
    score = {k: int(decoded[k]["Signed preference"]) for k in side}
    by_side = {s: [score[k] for k, v in side.items() if v == s] for s in "AB"}
    copies: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in answered:
        copies[(r["rater_id"], r["case_id"])].append(r["judgement_id"])
    copy_means = {
        s: mean(mean(score[k] for k in ids) for ids in copies.values() if side[ids[0]] == s)
        for s in "AB"
    }
    return [
        _row(
            id="D-S1",
            question="Checks on the comparative judgements",
            quantity="Answered cells with P1 as Material A",
            estimate=Printed("101", str(len(by_side["A"]))),
            also=(("as Material B", Printed("98", str(len(by_side["B"])))),),
            unit="answered criterion cell",
            computed_from=P2_RAW,
            location=sources.where("app:comparative-checks"),
        ),
        _row(
            id="D-S2",
            question="Checks on the comparative judgements",
            quantity="Mean preference for P1 when shown as Material A",
            estimate=Printed("-0.119", mean(by_side["A"])),
            also=(
                ("as Material B", Printed("+0.214", mean(by_side["B"]))),
                ("averaging rated copies, as A", Printed("-0.212", copy_means["A"])),
                ("as B", Printed("+0.105", copy_means["B"])),
            ),
            unit="answered criterion cell; descriptive",
            computed_from=f"{P2_RAW}; {DECODED}",
            location=sources.where("app:comparative-checks"),
        ),
    ]


ALLOCATION = {
    "rater-1": ("4 (18)", "4 (18)", "5 (18)", "+0.296"),
    "rater-2": ("4 (15)", "3 (15)", "6 (24)", "-0.407"),
    "rater-3": ("5 (18)", "4 (18)", "4 (15)", "+0.431"),
    "rater-4": ("5 (17)", "5 (15)", "2 (8)", "-0.175"),
}


def _allocation(sources: Sources) -> list[Result]:
    group = {
        r["learner_id"]: r["reconstructed_attainment_group"]
        for r in sources.sheet("13_P2_Learners")
    }
    decoded = {
        r["Judgement ID"]: int(r["Signed preference"])
        for r in sources.sheet(DECODED)
        if r["Status"] == "answered"
    }
    cases: dict[tuple[str, str], set[str]] = defaultdict(set)
    cells: Counter[tuple[str, str]] = Counter()
    scores: dict[str, list[int]] = defaultdict(list)
    for r in sources.sheet(P2_RAW):
        if r["response_status"] == "answered":
            key = (r["rater_id"], group[r["learner_id"]])
            cases[key].add(r["case_id"])
            cells[key] += 1
            scores[r["rater_id"]].append(decoded[r["judgement_id"]])
    rows = []
    for rater, (lower, middle, top, lean) in ALLOCATION.items():
        cell = {
            g: f"{len(cases[(rater, g)])} ({cells[(rater, g)]})" for g in ("lower", "middle", "top")
        }
        rows.append(
            _row(
                id=f"D-A-{rater}",
                question="Checks on the comparative judgements",
                quantity=f"{rater}: cases (answered cells) judged, top attainment group",
                estimate=Printed(top, cell["top"]),
                also=(
                    ("lower", Printed(lower, cell["lower"])),
                    ("middle", Printed(middle, cell["middle"])),
                    ("mean preference for P1", Printed(lean, mean(scores[rater]))),
                ),
                unit="case; answered cell",
                computed_from=f"{P2_RAW}; 13_P2_Learners",
                location=sources.where("app:comparative-checks", "tab:comparative-allocation"),
            )
        )
    return rows
