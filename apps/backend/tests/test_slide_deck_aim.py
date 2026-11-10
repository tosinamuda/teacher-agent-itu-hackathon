"""The introduction states the lesson's objective as what the class will be able to do."""

from __future__ import annotations

from app.domains.content_engine.rules.slide_deck.aim import unstated_aim
from tests.slide_deck_support import deck, slide

OBJECTIVES = [
    "Students will be able to estimate distances by using step length and number of steps."
]
OPENING = slide("Can you give an everyday situation where you estimate a distance?")


def test_an_introduction_that_states_the_aim_in_the_learners_words_has_no_fault() -> None:
    aim = slide("By the end, I can estimate a distance using my step length and number of steps.")

    assert unstated_aim(deck(intro=[OPENING, aim]), OBJECTIVES) == []


def test_an_introduction_with_no_aim_slide_is_sent_back_with_the_objective() -> None:
    issues = unstated_aim(deck(intro=[OPENING]), OBJECTIVES)

    assert len(issues) == 1
    assert issues[0].startswith("intro: none of the first slides states the aim")
    assert "Students will be able to estimate distances" in issues[0]


def test_an_aim_in_the_teachers_words_is_not_in_the_learners_words() -> None:
    focus = slide("Today we focus on estimating distances, as we do in everyday life.")

    assert len(unstated_aim(deck(intro=[OPENING, focus]), OBJECTIVES)) == 1


def test_an_aim_about_something_else_does_not_state_the_objective() -> None:
    other = slide("By the end, I can name the capital of every state.")

    assert len(unstated_aim(deck(intro=[OPENING, other]), OBJECTIVES)) == 1


def test_a_lesson_with_no_objective_needs_only_the_learners_words() -> None:
    assert unstated_aim(deck(intro=[slide("We will be able to estimate a distance.")]), []) == []
    assert len(unstated_aim(deck(intro=[OPENING]), [])) == 1


def test_only_the_introduction_states_an_aim() -> None:
    assert (
        unstated_aim(deck(core=[slide("A rule")], evaluation=[slide("A question")]), OBJECTIVES)
        == []
    )


def test_an_aim_that_comes_after_the_content_is_sent_back() -> None:
    aim = slide("By the end, I can estimate a distance using my step length and number of steps.")
    content = [slide("What an estimate is"), slide("Why estimate?")]

    assert unstated_aim(deck(intro=[OPENING, aim, *content]), OBJECTIVES) == []
    assert len(unstated_aim(deck(intro=[OPENING, *content, aim]), OBJECTIVES)) == 1


def test_an_aim_that_leaves_out_the_objectives_own_words_is_sent_back() -> None:
    vague = slide("By the end, I can estimate a distance by quick approximate calculation.")

    issues = unstated_aim(deck(intro=[OPENING, vague]), OBJECTIVES)

    assert len(issues) == 1 and "using the objective's own words" in issues[0]


def test_an_aim_that_drops_part_of_the_objective_is_sent_back() -> None:
    partial = slide("By the end, I can estimate distances using step length.")

    issues = unstated_aim(deck(intro=[OPENING, partial]), OBJECTIVES)

    assert len(issues) == 1
    assert issues[0].endswith("the aim leaves out: number")
