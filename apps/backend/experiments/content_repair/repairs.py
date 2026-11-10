"""Deterministic repairs — the mechanical fixes a ReAct agent can call as tools.

These mutate the step in place and return a short change-log string (good tool output).
They map 1:1 to the validators in this package so the experiment stays legible: the
LaTeX-row repair fixes exactly the missing-`\\` defect the validator flags, and the
figure embed reuses the production helper.
"""

from __future__ import annotations

import re
from typing import cast

from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    GroundedImage,
    build_grounded_figure_blocks,
)
from app.shared.json_types import JsonObject

from .validators import _ENV_ALT, block_list

_ENV_BLOCK = re.compile(r"\\begin\{(" + _ENV_ALT + r")\}(\{[^}]*\})?([\s\S]*?)\\end\{\1\}")


def repair_latex_rows(content: str) -> str:
    """Insert the missing `\\` row terminator before each inter-row `\\hline`.

    Leaves the leading top-border `\\hline` and already-terminated rows untouched.
    Idempotent; valid environments pass through unchanged. Generalised across all the
    tabular/aligned math environments, not just `array`.
    """

    def _fix(match: re.Match[str]) -> str:
        env, spec, body = match.group(1), match.group(2) or "", match.group(3)
        segments = re.split(r"\s*\\hline\s*", body)
        out = segments[0]
        for index in range(1, len(segments)):
            previous = segments[index - 1].strip()
            needs_terminator = previous != "" and not previous.endswith("\\\\")
            out += (" \\\\ \\hline " if needs_terminator else " \\hline ") + segments[index]
        return f"\\begin{{{env}}}{spec}{out}\\end{{{env}}}"

    return _ENV_BLOCK.sub(_fix, content)


def repair_step_latex(step: JsonObject) -> list[str]:
    """Repair LaTeX rows in the step's content + every block. Returns what changed."""
    changed: list[str] = []
    content = step.get("content")
    if isinstance(content, str):
        fixed = repair_latex_rows(content)
        if fixed != content:
            step["content"] = fixed
            changed.append("step content")
    for block in block_list(step):
        original = block.get("content")
        if isinstance(original, str):
            fixed = repair_latex_rows(original)
            if fixed != original:
                block["content"] = fixed
                changed.append(f"block {block.get('id')}")
    return changed


def embed_missing_figures(step: JsonObject, grounded_images: list[JsonObject]) -> list[str]:
    """Append grounded source figures the step hasn't embedded. Returns figure names."""
    blocks: list[JsonObject] = block_list(step)
    new_blocks = build_grounded_figure_blocks(
        blocks,
        grounded_images=cast(list[GroundedImage], grounded_images),
        step_id=str(step.get("step_id") or "step"),
    )
    blocks.extend(new_blocks)
    step["blocks"] = blocks
    return [str(block["url"]).rsplit("/", 1)[-1] for block in new_blocks]
