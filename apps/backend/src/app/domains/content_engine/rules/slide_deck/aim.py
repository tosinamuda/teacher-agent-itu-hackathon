"""The introduction states what the class will be able to do, in the learners' words."""

from __future__ import annotations

import math
import re
from collections.abc import Sequence

from app.domains.content_engine.rules.slide_deck.config import INTRO_STEP, LIMITS
from app.domains.content_engine.rules.slide_deck.coverage import words_of
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.questions import slides_of

_LEARNERS_WORDS = re.compile(r"\b(?:i|we|you) can\b|\bbe able to\b", re.IGNORECASE)
#: Words that every objective and every aim share, and so say nothing about the lesson.
_FILLER = frozenset(
    {"able", "that", "this", "from", "they", "will", "with", "using", "today", "students", "pupils"}
)
#: Words are compared by their first letters, so estimate, estimates and estimation match.
_STEM = 4
#: An aim states the objective when it keeps at least this share of the objective's words,
#: and never fewer than the minimum: it drops no part of what the class will be able to do.
_MIN_SHARED = 2
#: The aim comes right after the opening question: it is one of the first slides.
_EARLY = 3
_SHOWN = 80


def _stems(text: str) -> set[str]:
    return {word[:_STEM] for word in words_of(text) if len(word) >= _STEM and word not in _FILLER}


def _keeps_objective(text: str, objective: str) -> bool:
    wanted = _stems(objective)
    needed = max(_MIN_SHARED, math.ceil(LIMITS["aim_share_percent"] * len(wanted) / 100))
    return len(_stems(text) & wanted) >= needed


def _left_out(points: list[str], objective: str) -> list[str]:
    """The objective's words, in its order, that the points do not use."""
    used = _stems(" ".join(points))
    words = [w for w in words_of(objective) if len(w) >= _STEM and w not in _FILLER]
    return list(dict.fromkeys(w for w in words if w[:_STEM] not in used))


def _states_aim(points: list[str], objectives: Sequence[str]) -> bool:
    text = " ".join(points)
    if not _LEARNERS_WORDS.search(text):
        return False
    return not objectives or any(_keeps_objective(text, objective) for objective in objectives)


def _fault(step: str, objectives: Sequence[str], stated: list[str] | None) -> str:
    """What to send back: no aim, or an aim in the learners' words that falls short."""
    fault = (
        f"{step}: none of the first slides states the aim; give the second slide a point "
        "that says what the class will be able to do by the end, in the learners' words "
        '("By the end, I can ..."), using the objective\'s own words'
    )
    if not objectives:
        return fault
    fault = f"{fault}, from the objective {objectives[0][:_SHOWN]!r}"
    left_out = _left_out(stated, objectives[0]) if stated else []
    return f"{fault}; the aim leaves out: {', '.join(left_out)}" if left_out else fault


def _aim_in_learners_words(slides: list[list[str]]) -> list[str] | None:
    return next((points for points in slides if _LEARNERS_WORDS.search(" ".join(points))), None)


def unstated_aim(draft: Deck, objectives: Sequence[str]) -> list[str]:
    """The introduction, when no slide states the objective as what the class can do."""
    issues: list[str] = []
    for unit, part in draft.written():
        if unit.unit_id != INTRO_STEP:
            continue
        early = [points for _, points in slides_of(part)[:_EARLY]]
        if not any(_states_aim(points, objectives) for points in early):
            issues.append(_fault(unit.unit_id, objectives, _aim_in_learners_words(early)))
    return issues
