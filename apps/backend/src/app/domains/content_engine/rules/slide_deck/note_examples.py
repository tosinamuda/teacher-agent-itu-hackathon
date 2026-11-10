"""The worked examples of a step's note, as the slide checks read them.

A note writes a worked example in one of two forms. The current form has a ``Worked examples``
section whose examples are ``**Problem.** … **Solution.**`` with the working as bullet lines.
The form notes were first written in has a ``#### Example N.`` heading for each example, its
problem, then ``**Solution**`` and the working as a numbered list.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.domains.content_engine.rules.slide_deck.titles import title_of

_SECTION = re.compile(
    rf"^####\s+{re.escape(title_of('worked_examples'))}\s*$(.*?)(?=^####\s|\Z)",
    re.MULTILINE | re.DOTALL,
)
_CURRENT = re.compile(
    rf"\*\*{title_of('problem')}\.\*\*\s*(.+?)\s*\*\*{title_of('solution')}\.\*\*\s*(.+?)"
    rf"(?=\*\*{title_of('answer')}\.\*\*|\*\*\d+\.\*\*|\Z)",
    re.DOTALL,
)
_FIRST = re.compile(
    r"^####\s+(?:worked\s+)?example\b[^\n]*\n(.*?)(?=^####\s|\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)
_SOLUTION = re.compile(rf"\*\*{title_of('solution')}\.?\*\*", re.IGNORECASE)
_BULLET = re.compile(r"^\s*[-*]\s+(.+?)\s*$", re.MULTILINE)
_ITEM = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.+?)\s*$", re.MULTILINE)
_PARENTHESES = re.compile(r"\\\((.+?)\\\)", re.DOTALL)
_BRACKETS = re.compile(r"\\\[(.+?)\\\]", re.DOTALL)
#: What marks a note as working an example, in either form.
_CLAIMS_AN_EXAMPLE = re.compile(
    rf"^####\s+(?:worked\s+)?example\b|\*\*{title_of('problem')}\.\*\*",
    re.MULTILINE | re.IGNORECASE,
)


@dataclass(frozen=True)
class WorkedExample:
    problem: str
    #: The lines of the working, in order, as the note writes them.
    lines: list[str]


def _current_section(note: str) -> str:
    section = _SECTION.search(note)
    return section.group(1) if section else ""


def _in_dollars(text: str) -> str:
    """Maths the first form delimits with backslash pairs, delimited with $ signs."""
    return _BRACKETS.sub(
        lambda found: f"$${found[1]}$$", _PARENTHESES.sub(lambda found: f"${found[1]}$", text)
    )


def _first_form_bodies(note: str) -> list[str]:
    return [_in_dollars(body) for body in _FIRST.findall(note)]


def _first_form(note: str) -> list[WorkedExample]:
    found: list[WorkedExample] = []
    for body in _first_form_bodies(note):
        marker = _SOLUTION.search(body)
        if marker is not None:
            found.append(
                WorkedExample(body[: marker.start()].strip(), _ITEM.findall(body[marker.end() :]))
            )
    return found


def worked_examples(note: str) -> list[WorkedExample]:
    """The worked examples of one step's note, in either form, in the order written."""
    current = [
        WorkedExample(problem, _BULLET.findall(solution))
        for problem, solution in _CURRENT.findall(_current_section(note))
    ]
    return [*current, *_first_form(note)]


def worked_text(note: str) -> str:
    """The text of the note's worked examples, as written; empty when it has none."""
    first = [body for body in _first_form_bodies(note) if _SOLUTION.search(body)]
    return "\n".join([_current_section(note), *first]).strip()


def has_unreadable_examples(note: str) -> bool:
    """Whether the note works examples that neither form lets the checks read."""
    return bool(_CLAIMS_AN_EXAMPLE.search(note)) and not worked_examples(note)
