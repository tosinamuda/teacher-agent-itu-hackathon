"""Whether a test's questions sit at the size their objective names."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping

_SCALES: dict[str, float] = {"thousand": 1e3, "million": 1e6, "billion": 1e9, "trillion": 1e12}
_NUMBER = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(thousand|million|billion|trillion)?", re.IGNORECASE)
_NAMED = re.compile(r"\b(thousand|million|billion|trillion)s?\b", re.IGNORECASE)


def _value(text: str, scale: str | None) -> float | None:
    try:
        return float(text.replace(",", "").rstrip(".")) * (_SCALES[scale.lower()] if scale else 1.0)
    except ValueError:
        return None


def _largest_number(text: str) -> float:
    """The largest number written in ``text``, digits or digits with a scale word."""
    found = [_value(m.group(1), m.group(2)) for m in _NUMBER.finditer(text)]
    return max((v for v in found if v is not None), default=0.0)


def _named_scale(objective_text: str) -> float | None:
    """The smallest size the objective names, such as 1e9 for "billions and trillions"."""
    named = [_SCALES[m.group(1).lower()] for m in _NAMED.finditer(objective_text)]
    return min(named) if named else None


def reaches_scale(objective_text: str, items: Iterable[tuple[str, Mapping[str, str]]]) -> bool:
    """Some question of the objective uses numbers as large as the objective names.

    An objective that says "billions and trillions" is not tested by questions that stay under
    100,000. An objective that names no size asks nothing of the numbers.
    """
    scale = _named_scale(objective_text)
    if scale is None:
        return True
    return any(
        _largest_number(" ".join((stem, *options.values()))) >= scale for stem, options in items
    )
