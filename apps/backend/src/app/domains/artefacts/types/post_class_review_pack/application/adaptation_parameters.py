"""What a learner's mastery band and survey answers resolve to, for one objective.

The band and the learner's own answers fix every dimension a learner's section may adapt, by
rule. The writer is handed these settings rather than the band to interpret, and each section's
settings are kept in the run record, so what was asked of the writer is known without reading
its prose.
"""

from __future__ import annotations

import re
from typing import Literal, NamedTuple

from pydantic import BaseModel, ConfigDict

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
)

_SCORE = re.compile(r"\((\d)/5\)")
_LOW = 2
_HIGH = 4


Explanation = Literal["smaller_steps", "rule_and_reason", "brief_then_why"]
WorkedSupport = Literal["every_line", "key_line", "first_and_last"]
PracticeStart = Literal["easier", "as_class", "beyond_class"]


class AdaptationParameters(BaseModel):
    """The settings for each dimension a learner's section may adapt."""

    model_config = ConfigDict(extra="forbid")

    explanation: Explanation
    worked_support: WorkedSupport
    practice_start: PracticeStart
    hints: bool
    misconception_repair: bool


class _Band(NamedTuple):
    explanation: Explanation
    worked_support: WorkedSupport
    practice_start: PracticeStart


_BY_BAND = {
    "remediate": _Band("smaller_steps", "every_line", "easier"),
    "reinforce": _Band("rule_and_reason", "key_line", "as_class"),
    "extend": _Band("brief_then_why", "first_and_last", "beyond_class"),
}


def _score(phrase: str | None) -> int | None:
    found = _SCORE.search(phrase or "")
    return int(found.group(1)) if found else None


def resolve_parameters(state: ObjectiveLearnerState) -> AdaptationParameters:
    """The settings for one objective.

    The band sets the explanation, the worked support and where practice starts. Hints go to a
    learner who needs the most help, or who said they were unsure or found the work hard.
    """
    band = _BY_BAND[state.mastery_band]
    confidence, difficulty = _score(state.confidence), _score(state.perceived_difficulty)
    needs_help = (
        state.mastery_band == "remediate"
        or (confidence is not None and confidence <= _LOW)
        or (difficulty is not None and difficulty >= _HIGH)
    )
    return AdaptationParameters(
        explanation=band.explanation,
        worked_support=band.worked_support,
        practice_start=band.practice_start,
        hints=needs_help,
        misconception_repair=bool(state.misconception),
    )
