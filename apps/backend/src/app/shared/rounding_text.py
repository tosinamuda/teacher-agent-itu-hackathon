"""Rounding a note states: "round 7,500 to 7,000" is wrong, because 7,500 rounds to 8,000."""

from __future__ import annotations

import re

#: What says a number is rounded. A bare "round" is the preposition in "brackets round the sum", so
#: it counts only as the verb: followed by a direction, "to", or a number.
ROUNDING_WORDS = r"\b(?:rounded|rounding|nearest)\b|\brounds?\s+(?:off|up|down|to|\$?\d)"
ROUNDING_SIGNS = r"≈|\\approx"
_NUMBER = r"\d{1,3}(?:[,{}]+\d{3})+|\d+"
#: "round 7,500 to 7,000" and "round 7,500 steps to 7,000", never "round down 7,500 to 7,000".
_ROUNDING = re.compile(
    rf"\bround(?:s|ed|ing)?\s+({_NUMBER})(?![.,]?\d)\s+(?:[a-z]+\s+)?to\s+({_NUMBER})(?![.,]?\d)",
    re.IGNORECASE,
)


def _value(written: str) -> int:
    return int(re.sub(r"[,{}]", "", written))


def _nearest(number: int, place: int) -> int:
    """The number rounded to the nearest place, a half going up."""
    return (number + place // 2) // place * place


def wrong_roundings(text: str) -> list[str]:
    """One line for each "round A to B" whose B is not A rounded to the place B ends in zeros at."""
    faults: list[str] = []
    for match in _ROUNDING.finditer(text):
        number, rounded = _value(match.group(1)), _value(match.group(2))
        zeros = len(str(rounded)) - len(str(rounded).rstrip("0"))
        if zeros == 0 or rounded == 0:
            continue
        right = _nearest(number, 10**zeros)
        if right != rounded:
            faults.append(
                f"the text rounds {number:,} to {rounded:,}, but {number:,} rounds to "
                f"{right:,} at that place: round it correctly, or choose a number that "
                "rounds cleanly"
            )
    return faults
