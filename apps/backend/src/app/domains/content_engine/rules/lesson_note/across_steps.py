"""What the steps of a lesson note say to each other: a question asked in two steps."""

from __future__ import annotations

import re

from ..text_checks import question_stem
from .config import ASKED, EVALUATION_STEP

Steps = list[tuple[str, dict[str, object]]]

_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _same_problem(asked: str) -> str:
    """A problem's numbers when it has two or more, as a rewording keeps them, else its words."""
    numbers = sorted({found.replace(",", "").rstrip(".") for found in _NUMBER.findall(asked)})
    return " ".join(numbers) if len(numbers) >= 2 else question_stem(asked)


def texts_of(part: dict[str, object], field: str, name: str) -> list[str]:
    """The ``name`` text of each item of the part's ``field`` list."""
    items = part.get(field)
    return [
        str(item[name]).strip()
        for item in (items if isinstance(items, list) else [])
        if isinstance(item, dict) and isinstance(item.get(name), str)
    ]


def _asked(part: dict[str, object]) -> list[str]:
    """Every question the step puts to the class, and the problem of each worked example."""
    return [text for field, name in ASKED for text in texts_of(part, field, name)]


def repeated_questions(steps: Steps) -> list[str]:
    """A question asked in more than one step, told to the step that is not the evaluation's."""
    homes: dict[str, list[str]] = {}
    shown: dict[str, str] = {}
    for step, part in steps:
        for asked in _asked(part):
            stem = _same_problem(asked)
            where = homes.setdefault(stem, [])
            if step not in where:
                where.append(step)
            shown.setdefault(stem, asked)
    issues: list[str] = []
    for stem, where in homes.items():
        if len(where) < 2:
            continue
        change = (
            next(step for step in where if step != EVALUATION_STEP)
            if EVALUATION_STEP in where
            else where[-1]
        )
        others = ", ".join(step for step in where if step != change)
        issues.append(
            f"{change}: {shown[stem][:70]!r} is also asked in {others}; "
            "give each step its own question"
        )
    return issues
