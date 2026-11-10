"""Blind judge packets for a run that has the teacher's own note: three notes per step as A, B, C.

Run from ``apps/backend``::

    uv run python -m experiments.lesson_note_engine.judging <run> --judges 3

Each judge gets its own packet, with the three notes in a different random order per step, and
writes its verdicts as JSON. The keys that say which source wrote A, B and C stay in the run
folder, out of the packets' folder. ``--score`` unblinds the verdicts and prints the tally.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path

from app.shared.json_types import JsonObject

HERE = Path(__file__).parent
SOURCES = ("teacher", "current", "engine")
LABELS = ("A", "B", "C")
_HEADING = re.compile(r"\A####[^\n]*\n+")
#: A teacher's figure number, in a caption or a reference: "fig-06".
_FIG = re.compile(r"\bfig-(\d+)\b")

RUBRIC = """\
Score each note from 1 (poor) to 5 (excellent) on:

- correctness: the mathematics and facts are right.
- sequence: it teaches in the order explanation, example, solution, classwork, as the step needs.
- working: a solution shows its working line by line, in mathematical notation, with commentary
  tied to the working; commentary alone scores low. Score 3 when the step has nothing to work.
- states_content: it states the subject matter itself, as the class writes it down, rather than
  directing or narrating the lesson ("Ask students to…", "The teacher explains…").
- fit: it teaches this step's objective at this class's level, without padding or restating
  the objective.

Then rank the three notes from best to worst for a teacher to teach this step from, with no
ties, and guess which one the class teacher wrote by hand, with your confidence from 1 to 5.
"""

VERDICT_SHAPE = """\
{"judge": "<your model>", "items": [
  {"item": 1,
   "scores": {"A": {"correctness": 5, "sequence": 4, "working": 3, "states_content": 5, "fit": 4},
              "B": {...}, "C": {...}},
   "ranking": ["B", "A", "C"],
   "teacher_guess": "A", "teacher_confidence": 3,
   "reason": "one or two sentences"}
]}"""


def comparable(folder: Path) -> list[JsonObject]:
    """Every step that has a note from all three sources, with its lesson's context.

    A draft the engine could not finish has an empty note for each step. It is a failure to
    finish, counted where completion is measured, and there is no note to judge.
    """
    items: list[JsonObject] = []
    for path in sorted(folder.glob("LPV-*.json")):
        lesson = json.loads(path.read_text(encoding="utf-8"))
        notes = lesson["notes"]
        for step in lesson["steps"]:
            if all(notes.get(source, {}).get(step["step_id"]) for source in SOURCES):
                items.append(
                    {
                        "id": [lesson["plan_version_id"], step["step_id"]],
                        # A run paired with a control has the control's engine notes in the
                        # "current" slot, and they have no title heading to leave out.
                        "generator_heading": "paired_with" not in lesson,
                        "lesson": lesson["context"],
                        "step": step,
                        "notes": {source: notes[source][step["step_id"]] for source in SOURCES},
                    }
                )
    return items


def _note(source: str, text: str, *, generator_heading: bool) -> str:
    """A note as a judge reads it, with nothing that tells its source apart but the note.

    The current generator heads its note with the step title, which the reader has already.
    A teacher numbers figures through the lesson ("fig-06"), so they are numbered from 1 in
    each note, as the generated notes number theirs.
    """
    text = _HEADING.sub("", text, count=1) if source == "current" and generator_heading else text
    order = {number: index for index, number in enumerate(dict.fromkeys(_FIG.findall(text)), 1)}
    return _FIG.sub(lambda found: f"Figure {order[found.group(1)]}", text)


def _item_text(number: int, item: JsonObject, order: list[str]) -> str:
    step, lesson = item["step"], item["lesson"]
    activities = "\n".join(f"  - {a.get('who')}: {a.get('what')}" for a in step["activities"])
    lines = [
        f"## Item {number}",
        f"Lesson: {lesson['subject']}, {lesson['grade']}, {lesson['topic']}",
        f"Step: {step['title']} ({step['kind']})",
        f"Objective: {step['objective'] or '(none for this step)'}",
        f"What happens in class, from the plan:\n{activities or '  (not stated)'}",
    ]
    for label, source in zip(LABELS, order, strict=True):
        note = _note(
            source, item["notes"][source], generator_heading=bool(item["generator_heading"])
        )
        lines.append(f"### Note {label}\n\n{note}")
    return "\n\n".join(lines)


def write_packets(run: str, judges: int, seed: int) -> None:
    folder = HERE / "runs" / run
    items = comparable(folder)
    packets = folder / "judging"
    packets.mkdir(exist_ok=True)
    keys: JsonObject = {}
    for judge in range(1, judges + 1):
        order = random.Random(seed + judge)
        key: JsonObject = {}
        blocks = [
            f"# Lesson note review, packet {judge}\n\n{RUBRIC}\nReply shape:\n\n{VERDICT_SHAPE}"
        ]
        for number, item in enumerate(items, start=1):
            shuffled = order.sample(list(SOURCES), k=3)
            key[str(number)] = dict(zip(LABELS, shuffled, strict=True))
            blocks.append(_item_text(number, item, shuffled))
        (packets / f"packet-{judge}.md").write_text("\n\n---\n\n".join(blocks), encoding="utf-8")
        keys[str(judge)] = key
    (folder / "judging-keys.json").write_text(json.dumps(keys, indent=1))
    print(f"{len(items)} items in {judges} packets under {packets}")


def score(run: str) -> None:
    """Unblind every verdict file and print each source's mean scores, ranks and detection."""
    folder = HERE / "runs" / run
    keys = json.loads((folder / "judging-keys.json").read_text())
    totals: dict[str, Counter[str]] = {source: Counter() for source in SOURCES}
    firsts: Counter[str] = Counter()
    found = guesses = 0
    for path in sorted((folder / "judging").glob("verdict-*.json")):
        judge = path.stem.split("-")[1]
        for verdict in json.loads(path.read_text())["items"]:
            key = keys[judge][str(verdict["item"])]
            for label, marks in verdict["scores"].items():
                totals[key[label]].update(marks)
                totals[key[label]]["n"] += 1
            for place, label in enumerate(verdict["ranking"], start=1):
                totals[key[label]]["rank"] += place
            firsts[key[verdict["ranking"][0]]] += 1
            guesses += 1
            found += key[verdict["teacher_guess"]] == "teacher"
    for source in SOURCES:
        count = totals[source].pop("n") or 1
        means = {name: round(value / count, 2) for name, value in sorted(totals[source].items())}
        print(source, means, "ranked first", firsts[source])
    print(f"the teacher's note found {found} of {guesses} times")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run")
    parser.add_argument("--judges", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260926)
    parser.add_argument("--score", action="store_true", help="Unblind the verdicts and tally them")
    arguments = parser.parse_args()
    if arguments.score:
        score(arguments.run)
    else:
        write_packets(arguments.run, arguments.judges, arguments.seed)
