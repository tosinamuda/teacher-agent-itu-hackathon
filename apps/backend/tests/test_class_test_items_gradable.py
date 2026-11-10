"""A class test keeps only items that grade a right answer as right, drawing afresh for more."""

from __future__ import annotations

import asyncio

import pytest

from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.assessments.application.diagnostic_generator import DiagnosticMCQItem
from app.domains.assessments.application.diagnostic_service import (
    ClassTestLesson,
    DiagnosticGenerationError,
    DiagnosticGenerationService,
)
from app.domains.assessments.application.item_reader import ItemToRead
from app.domains.assessments.domain.item_checks import is_sound, says_what_it_asks
from app.shared.session_plan_view import LessonPlanObjectiveView


def _item(stem: str, options: dict[str, str], correct: str = "B") -> DiagnosticMCQItem:
    return DiagnosticMCQItem(
        stem=stem,
        options=options,
        correct_option=correct,
        distractor_misconceptions={},
        difficulty="easy",
    )


_SOUND = {"A": "12,000,000,000", "B": "12,000,000,000,000", "C": "1,200", "D": "120"}
#: The run's Q6: the answer written out twice, under B and under C.
_REPEATED = {
    "A": "five trillion twenty-three million four thousand seven",
    "B": "five trillion twenty-three billion four million seven thousand",
    "C": "Five trillion  twenty-three billion four million seven thousand",
    "D": "five trillion two hundred three billion four million seven thousand",
}


def test_an_item_whose_options_repeat_or_lack_the_answer_is_not_gradable() -> None:
    assert is_sound(_SOUND, "B")
    assert not is_sound(_REPEATED, "B")
    assert not is_sound(_SOUND, "E")
    assert not is_sound({**_SOUND, "D": "  "}, "B")


#: Options that differ by a capital letter inside them: the question is about capital letters.
_CAPITALS = {
    "A": "My uncle lives in Abuja, the capital of Nigeria.",
    "B": "My uncle lives in abuja, the capital of nigeria.",
    "C": "My uncle lives in abuja, the capital of Nigeria.",
    "D": "My uncle lives in Abuja, the Capital of Nigeria.",
}


def test_options_that_differ_by_a_capital_inside_them_are_different_answers() -> None:
    assert is_sound(_CAPITALS, "A")
    assert not is_sound({**_CAPITALS, "B": "my uncle lives in Abuja, the capital of Nigeria."}, "A")


class _Draws:
    """Hands out one scripted list of items per draw."""

    def __init__(self, *draws: list[DiagnosticMCQItem]) -> None:
        self.draws = list(draws)
        self.asked: list[int] = []

    async def generate(self, *, draw: int, **_: object) -> list[DiagnosticMCQItem]:
        self.asked.append(draw)
        return self.draws[draw] if draw < len(self.draws) else []


_LESSON = "A proper fraction has numerator < denominator; improper, numerator ≥ denominator."


class _Reader:
    """Answers each item as scripted by its stem; unscripted items read as keyed."""

    def __init__(self, reads: dict[str, set[str]] | None = None) -> None:
        self.reads = reads or {}
        self.read: list[ItemToRead] = []

    async def correct_options(self, item: ItemToRead) -> set[str]:
        self.read.append(item)
        return self.reads.get(item.stem, {"B"})


def _payloads(
    generator: _Draws, reader: _Reader | None = None, objective: str = "x"
) -> list[dict[str, object]]:
    service = DiagnosticGenerationService(generator=generator, reader=reader)  # type: ignore[arg-type]
    return asyncio.run(
        service._build_item_payloads(
            specification=seed_specification(ArtefactType.DIAGNOSTIC.value),
            objectives=[
                LessonPlanObjectiveView(lesson_objective_id="lop01", objective_text=objective)
            ],
            subtopic_id="sub",
            plan_version_id="LPV-1",
            lesson=ClassTestLesson(
                taught=_LESSON, subject="Mathematics", grade="JSS1", topic="Fractions"
            ),
            item_count=2,
        )
    )


def test_a_sound_first_draw_is_all_that_is_asked_for() -> None:
    generator = _Draws([_item("one", _SOUND), _item("two", _SOUND)])

    payloads = _payloads(generator)

    assert [p["stem"] for p in payloads] == ["one", "two"]
    assert generator.asked == [0]


def test_an_ungradable_item_is_replaced_from_a_fresh_draw() -> None:
    generator = _Draws(
        [_item("one", _SOUND), _item("repeats", _REPEATED)],
        [_item("one", _SOUND), _item("three", _SOUND)],
    )

    payloads = _payloads(generator)

    assert [p["stem"] for p in payloads] == ["one", "three"]
    assert generator.asked == [0, 1]


def test_an_objective_with_no_gradable_item_after_every_draw_fails_the_test() -> None:
    generator = _Draws(*[[_item("repeats", _REPEATED)]] * 3)

    with pytest.raises(DiagnosticGenerationError, match="objective_has_no_gradable_items"):
        _payloads(generator)
    assert generator.asked == [0, 1, 2]


_FRACTIONS = {"A": "5/6", "B": "8/5", "C": "4/4", "D": "2/3"}


def test_an_item_a_second_reader_finds_two_answers_to_is_replaced() -> None:
    """Staging's Q1: 8/5 keyed as the one improper fraction, while 4/4 is improper too."""
    generator = _Draws(
        [_item("Which is an improper fraction?", _FRACTIONS), _item("two", _SOUND)],
        [_item("three", _SOUND)],
    )
    reader = _Reader({"Which is an improper fraction?": {"B", "C"}})

    payloads = _payloads(generator, reader)

    assert [p["stem"] for p in payloads] == ["two", "three"]
    assert generator.asked == [0, 1]


def test_the_reader_is_given_the_lesson_and_never_the_key() -> None:
    reader = _Reader()

    _payloads(_Draws([_item("one", _SOUND), _item("two", _SOUND)]), reader)

    assert [item.stem for item in reader.read] == ["one", "two"]
    assert {item.lesson for item in reader.read} == {_LESSON}
    assert not any(hasattr(item, "correct_option") for item in reader.read)


def test_an_item_whose_key_the_reader_rejects_is_replaced() -> None:
    generator = _Draws([_item("one", _SOUND), _item("wrong key", _SOUND)], [_item("three", _SOUND)])

    payloads = _payloads(generator, _Reader({"wrong key": {"A"}}))

    assert [p["stem"] for p in payloads] == ["one", "three"]


def test_an_item_that_fails_the_shape_check_is_never_read() -> None:
    reader = _Reader()

    _payloads(
        _Draws([_item("repeats", _REPEATED), _item("one", _SOUND), _item("two", _SOUND)]), reader
    )

    assert [item.stem for item in reader.read] == ["one", "two"]


def test_a_stem_that_leaves_out_the_numbers_it_asks_about_is_refused() -> None:
    options = {
        "A": "4,523; 45,023",
        "B": "45,023; 4,523",
        "C": "45,236; 4,523",
        "D": "4,523; 45,236",
    }
    assert not says_what_it_asks(
        "Arrange the following three numbers from smallest to largest:", options
    )
    assert says_what_it_asks("Arrange 45,236; 4,523 and 45,023 from smallest to largest.", options)
    assert says_what_it_asks(
        "Arrange 36 million, 3.6 billion and 360 million from smallest.", options
    )
    assert says_what_it_asks(
        "Which of the following lists the numbers in order from largest to smallest?", options
    )
    both = {"A": "4,527", "B": "Both numbers are equal", "C": "4,572", "D": "4,257"}
    assert not says_what_it_asks("Which of the following numbers is larger?", both)
    assert says_what_it_asks("Which number is larger: 4,527 or 4,572?", both)
    assert says_what_it_asks("Which of the following numbers is the greatest?", _SOUND)
    embedded = "Which is true?\n\nA) 3,456 is larger than 2,987\nB) 2,987 is larger than 3,456"
    assert not says_what_it_asks(embedded, {"A": "x", "B": "y", "C": "z", "D": "w"})


def test_the_pipeline_draws_again_for_an_item_whose_stem_names_no_numbers() -> None:
    options = {"A": "1", "B": "2", "C": "3", "D": "4"}
    bare = _item("Arrange the following numbers from smallest to largest:", options)
    whole = _item("Arrange 3, 1 and 2 from smallest to largest.", options)
    generator = _Draws([bare, bare], [whole, _item("Arrange 9, 7 and 8 from smallest.", options)])

    payloads = _payloads(generator)

    assert [p["stem"] for p in payloads] == [
        "Arrange 3, 1 and 2 from smallest to largest.",
        "Arrange 9, 7 and 8 from smallest.",
    ]


def test_a_later_draw_brings_the_set_up_to_the_size_the_objective_names() -> None:
    small = {"A": "4,527", "B": "4,572", "C": "4,257", "D": "4,725"}
    large = {"A": "3 billion", "B": "3,600 million", "C": "0.36 trillion", "D": "30 million"}
    generator = _Draws(
        [
            _item("Which is larger, 4,527 or 4,572?", small),
            _item("Which is larger, 4,257 or 4,725?", small),
        ],
        [_item("Which is larger, 3 billion or 30 million?", large)],
    )

    payloads = _payloads(generator, objective="Compare numbers in billions and trillions")

    assert [p["stem"] for p in payloads] == [
        "Which is larger, 4,527 or 4,572?",
        "Which is larger, 3 billion or 30 million?",
    ]
    assert generator.asked == [0, 1]


def test_a_set_that_never_reaches_the_size_is_still_kept_after_the_draws() -> None:
    small = {"A": "4,527", "B": "4,572", "C": "4,257", "D": "4,725"}
    items = [
        _item("Which is larger, 4,527 or 4,572?", small),
        _item("Which is larger, 4,257 or 4,725?", small),
    ]
    generator = _Draws(items, items, items)

    payloads = _payloads(generator, objective="Compare numbers in billions and trillions")

    assert len(payloads) == 2
    assert generator.asked == [0, 1, 2]
