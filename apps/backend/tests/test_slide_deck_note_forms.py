"""A worked example is read from a note written in either form, and an unreadable one is said."""

from __future__ import annotations

from app.domains.content_engine.rules.slide_deck.coverage import (
    uncovered_examples,
    unreadable_examples,
)
from app.domains.content_engine.rules.slide_deck.note_examples import (
    has_unreadable_examples,
    worked_examples,
    worked_text,
)
from app.domains.content_engine.rules.slide_deck.working import (
    crowded_slides,
    missing_working,
)
from tests.slide_deck_support import deck, slide

#: A note in the form notes were first written in, as the lesson note of "Fractions - 1" has it.
FIRST_FORM = r"""#### Convert mixed fractions to improper fractions

- Recall that a mixed number consists of a whole number and a proper fraction.

#### Example 1.

Convert \(5\frac{3}{4}\) to an improper fraction.

**Solution**

1. Identify the whole number (5) and the fraction \(\frac{3}{4}\).
2. Multiply the whole number by the denominator: \(5 \times 4 = 20\).
3. Add the numerator: \(20 + 3 = 23\).
4. Write the result over the original denominator: \(\frac{23}{4}\).
\[\therefore 5\frac{3}{4}=\frac{23}{4}\]

#### Questions for the class
"""
PROBLEM = r"Convert $5\frac{3}{4}$ to an improper fraction."
#: The slide the agent wrote for it: the question, then each line of the working.
EXAMPLE_SLIDE = slide(
    PROBLEM,
    r"Identify the whole number 5 and the fraction $\frac{3}{4}$.",
    r"Multiply the whole number by the denominator: $5 \times 4 = 20$.",
    r"Add the numerator: $20 + 3 = 23$.",
    r"Write the result over the original denominator: $\therefore 5\frac{3}{4}=\frac{23}{4}$.",
    title="Example 1",
)


def test_an_example_in_the_first_form_is_read_with_its_problem_and_numbered_working() -> None:
    [example] = worked_examples(FIRST_FORM)

    assert example.problem == r"Convert $5\frac{3}{4}$ to an improper fraction."
    assert len(example.lines) == 4
    assert example.lines[2].startswith("Add the numerator")


def test_the_text_of_the_examples_is_the_example_and_not_the_teaching_points() -> None:
    text = worked_text(FIRST_FORM)

    assert "Add the numerator" in text
    assert "Recall that a mixed number" not in text


def test_a_slide_that_works_a_first_form_example_is_not_capped_as_a_teaching_slide() -> None:
    slides = deck(step02=[EXAMPLE_SLIDE])

    assert crowded_slides(slides, {"step02": FIRST_FORM}) == []
    assert missing_working(slides, {"step02": FIRST_FORM}) == []
    assert uncovered_examples(slides, {"step02": FIRST_FORM}) == []


def test_a_teaching_slide_with_five_points_is_still_capped() -> None:
    five = slide(*[f"Point number {n} of the idea" for n in range(5)], title="The idea")

    [issue] = crowded_slides(deck(step02=[five]), {"step02": FIRST_FORM})

    assert issue.startswith("step02: slide 1 has 5 points")


def test_an_example_the_checks_cannot_read_is_said_for_its_step() -> None:
    broken = "#### Example 1.\n\nConvert 5 3/4 to an improper fraction. The answer is 23/4.\n"

    assert has_unreadable_examples(broken)
    [issue] = unreadable_examples(deck(step02=[EXAMPLE_SLIDE]), {"step02": broken})
    assert issue.startswith("step02: the note works examples in a form these checks cannot read")


def test_a_note_with_no_examples_or_readable_ones_is_not_called_unreadable() -> None:
    assert not has_unreadable_examples("#### Teaching points\n\n- Nothing worked here.")
    assert not has_unreadable_examples(FIRST_FORM)
    assert unreadable_examples(deck(step02=[EXAMPLE_SLIDE]), {"step02": FIRST_FORM}) == []
