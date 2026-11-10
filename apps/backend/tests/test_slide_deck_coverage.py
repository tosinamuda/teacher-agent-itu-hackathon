"""Every worked example of the approved note has a slide that starts from its problem."""

from __future__ import annotations

import pytest

from app.domains.content_engine.rules.slide_deck.coverage import (
    uncovered_examples,
    worked_problems,
)
from app.domains.content_engine.rules.slide_deck.evaluation_drawings import (
    revealing_drawings,
)
from app.domains.content_engine.rules.slide_deck.pictures import unpictured_rounding
from app.domains.content_engine.rules.slide_deck.problem_numbers import holds
from app.domains.content_engine.rules.slide_deck.question_coverage import (
    note_questions,
    uncovered_questions,
)
from app.domains.content_engine.rules.slide_deck.questions import evaluation_slide_issues
from app.domains.content_engine.rules.slide_deck.review import (
    review,
    slide_deck_issues,
)
from tests.slide_deck_support import deck, slide

NOTE = """#### Teaching points

- Add the lengths, then convert.

#### Worked examples

**1.**

**Problem.**

A ribbon is 45 cm long and another is 1.2 m long. Find their total length in metres.

**Solution.**

- $45\\text{ cm}=0.45\\text{ m}$ — Convert to metres.

**Answer.**

$1.65\\text{ m}$

**2.**

**Problem.**

A tank holds 2,500 litres and 3,750 litres run out. How much is left?

**Solution.**

- $2{,}500-3{,}750$ — Subtract.

**Answer.**

Left: $1{,}250$ litres

#### Questions for the class

**1.**

**Question.**

Convert 30 cm to metres.
"""

RIBBON = slide(
    "A ribbon is 45 cm long and another is 1.2 m long. Find their total length in metres.",
    "$45\\text{ cm}=0.45\\text{ m}$",
    "$1.65\\text{ m}$",
)
TANK = slide(
    "A tank holds 2,500 litres and 3,750 litres run out. How much is left?",
    "$2{,}500-3{,}750$",
    title="Tank",
)


def test_the_problems_of_a_notes_worked_examples_are_read_in_order() -> None:
    assert worked_problems(NOTE) == [
        "A ribbon is 45 cm long and another is 1.2 m long. Find their total length in metres.",
        "A tank holds 2,500 litres and 3,750 litres run out. How much is left?",
    ]
    assert worked_problems("#### Teaching points\n\n- Nothing worked.") == []


def test_a_deck_whose_slides_start_from_each_worked_example_passes() -> None:
    assert uncovered_examples(deck(core=[RIBBON, TANK]), {"core": NOTE}) == []


def test_a_worked_example_with_no_slide_is_named_for_the_writer() -> None:
    issues = uncovered_examples(deck(core=[RIBBON]), {"core": NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("core: the note's worked example 'A tank holds 2,500 litres")
    assert "has no slide" in issues[0]


def test_a_slide_that_works_the_example_without_stating_its_problem_is_sent_back() -> None:
    working = slide(
        "Take away the litres that ran out",
        "$2{,}500-3{,}750$",
        "Left: $1{,}250$ litres",
        title="Tank: 2,500 and 3,750",
    )

    issues = uncovered_examples(deck(core=[RIBBON, working]), {"core": NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("core: slide 2 works the example")
    assert "make its first point the note's question" in issues[0]


def test_a_shortened_problem_is_not_the_question_in_full() -> None:
    label = slide("Ribbons: 45 cm, 1.2 m", "$1.65\\text{ m}$")

    issues = uncovered_examples(deck(core=[label, TANK]), {"core": NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("core: slide 1 starts the example 'A ribbon is 45 cm")
    assert "with a shortened problem" in issues[0]


def test_only_the_first_point_of_a_slide_may_run_to_a_whole_problem() -> None:
    long = " ".join(["word"] * 25)

    issues = slide_deck_issues(deck(core=[slide(long, long)]))

    assert len(issues) == 1
    assert "a point of 25 words runs past 12" in issues[0]


def test_the_evaluation_and_a_step_with_no_worked_examples_are_not_held_to_it() -> None:
    note = {"core": NOTE, "evaluation": NOTE, "intro": "#### Teaching points\n\n- Recall."}

    draft = deck(intro=[slide("Recall")], core=[RIBBON, TANK], evaluation=[slide("Another one")])

    assert uncovered_examples(draft, note) == []


def test_an_example_in_other_units_is_still_the_same_example() -> None:
    metres = slide(
        "A ribbon is 0.45 m long and another is 1.2 m long. Find their total length in metres.",
        "$1.65\\text{ m}$",
    )

    assert uncovered_examples(deck(core=[metres, TANK]), {"core": NOTE}) == []


@pytest.mark.parametrize(
    ("held", "problem", "expected"),
    [
        ("0.6 m, 8,315 steps", "60 cm, 8,315 steps", True),
        ("60 cm, 8,315 steps", "60 cm, 8,315 steps", True),
        ("60 cm, 8,000 steps", "60 cm, 8,315 steps", False),
        ("0.5 km, 1 km", "50 cm, 10,000 steps", False),
        ("50 cm, 10,000 steps", "50 cm, 10,000 steps", True),
    ],
)
def test_numbers_are_held_as_written_or_in_another_unit_when_they_are_specific(
    held: str, problem: str, expected: bool
) -> None:
    assert holds(held, problem) is expected


def test_the_evaluations_problem_in_another_unit_is_still_rehearsed() -> None:
    draft = deck(
        core=[slide("Step length 0.6 m, steps 8,315", "Estimate the distance")],
        evaluation=[slide("Step length 60 cm, steps 8,315", "Estimate the distance")],
    )

    assert len(evaluation_slide_issues(draft)) == 1


def test_the_review_reads_the_approved_note_of_the_lesson() -> None:
    sections = [{"unit_id": "core", "part": {"slides": [RIBBON]}}]
    payload = {
        "draft": {"sections": sections},
        "source": {"note": {"core": NOTE}, "objectives": []},
    }

    issues = review(payload)

    assert len(issues) == 1 and "has no slide" in issues[0]


ROUNDING_NOTE = NOTE.replace("$1.65\\text{ m}$", "$1.65\\text{ m}\\approx 2\\text{ m}$")


def test_a_step_that_rounds_in_a_worked_example_needs_a_drawing() -> None:
    issues = unpictured_rounding(deck(core=[RIBBON, TANK]), {"core": ROUNDING_NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("core: the note rounds a number")
    assert "number line" in issues[0]


def test_the_note_rounding_a_decimal_tells_the_writer_the_marks_to_write() -> None:
    note = NOTE.replace("$1.65\\text{ m}$", "$6.9\\text{ km}\\approx 7\\text{ km}$")

    issues = unpictured_rounding(deck(core=[RIBBON, TANK]), {"core": note})

    assert issues[0].endswith("; for 6.9 write \\foreach \\x/\\label in {0/6, 9/6.9, 10/7}")


def _with_comment(comment: str) -> str:
    return NOTE.replace("Convert to metres.", comment)


def test_round_as_a_preposition_is_not_rounding() -> None:
    for comment in (
        "Put brackets round the multiplication and the division.",
        "The minus before the bracket turns every sign inside it round.",
    ):
        assert (
            unpictured_rounding(deck(core=[RIBBON, TANK]), {"core": _with_comment(comment)}) == []
        )


def test_round_as_a_verb_is_rounding() -> None:
    for comment in (
        "Round 6.87 to the nearest whole number.",
        "Round $6.87$ here.",
        "Round up, because the next digit is 5.",
        "Rounded to one decimal place.",
        "Rounding gives 7.",
    ):
        issues = unpictured_rounding(deck(core=[RIBBON, TANK]), {"core": _with_comment(comment)})

        assert len(issues) == 1, comment


def test_a_drawn_step_a_step_that_does_not_round_and_the_evaluation_pass() -> None:
    drawn = {**RIBBON, "figure": "\\begin{tikzpicture}\\draw (0,0) -- (1,0);\\end{tikzpicture}"}

    assert unpictured_rounding(deck(core=[drawn, TANK]), {"core": ROUNDING_NOTE}) == []
    assert unpictured_rounding(deck(core=[RIBBON, TANK]), {"core": NOTE}) == []
    assert unpictured_rounding(deck(evaluation=[RIBBON]), {"evaluation": ROUNDING_NOTE}) == []


QUESTION_NOTE = """#### Questions for the class

**1.**

**Question.**

A ribbon is 45 cm long and another is 1.2 m long. Find their total length in metres.

**Expected answer.**

$1.65\\text{ m}$

**2.**

**Question.**

Why might we prefer an estimate rather than a precise measurement?

**Expected answer.**

Estimates are faster.

#### On the board

Total length.
"""


def test_the_questions_of_a_note_are_read_in_order() -> None:
    assert note_questions(QUESTION_NOTE) == [
        "A ribbon is 45 cm long and another is 1.2 m long. Find their total length in metres.",
        "Why might we prefer an estimate rather than a precise measurement?",
    ]


def test_a_question_the_note_puts_to_the_class_but_no_slide_does_is_told() -> None:
    note = {"evaluation": QUESTION_NOTE}
    ribbon = slide("A ribbon is 45 cm long.", "Another is 1.2 m long. Find the total length.")
    why = slide("Why might we prefer an estimate rather than a precise measurement?")

    assert uncovered_questions(deck(evaluation=[ribbon, why]), note) == []
    issues = uncovered_questions(deck(evaluation=[ribbon]), note)
    assert len(issues) == 1
    assert issues[0].startswith("evaluation: the note's question 'Why might we prefer an")
    assert uncovered_questions(deck(evaluation=[why]), note)[0].startswith(
        "evaluation: the note's question 'A ribbon is 45 cm"
    )


def test_a_question_with_one_number_is_not_met_by_another_slide_that_has_the_number() -> None:
    note = {
        "core": "#### Questions for the class\n\n**1.**\n\n**Question.**\n\nConvert a step"
        " length of 75 cm to metres.\n\n**Expected answer.**\n\n0.75 m\n"
    }
    example = slide("A student's steps are 75 cm long. He takes 9,200 steps to the park.")

    assert len(uncovered_questions(deck(core=[example]), note)) == 1
    asked = slide("Convert a step length of 75 cm to metres.")
    assert uncovered_questions(deck(core=[example, asked]), note) == []


def test_a_question_with_one_number_is_told_when_a_slide_changes_the_number() -> None:
    note = {
        "core": "#### Questions for the class\n\n**1.**\n\n**Question.**\n\nConvert a step"
        " length of 75 cm to metres.\n\n**Expected answer.**\n\n0.75 m\n"
    }
    changed = slide("An athlete's step length is 90 cm. Convert it to metres.")

    issues = uncovered_questions(deck(core=[changed]), note)
    assert len(issues) == 1 and "with the numbers the note gives" in issues[0]


def test_an_evaluation_drawing_with_numbers_no_question_states_is_sent_back() -> None:
    note = {"evaluation": QUESTION_NOTE}
    working = (
        "\\begin{tikzpicture}\\draw (0,0) -- (10,0);"
        "\\node[above=6pt] at (9.8,0) {\\Huge 1.65 m};\\end{tikzpicture}"
    )
    stated = (
        "\\begin{tikzpicture}\\draw (0,0) -- (10,0);"
        "\\node[above=6pt] at (4,0) {\\Huge 45 cm};\\end{tikzpicture}"
    )

    issues = revealing_drawings(deck(evaluation=[{**slide("A"), "figure": working}]), note)

    assert len(issues) == 1 and "the drawing shows 1.65" in issues[0]
    assert revealing_drawings(deck(evaluation=[{**slide("A"), "figure": stated}]), note) == []
    assert (
        revealing_drawings(deck(core=[{**slide("A"), "figure": working}]), {"core": QUESTION_NOTE})
        == []
    )
