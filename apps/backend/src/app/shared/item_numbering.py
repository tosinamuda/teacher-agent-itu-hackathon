"""Text that is about to be numbered, and the numbering it already carries.

A practice prompt is usually lifted out of a numbered task list in the teacher's note,
so it arrives already reading "1. Simplify …". Rendered into an ordered list it is
numbered a second time and the page opens "1. 1. Simplify …". The outer number is the
only thing tying an answer to its question, so it stays and the number the text brought
with it is the one that gives way.

What makes a leading number a list is having a next item, and that splits the two cases:

- **no successor** — the item's own number, arriving twice. Dropped.
- **a successor** — a run of sub-steps belonging to one item ("1. Draw AB. 2. Place the
  set-square. …"). Kept, and laid out one per line so the run reads as a list at the
  second level rather than trailing off the end of the first step.

Left alone deliberately:

- ``(a)`` / ``(b)`` parts, which split one question rather than number several;
- decimals — ``25.12 cm`` opens with digits and a dot and is not an enumerator, so an
  enumerator has to be followed by whitespace.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

# ``12.`` or ``12)`` standing on its own: at the start of the text or after whitespace,
# and followed by whitespace. The trailing-whitespace requirement is what separates an
# enumerator from a decimal ("3.5 cm") or a sentence-final figure ("… 3n x 10.").
_LEADING_ENUMERATOR_RE = re.compile(r"\A\s*(\d+)[.)]\s+")
_LETTERS = "abcdefghijklmnopqrstuvwxyz"


def under_supplied_number(text: str, *, letter_sub_steps: bool = False) -> str:
    """Prepare ``text`` to sit under a number its renderer supplies.

    Drops a leading enumerator that merely repeats that number, and breaks a run of
    sub-steps onto its own lines. Text carrying neither is returned unchanged.

    ``letter_sub_steps`` re-marks a kept run ``a.``, ``b.``, ``c.`` — for a surface with
    no stylesheet to draw the second level, where a run left in decimals would stack on
    the supplied number all over again.
    """
    leading = _LEADING_ENUMERATOR_RE.match(text)
    if not leading:
        return text
    first = int(leading.group(1))
    if not _successor_of(first).search(text, leading.end()):
        return text[leading.end() :]
    steps = _split_run(text, first, leading.end())
    if letter_sub_steps and len(steps) <= len(_LETTERS):
        return "\n".join(_marked(steps, _LETTERS[: len(steps)]))
    # Dots even where the run was written "1)": markdown reads only the dotted form as
    # a list, and without a list there is no second level for the stylesheet to letter.
    return "\n".join(_marked(steps, [str(first + offset) for offset in range(len(steps))]))


def _successor_of(number: int) -> re.Pattern[str]:
    """The enumerator that would continue a run from ``number``."""
    return re.compile(rf"(?<=\s){number + 1}[.)](?=\s)")


def _split_run(text: str, first: int, start: int) -> list[str]:
    """The run's steps, one per element.

    A run written out as one paragraph — "1. Draw PQ. 2. Place the compass at P. …" —
    is a list to a reader and a single item to markdown, which numbers the first step
    and leaves the rest trailing inside it. Splitting before each successor gives the
    list the line breaks it needs; a run already written one per line is unchanged.
    """
    steps, cursor, number = [], 0, first
    while match := _successor_of(number).search(text, start):
        steps.append(text[cursor : _break_before(text, match.start())])
        cursor = start = match.start()
        number += 1
    steps.append(text[cursor:])
    return steps


def _break_before(text: str, position: int) -> int:
    """Where the whitespace ahead of ``position`` begins — the split goes there."""
    return len(text[:position].rstrip())


def _marked(steps: list[str], markers: Sequence[str]) -> list[str]:
    """Each step of the run under its own marker, one marker per step."""
    return [
        _LEADING_ENUMERATOR_RE.sub(f"{marker}. ", step, count=1)
        for marker, step in zip(markers, steps, strict=True)
    ]


def marks_a_numbered_run(text: str) -> bool:
    r"""Whether this text labels its own parts ``1.`` ``2.`` ``3.``.

    An answer is prepared without seeing its question, so a question whose parts are
    numbered could be answered ``a. b. c.`` — nine items in the judged run were, all of
    them C0 — and a learner then has to count to match an answer to the part it answers.
    A caller holding both passes the question here and lets the answer follow it.
    """
    prepared = under_supplied_number(text)
    return len(_LEADING_ENUMERATOR_RE.findall(prepared)) >= 2 or bool(
        re.search(r"(?m)^\s*\d+[.)]\s.*\n\s*\d+[.)]\s", prepared)
    )
