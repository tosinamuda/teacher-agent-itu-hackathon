r"""Lift the teacher's own drawings out of note prose into addressable blocks.

A note written in LaTeX carries its diagrams as ``tikzpicture`` source sitting inside
explanation text, worked-example steps and practice questions. Left there, a figure has
no identity: nothing can attach it to a pack, the ``fig-01`` the prose points at resolves
to nothing, and every consumer that wants readable text has to strip ``\draw`` commands
with its own regex.

This module gives each figure a block of its own — ``variant="diagram_tikz"``, carrying
the note's label and the teacher's description where she wrote one — so a reference has
something to resolve against and a renderer has something to render.
"""

from __future__ import annotations

import re
from typing import Any

from app.shared.tikz_figures import FIGURE

# The note's own caption line: "**fig-01.** Line AB, with a point P marked above it."
# It runs from the label to the blank line before the drawing.
_CAPTION = re.compile(r"\*\*(fig-\d+)\.\*\*[ \t]*(.*?)(?=\n[ \t]*\n|\Z)", re.DOTALL)
# Every text field a block can carry prose in.
_TEXT_FIELDS = ("content", "problem", "question", "answer", "final_answer")


def _captions(text: str) -> list[tuple[str, str]]:
    """Every ``fig-NN`` label in reading order, with the description that follows it."""
    return [(match.group(1), " ".join(match.group(2).split())) for match in _CAPTION.finditer(text)]


def _extract(text: str, block_id: str, start: int) -> tuple[str, list[dict[str, Any]]]:
    """Strip the drawings out of one text field and return them as visual blocks.

    Captions are matched to drawings by position: the note writes each label directly
    above the figure it names. Where a field has fewer labels than drawings — a worked
    example that just shows the shape — the extra figures carry no caption, and only a
    render can say what they show.
    """
    captions = _captions(text)
    figures: list[dict[str, Any]] = []
    for index, source in enumerate(FIGURE.findall(text)):
        label, caption = captions[index] if index < len(captions) else (None, None)
        figures.append(
            {
                "id": f"{block_id}-fig-{start + index + 1:02d}",
                "type": "visual",
                "variant": "diagram_tikz",
                "figure_ref": label,
                "caption": caption or None,
                "source_tikz": source,
            }
        )
    return FIGURE.sub("", text), figures


def _lift_block(block: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """One block, with its drawings removed and returned alongside it."""
    cleaned = dict(block)
    block_id = str(block.get("id") or "block")
    figures: list[dict[str, Any]] = []
    for field in _TEXT_FIELDS:
        value = block.get(field)
        if isinstance(value, str) and "tikzpicture" in value:
            cleaned[field], found = _extract(value, block_id, len(figures))
            figures.extend(found)
    steps = block.get("steps")
    if isinstance(steps, list):
        rebuilt = []
        for entry in steps:
            content = entry.get("content") if isinstance(entry, dict) else None
            if isinstance(content, str) and "tikzpicture" in content:
                text, found = _extract(content, block_id, len(figures))
                figures.extend(found)
                entry = {**entry, "content": text}
            rebuilt.append(entry)
        cleaned["steps"] = rebuilt
    return cleaned, figures


def figures_in_text(text: str, id_prefix: str) -> list[dict[str, Any]]:
    """Every drawing in a run of note prose, as addressable visual blocks.

    The block-level ``lift_figures`` serves plans that store their note parsed into
    blocks; this serves the verbatim per-step note, which is one string.
    """
    if "tikzpicture" not in text:
        return []
    _, figures = _extract(text, id_prefix, 0)
    return figures


def lift_figures(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Every block, with each drawing following the block it was written inside.

    Idempotent: blocks holding no ``tikzpicture`` source come back unchanged, so this can
    run over already-lifted plans.
    """
    lifted: list[dict[str, Any]] = []
    for block in blocks:
        if not isinstance(block, dict):
            lifted.append(block)
            continue
        cleaned, figures = _lift_block(block)
        lifted.append(cleaned)
        lifted.extend(figures)
    return lifted
