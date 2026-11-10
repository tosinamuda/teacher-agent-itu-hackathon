"""What Part 1's raters said about the material itself, not about one condition versus another.

Every comparison in this study asks whether one configuration beat another, and all of
them are null or nearly so. That answers "which is better" and leaves "is any of it any
good" untouched — a different question, and the one the third Part 1 criterion was
written for: *is mathematically correct, clear, and useful for learning*, scored 1 to 5
against published anchors where 4 means suitable for independent review and practice.

Two units, kept apart. A *rating* is one rater's judgement; a *section* is a
packet-objective-criterion that two raters judged. 93% of ratings at 4 or above is not
93% of sections, and a section where the raters split 3/5 is not the same evidence as one
where both said 5. Sections are reported by what both raters said, and every score of 2
or below is listed individually rather than averaged into a mean.

No threshold is proposed here. The anchors are the instrument's own; where a cut is drawn
is the reader's decision and must not be made after seeing which cut flatters the result.

Run with::

    uv run python -m experiments.human_rating.absolute_quality "<delivered folder>"
"""

from __future__ import annotations

import re
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from app.domains.evaluation.domain.study_instrument import H1_CRITERIA

from . import sources
from .results import h1_rows

COPY = re.compile(r"-c\d+$")
CONDITIONS = ("C0", "C1", "C2", "C3")
NAMES = {index: c.construct for index, c in enumerate(H1_CRITERIA, 1)}
#: The instrument's own wording for each point, abbreviated to its operative clause.
ANCHORS = {
    1: "not meaningfully addressed / unsuitable for learning",
    2: "major weaknesses; substantial revision needed",
    3: "generally sound and usable, noticeable weaknesses",
    4: "suitable for independent review and practice; minor improvements",
    5: "fully meets the criterion",
}


def ratings(folder: Path) -> list[dict[str, Any]]:
    rows = h1_rows(folder, sources.plans())
    for row in rows:
        row["packet"] = COPY.sub("", row["internal_packet_id"])
    return rows


def distribution(rows: list[dict[str, Any]], criterion: int) -> list[dict[str, Any]]:
    """Per condition, how the 1-5 scores fell for one criterion."""
    out = []
    for condition in CONDITIONS:
        scores = [
            r["score"] for r in rows if r["criterion"] == criterion and r["condition"] == condition
        ]
        counts = Counter(scores)
        total = len(scores)
        out.append(
            {
                "criterion": NAMES[criterion],
                "condition": condition,
                "ratings": total,
                **{f"scored_{n}": counts[n] for n in range(1, 6)},
                "share_1_2": (counts[1] + counts[2]) / total,
                "share_3": counts[3] / total,
                "share_4_5": (counts[4] + counts[5]) / total,
                "mean": st.mean(scores),
            }
        )
    return out


def sections(rows: list[dict[str, Any]], criterion: int) -> list[dict[str, Any]]:
    """Per condition, what the *pair* of raters said about each section.

    A section counts as agreed-suitable only when both raters placed it at 4 or above.
    Sections where the two disagree by two points or more are counted separately rather
    than resolved into an average: on this instrument that disagreement is the finding.
    """
    cells: dict[tuple[str, int], dict[str, int]] = defaultdict(dict)
    condition_of: dict[tuple[str, int], str] = {}
    for row in rows:
        if row["criterion"] != criterion:
            continue
        key = (row["packet"], row["objective_index"])
        cells[key][row["rater"]] = row["score"]
        condition_of[key] = row["condition"]
    out = []
    for condition in CONDITIONS:
        pairs = [
            sorted(v.values())
            for k, v in cells.items()
            if condition_of[k] == condition and len(v) == 2
        ]
        total = len(pairs) or 1
        out.append(
            {
                "criterion": NAMES[criterion],
                "condition": condition,
                "sections_rated_twice": len(pairs),
                "both_at_4_or_above": sum(1 for lo, hi in pairs if lo >= 4),
                "both_at_4_or_above_share": sum(1 for lo, hi in pairs if lo >= 4) / total,
                "either_at_2_or_below": sum(1 for lo, hi in pairs if lo <= 2),
                "split_by_2_or_more": sum(1 for lo, hi in pairs if hi - lo >= 2),
            }
        )
    return out


def by_lesson(rows: list[dict[str, Any]], criterion: int) -> list[dict[str, Any]]:
    """Whether a favourable overall picture hides a lesson that did badly."""
    out = []
    for lesson in sorted({r["lesson"] for r in rows}):
        scores = [r["score"] for r in rows if r["criterion"] == criterion and r["lesson"] == lesson]
        counts = Counter(scores)
        out.append(
            {
                "criterion": NAMES[criterion],
                "lesson": lesson,
                "ratings": len(scores),
                "share_4_5": (counts[4] + counts[5]) / len(scores),
                "share_1_2": (counts[1] + counts[2]) / len(scores),
                "mean": st.mean(scores),
            }
        )
    return out


def by_rater(rows: list[dict[str, Any]], criterion: int) -> list[dict[str, Any]]:
    """How much of a favourable picture is one rater's severity."""
    out = []
    for rater in sorted({r["rater"] for r in rows}):
        scores = [r["score"] for r in rows if r["criterion"] == criterion and r["rater"] == rater]
        counts = Counter(scores)
        out.append(
            {
                "criterion": NAMES[criterion],
                "rater": rater,
                "ratings": len(scores),
                "share_4_5": (counts[4] + counts[5]) / len(scores),
                "mean": st.mean(scores),
            }
        )
    return out


def low_scores(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Every rating at 2 or below, individually. Nothing here is averaged away.

    Each carries what the same rater gave the same section on the other two criteria.
    A 2 for lesson-context beside a 5 for instructional quality is coherent — accurate
    material that teaches a different method — and reads very differently from a 2 whose
    neighbours are also 2.
    """
    siblings: dict[tuple[str, str, int], dict[int, int]] = defaultdict(dict)
    for row in rows:
        siblings[(row["rater"], row["packet"], row["objective_index"])][row["criterion"]] = row[
            "score"
        ]
    return [
        {
            "criterion": NAMES[r["criterion"]],
            "condition": r["condition"],
            "lesson": r["lesson"],
            "draw": r["draw"],
            "packet": r["packet"],
            "objective_index": r["objective_index"],
            "rater": r["rater"],
            "score": r["score"],
            "same_rater_other_criteria": sorted(
                v
                for k, v in siblings[(r["rater"], r["packet"], r["objective_index"])].items()
                if k != r["criterion"]
            ),
            "comment": (r["comment"] or "").strip(),
        }
        for r in sorted(rows, key=lambda r: (r["score"], r["condition"], r["lesson"]))
        if r["score"] <= 2
    ]


def _table(title: str, rows: list[dict[str, Any]]) -> None:
    print(f"\n── {title} ──")
    if not rows:
        print("   (none)")
        return
    keys = [k for k in rows[0] if k != "criterion"]
    width = {k: max(len(k), *(len(_cell(r[k])) for r in rows)) for k in keys}
    print("   " + "  ".join(k.rjust(width[k]) for k in keys))
    for row in rows:
        print("   " + "  ".join(_cell(row[k]).rjust(width[k]) for k in keys))


def _cell(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.1%}" if 0 <= value <= 1 else f"{value:.2f}"
    return str(value)


def report(folder: Path) -> None:
    rows = ratings(folder)
    print(f"═══ {len(rows)} Part 1 ratings, read as levels rather than differences ═══")
    print("\nThe anchors these scores carry:")
    for score, meaning in ANCHORS.items():
        print(f"   {score}  {meaning}")
    for criterion in sorted(NAMES):
        print(f"\n\n╔═══ {criterion}. {NAMES[criterion]} ═══")
        _table("ratings, by condition", distribution(rows, criterion))
        _table("sections, by what BOTH raters said", sections(rows, criterion))
        _table("by lesson", by_lesson(rows, criterion))
        _table("by rater", by_rater(rows, criterion))
    low = low_scores(rows)
    print(f"\n\n═══ every rating at 2 or below: {len(low)} of {len(rows)} ═══")
    print("   `others` is what the same rater gave the same section on the other criteria.\n")
    for row in low:
        print(
            f"   score {row['score']}  {row['criterion']:30s} {row['condition']} "
            f"{row['lesson']} draw {row['draw']} obj {row['objective_index']} "
            f"{row['rater']}  others={row['same_rater_other_criteria']}"
        )
        print(f"      {row['comment'] or '(no comment)'}")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    report(Path(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
