"""How a slide's points are written: words stay outside formulas, and a relation says something."""

from __future__ import annotations

import re

from app.shared.json_types import JsonObject, JsonValue
from app.shared.latex_plain import plain_maths

_MATHS = re.compile(r"\$([^$]*)\$")
_TEXT = re.compile(r"\\text\{[^{}]*\}")
_COMMAND = re.compile(r"\\[A-Za-z]+")
_WORD = re.compile(r"[A-Za-z]{3,}")
_RELATION = re.compile(r"[≈≠≤≥<>=]")
_APPROXIMATELY = "≈"


def _points(slide: JsonObject) -> list[str]:
    entries: JsonValue | None = slide.get("points")
    return [
        str(entry["point"]).strip()
        for entry in (entries if isinstance(entries, list) else [])
        if isinstance(entry, dict) and isinstance(entry.get("point"), str)
    ]


def _has_words_in_maths(point: str) -> bool:
    """A formula that holds a word, such as ``$Estimation = 5$``, rather than only symbols."""
    return any(
        _WORD.search(_COMMAND.sub("", _TEXT.sub("", inside))) for inside in _MATHS.findall(point)
    )


def _standing_alone(point: str) -> bool:
    """An approximation with nothing before it, such as ``≈ 2 km``: a measure of nothing."""
    return plain_maths(point).lstrip().startswith(_APPROXIMATELY)


def _same_both_sides(point: str) -> bool:
    """A relation whose two sides read the same, such as ``2 km ≈ 2 km``."""
    sides = [" ".join(side.split()).casefold() for side in _RELATION.split(plain_maths(point))]
    return any(left and left == right for left, right in zip(sides, sides[1:], strict=False))


def wording_faults(where: str, slide: JsonObject) -> list[str]:
    """Each point of a slide that is worded so it says nothing; each names its slide."""
    faults: list[str] = []
    for point in _points(slide):
        if _has_words_in_maths(point):
            faults.append(
                f"{where}: {point[:50]!r} has words inside $ signs; write words as plain text, "
                "and put a unit or a word inside a formula in \\text{}"
            )
        if _standing_alone(point):
            faults.append(
                f"{where}: {point[:50]!r} starts with {_APPROXIMATELY} and names nothing before "
                "it; name the thing the measure belongs to, or leave the point out"
            )
        if _same_both_sides(point):
            faults.append(
                f"{where}: {point[:50]!r} has the same on both sides of its relation; "
                "say what the measure belongs to, or leave the point out"
            )
    return faults
