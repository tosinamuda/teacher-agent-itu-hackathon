"""Turn the blinded judgments into a readable, de-anonymised report.

Blinding runs one way: the judge saw an opaque id and nothing else, and the mapping back
to a condition is applied only here, after every judgment is fixed. So the report can name
conditions without the ratings ever having been made in sight of one.

The endpoint is C1 - C0 and is reported as such whatever else the run contains. The
remaining conditions are reported beside it, never in place of it: H1a was frozen on one
comparison, and a run that also draws C2 and C3 does not get to choose a different one
afterwards.

    uv run python -m experiments.h1_condition_eval.rating_report <run-label>
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.domains.evaluation.application.constants import H1_RUBRIC
from experiments.h1_condition_eval.note_editorial import describe_note_source

HERE = Path(__file__).parent
DIMENSIONS = tuple(str(c["criterion_id"]) for c in H1_RUBRIC)
LABELS = {str(c["criterion_id"]): str(c["label"]) for c in H1_RUBRIC}
# The frozen endpoint: the one comparison H1a was registered on.
BASELINE, TREATMENT = "C0", "C1"
# Ladder order, so a report reads C0, C1, C2, C3 whatever order the key file is in.
LADDER = ("C0", "C1", "C2", "C3")


def _load(run_label: str) -> tuple[dict, dict, dict]:
    rating = HERE / "runs" / run_label / "rating"
    key = {r["candidate_id"]: r for r in json.loads((rating / "_key.json").read_text())}
    data = json.loads((rating / "judgments.json").read_text())
    judged = {j["candidate_id"]: j for j in data["judgments"]}
    return key, judged, data


def _scores(judged: dict, key: dict) -> dict[tuple[str, str], list[dict]]:
    """Every judgment for a cell, draw-ordered — not the last one to be read.

    Keyed by (lesson, condition) alone this silently kept whichever draw came last, so a
    run judged on all three repeats reported one of them and looked like a run judged on
    one. The repeat is in the key file; it belongs in the ordering.
    """
    cells: dict[tuple[str, str], list[tuple[int, dict]]] = {}
    for cid, judgment in judged.items():
        row = key[cid]
        cells.setdefault((row["lesson"], row["condition"]), []).append((row["repeat"], judgment))
    return {cell: [j for _, j in sorted(draws)] for cell, draws in cells.items()}


def _conditions(by: dict) -> list[str]:
    """The conditions this run actually judged, in ladder order."""
    present = {condition for _, condition in by}
    return [code for code in LADDER if code in present] + sorted(present - set(LADDER))


def _mean(by: dict, lesson: str, condition: str, dimension: str) -> float:
    draws = by[(lesson, condition)]
    return sum(float(j[dimension]["score"]) for j in draws) / len(draws)


def _arm_mean(by: dict, lessons: list[str], condition: str, dimension: str) -> float:
    return sum(_mean(by, lesson, condition, dimension) for lesson in lessons) / len(lessons)


def _table(header: list[str], rows: list[list[str]], numeric: bool = False) -> list[str]:
    rule = "---: " if numeric else "--- "
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join([rule.strip()] * len(header)) + " |",
        *("| " + " | ".join(row) + " |" for row in rows),
    ]


def _endpoint(by: dict, lessons: list[str]) -> list[str]:
    """C1 against C0, lesson by lesson. The registered comparison, reported alone."""
    drawn = len(by[(lessons[0], BASELINE)])
    lines = [
        f"## The endpoint — {TREATMENT} against {BASELINE}\n",
        f"Each cell is {BASELINE} -> {TREATMENT}, averaged over {drawn} generation "
        "draw(s) of that arm.\n",
    ]
    tally = {d: [0, 0, 0] for d in DIMENSIONS}
    rows = []
    for lesson in lessons:
        cells = []
        for dimension in DIMENSIONS:
            a = _mean(by, lesson, BASELINE, dimension)
            b = _mean(by, lesson, TREATMENT, dimension)
            tally[dimension][0 if b > a else 1 if b == a else 2] += 1
            cells.append(f"{a:.2f} -> {b:.2f} ({b - a:+.2f})")
        rows.append([lesson, *cells])
    lines += _table(["lesson", *(LABELS[d] for d in DIMENSIONS)], rows)
    lines += [""] + _table(
        ["dimension", f"{TREATMENT} higher", "tied", f"{TREATMENT} lower"],
        [[LABELS[d], *(str(n) for n in tally[d])] for d in DIMENSIONS],
        numeric=True,
    )
    return lines + [""]


def _ladder(by: dict, lessons: list[str], conditions: list[str]) -> list[str]:
    """Every arm's mean, and its margin over the control.

    Descriptive only. C2 and C3 are not part of H1a, and a difference read off this
    table is a lead to follow with a registered comparison, not a result.
    """
    if len(conditions) <= 2:
        return []
    lines = [
        "## The rest of the ladder\n",
        "Mean over the six lessons and every draw, then the margin over "
        f"{BASELINE}. Descriptive: {TREATMENT}-{BASELINE} above is the study's",
        "endpoint, and nothing here was registered as a comparison.\n",
    ]
    rows = []
    for condition in conditions:
        cells = []
        for dimension in DIMENSIONS:
            mean = _arm_mean(by, lessons, condition, dimension)
            control = _arm_mean(by, lessons, BASELINE, dimension)
            margin = "" if condition == BASELINE else f" ({mean - control:+.2f})"
            cells.append(f"{mean:.2f}{margin}")
        rows.append([condition, *cells])
    return lines + _table(["arm", *(LABELS[d] for d in DIMENSIONS)], rows, numeric=True) + [""]


def _spread(by: dict, lessons: list[str], conditions: list[str]) -> list[str]:
    """How far one arm's own draws disagree, which bounds how small a margin can be read.

    The same arm, the same inputs, three generations: whatever range that produces is the
    floor. A margin inside it is the draw, not the treatment.
    """
    lines = [
        "## Spread within an arm\n",
        "Range across the draws of one arm, averaged over the six lessons. A margin",
        "smaller than this is not distinguishable from re-running the same condition.\n",
    ]
    rows = []
    for dimension in DIMENSIONS:
        cells = []
        for condition in conditions:
            ranges = [
                max(j[dimension]["score"] for j in by[(lesson, condition)])
                - min(j[dimension]["score"] for j in by[(lesson, condition)])
                for lesson in lessons
            ]
            cells.append(f"{sum(ranges) / len(ranges):.2f}")
        rows.append([LABELS[dimension], *cells])
    return lines + _table(["dimension", *conditions], rows, numeric=True) + [""]


def _against(by: dict, baseline: dict, label: str, lessons: list[str]) -> list[str]:
    """Both runs' C1-C0 margins side by side, when an input change separates them.

    A margin that moves under a payload change is the thing to look at; a margin that
    holds is the thing to report. Neither is readable from two separate files.
    """
    lines = [
        f"## Against `{label}`\n",
        f"Each cell is that run's {TREATMENT}-{BASELINE} margin, then this one's.\n",
    ]
    rows = []
    for lesson in lessons:
        cells = []
        for dimension in DIMENSIONS:
            was = _margin(baseline, lesson, dimension)
            now = _margin(by, lesson, dimension)
            moved = "" if was == now else "  **moved**"
            cells.append(f"{was:+.2f} -> {now:+.2f}{moved}")
        rows.append([lesson, *cells])
    lines += _table(["lesson", *(LABELS[d] for d in DIMENSIONS)], rows)
    lines += [""] + _table(
        ["dimension", "mean margin there", "mean margin here"],
        [
            [
                LABELS[d],
                f"{sum(_margin(baseline, lesson, d) for lesson in lessons) / len(lessons):+.2f}",
                f"{sum(_margin(by, lesson, d) for lesson in lessons) / len(lessons):+.2f}",
            ]
            for d in DIMENSIONS
        ],
        numeric=True,
    )
    return lines + [""] + _how_much_moves_anyway(by, baseline, lessons)


def _how_much_moves_anyway(by: dict, baseline: dict, lessons: list[str]) -> list[str]:
    """How far each ARM moved between the runs, which bounds how far a margin can be read.

    An arm whose payload barely changed still moves, and that movement is the floor: a
    margin that shifts by less than it is not a finding. Only the arms BOTH runs drew —
    an arm the earlier run never judged has no movement to measure.
    """
    lines = [
        "### How much moves anyway\n",
        "Each arm's own scores, between the two runs. Where an arm's inputs barely changed,",
        "what moved is the draw and the judge, not the treatment.\n",
    ]
    rows = []
    for condition in [c for c in _conditions(by) if c in _conditions(baseline)]:
        moves = [
            abs(_mean(by, lesson, condition, d) - _mean(baseline, lesson, condition, d))
            for lesson in lessons
            for d in DIMENSIONS
        ]
        shifted = [m for m in moves if m]
        mean = sum(shifted) / len(shifted) if shifted else 0.0
        rows.append([condition, str(len(shifted)), str(len(moves)), f"{mean:.2f}"])
    header = ["arm", "scores that moved", "of", "mean size of a move"]
    return lines + _table(header, rows, numeric=True) + [""]


def _margin(by: dict, lesson: str, dimension: str) -> float:
    return _mean(by, lesson, TREATMENT, dimension) - _mean(by, lesson, BASELINE, dimension)


def _judgment(lesson: str, condition: str, judgments: list[dict], cids: list[str]) -> list[str]:
    lines = []
    for draw, (judgment, cid) in enumerate(zip(judgments, cids, strict=True), start=1):
        lines.append(f"### {lesson} — {condition}, draw {draw}  `{cid}`\n")
        for dimension in DIMENSIONS:
            entry = judgment[dimension]
            lines.append(f"**{LABELS[dimension]} — {entry['score']}/5**\n")
            lines += [f"- {item}" for item in entry.get("evidence", [])]
            lines.append(f"\n> {entry['rationale']}\n")
    return lines


def _notes_line(run_label: str) -> str:
    """Which notes the generation read, on the face of every rating.

    Both judged runs of 2026-08-11 were generated from the uncorrected transcription and
    no report said so — the setting lived in ``fingerprint.json`` as a SHA-256, which is
    unreadable on purpose. A rating that does not name its inputs invites the reader to
    assume the good ones.
    """
    run = json.loads((HERE / "runs" / run_label / "run.json").read_text())
    arm = run.get("arm")
    if not arm:
        return (
            "- **Notes.** NOT RECORDED — this run predates run.json carrying its arm. "
            "Read `fingerprint.json`: `arm.note_source` is sha256('raw') or sha256('clean')."
        )
    return f"- **Notes.** {describe_note_source(str(arm.get('note_source', '')))}"


def _preamble(run_label: str, data: dict, conditions: list[str]) -> list[str]:
    return [
        f"# Blinded rating — run `{run_label}`\n",
        "A manipulation check, not the study's endpoint: it asks whether the lesson-plan",
        f"information {TREATMENT} receives is *visible* to a reader who is given the "
        "teacher's plan and",
        f"one anonymous pack. It does not establish that {TREATMENT} is better; that is the expert",
        "raters' question.\n",
        _notes_line(run_label),
        f"- **Judge.** {data['judge_model']}",
        f"- **Judgments per candidate.** {data['judges_per_candidate']}",
        f"- **Generation draw.** {data['generation_draw']}",
        f"- **Arms judged.** {', '.join(conditions)}",
        f"- **Rubric.** the frozen H1 rubric, unchanged: {', '.join(LABELS.values())}\n",
        "Every judge saw one packet under an opaque id, with no mention of conditions, of",
        "lesson plans as a treatment, or that an experiment exists. Candidates were rated",
        "independently and every difference taken afterwards.\n",
        "---\n",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_label")
    parser.add_argument("--against", help="an earlier run's label, to show both C1-C0 margins")
    args = parser.parse_args()

    key, judged, data = _load(args.run_label)
    by = _scores(judged, key)
    by_id: dict[tuple[str, str], list[str]] = {}
    for cid in judged:
        row = key[cid]
        by_id.setdefault((row["lesson"], row["condition"]), []).append(cid)
    for cids in by_id.values():
        cids.sort(key=lambda cid: key[cid]["repeat"])
    lessons = sorted({lesson for lesson, _ in by})
    conditions = _conditions(by)

    lines = _preamble(args.run_label, data, conditions)
    lines += _endpoint(by, lessons)
    lines += _ladder(by, lessons, conditions)
    if len(by[(lessons[0], BASELINE)]) > 1:
        lines += _spread(by, lessons, conditions)
    if args.against:
        baseline_key, baseline_judged, _ = _load(args.against)
        lines += ["---\n"] + _against(
            by, _scores(baseline_judged, baseline_key), args.against, lessons
        )
    lines += ["---\n", "## Every judgment, with its evidence\n"]
    for lesson in lessons:
        for condition in conditions:
            cell = (lesson, condition)
            lines += _judgment(lesson, condition, by[cell], by_id[cell])

    out = HERE / "runs" / args.run_label / "rating" / "RATING-RESULTS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out} — {len(out.read_text()):,} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
