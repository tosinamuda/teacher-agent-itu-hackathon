"""Validate a harness-generated pack, and project it into the study's sections.

An agent writes prose into a file; nothing about that is checked by the model
that wrote it. So the file is validated on the way IN, before it is rendered or
judged. A pack that is short because its markup broke would otherwise score as a
bad pack rather than failing as a broken run — the same class of silent
degradation as a truncated generation, and the one this study can least absorb.

Two passes, as ``lesson_document`` does for lesson XML: the RELAX NG grammar
fixes shape, and the checks below cover what a grammar cannot see — that every
objective got a section, that the ids resolve, and that no answer was written
inside its own prompt.

    uv run python -m experiments.h1_condition_eval.sections_document \\
        validate <workspace>/sections.xml --curriculum <workspace>/inputs/curriculum.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lxml import etree

HERE = Path(__file__).parent
GRAMMAR = HERE / "dsh-harness" / "sections.rng"


class SectionsInvalid(SystemExit):
    """A pack that must not reach a rater."""


def _text(element: etree._Element | None) -> str:
    return "".join(map(str, element.itertext())).strip() if element is not None else ""


def _objective_ids(curriculum: Path) -> list[str]:
    payload = json.loads(curriculum.read_text())
    return [str(objective["id"]) for objective in payload.get("objectives") or []]


def shape_errors(tree: etree._ElementTree) -> list[str]:
    """What the grammar rejects, as readable lines."""
    grammar = etree.RelaxNG(etree.parse(str(GRAMMAR)))
    if grammar.validate(tree):
        return []
    return [f"line {error.line}: {error.message}" for error in grammar.error_log]


def content_errors(tree: etree._ElementTree, objectives: list[str]) -> list[str]:
    """What a grammar cannot see, and what the renderer or the study needs."""
    errors: list[str] = []
    sections = tree.getroot().findall("section")
    covered = [section.get("objective") or "" for section in sections]

    for objective in objectives:
        if objective not in covered:
            errors.append(f"objective {objective!r} has no section")
    for index, objective in enumerate(covered, start=1):
        if objective not in objectives:
            errors.append(f"section {index} names unknown objective {objective!r}")
    if len(covered) != len(set(covered)):
        errors.append("two sections claim the same objective")
    # The generator is asked for sections in objective order, and the renderer
    # emits them in file order, so a reordered file silently reorders the pack.
    if covered != [o for o in objectives if o in covered]:
        errors.append(f"sections are out of objective order: {covered} against {objectives}")

    for index, section in enumerate(sections, start=1):
        where = f"section {index} ({section.get('objective')})"
        if not _text(section.find("title")):
            errors.append(f"{where}: empty title")
        kinds = {block.get("type") for block in section.findall("block")}
        if "explanation" not in kinds:
            errors.append(f"{where}: no explanation block")
        if "worked_example" not in kinds:
            errors.append(f"{where}: no worked_example block")
        for position, item in enumerate(section.findall("practice"), start=1):
            prompt, answer = _text(item.find("prompt")), _text(item.find("answer"))
            if not prompt:
                errors.append(f"{where} practice {position}: empty prompt")
            if not answer:
                errors.append(f"{where} practice {position}: empty answer")
            # The separation the renderer depends on. An answer restated inside
            # its prompt defeats self-testing however the fields are filled in.
            if answer and answer in prompt:
                errors.append(f"{where} practice {position}: the answer is inside the prompt")
    return errors


def as_sections(tree: etree._ElementTree) -> list[dict[str, Any]]:
    """The pack in the shape ``rater_packets`` renders, so one renderer serves both arms."""
    out: list[dict[str, Any]] = []
    for section in tree.getroot().findall("section"):
        objective = section.get("objective") or ""
        blocks = [
            {
                "block_id": f"objective:{objective}:b{index}",
                "block_type": block.get("type"),
                "text": _text(block),
            }
            for index, block in enumerate(section.findall("block"))
        ]
        practice = [
            {
                "item_id": f"objective:{objective}:p{index}",
                "prompt": _text(item.find("prompt")),
                "answer": _text(item.find("answer")),
                "worked_solution": _text(item.find("worked-solution")),
            }
            for index, item in enumerate(section.findall("practice"), start=1)
        ]
        out.append(
            {
                "section_id": f"objective:{objective}",
                "lesson_objective_id": objective,
                "title": _text(section.find("title")),
                "blocks": blocks,
                "practice": practice,
            }
        )
    return out


def validate(path: Path, curriculum: Path) -> int:
    try:
        tree = etree.parse(str(path))
    except etree.XMLSyntaxError as error:
        raise SectionsInvalid(f"{path.name} is not well-formed XML: {error}") from error

    errors = shape_errors(tree) + content_errors(tree, _objective_ids(curriculum))
    if errors:
        for line in errors:
            print(f"  {line}")
        raise SectionsInvalid(f"{path.name}: {len(errors)} problem(s)")

    sections = as_sections(tree)
    practice = sum(len(section["practice"]) for section in sections)
    print(f"{path.name}: {len(sections)} sections, {practice} practice items, valid")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "project"))
    parser.add_argument("path", type=Path)
    parser.add_argument("--curriculum", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "project":
        print(json.dumps(as_sections(etree.parse(str(args.path))), indent=2))
        return 0
    return validate(args.path, args.curriculum)


if __name__ == "__main__":
    raise SystemExit(main())
