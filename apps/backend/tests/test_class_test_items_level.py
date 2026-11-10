"""A class test is held to the size its objective names and to the label its stems allow."""

from __future__ import annotations

import pytest

from app.domains.assessments.application.diagnostic_generator import DiagnosticMCQItem
from app.domains.assessments.application.exit_ticket_payload import exit_ticket_payload
from app.domains.assessments.domain.item_level import (
    labelled,
    largest_number,
    named_scale,
    reaches_scale,
)

_SMALL = {"A": "4,527", "B": "4,572", "C": "4,257", "D": "4,725"}
_LARGE = {"A": "3 billion", "B": "3,600 million", "C": "0.36 trillion", "D": "30 million"}


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("5,120,000,000", 5.12e9),
        ("0.36 trillion", 3.6e11),
        ("3,600 million", 3.6e9),
        ("Arrange 45,682 ; 12,395 ; 8,207.", 45682.0),
        ("₦435.01 billion", 4.3501e11),
        ("no numbers here", 0.0),
    ],
)
def test_the_largest_number_in_a_text_counts_a_scale_word(text: str, value: float) -> None:
    assert largest_number(text) == pytest.approx(value)


def test_an_objective_names_the_smallest_size_it_mentions() -> None:
    assert named_scale("Read, write and compare numbers in billions and trillions") == 1e9
    assert named_scale("Round numbers to the nearest thousand") == 1e3
    assert named_scale("Add fractions with a common denominator") is None


def test_a_set_reaches_the_size_its_objective_names_or_it_does_not() -> None:
    objective = "Read, write and compare numbers in billions and trillions"
    small = [("Which is larger?", _SMALL)]
    large = [("Arrange 3 billion, 3,600 million and 0.36 trillion.", _LARGE)]

    assert not reaches_scale(objective, small)
    assert reaches_scale(objective, [*small, *large])
    assert reaches_scale("Add fractions", small)


@pytest.mark.parametrize(
    ("stem", "label", "expected"),
    [
        ("Arrange 500.5 million, 50.5 billion and 0.055 trillion from smallest.", "easy", "medium"),
        ("Which number is larger: 0.08 trillion or 800 billion?", "easy", "medium"),
        ("Which number is larger: 4,302 or 4,320?", "easy", "easy"),
        ("Which number is larger: 3 billion or 4 billion?", "easy", "easy"),
        ("Arrange 36 million, 3.6 billion and 360 million.", "hard", "hard"),
        ("Which number is larger: 4,302 or 4,320?", "medium", "medium"),
    ],
)
def test_a_label_is_raised_to_what_the_stem_allows_and_never_lowered(
    stem: str, label: str, expected: str
) -> None:
    assert labelled(label, stem) == expected


def test_the_stored_item_carries_the_label_its_stem_allows() -> None:
    item = DiagnosticMCQItem(
        stem="Arrange 36 million, 3.6 billion and 360 million from smallest to largest.",
        options={"A": "36 million", "B": "360 million", "C": "3.6 billion", "D": "all equal"},
        correct_option="A",
        distractor_misconceptions={"B": "x_y", "C": "x_z", "D": "x_w"},
        difficulty="easy",
    )

    payload = exit_ticket_payload(
        item, subtopic_id="s", plan_version_id="p", lesson_objective_id="lop01"
    )

    assert payload["difficulty"] == "medium"
