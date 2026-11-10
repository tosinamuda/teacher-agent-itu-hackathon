"""The introduction opens with the question the note puts to the class."""

from __future__ import annotations

from app.domains.content_engine.rules.slide_deck.opening import unopened_lesson
from tests.slide_deck_support import deck, slide

NOTE = """#### Questions for the class

**1.**

**Question.**

Can you give an everyday situation where you estimate a distance?

**Expected answer.**

How far home is from school.

**2.**

**Question.**

Why might we prefer an estimate rather than a precise measurement?

**Expected answer.**

It is faster.
"""
OPENING = slide("Can you give an everyday situation where you estimate a distance?")
AIM = slide("By the end, I can estimate a distance using my step length.")
IDEA = slide("A field is about three football-pitch lengths.")


def test_an_introduction_that_opens_with_the_notes_first_question_has_no_fault() -> None:
    assert unopened_lesson(deck(intro=[OPENING, AIM, IDEA]), {"intro": NOTE}) == []


def test_an_introduction_that_opens_with_something_else_is_sent_back_with_the_question() -> None:
    issues = unopened_lesson(deck(intro=[IDEA, OPENING, AIM]), {"intro": NOTE})

    assert len(issues) == 1
    assert issues[0].startswith("intro: the first slide must put the note's first question")
    assert "Can you give an everyday situation" in issues[0]


def test_the_second_question_does_not_open_the_lesson() -> None:
    why = slide("Why might we prefer an estimate rather than a precise measurement?")

    assert len(unopened_lesson(deck(intro=[why, OPENING]), {"intro": NOTE})) == 1


def test_only_the_introduction_with_a_question_is_held_to_it() -> None:
    assert unopened_lesson(deck(intro=[IDEA]), {"intro": "#### Teaching points\n\n- Recall."}) == []
    assert unopened_lesson(deck(core=[IDEA]), {"core": NOTE}) == []
