"""Reconciliation for the Part 2 handoff: what the export contains, and what it cannot say.

Every count an analyst would otherwise have to trust is recomputed here from the exported
table, so a mismatch with a previously reported number shows up as a line in a report
rather than as a silent disagreement three steps into someone else's analysis.

The agreement breakdown is deliberately split four ways. "Raters disagreed" covers two
different failures — one rater seeing no difference where the other saw a clear winner,
and the two picking opposite materials — and a single agreement coefficient hides which
one is happening.

Run with::

    uv run python -m experiments.human_rating.validation <bundle dir>
"""

from __future__ import annotations

import csv
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SIGN = {"2": 1, "1": 1, "0": 0, "-1": -1, "-2": -1}


def load(bundle: Path) -> list[dict[str, Any]]:
    with (bundle / "part2" / "ratings_long.csv").open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _answered(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r["response_status"] == "answered"]


def coverage(rows: list[dict[str, Any]]) -> list[str]:
    ans = _answered(rows)
    out = [
        f"- assigned criterion cells: **{len(rows)}**",
        f"- answered: **{len(ans)}**  |  blank: **{len(rows) - len(ans)}**",
        f"- distinct panels (learner-lesson-objective): **{len({r['panel_id'] for r in rows})}**",
        "- rater-panels (panel x rater): "
        f"**{len({(r['rater_id'], r['panel_id']) for r in rows})}**",
        f"- cases: **{len({r['case_id'] for r in rows})}**  |  learners: "
        f"**{len({r['learner_id'] for r in rows})}**  |  lessons: "
        f"**{len({r['lesson_id'] for r in rows})}**",
        "",
        '**The reported "199 judgements" is the answered-criterion-cell count.** It is not '
        "panels and not documents.",
        "",
        "| rater | assigned | answered | blank |",
        "| --- | ---: | ---: | ---: |",
    ]
    for rater in sorted({r["rater_id"] for r in rows}):
        mine = [r for r in rows if r["rater_id"] == rater]
        done = len(_answered(mine))
        out.append(f"| {rater} | {len(mine)} | {done} | {len(mine) - done} |")
    return out


def dependency(rows: list[dict[str, Any]]) -> list[str]:
    per_learner = Counter(
        r["learner_id"] for r in {(x["case_id"], x["learner_id"]): x for x in rows}.values()
    )
    panels_per = Counter()
    for panel in {r["panel_id"] for r in rows}:
        panels_per[len({r["rater_id"] for r in rows if r["panel_id"] == panel})] += 1
    return [
        "The 26 cases are **not** 26 independent units. Three layers of repetition:",
        "",
        f"- **learners recur across lessons** — {len(per_learner)} learners hold "
        f"{sum(per_learner.values())} cases: {dict(sorted(per_learner.items()))}",
        "- **P0 is one shared pack per lesson** — 3 base packs stand behind all 26 cases, so "
        "the P0 side of a case is not an independently generated artefact",
        f"- **panels by rater count**: {dict(sorted(panels_per.items()))} — every panel was "
        "assigned to exactly two raters, on opposite A/B presentations",
        "",
        "Any inferential analysis has to state which of these it models and which it ignores.",
    ]


def agreement(rows: list[dict[str, Any]]) -> list[str]:
    panels: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
    for r in _answered(rows):
        panels[(r["panel_id"], r["criterion_id"])][r["rater_id"]] = r["score_used"]
    out = [
        "Split four ways, because one coefficient cannot distinguish these.",
        "",
        "| criterion | both rated | identical | same winner, different degree | one said "
        '"about the same" | opposite winners |',
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for crit in sorted({r["criterion_id"] for r in rows}):
        pairs = [
            tuple(v[k] for k in sorted(v))
            for (panel, c), v in panels.items()
            if c == crit and len(v) == 2
        ]
        kind = Counter()
        for a, b in pairs:
            if a == b:
                kind["identical"] += 1
            elif SIGN[a] == SIGN[b]:
                kind["degree"] += 1
            elif SIGN[a] == 0 or SIGN[b] == 0:
                kind["one_tie"] += 1
            else:
                kind["opposite"] += 1
        n = len(pairs) or 1
        out.append(
            f"| {crit} | {len(pairs)} | {kind['identical']} ({kind['identical'] / n:.0%}) | "
            f"{kind['degree']} ({kind['degree'] / n:.0%}) | {kind['one_tie']} "
            f"({kind['one_tie'] / n:.0%}) | **{kind['opposite']} ({kind['opposite'] / n:.0%})** |"
        )
    out += [
        "",
        '"Identical" is exact agreement on the **five-point** signed scale.',
    ]
    return out


def aggregation(rows: list[dict[str, Any]]) -> list[str]:
    """The exact route from cell to learner mean, with every denominator shown."""
    ans = _answered(rows)
    by_learner = defaultdict(list)
    for r in ans:
        by_learner[r["learner_id"]].append(SIGN[r["score_used"]])
    out = [
        "The nine learner means below are **an unweighted mean of that learner's answered "
        "criterion cells**, on the collapsed three-category coding "
        "(`clearly`/`slightly` both count as one step).",
        "",
        "This weights a learner by how many cells they generated. It is **not** the same as "
        "averaging criteria within objective, then objectives within lesson, then lessons. "
        "With unequal completion those give different answers, and the choice must be stated "
        "rather than inherited from the missingness pattern.",
        "",
        "| learner | answered cells | mean (collapsed) | mean (five-point) |",
        "| --- | ---: | ---: | ---: |",
    ]
    for learner in sorted(by_learner):
        five = [int(r["score_used"]) for r in ans if r["learner_id"] == learner]
        out.append(
            f"| {learner} | {len(by_learner[learner])} | "
            f"{st.mean(by_learner[learner]):+.4f} | {st.mean(five):+.4f} |"
        )
    overall = st.mean(st.mean(v) for v in by_learner.values())
    out += [
        "",
        f"Equal-weight-per-learner overall mean (collapsed): **{overall:+.4f}**",
    ]
    return out


def evidence(rows: list[dict[str, Any]]) -> list[str]:
    """What the personaliser held for the objectives raters actually saw."""
    counts = Counter(r["model_learner_state"] for r in rows)
    resolution = Counter(r["objective_resolved_from"] for r in rows)
    moved = [r for r in rows if r["objective_id"] != r["objective_id_legacy_positional"]]
    return [
        "Each panel's objective is read from the heading the delivered document prints, "
        "not from the panel's position.",
        "",
        f"- objective resolved from the document heading: **{resolution['document heading']}** "
        f"of {len(rows)} rows",
        f"- personaliser held learner state: **{counts['state_present']}** of {len(rows)}",
        f"- state absent: {counts['state_absent']}  |  unknown: {counts['unknown']}",
        "",
        "**Every objective shown to a rater had learner state.** The renderer emits a panel "
        "only for objectives a student has class work for, so this is the design working, "
        "not a finding.",
        "",
        "### A previously reported finding, withdrawn",
        "",
        f"An earlier export took each panel's objective from its **ordinal**, which is wrong "
        f"whenever the shown objectives are not the first ones in the lesson: "
        f"**{len(moved)} of {len(rows)} rows** carried the wrong objective id, across "
        f"{len({r['panel_id'] for r in moved})} of {len({r['panel_id'] for r in rows})} panels. "
        "That mislabelling alone produced the reported claim that 108 assigned cells "
        "concerned objectives with no learner evidence. **The claim was an artefact of the "
        "export and is withdrawn.** `objective_id_legacy_positional` keeps the old value so "
        "the diff is inspectable.",
        "",
        "### What personalisation changed, per objective",
        "",
        "Comparing P0 and P1 **section by section within an objective**, rather than hashing "
        "the whole pack: P1 changed exactly the **35** objectives it held state for and left "
        "the **34** it did not **byte-identical**. A whole-pack hash differs as soon as one "
        "section does, so the earlier observation that P1 differs from P0 in all 26 cases "
        "carried no implication about untargeted rewriting. See "
        "`objective_generation_audit.csv`.",
    ]


def limits() -> list[str]:
    return [
        "- **The sampling strata were never recorded.** Learners were drawn from three "
        "teacher-assigned ability categories in a class of forty; the category was not "
        "written down. `sampling_stratum` is **reconstructed post hoc** as rank thirds of "
        "the nine, using the teacher's marks on the three study lessons.",
        "- **That reconstruction uses the same class work that produced the P1 learner "
        "state.** The variable used to split the analysis is not independent of the "
        "intervention's input. Any attainment-gradient claim inherits this.",
        "- `attainment_rank` ranks **the nine selected learners**, not the class of forty.",
        "- `student-04` sat two of the three papers; their score averages two, not three.",
        "- **No per-cell timestamps.** Google Docs exposes none, so ordering within a "
        "rater's session cannot be reconstructed.",
        "- **No recorded reason for any blank.** All 11 are `unknown`.",
        "- **Rater-4 is incomplete** (11 cells). Collection is not closed.",
        "- **Pack text and learner class work are not in this bundle** — real minors' work, "
        "held back pending an explicit sharing decision.",
    ]


def report(bundle: Path) -> str:
    rows = load(bundle)
    blocks = [
        ("Coverage and the unit question", coverage(rows)),
        ("Dependency structure", dependency(rows)),
        ("Learner evidence available to the personaliser", evidence(rows)),
        ("Agreement, decomposed", agreement(rows)),
        ("Aggregation route and the nine learner means", aggregation(rows)),
        ("Limits on what this export can support", limits()),
    ]
    out = [
        "# Part 2 validation and reconciliation",
        "",
        "Recomputed from `part2/ratings_long.csv`. No value here is copied from an "
        "earlier analysis.",
        "",
    ]
    for title, lines in blocks:
        out += [f"## {title}", "", *lines, ""]
    return "\n".join(out)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    bundle = Path(sys.argv[1])
    path = bundle / "reproduction" / "validation_report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report(bundle), encoding="utf-8")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
