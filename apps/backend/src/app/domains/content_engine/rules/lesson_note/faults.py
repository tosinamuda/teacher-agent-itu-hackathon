"""What one step's note must hold to teach from: enough text, no second thought, and it is right."""

from __future__ import annotations

import json

from ..text_checks import (
    FALSE_SIZE_RULE_FIX,
    SECOND_THOUGHT_FIX,
    corrects_itself,
    states_false_size_rule,
    text_chars,
    wrong_roundings,
)
from .config import MIN_NOTE_CHARS


def step_faults(part: dict[str, object]) -> list[str]:
    """What a step's note lacks to teach from: it is not a few headings, and it is right."""
    faults: list[str] = []
    if (chars := text_chars(part)) < MIN_NOTE_CHARS:
        faults.append(
            f"the note holds {chars} characters of text; add substance, such as more teaching "
            "points, a worked example or questions, until a teacher can teach from it"
        )
    text = json.dumps(part, ensure_ascii=False)
    if corrects_itself(text):
        faults.append(SECOND_THOUGHT_FIX)
    if states_false_size_rule(text):
        faults.append(FALSE_SIZE_RULE_FIX)
    faults.extend(wrong_roundings(text))
    return faults
