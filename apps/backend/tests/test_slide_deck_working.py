"""A worked example's slide shows every line of the note's working."""

from __future__ import annotations

from app.domains.content_engine.rules.slide_deck.working import (
    crowded_slides,
    missing_working,
    reasons_on_slides,
    worked_lines,
)
from tests.slide_deck_support import deck, slide

NOTE = """#### Worked examples

**1.**

**Problem.**

A student's steps are 75 cm long. He takes 9,200 steps to the park. Estimate the distance.

**Solution.**

- $0.75\\text{ m}=\\frac{75\\text{ cm}}{100}$ — Convert step length to metres.
- $0.75\\text{ m}\\times 9{,}200 = 6{,}900\\text{ m}$ — Multiply by the number of steps.
- $6{,}900\\text{ m}=6.9\\text{ km}$ — Convert metres to kilometres.

**Answer.**

Approximately $6.9\\text{ km}$

**2.**

**Problem.**

A step is 0.5 m long and a pupil takes 9,200 steps. Estimate the distance.

**Solution.**

- Think about the steps. — No numbers here.
- $0.5\\text{ m}\\times 9{,}200 = 4{,}600\\text{ m}$ — Multiply.

**Answer.**

$4.6\\text{ km}$

#### Questions for the class
"""
PROBLEM = (
    "A student's steps are 75 cm long. He takes 9,200 steps to the park. Estimate the distance."
)
FULL = [
    PROBLEM,
    "$0.75\\text{ m}=\\frac{75\\text{ cm}}{100}$",
    "$0.75\\text{ m}\\times 9{,}200 = 6{,}900\\text{ m}$",
    "$6{,}900\\text{ m}=6.9\\text{ km}$",
]
SECOND = slide(
    "A step is 0.5 m long and a pupil takes 9,200 steps. Estimate the distance.",
    "$0.5\\text{ m}\\times 9{,}200 = 4{,}600\\text{ m}$",
)


def test_the_lines_of_each_worked_solution_are_read_with_their_problem() -> None:
    lines = worked_lines(NOTE)

    assert [problem for problem, _ in lines] == [PROBLEM, SECOND["points"][0]["point"]]
    assert len(lines[0][1]) == 3 and lines[1][1][0] == "Think about the steps. — No numbers here."


def test_a_slide_with_every_line_of_the_working_has_no_fault() -> None:
    assert missing_working(deck(core=[slide(*FULL), SECOND]), {"core": NOTE}) == []


def test_a_slide_that_drops_the_first_line_is_sent_back_with_the_line() -> None:
    dropped = slide(FULL[0], FULL[2], FULL[3])

    issues = missing_working(deck(core=[dropped, SECOND]), {"core": NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("core: slide 1 works the example")
    assert "leaves out the note's line '0.75 m = (75 cm)/100'" in issues[0]


def test_two_lines_written_as_one_point_hold_both() -> None:
    merged = slide(
        FULL[0], FULL[1], "$0.75\\text{ m}\\times 9{,}200 = 6{,}900\\text{ m} = 6.9\\text{ km}$"
    )

    assert missing_working(deck(core=[merged, SECOND]), {"core": NOTE}) == []


def test_the_evaluation_and_an_example_with_no_slide_are_left_to_the_other_checks() -> None:
    assert missing_working(deck(core=[SECOND]), {"core": NOTE}) == []
    assert missing_working(deck(evaluation=[slide(FULL[0])]), {"evaluation": NOTE}) == []


def test_a_working_point_that_carries_the_notes_reason_is_sent_back() -> None:
    reasoned = slide(
        FULL[0],
        FULL[1] + " — convert step length to metres",
        FULL[2],
        FULL[3],
    )

    issues = reasons_on_slides(deck(core=[reasoned, SECOND]), {"core": NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("core: slide 1 writes the reason after the line")
    assert "speaker notes" in issues[0]


def test_a_reason_worded_without_the_dash_is_still_the_reason() -> None:
    reasoned = slide(FULL[0], FULL[1] + " (convert step length to metres)", FULL[2], FULL[3])

    assert len(reasons_on_slides(deck(core=[reasoned, SECOND]), {"core": NOTE})) == 1


def test_working_lines_alone_carry_no_reason() -> None:
    assert reasons_on_slides(deck(core=[slide(*FULL), SECOND]), {"core": NOTE}) == []


def test_a_teaching_slide_of_five_points_is_sent_back_but_a_worked_example_is_not() -> None:
    rule = slide("One", "Two", "Three", "Four", "Five", title="The rule")

    issues = crowded_slides(deck(core=[slide(*FULL, "$6.9\\text{ km}$"), rule]), {"core": NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("core: slide 2 has 5 points")
    assert crowded_slides(deck(core=[slide("One", "Two", "Three", "Four")]), {"core": NOTE}) == []
    assert crowded_slides(deck(evaluation=[rule]), {"evaluation": NOTE}) == []


def test_the_numbers_of_a_reason_are_not_numbers_the_slide_must_show() -> None:
    note = NOTE.replace(
        "Multiply by the number of steps.", "Multiply by the 9,200 steps and then by 2."
    ).replace("Convert step length to metres.", "Divide by 100 and check 5 digits.")

    assert missing_working(deck(core=[slide(*FULL), SECOND]), {"core": note}) == []


NOTE_WITHOUT_NUMBERS = """#### Worked examples

**1.**

**Problem.**

Name the type of each noun in the sentence 'The trader sold a bunch of bananas in Ibadan.'

**Solution.**

- $\\text{trader}\\ \\rightarrow\\ \\text{common}$ — trader names any trader, so it is common.
- $\\text{Ibadan}\\ \\rightarrow\\ \\text{proper}$ — Ibadan names one place, so it is proper.

**Answer.**

Trader is a common noun and Ibadan is a proper noun.

#### Questions for the class
"""


def test_an_example_with_no_numbers_has_no_slide_the_working_checks_can_tell_it_by() -> None:
    summary = slide(
        "Common noun: any one of a class — trader, market.",
        "Proper noun: one particular one — Chimaka, Ibadan.",
    )
    steps = deck(core=[summary])
    note = {"core": NOTE_WITHOUT_NUMBERS}

    assert reasons_on_slides(steps, note) == []
    assert missing_working(steps, note) == []
