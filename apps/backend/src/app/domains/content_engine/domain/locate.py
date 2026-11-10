"""Find where a piece of text sits in a draft's parts, whatever the type of the content.

A part is plain data by the schema of its unit, so the search needs no knowledge of the type:
it reads every text field and reports the unit and the path of each one that holds the text.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass

from app.shared.json_types import JsonValue

#: The most places one search reports.
MOST_PLACES = 8
#: The shortest field text that counts as covered by a selection that spans several fields.
_SHORTEST_COVERED = 12
#: How much text of a field is shown before and after the match, or from the start of the field.
_AROUND = 70
#: The marks of markdown and maths, which a page draws and so a selection does not hold.
_MARKS = frozenset("*_`$")


@dataclass(frozen=True)
class Place:
    """A text field of a part: its unit, its path in the part, and where in it the text is."""

    unit_id: str
    path: str
    #: The text around the match, or the start of the field when a selection covers it whole.
    context: str
    #: The line of the field the match is on, for a field of several lines.
    line: int | None = None


def _plain(text: str) -> tuple[str, list[int]]:
    """The text as a page shows it, folded for comparing, with where each character came from."""
    chars: list[str] = []
    origin: list[int] = []
    for index, char in enumerate(text):
        if char in _MARKS:
            continue
        if char.isspace():
            if chars and chars[-1] != " ":
                chars.append(" ")
                origin.append(index)
            continue
        for folded in char.casefold():
            chars.append(folded)
            origin.append(index)
    if chars and chars[-1] == " ":
        chars.pop()
        origin.pop()
    return "".join(chars), origin


def _leaves(value: JsonValue, path: tuple[str | int, ...]) -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield ".".join(str(step) for step in path), value
    elif isinstance(value, Mapping):
        for key, inner in value.items():
            yield from _leaves(inner, (*path, key))
    elif isinstance(value, list):
        for index, inner in enumerate(value):
            yield from _leaves(inner, (*path, index))


def _shown(text: str, start: int, end: int) -> str:
    """The text from ``start`` to ``end`` with some around it, and \u2026 where it is cut."""
    first, last = max(0, start - _AROUND), min(len(text), end + _AROUND)
    return ("\u2026" if first else "") + text[first:last] + ("\u2026" if last < len(text) else "")


def _holding(unit_id: str, path: str, text: str, wanted: str) -> Place | None:
    plain, origin = _plain(text)
    at = plain.find(wanted)
    if at < 0:
        return None
    start, end = origin[at], origin[at + len(wanted) - 1] + 1
    line = text.count("\n", 0, start) + 1 if "\n" in text else None
    return Place(unit_id, path, _shown(text, start, end), line)


def locate(parts: Mapping[str, Mapping[str, JsonValue]], text: str) -> list[Place]:
    """The fields that hold ``text``, or, when none does, those a selection of it covers.

    A selection inside one field finds that field, the line it is on and the text around it. One
    that runs across several fields finds the fields it covers whole, which have enough text to
    tell them from any other.
    """
    wanted, _ = _plain(text)
    if not wanted:
        return []
    fields = [
        (unit_id, path, value)
        for unit_id, part in parts.items()
        for path, value in _leaves(dict(part), ())
    ]
    holding = [
        place
        for unit_id, path, value in fields
        if (place := _holding(unit_id, path, value, wanted)) is not None
    ]
    if holding:
        return holding[:MOST_PLACES]
    covered = [
        Place(unit_id, path, _shown(value, 0, 0))
        for unit_id, path, value in fields
        if len(_plain(value)[0]) >= _SHORTEST_COVERED and _plain(value)[0] in wanted
    ]
    return covered[:MOST_PLACES]
