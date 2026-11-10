"""Mutable section draft and the tools an LLM uses to write it."""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal, TypeGuard

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)

# "visual" is absent: figures are attached from the lesson plan after generation.
AuthorableBlockType = Literal["explanation", "worked_example"]
AUTHORABLE: tuple[AuthorableBlockType, ...] = ("explanation", "worked_example")


def _is_authorable(block_type: str) -> TypeGuard[AuthorableBlockType]:
    """Narrow a model-supplied block type to the ones a section may author."""
    return block_type in AUTHORABLE


# The format a reader-facing string must be written in. It is stated on every tool that
# takes one, because the tool roster is the only prompt the composer reads for its text:
# the output schema's field descriptions never reach a loop that writes through tools.
# Every surface escapes a field before converting its markdown, so a <strong> the model
# emits is shown to the reader as the six characters <strong>.
MARKDOWN_ONLY = (
    "Text is markdown — **bold**, *italic*, - lists, $LaTeX$ for maths — and never HTML: "
    "the page shows a <strong> tag to the reader as the literal characters <strong>."
)


_TAKES_READER_TEXT = frozenset({"add_block", "revise_block", "add_practice", "revise_practice"})


def _markdown_only(tool: Callable[..., str]) -> Callable[..., str]:
    tool.__doc__ = f"{(tool.__doc__ or '').rstrip()}\n\n{MARKDOWN_ONLY}\n"
    return tool


class SectionDraft:
    """The draft the composer writes into, and the section it becomes."""

    def __init__(self, unit: SectionGenerationUnit) -> None:
        self.unit = unit
        self.title = ""
        self.blocks: list[ReviewPackBlock] = []
        self.practice: list[ReviewPackPracticeItem] = []

    def as_file(self) -> str:
        lines = [f"# {self.title}" if self.title else "# (no title yet)", ""]
        for block in self.blocks:
            lines.extend([f"[{handle(block.block_id)}] ({block.block_type})", block.text, ""])
        for item in self.practice:
            lines.append(f"[{handle(item.item_id)}] (practice)")
            lines.extend([item.prompt, f"answer: {item.answer}", ""])
        return "\n".join(lines).rstrip() + "\n"

    def add_practice(self, prompt: str, answer: str, worked_solution: str | None) -> str:
        item_id = f"{self.unit.unit_id}:p{len(self.practice)}"
        self.practice.append(
            ReviewPackPracticeItem(
                item_id=item_id,
                prompt=prompt.strip(),
                answer=answer.strip(),
                worked_solution=(worked_solution or "").strip() or None,
            )
        )
        return item_id

    def item(self, item_id: str) -> ReviewPackPracticeItem | None:
        return next((item for item in self.practice if item.item_id == item_id), None)

    def add(self, block_type: AuthorableBlockType, text: str) -> str:
        # One note per unit, so provenance is a fact about the unit rather than
        # something to ask the writer for block by block.
        block_id = f"{self.unit.unit_id}:b{len(self.blocks)}"
        self.blocks.append(
            ReviewPackBlock(
                block_id=block_id,
                block_type=block_type,
                text=text.strip(),
                lesson_objective_id=self.unit.lesson_objective_id,
                source_refs=[i.source_ref for i in self.unit.source_evidence if i.source_ref],
            )
        )
        return block_id

    def block(self, block_id: str) -> ReviewPackBlock | None:
        return next((block for block in self.blocks if block.block_id == block_id), None)

    def to_section(self) -> ReviewPackSection:
        return ReviewPackSection(
            section_id=self.unit.unit_id,
            title=self.title or self.unit.objective_text or "Revision section",
            lesson_objective_id=self.unit.lesson_objective_id,
            blocks=self.blocks,
            practice=self.practice,
        )


def composition_tools(draft: SectionDraft, pipeline: ReviewPackPipeline = CURRENT_PIPELINE) -> list:
    """The whole roster: title, the instructional stream, and the practice stream.

    Pipeline 2026-09-02 states the text format on every tool that takes reader-facing
    text; 2026-08-25 does not. The tools are built fresh per call, so stating it here
    changes only this roster.
    """
    tools = [*_instruction_tools(draft), *_practice_tools(draft)]
    if pipeline is ReviewPackPipeline.V2026_09_02:
        for tool in tools:
            if tool.__name__ in _TAKES_READER_TEXT:
                _markdown_only(tool)
    return tools


def _instruction_tools(draft: SectionDraft) -> list:
    # These docstrings are prompt text: dspy renders them as the tool roster.

    def set_title(title: str) -> str:
        """Set the learner-facing section title. Call once, before writing blocks."""
        draft.title = title.strip()
        return f"Title set to {draft.title!r}."

    def add_block(block_type: str, text: str) -> str:
        """Append one instructional block to the draft and return its id.

        block_type is one of: explanation, worked_example. Practice is added with
        add_practice, which takes the answer alongside the question.
        """
        if not _is_authorable(block_type):
            return f"Unknown block_type {block_type!r}. Use one of: {', '.join(AUTHORABLE)}."
        if not text.strip():
            return "Refused: a block must carry text."
        return f"Added {handle(draft.add(block_type, text))}."

    def read_draft() -> str:
        """Read the whole draft as written so far."""
        return draft.as_file()

    def revise_block(block_id: str, text: str) -> str:
        """Replace one block's text, leaving every other block untouched.

        block_id is the short id add_block returned and read_draft shows, like `b3`.
        """
        known = [b.block_id for b in draft.blocks]
        resolved = _resolve(block_id, known)
        block = draft.block(resolved) if resolved else None
        if block is None:
            listed = ", ".join(handle(k) for k in known) or "none yet — add_block first"
            return f"No block {block_id!r}. The ids are: {listed}."
        block.text = text.strip()
        return f"Revised {handle(block.block_id)}."

    return [set_title, add_block, read_draft, revise_block]


def handle(full_id: str) -> str:
    """How a draft addresses one of its own parts: `b3`, `p0`.

    Every id in a draft carries the same unit prefix — `step:step-t2w09-03:` on all of
    them — so within a draft the prefix distinguishes nothing and only gives a writer
    something to copy wrongly. It stays on the stored id, which travels downstream and
    has to be unique across units; it comes off the address the tools take and show.
    """
    return full_id.rsplit(":", 1)[-1]


def _resolve(wanted: str, known: list[str]) -> str | None:
    """The id the writer meant, when what it sent is not exactly an id.

    Unit ids are namespaced — `step:step-t2w09-03` — so a practice item reads
    `step:step-t2w09-03:p0`: a `step:` prefix, a nested `step-...`, and two colons. A
    writer that takes the leading `step:` for a display label and sends
    `step-t2w09-03:p0` is making the obvious reading of it, and refusing that is a
    refusal on a technicality. So an unambiguous tail match is accepted.

    This is not leniency for its own sake. One loop spent its whole budget on this: it
    called read_draft, mis-copied the id, was told the id was unknown, called read_draft
    again, and never wrote anything. The turn was scored as a section.
    """
    if wanted in known:
        return wanted
    exact = [k for k in known if handle(k) == wanted.rsplit(":", 1)[-1]]
    if len(exact) == 1:
        return exact[0]
    tails = [k for k in known if k.endswith(wanted) or k.endswith(f":{wanted}")]
    return tails[0] if len(tails) == 1 else None


def _practice_tools(draft: SectionDraft) -> list:
    def add_practice(prompt: str, answer: str, worked_solution: str = "") -> str:
        """Append one practice question and the answer the learner checks it against.

        Do not write the answer into the question, and do not add an answers section
        of your own: the answers are collected after the activities for you. Give a
        worked_solution where the answer alone would not show the learner what to do.
        """
        if not prompt.strip():
            return "Refused: a practice item must carry a question."
        if not answer.strip():
            return "Refused: a practice item must carry the answer it is checked against."
        return f"Added {handle(draft.add_practice(prompt, answer, worked_solution))}."

    def revise_practice(item_id: str, prompt: str, answer: str, worked_solution: str = "") -> str:
        """Replace one practice item, leaving every other item untouched.

        item_id is the short id add_practice returned and read_draft shows, like `p0`.
        """
        known = [i.item_id for i in draft.practice]
        resolved = _resolve(item_id, known)
        item = draft.item(resolved) if resolved else None
        if item is None:
            # Name the ids. "Call read_draft to see what exists" is no help to a writer
            # that has already read the draft and mis-copied what it saw.
            listed = ", ".join(handle(k) for k in known) or "none yet — add_practice first"
            return f"No practice item {item_id!r}. The ids are: {listed}."
        item.prompt, item.answer = prompt.strip(), answer.strip()
        item.worked_solution = worked_solution.strip() or None
        return f"Revised {handle(item.item_id)}."

    return [add_practice, revise_practice]
