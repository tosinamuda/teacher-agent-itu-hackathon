"""Draft a canonical document for a frozen lesson, from her note's own headings.

The regions come from the note, not from the plan's blocks: the document describes her
file, and ``lesson_plan_projection diff`` then reports wherever the frozen blocks
disagree with that description. That is the point of running it — a disagreement is a
finding about the transcription, not a bug in the draft.

A draft is a starting point to be READ. Roles are proposed by rule and every proposal is
printed, because ``role`` is the one field a reader has to confirm.

Nothing of her prose is written into the XML; the tool refuses to emit a document that
carries any, so a mistake here cannot quietly become a fifth copy.

    uv run python -m experiments.h1_condition_eval.lesson_migration draft t3-w09
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from lxml import etree

from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.lesson_document import heading_sets_work, read_headings
from experiments.h1_condition_eval.note_editorial import note_path

HERE = Path(__file__).parent
LESSONS = HERE / "lessons"


HEADER = """<?xml version="1.0" encoding="utf-8"?>
<!--
  A canonical lesson. Structure is declared here; her prose lives in notes-clean/ and is
  referenced, never copied. A <section> addresses a region of that file by the heading
  the note itself carries, so there is exactly one copy of every sentence she wrote and
  the surfaces select rather than parse.

  Hand-edit this file. Only `lesson_migration draft` with its force flag overwrites
  it, and a double hyphen cannot be written in here to say so.
-->
"""


def _readable(root: etree._Element) -> str:
    """Serialised so a person can edit it: one attribute per line on the root, and a
    blank line before each top-level element."""
    body = str(etree.tostring(root, encoding="unicode", pretty_print=True))
    opening = body[: body.index(">") + 1]
    name, *attributes = re.findall(r'\S+?="[^"]*"|^<\w+', opening)
    wrapped = f"{name}\n" + "\n".join(f"        {a}" for a in attributes) + ">"
    body = wrapped + body[body.index(">") + 1 :]
    for tag in ("curriculum", "objectives", "entry-behaviour", "materials", "references", "step"):
        body = body.replace(f"\n  <{tag}", f"\n\n  <{tag}")
    return HEADER + body


def _headings(text: str) -> list[str | None]:
    """Every heading she wrote, in order, with None first when text precedes them.

    A heading is a line starting with hashes; its text is that line with the hashes
    taken off. Compared as text, the way ``lesson_document`` resolves the same lines,
    so the draft and the loader cannot disagree about where a region begins.
    """
    found: list[str | None] = []
    preamble = False
    for _, line in _lines(text):
        if line.startswith("#"):
            found.append(line.lstrip("#").strip())
        elif not found and line.strip():
            preamble = True
    if not found:
        return [None]
    return ([None] if preamble else []) + found


def _role(heading: str | None, step: dict[str, Any]) -> str:
    """Proposed, never decided. Printed for a reader to confirm or overrule."""
    if step["step_kind"] != "core":
        return "recall"
    if heading and heading_sets_work(heading):
        return "set-work"
    worked = {
        str(block.get("problem") or "")
        for block in step.get("blocks") or []
        if block.get("type") == "worked_example"
    }
    if heading and heading[len(_enumerator(heading)) :].strip() in worked:
        return "worked-example"
    return "explanation"


def _enumerator(heading: str) -> str:
    """The enumerator her heading carries, read from ``note_headings.json``."""
    return str(read_headings().get(heading, {}).get("enumerator") or "")


def _final_answer(body: str) -> str:
    """The one answer this example reaches. Proposed; the reader confirms.

    An example whose working is split into lettered parts reaches one answer per part,
    so the last line is only the last part's and nothing is proposed.
    """
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    lettered = [line for line in lines if line.startswith(("(a)", "(b)", "(c)"))]
    return "" if len(lettered) > 2 else (lines[-1] if lines else "")


def _solution_marker(body: str) -> str:
    """Her answer marker in this region, verbatim. Proposed; the reader confirms."""
    found = [line.strip() for line in body.splitlines() if line.strip("*:. ") == "Solution"]
    return found[0] if len(found) == 1 else ""


def _append_items(parent: etree._Element, tag: str, values: list[str]) -> None:
    if not values:
        return
    holder = etree.SubElement(parent, tag)
    for value in values:
        etree.SubElement(holder, "item").text = value


def _note_element(step: dict[str, Any], lesson: str, proposals: list[str]) -> etree._Element:
    path = note_path(lesson, step["step_id"])
    text = path.read_text(encoding="utf-8")
    note = etree.Element("note")
    note.set("src", f"../notes-clean/{lesson}/{step['step_id']}.md")
    note.set("sha256", hashlib.sha256(text.encode("utf-8")).hexdigest())
    for index, heading in enumerate(_headings(text), start=1):
        section = etree.SubElement(note, "section")
        section.set("id", f"b{index}")
        role = _role(heading, step)
        section.set("role", role)
        if heading:
            section.set("heading", heading)
            if enumerator := _enumerator(heading):
                section.set("enumerator", enumerator)
        if role == "worked-example":
            region = _region(text, heading)
            if marker := _solution_marker(region):
                section.set("solution", marker)
            if answer := _final_answer(region):
                section.set("final-answer", answer)
        if step["step_kind"] != "core":
            section.set("delivered", "false")
        proposals.append(f"    {step['step_id']}:b{index}  {role:<15} {heading or '(no heading)'}")
        for label in _figure_labels(text, heading):
            figure = etree.SubElement(section, "figure")
            if label is not None:
                figure.set("ref", label)
    return note


def _region(text: str, heading: str | None) -> str:
    """The slice of the note this heading owns, for proposing what is inside it."""
    headings = _headings(text)
    bounds = _bounds(text, headings)
    position = headings.index(heading)
    stop = bounds[position + 1] if position + 1 < len(bounds) else len(text)
    return text[bounds[position] : stop]


def _bounds(text: str, headings: list[str | None]) -> list[int]:
    starts = []
    for name in headings:
        if name is None:
            starts.append(0)
            continue
        starts.append(
            next(
                offset
                for offset, line in _lines(text)
                if line.startswith("#") and line.lstrip("#").strip() == name
            )
        )
    return starts


def _lines(text: str) -> Iterator[tuple[int, str]]:
    offset = 0
    for line in text.splitlines(keepends=True):
        yield offset, line.rstrip("\n")
        offset += len(line)


def _figure_labels(text: str, heading: str | None) -> list[str | None]:
    """One entry per drawing in this region: her label for it, or None if she wrote none.

    Paired by position within the region. ``note_figures`` pairs across the whole note,
    which agrees here only because every lesson in the corpus is all-labelled or
    none-labelled; per region is the model the document actually means.
    """
    region = _region(text, heading)
    labels = [
        line.split("**")[1].rstrip(".") for _, line in _lines(region) if line.startswith("**fig-")
    ]
    drawings = sum(
        1 for _, line in _lines(region) if line.strip().startswith(r"\begin{tikzpicture}")
    )
    return [labels[i] if i < len(labels) else None for i in range(drawings)]


def _step_element(step: dict[str, Any], lesson: str, proposals: list[str]) -> etree._Element:
    element = etree.Element("step")
    element.set("id", step["step_id"])
    element.set("kind", step["step_kind"])
    if step.get("lesson_objective_id"):
        element.set("objective", step["lesson_objective_id"])
    if step.get("estimated_minutes") is not None:
        element.set("minutes", str(step["estimated_minutes"]))
    if step.get("title"):
        element.set("title", step["title"])
    if step.get("instructional_type"):
        element.set("instructional-type", step["instructional_type"])
    if step.get("content"):
        etree.SubElement(element, "plan-content").text = step["content"]
    if activities := step.get("activities") or []:
        holder = etree.SubElement(element, "activities")
        for activity in activities:
            child = etree.SubElement(holder, "activity")
            child.set("who", str(activity.get("who") or ""))
            if activity.get("sets_work") is not None:
                child.set("sets-work", "true" if activity["sets_work"] else "false")
            child.text = str(activity.get("what") or "")
    if step.get("note_file"):
        element.append(_note_element(step, lesson, proposals))
    questions = [
        block
        for block in step.get("blocks") or []
        if step["step_kind"] == "evaluation" and block.get("question")
    ]
    if questions:
        holder = etree.SubElement(element, "questions")
        for index, block in enumerate(questions, start=1):
            child = etree.SubElement(holder, "question")
            child.set("id", f"q{index}")
            if block.get("lesson_objective_id"):
                child.set("objective", block["lesson_objective_id"])
            child.text = block["question"]
    return element


def draft(lesson: str, *, force: bool = False) -> int:
    plan = next(
        case["plan"]
        for case in json.loads(EVAL_SET_PATH.read_text())["cases"]
        if case["lesson"] == lesson
    )
    root = etree.Element("lesson")
    for key, value in (
        ("id", lesson),
        ("plan-id", plan["plan_id"]),
        ("session-id", plan["session_id"]),
        ("subject", plan["subject"]),
        ("track", plan["track"]),
        ("grade", plan["grade"]),
        ("term", plan["term"]),
        ("week", str(plan["week"])),
        ("topic", plan["topic"]),
        ("subtopic", plan["subtopic"]),
    ):
        root.set(key, str(value))
    curriculum = etree.SubElement(root, "curriculum")
    for objective in plan["curriculum_objectives"]:
        child = etree.SubElement(curriculum, "objective")
        child.set("id", objective["curriculum_objective_id"])
        child.text = objective["objective_text"]
    objectives = etree.SubElement(root, "objectives")
    for objective in plan["lesson_plan_objectives"]:
        child = etree.SubElement(objectives, "objective")
        child.set("id", objective["lesson_objective_id"])
        child.set("curriculum", objective["curriculum_objective_id"])
        if objective.get("kc_type"):
            child.set("kc-type", objective["kc_type"])
        child.text = objective["objective_text"]
    _append_items(root, "entry-behaviour", [i for i in plan.get("entry_behaviour") or [] if i])
    _append_items(root, "materials", [i for i in plan.get("instructional_materials") or [] if i])
    _append_items(root, "references", [i for i in plan.get("references") or [] if i])

    proposals: list[str] = []
    for step in plan["steps"]:
        root.append(_step_element(step, lesson, proposals))

    out = LESSONS / f"{lesson}.xml"
    if out.exists() and not force:
        raise SystemExit(f"{out.name} exists — hand edits are the point. Pass --force to redraft.")
    etree.indent(root, space="  ")
    out.write_text(_readable(root), encoding="utf-8")
    _refuse_prose(out, plan)
    print(f"drafted {out.relative_to(HERE)} — roles PROPOSED, read them:")
    print("\n".join(proposals))
    return 0


def _refuse_prose(path: Path, plan: dict[str, Any]) -> None:
    """No sentence of her note may have landed in the document."""
    written = path.read_text(encoding="utf-8")
    for step in plan["steps"]:
        for line in (step.get("note") or "").splitlines():
            stripped = line.strip()
            if len(stripped) > 40 and "#" not in stripped and stripped in written:
                path.unlink()
                raise SystemExit(f"{path.name}: carries note prose — {stripped[:60]!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("draft",))
    parser.add_argument("lesson")
    parser.add_argument("--force", action="store_true", help="redraft over an edited file")
    args = parser.parse_args()
    return draft(args.lesson, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
