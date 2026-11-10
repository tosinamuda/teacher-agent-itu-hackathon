"""Deterministic fidelity/invention proxies, scored against the teacher's note.

One rater per lesson at n=5 moves the same arm by 0.4 between runs, which is
wider than every arm difference measured so far. These score every cell without
a rater, so an arm can be compared on all runs at once rather than on the five
a rating round covered.

A note's quantities are what a pack must carry through: its worked examples,
measurements and answers are all numeric. So:

    recall    — the note's quantities that reach the pack (did it teach them)
    invention — the pack's quantities absent from the note (did it make them up)

Both are proxies. Recall is bounded above by what a pack SHOULD carry (a pack
need not repeat every number), so compare it between arms on one lesson, never
read it as an absolute score.

NEITHER MEANS ANYTHING FOR A CONDITION THAT NEVER RECEIVES THE NOTE. C0 and C1
are generated without it, so "the note's quantities that reach the pack" can
only measure coincidence, and single digits coincide with everything: on
`t3-w05` a C1 pack scored 0.412 whose every match was a one-digit number, while
missing 48, 27, 75 and 7.5 — the answers to all four of her worked examples.
Use these to compare C2/C3 arms, and as a dud screen anywhere. Use a rater to
compare C0 with C1.

Read them against run-to-run spread, never as a single figure. Re-running the
SAME condition on unchanged data moved recall by a median of 0.094 across four
runs (t3-w09: 0.182) — wider than almost every arm difference ever measured
with it, so a k=3 median cannot resolve differences of that size.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# TikZ coordinates are drawing source, not taught quantities: "(2.4,0)" is a
# line's endpoint, and counting it would score packs on geometry they never see.
_TIKZ_BLOCK = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
# A figure's own label is a name, not a taught quantity. "fig-01" put "01", "02" and "03"
# into t3-w05's note quantities, so a pack was scored on whether it reproduced the
# transcription's figure numbering.
_FIGURE_LABEL = re.compile(r"\bfig-\d+", re.IGNORECASE)
_QUANTITY = re.compile(r"\d+(?:[.,]\d+)?")


def quantities(text: str) -> set[str]:
    """Every quantity a reader would see: drawing source and figure labels excluded."""
    prose = _FIGURE_LABEL.sub(" ", _TIKZ_BLOCK.sub(" ", text))
    return {match.group(0).rstrip(".,").replace(",", "") for match in _QUANTITY.finditer(prose)}


def pack_text(sections: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for section in sections:
        parts.append(section.get("title") or "")
        for block in section.get("blocks") or []:
            parts.extend([block.get("text") or "", block.get("caption") or ""])
    return "\n".join(part for part in parts if part)


def score(note: str, sections: list[dict[str, Any]]) -> dict[str, float | int]:
    """Recall of the note's quantities, and how much of the pack is not in it."""
    source = quantities(note)
    written = quantities(pack_text(sections))
    if not source:
        return {"note_quantities": 0, "recall": 0.0, "invention": 0.0}
    carried = source & written
    invented = written - source
    return {
        "note_quantities": len(source),
        "recall": round(len(carried) / len(source), 3),
        "invention": round(len(invented) / len(written), 3) if written else 0.0,
    }


def notes_by_lesson(eval_set: Path) -> dict[str, str]:
    """Each lesson's whole note — the reference every arm is scored against."""
    cases = json.loads(eval_set.read_text())["cases"]
    return {
        case["lesson"]: "\n\n".join(
            step["note"] for step in case["plan"]["steps"] if step.get("note")
        )
        for case in cases
    }


def main() -> int:
    """Score every recorded run, so arms compare without a new rating round."""
    runs_dir = Path(__file__).parent / "runs"
    notes = notes_by_lesson(Path(__file__).parent / "eval_set.json")
    rows: list[dict[str, Any]] = []
    for run_path in sorted(runs_dir.glob("*/run.json")):
        for case in json.loads(run_path.read_text()).get("cases", []):
            if not case.get("sections_json"):
                continue
            result = score(notes.get(case["lesson"], ""), case["sections_json"])
            rows.append(
                {
                    "run": run_path.parent.name,
                    "arm": f"{case.get('generator', '?')}/{case.get('signatures', 'shared')}",
                    "condition": case["condition"],
                    **result,
                }
            )
    by_arm: dict[tuple[str, str], list[float]] = {}
    for row in rows:
        by_arm.setdefault((row["arm"], row["condition"]), []).append(row["recall"])
    print(f"{'arm':28s} {'cond':5s} {'cells':>5s} {'recall':>7s}")
    print("-" * 50)
    for (arm, condition), values in sorted(by_arm.items()):
        print(f"{arm:28s} {condition:5s} {len(values):5d} {sum(values) / len(values):7.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
