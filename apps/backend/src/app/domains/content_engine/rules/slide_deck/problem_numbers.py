"""The numbers of a problem, and whether a slide's text holds them all."""

from __future__ import annotations

import re

from app.shared.latex_plain import plain_maths

_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")
#: A problem whose numbers have this many significant digits between them is told from
#: another by its digits alone. A shorter one (50 cm, 10,000 steps) would match 5 and 1
#: wherever they stand, so it is told only by its numbers as written.
_SPECIFIC_DIGITS = 4


def _written(text: str) -> set[str]:
    return {found.replace(",", "") for found in _NUMBER.findall(plain_maths(text))}


def _significant(number: str) -> str:
    """The digits that give a number its value, without its point or the zeros that place it."""
    return number.replace(".", "").strip("0") or "0"


def number_count(text: str) -> int:
    """How many different numbers ``text`` writes."""
    return len(_written(text))


def holds(held: str, problem: str) -> bool:
    """Whether ``held`` writes every number of ``problem``.

    A specific problem is also held when its digits are there in another unit, so 60 cm and
    8,315 steps are held by 0.6 m and 8,315 steps.
    """
    needed, present = _written(problem), _written(held)
    if needed <= present:
        return True
    digits = {_significant(number) for number in needed}
    return sum(map(len, digits)) >= _SPECIFIC_DIGITS and digits <= {
        _significant(number) for number in present
    }
