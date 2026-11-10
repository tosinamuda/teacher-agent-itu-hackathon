"""Part 2 results: adaptation scope, RQ2, the overall comparison, attainment and responsiveness."""

from __future__ import annotations

import random
from collections import Counter, defaultdict
from fractions import Fraction
from statistics import mean
from typing import Any

from scipy import stats

from . import comments
from .exact import sign_flip
from .record import Printed, Result
from .sources import Row, Sources

DECODED = "26_P2_Decoded"
SCOPE = "16_P2_Scope_Raw"
LEARNERS = "13_P2_Learners"
EXACT_84 = "43_Exact_84"
CALIBRATION = "adaptive_calibration"
CRITERIA = {
    "learner_evidence_alignment": ("25/67", "24/67", "18/67", "6/32", "-0.106"),
    CALIBRATION: ("38/67", "22/67", "7/67", "11/32", "+0.224"),
    "instructional_integrity": ("20/65", "25/65", "20/65", "3/30", "-0.314"),
}


def results(sources: Sources) -> list[Result]:
    decoded = sources.sheet(DECODED)
    answered = [r for r in decoded if r["Status"] == "answered"]
    return [
        *_scope(sources),
        *_hypothesis(sources, answered),
        *_overall(sources, decoded, answered),
        *_by_criterion(sources, answered),
        *_by_band(sources, answered),
        *_attainment(sources, answered),
        *comments.results(sources, len(answered)),
    ]


def _row(**fields: Any) -> Result:
    return Result(part="Part 2", **fields)


#: Mean direction of preference for P1, and the judgements favouring P1 and P0, by band group
#: and criterion, as §6.7 prints them.
BAND_DIRECTIONS = {
    ("remediate and reinforce", "adaptive_calibration"): ("+0.455", "14", "5"),
    ("remediate and reinforce", "instructional_integrity"): ("+0.318", "9", "3"),
    ("remediate and reinforce", "learner_evidence_alignment"): ("+0.273", "12", "7"),
    ("extend", "adaptive_calibration"): ("+0.104", "24", "17"),
    ("extend", "instructional_integrity"): ("-0.312", "11", "22"),
    ("extend", "learner_evidence_alignment"): ("-0.083", "13", "17"),
}
BAND_GROUPS = {"remediate and reinforce": ("remediate", "reinforce"), "extend": ("extend",)}


def _by_band(sources: Sources, answered: list[Row]) -> list[Result]:
    """The Part 2 comparison disaggregated by band, as the analysis plan specifies."""
    bands = _states(sources)
    rows = []
    for (group, criterion), (direction, for_p1, for_p0) in BAND_DIRECTIONS.items():
        states = {key for key, band in bands.items() if band in BAND_GROUPS[group]}
        panels: dict[tuple[str, str, str], list[int]] = defaultdict(list)
        for r in answered:
            key = (r["Lesson"], r["Learner"], r["Objective"])
            if r["Criterion"] == criterion and key in states:
                panels[key].append(int(r["Collapsed preference"]))
        judgements = [value for values in panels.values() for value in values]
        rows.append(
            _row(
                id=f"P2-BAND-{BAND_GROUPS[group][0]}-{criterion}",
                question="RQ2, by band",
                quantity=f"Mean direction of preference for P1, {group} states, {criterion}",
                estimate=Printed(
                    direction, float(mean(Fraction(sum(v), len(v)) for v in panels.values()))
                ),
                also=(
                    ("favouring P1", Printed(for_p1, str(judgements.count(1)))),
                    ("favouring P0", Printed(for_p0, str(judgements.count(-1)))),
                ),
                unit=f"learner-objective panel (n = {len(panels)}), descriptive",
                location=sources.where("sec:the-overall-comparison"),
                computed_from=f"{DECODED}; run record (bands)",
            )
        )
    return rows


def _scope(sources: Sources) -> list[Result]:
    scope = sources.sheet(SCOPE)
    present = [r for r in scope if r["model_learner_state"] == "state_present"]
    absent = [r for r in scope if r["model_learner_state"] == "state_absent"]
    changed = sum(str(r["objective_section_changed"]).lower() == "true" for r in present)
    kept = sum(str(r["objective_section_changed"]).lower() == "false" for r in absent)
    cases = {r["case_id"] for r in scope}
    preserved = {c for c in cases if all(r["sections_in_p1"] for r in scope if r["case_id"] == c)}
    common = {
        "question": "Adaptation scope",
        "location": sources.where("sec:adaptation-scope"),
        "computed_from": SCOPE,
    }
    return [
        _row(
            id="P2-S1",
            quantity="Sections with learner state that were personalised",
            estimate=Printed("35", str(changed)),
            also=(
                ("of sections", Printed("69", str(len(scope)))),
                ("sections without state passed through unchanged", Printed("34", str(kept))),
            ),
            unit="case-objective section",
            test="section digest, P0 against P1",
            **common,
        ),
        _row(
            id="P2-S2",
            quantity="Personalised packs keeping every base-pack objective",
            estimate=Printed("26", str(len(preserved))),
            unit="case",
            test="objective identifiers, P0 against P1",
            **common,
        ),
    ]


def _states(sources: Sources) -> dict[tuple[str, str, str], str]:
    return {
        (case["lesson"], case["student"], objective): state["mastery_band"]
        for case in sources.run()["cases"]
        for objective, state in (case.get("learner_states") or {}).items()
    }


def _hypothesis(sources: Sources, answered: list[Row]) -> list[Result]:
    bands = _states(sources)
    counts = Counter(bands.values())
    target = {key for key, band in bands.items() if band in ("remediate", "reinforce")}
    rows = [
        r
        for r in answered
        if r["Criterion"] == CALIBRATION and (r["Lesson"], r["Learner"], r["Objective"]) in target
    ]
    direction = [int(r["Collapsed preference"]) for r in rows]
    panels: dict[tuple[str, str, str], list[Row]] = defaultdict(list)
    for r in rows:
        panels[(r["Lesson"], r["Learner"], r["Objective"])].append(r)
    by_direction = [
        Fraction(sum(int(x["Collapsed preference"]) for x in v), len(v)) for v in panels.values()
    ]
    by_strength = [
        Fraction(sum(int(x["Signed preference"]) for x in v), len(v)) for v in panels.values()
    ]
    learners: dict[str, list[Fraction]] = defaultdict(list)
    for key, value in zip(panels, by_direction, strict=True):
        learners[key[1]].append(value)
    by_learner = [sum(v, Fraction(0)) / len(v) for v in learners.values()]
    p_direction = sign_flip(by_direction)
    where = sources.where("sec:rq2-adaptive-calibration")
    common = {
        "question": "RQ2, H2",
        "location": where,
        "computed_from": f"{DECODED}; run record (bands)",
    }
    return [
        _row(
            id="P2-B1",
            quantity="Learner-objective states banded remediate",
            estimate=Printed("7", str(counts["remediate"])),
            also=(
                ("reinforce", Printed("4", str(counts["reinforce"]))),
                ("extend", Printed("24", str(counts["extend"]))),
            ),
            unit="learner-objective state",
            question="RQ2, H2",
            location=where,
            computed_from="run record",
        ),
        _row(
            id="P2-H2-count",
            quantity="Answered adaptive-calibration judgements favouring P1",
            estimate=Printed("14", str(direction.count(1))),
            also=(
                ("favouring P0", Printed("5", str(direction.count(-1)))),
                ("no preference", Printed("2", str(direction.count(0)))),
                ("judgements", Printed("21", str(len(direction)))),
                ("states", Printed("11", str(len(target)))),
            ),
            unit="criterion judgement",
            **common,
        ),
        _row(
            id="P2-H2",
            quantity="Mean direction of preference for P1, remediate and reinforce states",
            estimate=Printed("+0.455", float(mean(by_direction))),
            p=Printed(".0488", p_direction),
            sidedness="one-sided",
            test="exact sign-flip over panels",
            unit=f"learner-objective panel (n = {len(by_direction)})",
            also=(
                ("two-sided", Printed(".0977", 2 * p_direction)),
                ("panels favouring P1", Printed("7", str(sum(v > 0 for v in by_direction)))),
            ),
            **common,
        ),
        _row(
            id="P2-H2-strength",
            quantity="Mean preference strength, same panels, -2 to +2",
            estimate=Printed("+0.682", float(mean(by_strength))),
            p=Printed(".0684", sign_flip(by_strength)),
            sidedness="one-sided",
            test="exact sign-flip over panels",
            unit=f"panel (n = {len(by_strength)})",
            **common,
        ),
        _row(
            id="P2-H2-learner",
            quantity="Mean direction blocked by learner",
            estimate=Printed("+0.242", float(mean(by_learner))),
            p=Printed(".2500", sign_flip(by_learner)),
            sidedness="one-sided",
            test="exact sign-flip over learners",
            unit=f"learner (n = {len(by_learner)})",
            **common,
        ),
    ]


def _case_means(answered: list[Row], criterion: str | None = None) -> dict[str, float]:
    cells: dict[str, list[int]] = defaultdict(list)
    for r in answered:
        if criterion is None or r["Criterion"] == criterion:
            cells[r["Case"]].append(int(r["Signed preference"]))
    return {case: mean(values) for case, values in cells.items()}


def _overall(sources: Sources, decoded: list[Row], answered: list[Row]) -> list[Result]:
    means = list(_case_means(answered).values())
    low, high = stats.t.interval(0.95, len(means) - 1, loc=mean(means), scale=stats.sem(means))
    wilcoxon = stats.wilcoxon(means).pvalue
    lower, upper, learner_mean = _learner_bootstrap(sources, answered)
    common = {
        "question": "RQ2, overall comparison",
        "location": sources.where("sec:the-overall-comparison"),
        "computed_from": DECODED,
    }
    same = sum(int(r["Signed preference"]) == 0 for r in answered)
    return [
        _row(
            id="P2-O1",
            quantity="Answered criterion judgements",
            estimate=Printed("199", str(len(answered))),
            also=(
                ("issued", Printed("210", str(len(decoded)))),
                ("about the same", Printed("45", str(same))),
            ),
            unit="criterion judgement",
            **common,
        ),
        _row(
            id="P2-O2",
            quantity="Mean preference for P1, -2 to +2",
            estimate=Printed("-0.061", mean(means)),
            interval=(Printed("-0.42", low), Printed("+0.30", high)),
            p=Printed(".798", wilcoxon),
            sidedness="two-sided",
            test="Student's t interval; Wilcoxon signed-rank p",
            unit=f"case (n = {len(means)})",
            also=(
                ("cases favouring P1", Printed("13", str(sum(m > 0 for m in means)))),
                ("favouring P0", Printed("12", str(sum(m < 0 for m in means)))),
                ("tied", Printed("1", str(sum(m == 0 for m in means)))),
            ),
            **common,
        ),
        _row(
            id="P2-O3",
            quantity="Mean preference for P1, each learner weighted equally",
            estimate=Printed("+0.023", learner_mean),
            interval=(Printed("-0.20", lower), Printed("+0.25", upper)),
            test="cluster bootstrap over learners within attainment group, 20,000 replicates, "
            "seed 0",
            unit="learner (n = 9)",
            note="resampled; the interval's last digit can move with the seed",
            **common,
        ),
    ]


def _learner_bootstrap(sources: Sources, answered: list[Row]) -> tuple[float, float, float]:
    cells: dict[str, list[int]] = defaultdict(list)
    for r in answered:
        cells[r["Learner"]].append(int(r["Signed preference"]))
    learner_means = {learner: mean(values) for learner, values in cells.items()}
    groups: dict[str, list[str]] = defaultdict(list)
    for r in sources.sheet(LEARNERS):
        groups[r["reconstructed_attainment_group"]].append(r["learner_id"])
    generator = random.Random(0)
    draws = sorted(
        mean(
            learner_means[generator.choice(members)] for members in groups.values() for _ in members
        )
        for _ in range(20_000)
    )
    return (
        draws[int(0.025 * len(draws))],
        draws[int(0.975 * len(draws)) - 1],
        mean(learner_means.values()),
    )


def _by_criterion(sources: Sources, answered: list[Row]) -> list[Result]:
    common = {
        "question": "RQ2, by criterion",
        "location": sources.where("sec:the-overall-comparison", "tab:part2-by-criterion"),
        "computed_from": DECODED,
    }
    rows = []
    for criterion, (p1, p0, same, opposite, case_mean) in CRITERIA.items():
        chosen = [r for r in answered if r["Criterion"] == criterion]
        arms = Counter(r["Preferred arm"] for r in chosen)
        joint, crossed = _opposite(chosen)
        n = len(chosen)
        rows.append(
            _row(
                id=f"P2-C-{criterion.split('_')[0]}",
                quantity=f"{criterion}: judgements favouring P1",
                estimate=Printed(p1, f"{arms['P1']}/{n}"),
                also=(
                    ("favouring P0", Printed(p0, f"{arms['P0']}/{n}")),
                    ("about the same", Printed(same, f"{n - arms['P1'] - arms['P0']}/{n}")),
                    ("opposite choices", Printed(opposite, f"{crossed}/{joint}")),
                    (
                        "case-level mean",
                        Printed(case_mean, mean(_case_means(answered, criterion).values())),
                    ),
                ),
                unit="criterion judgement; no test",
                **common,
            )
        )
    return rows


def _opposite(chosen: list[Row]) -> tuple[int, int]:
    """Panels both raters answered on this criterion, and those with opposite choices."""
    by_panel: dict[str, list[int]] = defaultdict(list)
    for r in chosen:
        by_panel[r["Panel"]].append(int(r["Collapsed preference"]))
    joint = [v for v in by_panel.values() if len(v) == 2]
    return len(joint), sum(v[0] * v[1] < 0 for v in joint)


def _attainment(sources: Sources, answered: list[Row]) -> list[Result]:
    cells: dict[str, list[int]] = defaultdict(list)
    for r in answered:
        cells[r["Learner"]].append(int(r["Signed preference"]))
    group_of = {
        r["learner_id"]: r["reconstructed_attainment_group"] for r in sources.sheet(LEARNERS)
    }
    by_group: dict[str, list[float]] = defaultdict(list)
    for learner, values in cells.items():
        by_group[group_of[learner]].append(mean(values))
    ranked = sorted(cells, key=lambda learner: mean(cells[learner]))
    exact = next(
        r for r in sources.sheet(EXACT_84) if r.get("Diagnostic") == "Lower-tail proportion"
    )
    common = {
        "question": "RQ2, attainment (exploratory)",
        "location": sources.where("sec:the-attainment-gradient"),
    }
    return [
        _row(
            id="P2-X1",
            quantity="Preference for P1 by reconstructed attainment group, lower",
            estimate=Printed("+0.400", mean(by_group["lower"])),
            also=(
                ("middle", Printed("+0.361", mean(by_group["middle"]))),
                ("highest", Printed("-0.692", mean(by_group["top"]))),
            ),
            unit="learner, weighted equally",
            computed_from=f"{DECODED}; {LEARNERS}",
            note="exploratory: groups reconstructed from the same class work; rater "
            "allocation uneven",
            **common,
        ),
        _row(
            id="P2-X2",
            quantity="Top three learners occupy the three lowest preference ranks",
            estimate=Printed("3", str(sum(group_of[learner] == "top" for learner in ranked[:3]))),
            p=Printed(".012", float(exact["Value"])),
            sidedness="one-sided (lower tail)",
            test="exact permutation of the 84 three-of-nine groupings",
            unit="learner (n = 9)",
            computed_from=f"{DECODED}; {EXACT_84}",
            note="exploratory; no further analysis",
            **common,
        ),
    ]
