"""One row of the register, and whether a recomputed value reproduces the figure printed for it."""

from __future__ import annotations

import re
from dataclasses import dataclass

#: A row's status. A reported result is either recomputed here from the workbook, or read from a
#: recorded output this package does not refit; an archived one is kept for the record only.
RECOMPUTED = "reported; recomputed from the workbook"
CARRIED = "reported; read from a recorded output"
READING = "reported; the researcher's reading, counted here"
NOT_REPORTED = "archived; not reported in the dissertation"

Number = float | int


@dataclass(frozen=True)
class Printed:
    """A figure as the dissertation prints it, with the recomputed value it must round to."""

    text: str
    #: A number is compared at the precision printed; text (a count such as '95/101') exactly.
    value: Number | str | None

    def reproduces(self) -> bool | None:
        """``None`` when there is nothing recomputed to compare."""
        if self.value is None:
            return None
        if isinstance(self.value, str):
            return self.value == self.text
        return agrees(self.value, self.text)


@dataclass(frozen=True)
class Result:
    id: str
    part: str
    question: str
    quantity: str
    estimate: Printed
    test: str = ""
    unit: str = ""
    location: str = ""
    status: str = RECOMPUTED
    computed_from: str = ""
    interval: tuple[Printed, Printed] | None = None
    p: Printed | None = None
    sidedness: str = ""
    #: Further figures the dissertation prints for this result, each checked like the estimate.
    also: tuple[tuple[str, Printed], ...] = ()
    note: str = ""

    def figures(self) -> list[Printed]:
        low_high = list(self.interval) if self.interval else []
        extra = [figure for _, figure in self.also]
        return [self.estimate, *low_high, *([self.p] if self.p else []), *extra]

    def also_text(self) -> str:
        return "; ".join(f"{label} {figure.text}" for label, figure in self.also)

    def reproduces(self) -> str:
        """'yes', 'NO', 'partly (k of n)' or 'not recomputed' across every printed figure."""
        checks = [figure.reproduces() for figure in self.figures()]
        compared = [check for check in checks if check is not None]
        if not compared:
            return "not recomputed"
        if not all(compared):
            return "NO"
        return (
            "yes" if len(compared) == len(checks) else f"partly ({len(compared)} of {len(checks)})"
        )


_NUMBER = re.compile(r"[−+-]?\d*\.?\d+")


def agrees(value: Number, printed: str) -> bool:
    """Whether ``value`` rounds to the number printed, at the precision it is printed to.

    ``printed`` may carry a sign, a leading-dot decimal or a percentage; it is matched to its last
    printed digit.
    """
    text = printed.strip().replace("−", "-").replace(",", "")
    match = _NUMBER.search(text)
    if match is None:
        raise ValueError(f"no number in {printed!r}")
    digits = match.group(0).replace("−", "-")
    shown = float(digits)
    scale = 100 if "%" in text[match.end() :] else 1
    decimals = len(digits.split(".")[1]) if "." in digits else 0
    return bool(abs(value * scale - shown) <= 0.5 * 10**-decimals + 1e-12)
