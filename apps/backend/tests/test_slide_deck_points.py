"""How long a point may be: twelve words, and forty for the first, which states a worked example."""

from __future__ import annotations

import pytest

from app.domains.content_engine.rules.slide_deck.review import (
    MAX_FIRST_POINT_WORDS,
    MAX_POINT_WORDS,
    _point_faults,
)


def _words(count: int) -> str:
    return " ".join(["word"] * count)


def test_the_first_point_may_hold_a_worked_examples_question_of_forty_words() -> None:
    assert MAX_FIRST_POINT_WORDS == 40
    assert _point_faults("slide 2", [_words(40), _words(MAX_POINT_WORDS)]) == []


def test_a_first_point_over_forty_words_is_sent_back() -> None:
    faults = _point_faults("slide 2", [_words(41)])

    assert len(faults) == 1 and "a point of 41 words runs past 40" in faults[0]


@pytest.mark.parametrize("length", [MAX_POINT_WORDS + 1, 40])
def test_a_later_point_stays_at_twelve_words(length: int) -> None:
    faults = _point_faults("slide 2", ["Intro", _words(length)])

    assert len(faults) == 1 and f"runs past {MAX_POINT_WORDS}" in faults[0]
