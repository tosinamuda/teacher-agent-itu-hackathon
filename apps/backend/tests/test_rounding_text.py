"""A rounding a note states is checked: 7,500 rounds to 8,000, not 7,000."""

from __future__ import annotations

import pytest

from app.shared.rounding_text import wrong_roundings


@pytest.mark.parametrize(
    "text",
    [
        "Round 7,500 to 7,000 for a quick estimate",
        "Why is it acceptable to round 7,500 steps to 7,000 when estimating?",
        "round 8{,}500 to 8{,}000",
        "We round 8,350 to 8,300.",
        "Rounding 66,000 to 60,000 keeps it simple.",
    ],
)
def test_a_wrong_rounding_is_reported_with_the_right_one(text: str) -> None:
    faults = wrong_roundings(text)

    assert len(faults) == 1 and "rounds to" in faults[0]


@pytest.mark.parametrize(
    "text",
    [
        "Round 7,500 to 8,000 for a quick estimate",
        "Round 8,315 to 8,000.",
        "Round 9,200 steps to 9,000.",
        "round down 7,500 to 7,000",
        "Round 3.46 to 3.5.",
        "Round 8,350 to 8,400.",
        "Round the answer to 3.85 km.",
    ],
)
def test_a_right_rounding_or_none_is_not_reported(text: str) -> None:
    assert wrong_roundings(text) == []


def test_a_lesson_note_with_a_wrong_rounding_goes_back_to_the_writer() -> None:
    from app.domains.content_engine.rules.lesson_note.faults import step_faults

    part = {"explanation": "Walk 7,500 steps. Round 7,500 to 7,000 for a quick estimate. " * 6}

    assert any("rounds 7,500 to 7,000" in fault for fault in step_faults(part))
