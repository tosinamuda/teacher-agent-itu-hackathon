"""A number line on a slide places each mark where its value belongs."""

from __future__ import annotations

import math
import re

from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.questions import slides_of

_MARKS = re.compile(r"\\foreach\s*\\x/\\label\s+in\s*\{([^{}]*)\}")
_NUMBER = r"-?\d+(?:\.\d+)?"
#: A label's first number, after any size command such as ``\\Large``.
_LABEL = rf"\{{\s*(?:\\[A-Za-z]+\s*)*({_NUMBER})"
_AT_LABEL = re.compile(rf"at\s*\(\s*({_NUMBER})\s*,\s*-?[\d.]+\s*\)\s*{_LABEL}")
_NODE_LABEL = re.compile(
    rf"\(\s*({_NUMBER})\s*,\s*-?[\d.]+\s*\)\s*node\s*(?:\[[^\]]*\])?\s*{_LABEL}"
)
_AXIS = re.compile(r"\(\s*(-?[\d.]+)\s*,\s*0\s*\)\s*--\s*\(\s*(-?[\d.]+)\s*,\s*0\s*\)")
_HEIGHT = re.compile(r"\(\s*-?[\d.]+\s*,\s*(-?[\d.]+)\s*\)")
#: A drawing taller than this above or below its axis is a shape, not a number line.
_MAX_RISE = 1.5
#: A label may carry its unit, as in ``6.9\,km``.
_MARK = re.compile(rf"^\s*({_NUMBER})\s*/\s*({_NUMBER})")
_ITEM_BREAK = re.compile(r"(?<!\\),")
#: How far, in centimetres, a mark may sit from its place before the line misleads.
_TOLERANCE = 0.1
_LINE_LENGTH = 10
#: The picture is scaled to the slide's width, so a line longer than this shrinks its labels.
_MAX_LINE_LENGTH = 12
#: Two labels of listed marks need this much room, in centimetres, for each character of the
#: longer one, and this much besides, to stand apart.
_ROOM_PER_CHARACTER, _ROOM_BESIDES = 0.22, 0.3
#: The size commands and their point sizes; the room a character needs grows with them.
_SIZES = {"large": 12.0, "Large": 14.4, "LARGE": 17.28, "huge": 20.74, "Huge": 24.88}
_PLAIN_POINTS, _BIG_ENOUGH = 10.0, ("LARGE", "huge", "Huge")
_FIGURES = re.compile(r"\d[\d,]*(?:\.\d+)?")
_NODE_TEXT = re.compile(r"\\node[^;{]*\{([^{}]*)\}")
_SIZE_COMMAND = re.compile(r"\\(large|Large|LARGE|huge|Huge)\b")
_PLACED_NODE = re.compile(
    rf"\\node\s*(?:\[([^\]]*)\])?\s*at\s*\(\s*({_NUMBER})\s*,[^)]*\)\s*\{{([^{{}}]*)\}}"
)
_COMMAND_WORD = re.compile(r"\\[A-Za-z]+\s*")


def marks_to_write(value: float) -> str:
    """The foreach list for a number between two whole numbers, on a line 10 cm long."""
    low, high = math.floor(value), math.ceil(value)
    at = _LINE_LENGTH * (value - low) / (high - low)
    return f"{{0/{low}, {at:g}/{value:g}, {_LINE_LENGTH}/{high}}}"


def label_numbers(figure: str) -> list[str]:
    """The numbers a drawing prints as labels, as written, in the order they first appear."""
    texts = [f"{value:g}" for value in _listed_marks(figure)]
    texts += [number for body in _NODE_TEXT.findall(figure) for number in _FIGURES.findall(body)]
    return list(dict.fromkeys(texts))


def _is_number_line(figure: str) -> bool:
    return bool(_AXIS.search(figure)) and all(
        abs(float(rise)) <= _MAX_RISE for rise in _HEIGHT.findall(figure)
    )


def _listed_marks(figure: str) -> dict[float, float]:
    marks: dict[float, float] = {}
    for listed in _MARKS.findall(figure):
        for item in _ITEM_BREAK.split(listed):
            if found := _MARK.match(item):
                marks[float(found.group(2))] = float(found.group(1))
    return marks


def marks_of(figure: str) -> dict[float, float]:
    """The marks a number line places, as value to position; empty for any other drawing."""
    if not _is_number_line(figure):
        return {}
    marks = _listed_marks(figure)
    for labelled in (*_AT_LABEL.findall(figure), *_NODE_LABEL.findall(figure)):
        marks[float(labelled[1])] = float(labelled[0])
    return marks


def _font_scale(figure: str) -> float:
    """How much wider than a character of the large size the figure's largest labels are."""
    points = max((_SIZES[name] for name in _SIZE_COMMAND.findall(figure)), default=_PLAIN_POINTS)
    return points / _SIZES["large"]


def _room(low: float, high: float, scale: float) -> float:
    longer = max(len(f"{low:,g}"), len(f"{high:,g}"))
    return _ROOM_PER_CHARACTER * scale * longer + _ROOM_BESIDES


def _placed_labels(figure: str) -> dict[str, list[tuple[float, int]]]:
    """Each side of the line to the labels set on it by a node: position and characters."""
    sides: dict[str, list[tuple[float, int]]] = {"above": [], "below": []}
    for options, at, body in _PLACED_NODE.findall(figure):
        side = "above" if "above" in options else "below"
        sides[side].append((float(at), len(_COMMAND_WORD.sub("", body).strip())))
    return sides


def _placed_squeeze(figure: str) -> float:
    """How many times too close the nearest labels set on one side of the line stand."""
    scale = _font_scale(figure)
    squeezes = [
        (_ROOM_PER_CHARACTER * scale * max(left[1], right[1]) + _ROOM_BESIDES)
        / max(right[0] - left[0], 1e-9)
        for labels in _placed_labels(figure).values()
        for left, right in zip(sorted(labels), sorted(labels)[1:], strict=False)
    ]
    return max(squeezes, default=0.0)


def _crowded(figure: str) -> list[str]:
    """The fault of labels, set side by side, that would overlap; at most one."""
    marks = _listed_marks(figure) if _is_number_line(figure) else {}
    values = sorted(marks)
    scale = _font_scale(figure)
    pairs = [(low, high) for low, high in zip(values, values[1:], strict=False)]
    squeeze = max(
        (_room(low, high, scale) / max(abs(marks[high] - marks[low]), 1e-9) for low, high in pairs),
        default=0.0,
    )
    if max(squeeze, _placed_squeeze(figure) if marks_of(figure) else 0.0) <= 1:
        return []
    return [
        "the labels of the marks run together; write the label of the number you mark above "
        "the line and the labels of the whole numbers below it. Do not lengthen the line: a "
        "longer line makes every label smaller"
    ]


def _long_line(figure: str) -> list[str]:
    """The fault of a number line so long that the slide shows its labels small; at most one."""
    longest = max(
        (abs(float(end) - float(start)) for start, end in _AXIS.findall(figure)), default=0
    )
    if longest <= _MAX_LINE_LENGTH:
        return []
    return [
        f"the line is {longest:g} long, and the slide shrinks a picture to its width, so its "
        f"labels become small; draw the line {_LINE_LENGTH} long"
    ]


def _small_labels(figure: str) -> list[str]:
    """The fault of a number line whose labels are too small to read from the back."""
    if not _is_number_line(figure):
        return []
    small = any(
        not any(size in found for size in _BIG_ENOUGH)
        for text in _NODE_TEXT.findall(figure)
        for found in [_SIZE_COMMAND.findall(text)]
    )
    return (
        [
            "the labels are too small to read from the back of the room; start every label "
            "with \\Huge, as in \\node[below=4pt] at (0,0) {\\Huge 6}"
        ]
        if small
        else []
    )


def _place(value: float, low: tuple[float, float], high: tuple[float, float]) -> float:
    (low_value, low_at), (high_value, high_at) = low, high
    return low_at + (value - low_value) * (high_at - low_at) / (high_value - low_value)


def _faults(marks: dict[float, float]) -> list[str]:
    values = sorted(marks)
    low, high = (values[0], marks[values[0]]), (values[-1], marks[values[-1]])
    faults = [
        f"the mark {value:g} is at x={marks[value]:g} and belongs at x={want:.2f}"
        for value in values[1:-1]
        if abs((want := _place(value, low, high)) - marks[value]) > _TOLERANCE
    ]
    for value in values:
        edges = (math.floor(value), math.ceil(value))
        if value != edges[0] and not all(float(edge) in marks for edge in edges):
            faults.append(
                f"{value:g} lies between {edges[0]} and {edges[1]}: mark both, and place "
                f"{value:g} the same share of the way between them; write the marks as "
                f"\\foreach \\x/\\label in {marks_to_write(value)}"
            )
    return faults


def _slide_faults(figure: str) -> list[str]:
    marks = marks_of(figure)
    if not marks:
        return []
    return [*_faults(marks), *_crowded(figure), *_long_line(figure), *_small_labels(figure)]


def number_line_issues(draft: Deck) -> list[str]:
    """Each number line whose marks are not spaced by their values, or lack a whole number."""
    return [
        f"{unit.unit_id}: slide {number}: {fault}"
        for unit, part in draft.written()
        for number, (slide, _) in enumerate(slides_of(part), start=1)
        for fault in _slide_faults(str(slide.get("figure") or ""))
    ]
