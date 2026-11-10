"""A revision material as a rater reads it — whole, or one section at a time.

Answers sit after the questions they belong to, never under them: a rater who reads
the answer beside the question cannot judge whether the practice tests anything.
"""

from __future__ import annotations

import re
from typing import Any

from experiments.h1_condition_eval.rater_packets import _numbered_here

from . import figures

Section = dict[str, Any]


def whole(sections: list[Section], *, level: int = 3) -> list[str]:
    """Every section in order, practice in place, all answers collected at the end."""
    lines: list[str] = []
    answers: list[str] = []
    for section in sections:
        lines += body(section, level=level)
        if section.get("practice"):
            answers += [f"**{section.get('title')}**", ""] + _answers(section) + [""]
    if answers:
        lines += [f"{'#' * level} Answers to the practice", ""] + answers
    return lines


def one(section: Section, *, level: int = 4) -> list[str]:
    """One section with its own practice and, after it, its own answers."""
    lines = body(section, level=level)
    if section.get("practice"):
        lines += [f"{'#' * (level + 1)} Answers", ""] + _answers(section) + [""]
    return lines


def _figure_number(block: dict[str, Any]) -> int:
    match = re.search(r"(\d+)", str(block.get("figure_ref") or ""))
    return int(match.group(1)) if match else 0


def in_figure_order(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A run of figures in the order the prose cites them.

    The packs store some runs descending — fig-07, fig-06, fig-05 — so a reader working
    through examples 1, 2 and 3 met the third drawing first. Only a consecutive run of
    figures is reordered, never across the prose between them, so a drawing cannot move
    away from the passage it belongs to.
    """
    ordered: list[dict[str, Any]] = []
    run: list[dict[str, Any]] = []
    for block in blocks:
        if (block.get("block_type") or "") == "visual":
            run.append(block)
            continue
        ordered += sorted(run, key=_figure_number)
        run = []
        ordered.append(block)
    return ordered + sorted(run, key=_figure_number)


def prose(section: Section, *, level: int) -> list[str]:
    """The section's title, what it says and what it draws — everything but the practice."""
    return [f"{'#' * level} {section.get('title')}", ""] + _content(section)


def _content(section: Section) -> list[str]:
    lines: list[str] = []
    for block in in_figure_order(section.get("blocks") or []):
        if text := (block.get("text") or "").strip():
            lines += [text, ""]
        elif caption := (block.get("caption") or "").strip():
            drawing = figures.png_for(block)
            label = block.get("figure_ref") or "Figure"
            if drawing:
                # No alt text: pandoc turns it into a second caption under the drawing.
                lines += [f"![]({drawing})", "", f"*{label}. {caption}*", ""]
            else:
                lines += [f"*[{label}: {caption}]*", ""]
    return lines


def practice(section: Section) -> list[str]:
    items = section.get("practice") or []
    if not items:
        return []
    return [
        "**Practice**",
        "",
        *(f"{i}. {_numbered_here(item.get('prompt'))}" for i, item in enumerate(items, 1)),
        "",
    ]


def parts(section: Section) -> list[list[str]]:
    """One section in the pieces a comparison sets against each other.

    Two materials rarely explain at the same length, so a single column of each drifts
    out of step and a rater hunting for the other one's practice reads down the page
    instead of across it. The named pieces are returned apart so they can be set in a
    row each.

    The title is set bold rather than as a heading: a Word heading keeps itself with the
    block that follows, and in a cell taller than the page that is left, the pair takes
    the whole table to the next page and leaves the one it was on empty.
    """
    answers = section.get("practice") and ["**Answers**", "", *_answers(section), ""]
    return [
        [f"**{section.get('title')}**", "", *_content(section)],
        practice(section),
        answers or [],
    ]


def body(section: Section, *, level: int) -> list[str]:
    return prose(section, level=level) + practice(section)


def _answers(section: Section) -> list[str]:
    lines = []
    for i, item in enumerate(section.get("practice") or [], start=1):
        lines.append(f"{i}. {_numbered_here(item.get('answer'), like=item.get('prompt'))}")
        if solution := (item.get("worked_solution") or "").strip():
            lines.append(f"   {solution}")
    return lines


def by_objective(sections: list[Section]) -> dict[str, list[Section]]:
    out: dict[str, list[Section]] = {}
    for section in sections:
        out.setdefault(str(section.get("lesson_objective_id") or ""), []).append(section)
    return out
