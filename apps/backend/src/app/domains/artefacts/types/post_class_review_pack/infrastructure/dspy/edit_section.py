"""Revise a section the way a coding agent revises code: a file, tools, anchors.

The blind patch path hands a model the whole section object and quoted
complaints, and trusts it to retype everything else unchanged — which is how
repair collateral happens. Here the section is materialised as a FILE the
learner-view way, findings become line-anchored review comments, and the
reviser is an agent with two tools: read numbered lines, and a unique-match
string replacement. The edit contract makes out-of-span damage unrepresentable
instead of detectable: an edit applies only where its old text occurs exactly
once, and text blocks map back to their own blocks by invisible markers.
"""

from __future__ import annotations

import re
from collections.abc import Callable

import dspy

from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.infra.dspy_agent_loop import run_agent_loop, termination_of, trajectory_of

from .contracts.edit_section import ResolveSectionFindings
from .prompt_fingerprint import record_prompt
from .tracing import record

# Invisible block anchors: present in the working file so edits map back to the
# block they were made in, stripped from anything a learner or rater sees.
_MARKER = re.compile(r"^<!-- block:(?P<block_id>\S+) -->$", re.MULTILINE)
DEFAULT_EDITING_LOOP: Callable[..., dspy.Module] = dspy.ReActV2


def section_to_file(section: ReviewPackSection) -> str:
    """The section as an editable file: learner-view text under block markers."""
    lines: list[str] = [f"# {section.title}", ""]
    for block in section.blocks:
        lines.append(f"<!-- block:{block.block_id} -->")
        if block.block_type == "visual":
            label = block.figure_ref or "figure"
            lines.append(f"[figure {label}: {block.caption or ''}]".rstrip())
        else:
            lines.append(block.text or "")
        lines.append("")
    for item in section.practice:
        lines.append(f"<!-- practice:{item.item_id} -->")
        lines.append(item.prompt)
        lines.append(f"<!-- answer:{item.item_id} -->")
        lines.append(item.answer)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def file_to_section(text: str, original: ReviewPackSection) -> ReviewPackSection:
    """Map the edited file back onto the section's blocks.

    Only prose blocks accept edits; a visual block's region renders from its
    caption, so its region is ignored on the way back and the figure rides
    through untouched. A block whose marker was deleted keeps its original
    text — losing an anchor must never lose content.
    """
    regions: dict[str, str] = {}
    matches = list(_MARKER.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        regions[match.group("block_id")] = text[start:end].strip()
    revised = original.model_copy(deep=True)
    title = text.lstrip().split("\n", 1)[0]
    if title.startswith("# ") and title[2:].strip():
        revised.title = title[2:].strip()
    for block in revised.blocks:
        if block.block_type == "visual":
            continue
        if block.block_id in regions:
            block.text = regions[block.block_id]
    return revised


def locate(text: str, quote: str) -> int | None:
    """1-indexed line where a finding's quote starts, or None."""
    position = text.find(quote.strip())
    if position < 0:
        return None
    return text.count("\n", 0, position) + 1


def editing_tools(buffer: dict[str, str]) -> list:
    def read_lines(start_line: int = 1, end_line: int | None = None) -> str:
        """Read the section file as numbered lines (1-indexed, inclusive)."""
        lines = buffer["text"].splitlines()
        end = len(lines) if end_line is None else min(end_line, len(lines))
        return "\n".join(
            f"{index}: {line}"
            for index, line in enumerate(
                lines[max(start_line, 1) - 1 : end], start=max(start_line, 1)
            )
        )

    def edit(old_text: str, new_text: str) -> str:
        """Replace old_text with new_text. old_text must occur EXACTLY once."""
        count = buffer["text"].count(old_text)
        if count == 0:
            return "No match — copy old_text exactly from read_lines (without the line numbers)."
        if count > 1:
            return f"{count} matches — include more surrounding text so old_text is unique."
        if "<!-- block:" in old_text or "[figure" in old_text.split("\n", 1)[0]:
            return "Refused: marker and figure lines must not be edited."
        buffer["text"] = buffer["text"].replace(old_text, new_text, 1)
        return "Edited."

    return [read_lines, edit]


class EditSection(dspy.Module):
    """Apply critic findings through anchored edits to one section."""

    def __init__(
        self,
        *,
        lm: dspy.BaseLM,
        max_iters: int = 10,
        loop: Callable[..., dspy.Module] = DEFAULT_EDITING_LOOP,
    ) -> None:
        super().__init__()
        self.lm = lm
        self.max_iters = max_iters
        # Prompt-parsed ``ReAct`` asks for each turn as text and gpt-oss answers a long
        # editing loop in prose or as concatenated JSON objects, which the adapter cannot
        # read: 5 of 25 span-local repairs died that way. ``ReActV2`` puts the turn in a
        # tool_calls field instead, so there is no text field to pollute.
        self.loop = loop

    async def aforward(
        self, *, section: ReviewPackSection, findings: list[str]
    ) -> ReviewPackSection:
        buffer = {"text": section_to_file(section)}
        anchored = []
        for finding in findings:
            quote_match = re.search(r'"([^"]+)"', finding)
            line = locate(buffer["text"], quote_match.group(1)) if quote_match else None
            anchored.append(f"line {line}: {finding}" if line else finding)
        agent = self.loop(
            ResolveSectionFindings,
            tools=editing_tools(buffer),
            max_iters=self.max_iters,
        )
        record_prompt("section_editing", ResolveSectionFindings)
        # ``run_agent_loop`` threads a sync-only loop; calling ``acall`` directly raises
        # AttributeError on ReActV2, which has no ``aforward``.
        result = await run_agent_loop(agent, self.lm, {"findings": anchored})
        record(
            {
                "kind": "revise",
                "section_id": section.section_id,
                "findings": anchored,
                "termination": termination_of(result),
                "trajectory": trajectory_of(result),
            }
        )
        return file_to_section(buffer["text"], section)

    async def revise(self, *, section: ReviewPackSection, findings: list[str]) -> ReviewPackSection:
        edited: ReviewPackSection = await self.acall(section=section, findings=findings)
        return edited
