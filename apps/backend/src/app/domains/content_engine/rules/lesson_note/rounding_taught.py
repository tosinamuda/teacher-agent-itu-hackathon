"""A lesson note that asks the class to round or estimate has taught it first."""

from __future__ import annotations

import json
import re

from app.shared.rounding_text import ROUNDING_SIGNS, ROUNDING_WORDS

from .across_steps import Steps, texts_of
from .config import EVALUATION_STEP, PRACTISED, WORKED

_ASKS = re.compile(rf"{ROUNDING_WORDS}|\b(?:estimat\w*|approximat\w*)\b", re.IGNORECASE)
_SHOWS = re.compile(f"{ROUNDING_SIGNS}|{ROUNDING_WORDS}", re.IGNORECASE)


def _questions(part: dict[str, object]) -> list[str]:
    return [text for field, name in PRACTISED for text in texts_of(part, field, name)]


def _workings(part: dict[str, object]) -> list[str]:
    """The working and the answer of each worked example, as text."""
    examples = part.get(WORKED)
    return (
        [json.dumps(item, ensure_ascii=False) for item in examples]
        if isinstance(examples, list)
        else []
    )


def rounding_taught(steps: Steps) -> list[str]:
    """Faults of a finished note that asks for a rounded answer it never showed or practised."""
    asking = [
        (step, question)
        for step, part in steps
        for question in _questions(part)
        if _ASKS.search(question)
    ]
    if not asking:
        return []
    issues: list[str] = []
    if not any(_SHOWS.search(worked) for _, part in steps for worked in _workings(part)):
        teaching = next((step for step, part in steps if _workings(part)), steps[0][0])
        issues.append(
            f"{teaching}: {asking[0][1][:70]!r} asks the class to round or estimate, but no "
            "worked example shows it; give a worked example whose working rounds a result in "
            "a line of its own, and say to which place"
        )
    if all(step == EVALUATION_STEP for step, _ in asking):
        practice = [step for step, part in steps if step != EVALUATION_STEP and _questions(part)]
        if practice:
            issues.append(
                f"{practice[-1]}: the evaluation asks the class to round or estimate, but no "
                "question before it practises that; give a question that asks for a rounded answer"
            )
    return issues
