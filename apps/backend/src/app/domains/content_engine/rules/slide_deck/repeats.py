"""A step shows each idea once: a slide whose points another slide of the step already shows."""

from __future__ import annotations

import re

from app.domains.content_engine.rules.slide_deck.config import MEASURE_UNITS
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.questions import slides_of
from app.shared.latex_plain import plain_maths

_SPACES = re.compile(r"\s+")
_MEASURE = re.compile(r"(?<![\w.,])(\d[\d,]*(?:\.\d+)?)\s*(" + "|".join(MEASURE_UNITS) + r")\b")


def _said(point: str) -> str:
    return _SPACES.sub(" ", plain_maths(point)).strip().rstrip(".").casefold()


def repeated_slides(draft: Deck) -> list[str]:
    """Each slide that says nothing its step does not say on another slide, told which one."""
    issues: list[str] = []
    for unit, part in draft.written():
        shown = [{_said(point) for point in points} - {""} for _, points in slides_of(part)]
        for number, points in enumerate(shown, start=1):
            same = next(
                (
                    other
                    for other, theirs in enumerate(shown, start=1)
                    if other != number and points <= theirs and (points < theirs or other < number)
                ),
                None,
            )
            if points and same is not None:
                issues.append(
                    f"{unit.unit_id}: slide {number} shows only what slide {same} shows; "
                    "show each idea once, on one slide"
                )
    return issues


def repeated_drawings(draft: Deck) -> list[str]:
    """Each drawing that an earlier slide of the deck already has, told which slide."""
    seen: dict[str, str] = {}
    issues: list[str] = []
    for unit, part in draft.written():
        for number, (slide, _) in enumerate(slides_of(part), start=1):
            figure = _SPACES.sub(" ", str(slide.get("figure") or "")).strip()
            where = f"{unit.unit_id} slide {number}"
            if figure and figure in seen:
                issues.append(
                    f"{where} has the same drawing as {seen[figure]}; draw it once, on the "
                    "slide it belongs to"
                )
            elif figure:
                seen[figure] = where
    return issues


def _measures(point: str) -> list[tuple[str, str]]:
    return _MEASURE.findall(plain_maths(point))


def _slide_measure_faults(
    where: str, measures: list[tuple[str, str]], earlier: dict[tuple[str, str], int]
) -> list[str]:
    """Faults of one slide's measures; ``earlier`` maps each measure to the slide that had it."""
    number = int(where.rsplit(" ", 1)[1])
    faults: list[str] = []
    for measure in dict.fromkeys(measures):
        shown = f"{measure[0]} {measure[1]}"
        if measures.count(measure) > 1:
            faults.append(f"{where} says {shown} more than once; say a measure once on a slide")
        elif measure in earlier:
            faults.append(
                f"{where} says {shown} again, as slide {earlier[measure]} does; "
                "say a measure once in a step"
            )
        earlier.setdefault(measure, number)
    return faults


def repeated_measures(draft: Deck) -> list[str]:
    """Each measure, such as ``2 km``, that a step says twice outside its working.

    A slide that works a problem, with an ``=`` in its points, may repeat what it works.
    """
    issues: list[str] = []
    for unit, part in draft.written():
        earlier: dict[tuple[str, str], int] = {}
        for number, (_, points) in enumerate(slides_of(part), start=1):
            if any("=" in plain_maths(point) for point in points):
                continue
            measures = [measure for point in points for measure in _measures(point)]
            issues += _slide_measure_faults(f"{unit.unit_id}: slide {number}", measures, earlier)
    return issues
