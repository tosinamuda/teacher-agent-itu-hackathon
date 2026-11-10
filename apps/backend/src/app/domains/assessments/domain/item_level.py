"""Whether a class-test item sits at the size and difficulty its lesson asks of it."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping

SCALES: dict[str, float] = {"thousand": 1e3, "million": 1e6, "billion": 1e9, "trillion": 1e12}
_ORDER = ("easy", "medium", "hard")
_NUMBER = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(thousand|million|billion|trillion)?", re.IGNORECASE)
_NAMED = re.compile(r"\b(thousand|million|billion|trillion)s?\b", re.IGNORECASE)


def _value(text: str, scale: str | None) -> float | None:
    try:
        return float(text.replace(",", "").rstrip(".")) * (SCALES[scale.lower()] if scale else 1.0)
    except ValueError:
        return None


def largest_number(text: str) -> float:
    """The largest number written in ``text``, digits or digits with a scale word."""
    found = [_value(m.group(1), m.group(2)) for m in _NUMBER.finditer(text)]
    return max((v for v in found if v is not None), default=0.0)


def named_scale(objective_text: str) -> float | None:
    """The smallest size the objective names, such as 1e9 for "billions and trillions"."""
    named = [SCALES[m.group(1).lower()] for m in _NAMED.finditer(objective_text)]
    return min(named) if named else None


def item_text(stem: str, options: Mapping[str, str]) -> str:
    return " ".join((stem, *options.values()))


def reaches_scale(objective_text: str, items: Iterable[tuple[str, Mapping[str, str]]]) -> bool:
    """Some question of the objective uses numbers as large as the objective names.

    An objective that says "billions and trillions" is not tested by questions that stay under
    100,000. An objective that names no size asks nothing of the numbers.
    """
    scale = named_scale(objective_text)
    if scale is None:
        return True
    return any(largest_number(item_text(stem, options)) >= scale for stem, options in items)


def least_difficulty(stem: str) -> str:
    """The lowest label the work in the stem allows: mixed sizes or a decimal size is medium."""
    sizes = {m.group(2).lower() for m in _NUMBER.finditer(stem) if m.group(2)}
    decimal_size = any(m.group(2) and "." in m.group(1) for m in _NUMBER.finditer(stem))
    return "medium" if len(sizes) > 1 or decimal_size else "easy"


def labelled(difficulty: str, stem: str) -> str:
    """The item's label, raised to the least its stem allows."""
    least = least_difficulty(stem)
    return least if _ORDER.index(least) > _ORDER.index(difficulty) else difficulty
