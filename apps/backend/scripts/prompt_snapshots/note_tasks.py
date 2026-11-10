"""Task-shaped lines in a teacher's note, and what she did with each one next.

``student_tasks`` reads a core step's ``practice`` blocks. Where a step has none,
the open question is whether she set no work or whether work she did set was
typed as something else during transcription — so this finds the candidate lines
and reports what follows each.

What follows is the evidence that separates the two readings. A line she then
solved on the page is a worked example she wrote out, not work she set. A line
followed by the drawing of that stage is one move in a construction she performed
at the board. Only a line with neither is genuinely open.

This classifies **context, never intent**. The source pages settle intent; the
classification exists so that a reader is deciding against the surrounding text
rather than against a count.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (
    REVIEW_MARKUP,
)

_TIKZ = re.compile(
    r"(?:\\begin\{center\}\s*)?\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}"
    r"(?:\s*\\end\{center\})?",
    re.DOTALL,
)

_IMPERATIVES = (
    "Bisect",
    "Calculate",
    "Complete",
    "Construct",
    "Copy",
    "Determine",
    "Draw",
    "Evaluate",
    "Find",
    "List",
    "Mark",
    "Measure",
    "Name",
    "Place",
    "Simplify",
    "Solve",
    "State",
    "Work out",
    "Write",
)
#: A leading enumerator (``1.``, ``(a)``, ``ii)``) and bold markers are hers; the
#: verb after them is what makes a line read as an instruction.
_TASK_LINE = re.compile(
    r"\A(?:\*\*)?(?:\(?[a-z0-9]{1,3}[.)]\s*)?(?:\*\*)?\s*(?:" + "|".join(_IMPERATIVES) + r")\b",
    re.IGNORECASE,
)
_SOLUTION = re.compile(r"\A\**\s*Solution\b", re.IGNORECASE)
_FIGURE = re.compile(r"\A\*\*fig-\d+", re.IGNORECASE)

#: How far after a line to look for what resolves it. Her worked examples put the
#: solution one or two paragraphs on, behind the question's own sub-parts.
_LOOKAHEAD = 3


class Disposition(str, Enum):
    """What the note does with a task-shaped line immediately after writing it."""

    WORKED = "worked"
    DEMONSTRATED = "demonstrated"
    OPEN = "open"


DISPOSITION_MEANING = {
    Disposition.WORKED: "she solves it on the page — a worked example, not work set",
    Disposition.DEMONSTRATED: "the drawing of this stage follows — a construction performed",
    Disposition.OPEN: "neither a solution nor a stage drawing follows",
}


@dataclass(frozen=True)
class NoteTask:
    """One task-shaped line, with the paragraph that decides how to read it."""

    line: str
    disposition: Disposition
    followed_by: str


def paragraphs(note: str) -> list[str]:
    """The note's prose paragraphs, with review markup and drawing source removed."""
    stripped = _TIKZ.sub("", REVIEW_MARKUP.sub("", note or ""))
    return [block.strip() for block in re.split(r"\n\s*\n", stripped) if block.strip()]


def _disposition(following: list[str]) -> tuple[Disposition, str]:
    """A solution outranks a figure wherever both appear.

    Her worked examples often put the figure first and solve underneath it, so
    taking whichever came first would read a solved example as a construction
    stage. A construction stage never carries a solution, so the reverse
    misreading cannot happen.
    """
    for paragraph in following:
        if _SOLUTION.match(paragraph):
            return Disposition.WORKED, paragraph
    for paragraph in following:
        if _FIGURE.match(paragraph):
            return Disposition.DEMONSTRATED, paragraph
    return Disposition.OPEN, following[0] if following else ""


def task_lines(note: str) -> list[NoteTask]:
    """Every task-shaped line in the note, each with what the note does next."""
    blocks = paragraphs(note)
    found = []
    for index, block in enumerate(blocks):
        if not _TASK_LINE.match(block):
            continue
        disposition, evidence = _disposition(blocks[index + 1 : index + 1 + _LOOKAHEAD])
        found.append(NoteTask(line=block, disposition=disposition, followed_by=evidence))
    return found
