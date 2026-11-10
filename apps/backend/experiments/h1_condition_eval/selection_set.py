"""The set a harness is chosen on, held out from the set H1a is measured on.

**Why it is synthetic.** The teacher captured six lessons and all six are in the frozen
eval set — `Dataset/transcripts` holds exactly `t2-w09`, `t3-w02`, `t3-w04`, `t3-w05`,
`t3-w06` and `t3-w09`, and the two folders marked "not-picked" are two of those same six.
There is no seventh lesson to hold out. Selecting a harness on any part of the frozen set
would tune the instrument on the data the preregistered endpoint is measured on, so the
selection set is built rather than sampled.

**What it is built to cover.** Not arbitrary lessons: the structural shapes the cohort
audit found in her real plans, which are the shapes a harness has to cope with.

| Selection lesson | shape it reproduces | seen in |
| --- | --- | --- |
| `sel-rich` | practice blocks on every core step | t2-w09 |
| `sel-noprac` | notes and worked examples, no practice block | t3-w02, t3-w04, t3-w09 |
| `sel-noeval` | no evaluation step at all | t3-w06 |
| `sel-drawn` | a TikZ figure inside the note | t3-w04, t3-w06 |

**The caveat, stated rather than buried.** A harness chosen here is chosen on constructed
lessons. It transfers to the study only insofar as these shapes are the ones that matter,
and that is an assumption the bake-off cannot test. What this set does guarantee is the
thing selection most needs: nothing chosen on it has seen the frozen data.

    uv run python -m experiments.h1_condition_eval.selection_set
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.domains.experiments.domain.types import ConditionCode

SELECTION_SET_PATH = Path(__file__).parent / "selection_set.json"

SCREENING_CONDITION = ConditionCode.C2
"""Screening happens at a GROUNDED condition, and this is not a detail.

Recall and invention are scored against the teacher's note, and C0 and C1 never receive it —
for those arms the numbers can only measure coincidence. A harness bake-off screened at C0
or C1 would be comparing harnesses on a metric that cannot see what they were given.
"""


def _step(
    step_id: str,
    objective_id: str,
    note: str,
    *,
    blocks: list[dict] | None = None,
    activities: list[dict] | None = None,
) -> dict:
    return {
        "step_id": step_id,
        "step_kind": "core",
        "lesson_objective_id": objective_id,
        "instructional_type": "explain_then_practise",
        "note": note,
        "blocks": blocks or [],
        "activities": activities
        or [
            {"who": "teacher", "what": "Explains the rule and works an example"},
            {"who": "student", "what": "Solves questions in their notes"},
        ],
    }


def _evaluation(objective_ids: list[str]) -> dict:
    return {
        "step_id": "sel-eval",
        "step_kind": "evaluation",
        "blocks": [
            {
                "type": "question",
                "lesson_objective_id": objective_id,
                "question": f"Check question for {objective_id}.",
            }
            for objective_id in objective_ids
        ],
    }


def _lesson(key: str, topic: str, steps: list[dict], *, evaluation: bool = True) -> dict:
    objectives = sorted({step["lesson_objective_id"] for step in steps})
    return {
        "plan_id": f"{key}-selection",
        "session_id": key,
        "subject": "Mathematics",
        "track": "core",
        "grade": "JSS1",
        "term": "Selection Term",
        "week": 1,
        "topic": topic,
        "subtopic": f"{topic}: selection-set construction",
        "theme": "Number and numeration",
        "entry_behaviour": ["Learners can add and multiply whole numbers."],
        "instructional_materials": ["Counters", "Number chart"],
        "references": ["Selection-set reference, chapter 1"],
        "lesson_plan_objectives": [
            {"lesson_objective_id": objective, "objective_text": f"Objective {objective}."}
            for objective in objectives
        ],
        "steps": [*steps, *([_evaluation(objectives)] if evaluation else [])],
    }


LESSONS: dict[str, dict] = {
    "sel-rich": _lesson(
        "sel-rich",
        "Multiples and factors",
        [
            _step(
                "sel-rich-01",
                "sel-rich-obj-1",
                "A multiple of a number is what you get when you multiply it by a whole "
                "number.\nExample: the multiples of 4 are 4, 8, 12, 16, 20, 24, 28.\n"
                "The multiples of 7 are 7, 14, 21, 28, 35, 42.\n"
                "28 appears in both lists, so 28 is a common multiple of 4 and 7.\n"
                "The lowest common multiple of 6 and 9 is 18, because the multiples of 6 "
                "are 6, 12, 18 and the multiples of 9 are 9, 18.",
                blocks=[
                    {"type": "explanation", "text": "Multiples come from multiplying."},
                    {"type": "practice", "question": "List the first four multiples of 6."},
                ],
            ),
            _step(
                "sel-rich-02",
                "sel-rich-obj-2",
                "A factor divides a number exactly.\nExample: the factors of 12 are 1, 2, 3, "
                "4, 6 and 12.\nThe factors of 18 are 1, 2, 3, 6, 9 and 18.\n"
                "The common factors of 12 and 18 are 1, 2, 3 and 6, so their highest "
                "common factor is 6.\n30 = 2 x 3 x 5, which is its prime factorisation.",
                blocks=[
                    {"type": "worked_example", "text": "12 = 3 x 4, so 3 and 4 are factors."},
                    {"type": "practice", "question": "List all the factors of 18."},
                ],
            ),
        ],
    ),
    "sel-noprac": _lesson(
        "sel-noprac",
        "Place value",
        [
            _step(
                "sel-noprac-01",
                "sel-noprac-obj-1",
                "Each digit has a value that depends on its position.\n"
                "In 4 528, the 5 stands for 5 hundreds, the 2 stands for 2 tens and the 8 "
                "stands for 8 units.\nIn 70 316 the 7 stands for 70 000 and the 3 stands "
                "for 300.\nThe value of 9 in 9 041 is 9 000.",
                blocks=[{"type": "explanation", "text": "Position decides value."}],
            ),
            _step(
                "sel-noprac-02",
                "sel-noprac-obj-2",
                "To write a number in expanded form, split it by place value.\n"
                "4 528 = 4000 + 500 + 20 + 8.\n70 316 = 70000 + 300 + 10 + 6.\n"
                "9 041 = 9000 + 40 + 1.\nAdding them back gives the original number, so "
                "4000 + 500 + 20 + 8 = 4528.",
                blocks=[{"type": "worked_example", "text": "4 528 = 4000 + 500 + 20 + 8."}],
            ),
        ],
    ),
    "sel-noeval": _lesson(
        "sel-noeval",
        "Rounding whole numbers",
        [
            _step(
                "sel-noeval-01",
                "sel-noeval-obj-1",
                "To round to the nearest ten, look at the units digit.\n"
                "47 rounds to 50 because 7 is 5 or more.\n"
                "23 rounds to 20, 85 rounds to 90 and 61 rounds to 60.\n"
                "To round 3 472 to the nearest hundred, look at the tens digit: 7 is 5 or "
                "more, so 3 472 rounds to 3 500.\n"
                "To the nearest thousand, 3 472 rounds to 3 000 because 4 is less than 5.",
                blocks=[{"type": "explanation", "text": "Look at the digit to the right."}],
            ),
        ],
        evaluation=False,
    ),
    "sel-drawn": _lesson(
        "sel-drawn",
        "Lines and angles",
        [
            _step(
                "sel-drawn-01",
                "sel-drawn-obj-1",
                "A right angle measures 90 degrees.\nA straight angle measures 180 "
                "degrees and a full turn measures 360 degrees.\nAn acute angle is less "
                "than 90 degrees, so 35 degrees and 72 degrees are acute.\nAn obtuse "
                "angle is between 90 and 180 degrees, so 115 degrees is obtuse.\n"
                "Two angles on a straight line add to 180, so if one is 55 the other is "
                "125.\n\n"
                "**fig-01.** Two lines meeting at a right angle, with the square mark shown.\n\n"
                "\\begin{center}\n\\begin{tikzpicture}\n  \\draw (0,0) -- (3,0);\n"
                "  \\draw (0,0) -- (0,3);\n  \\draw (0,0.3) -- (0.3,0.3) -- (0.3,0);\n"
                "\\end{tikzpicture}\n\\end{center}",
                blocks=[{"type": "explanation", "text": "A right angle is 90 degrees."}],
            ),
        ],
    ),
}


def freeze() -> dict[str, list[dict]]:
    """Pin each selection lesson with a content hash, as the eval set does."""
    return {
        "cases": [
            {
                "lesson": key,
                "plan_sha256": hashlib.sha256(
                    json.dumps(plan, sort_keys=True).encode()
                ).hexdigest()[:16],
                "plan": plan,
            }
            for key, plan in LESSONS.items()
        ]
    }


def frozen_eval_lessons() -> set[str]:
    """The lessons H1a is measured on. Selection must not touch any of them."""
    from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

    cases = json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))["cases"]
    return {case["lesson"] for case in cases}


def main() -> int:
    SELECTION_SET_PATH.write_text(json.dumps(freeze(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(LESSONS)} selection lessons to {SELECTION_SET_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
