#!/usr/bin/env python3
"""Check `sections.xml` against the contract, from inside the agent's workspace.

Copied into the workspace beside the task so the agent can check its own output
and fix it before finishing. Deliberately standalone: the standard library only,
no imports from this repository and no lxml, so the workspace stays isolated and
the check cannot fail for reasons that have nothing to do with the pack.

This is the agent's own check, not the gate. `sections_document.py` validates
again on ingest, against the RELAX NG grammar, and that one is authoritative —
an agent that skips or misreads this must still not get a bad pack to a rater.

    python3 check_sections.py            # sections.xml against inputs/curriculum.json
    python3 check_sections.py <xml> <curriculum.json>
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

BLOCK_TYPES = {"explanation", "worked_example"}
#: What may appear inside each element. The grammar on ingest enforces this, and
#: this checker did not: a pack that nested <prompt> inside a <block> instead of a
#: <practice> passed here and was refused there, because a loop over `practice`
#: cannot see a prompt that is somewhere else. An agent told OK by its own gate
#: and rejected by the real one has no way to repair itself.
ALLOWED_CHILDREN = {
    "sections": {"section"},
    "section": {"title", "block", "practice"},
    "block": set(),
    "practice": {"prompt", "answer", "worked-solution"},
}


def text_of(element: ET.Element | None) -> str:
    return "".join(element.itertext()).strip() if element is not None else ""


def misplaced(root: ET.Element) -> list[str]:
    """Elements sitting under a parent that does not take them.

    Named with the parent, because "did not expect <prompt> here" is only
    actionable if you know where "here" was.
    """
    found: list[str] = []
    for parent in root.iter():
        allowed = ALLOWED_CHILDREN.get(parent.tag)
        if allowed is None:
            continue
        for child in parent:
            if child.tag not in allowed:
                where = f"<{parent.tag}>" + (
                    f' type="{parent.get("type")}"' if parent.get("type") else ""
                )
                found.append(
                    f"<{child.tag}> cannot go inside {where}"
                    + (
                        " — a question and its answer belong in <practice>"
                        if child.tag in {"prompt", "answer", "worked-solution"}
                        else ""
                    )
                )
    return found


def problems(xml_path: Path, curriculum_path: Path) -> list[str]:
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as error:
        # By far the most likely cause, and the one worth naming: `<` and `&` are
        # the only characters XML reserves. Backslashes are ordinary here.
        return [
            f"{xml_path.name} is not well-formed XML: {error}",
            "  a bare '<' or '&' in the text is the usual cause — write &lt; and &amp;",
        ]

    if root.tag != "sections":
        return [f"root element is <{root.tag}>, expected <sections>"]

    objectives = [str(o["id"]) for o in json.loads(curriculum_path.read_text())["objectives"]]
    sections = root.findall("section")
    found: list[str] = []
    out: list[str] = []

    out += misplaced(root)

    for index, section in enumerate(sections, start=1):
        objective = section.get("objective")
        where = f"section {index}"
        if not objective:
            out.append(f"{where}: no objective attribute")
        else:
            found.append(objective)
            if objective not in objectives:
                out.append(f"{where}: objective {objective!r} is not in the curriculum")
        if not text_of(section.find("title")):
            out.append(f"{where}: empty or missing <title>")

        kinds = [block.get("type") for block in section.findall("block")]
        for kind in kinds:
            if kind not in BLOCK_TYPES:
                out.append(f"{where}: block type {kind!r} — use one of {sorted(BLOCK_TYPES)}")
        if "explanation" not in kinds:
            out.append(f'{where}: needs at least one <block type="explanation">')
        if "worked_example" not in kinds:
            out.append(f'{where}: needs at least one <block type="worked_example">')

        for position, item in enumerate(section.findall("practice"), start=1):
            prompt, answer = text_of(item.find("prompt")), text_of(item.find("answer"))
            if not prompt:
                out.append(f"{where} practice {position}: empty or missing <prompt>")
            if not answer:
                out.append(f"{where} practice {position}: empty or missing <answer>")
            if answer and answer in prompt:
                out.append(
                    f"{where} practice {position}: the answer appears inside the prompt — "
                    "keep them separate so the learner can attempt the question first"
                )

    for objective in objectives:
        if objective not in found:
            out.append(f"objective {objective!r} has no section")
    if len(found) != len(set(found)):
        out.append("two sections claim the same objective")
    ordered = [o for o in objectives if o in found]
    if found != ordered:
        out.append(f"sections are out of objective order: {found}, expected {ordered}")
    return out


def main() -> int:
    xml_path = Path(sys.argv[1] if len(sys.argv) > 1 else "sections.xml")
    curriculum = Path(sys.argv[2] if len(sys.argv) > 2 else "inputs/curriculum.json")
    if not xml_path.exists():
        print(f"{xml_path} does not exist yet")
        return 1

    found = problems(xml_path, curriculum)
    if found:
        print(f"{len(found)} problem(s):")
        for line in found:
            print(f"  {line}")
        return 1

    root = ET.parse(xml_path).getroot()
    sections = root.findall("section")
    practice = sum(len(s.findall("practice")) for s in sections)
    print(f"OK — {len(sections)} sections, {practice} practice items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
