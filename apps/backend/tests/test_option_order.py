"""A generated item's answer is moved off A, and every option keeps its text and its code."""

from __future__ import annotations

from collections import Counter

from app.domains.assessments.domain.option_order import placed

OPTIONS = {"A": "29/6", "B": "30/6", "C": "24/5", "D": "5/6"}
CODES = {"B": "add_denominator", "C": "swap_parts", "D": "ignore_whole"}


def test_the_answer_and_each_wrong_option_keep_their_text_and_code() -> None:
    result = placed(OPTIONS, "A", CODES, stem="Convert 4 5/6 to an improper fraction.")

    assert result.options[result.correct_option] == "29/6"
    assert sorted(result.options.values()) == sorted(OPTIONS.values())
    assert result.correct_option not in result.misconceptions
    assert {result.options[letter]: code for letter, code in result.misconceptions.items()} == {
        "30/6": "add_denominator",
        "24/5": "swap_parts",
        "5/6": "ignore_whole",
    }


def test_the_same_item_is_always_placed_the_same_way() -> None:
    stem = "Convert 22/5 to a mixed number."

    assert placed(OPTIONS, "A", CODES, stem=stem) == placed(OPTIONS, "A", CODES, stem=stem)


def test_answers_written_first_are_spread_across_the_letters() -> None:
    answers = Counter(
        placed(OPTIONS, "A", CODES, stem=f"Item {n}").correct_option for n in range(400)
    )

    assert set(answers) == {"A", "B", "C", "D"}
    assert min(answers.values()) > 60
