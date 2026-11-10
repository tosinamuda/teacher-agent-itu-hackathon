"""The lesson note's check script: what its steps say to each other and what each must hold."""

from __future__ import annotations

from app.domains.content_engine.rules.lesson_note.across_steps import repeated_questions
from app.domains.content_engine.rules.lesson_note.review import review
from app.domains.content_engine.rules.lesson_note.rounding_taught import rounding_taught
from app.shared.json_types import JsonObject


def _draft(type: str, **parts: JsonObject) -> list[tuple[str, dict[str, object]]]:
    return [(step, dict(part)) for step, part in parts.items()]


def _asking(*questions: str) -> JsonObject:
    return {"questions_for_the_class": [{"question": q, "expected_answer": "x"} for q in questions]}


def test_a_question_asked_in_two_steps_is_told_to_the_step_that_is_not_the_evaluation() -> None:
    draft = _draft(
        "lesson-note",
        core1=_asking("What is 1/4 + 2/4?", "What is 3/8 + 2/8?"),
        evaluation=_asking("what is  1/4 + 2/4?"),
    )

    issues = repeated_questions(draft)

    assert len(issues) == 1
    assert issues[0].startswith("core1: 'What is 1/4 + 2/4?' is also asked in evaluation")


def test_a_worked_example_problem_asked_again_in_another_step_is_repeated() -> None:
    draft = _draft(
        "lesson-note",
        core1={"worked_examples": [{"problem": "60 cm x 8,000 steps"}]},
        core2=_asking("60 cm x 8,000 steps"),
    )

    assert [issue.split(":")[0] for issue in repeated_questions(draft)] == ["core2"]


def test_a_question_reworded_around_the_same_numbers_is_the_same_problem() -> None:
    draft = _draft(
        "lesson-note",
        core1=_asking(
            "A student's steps are 60 cm long. He takes 8,315 steps. Estimate the distance."
        ),
        evaluation=_asking("If a step is 60 cm and a student takes 8,315 steps, how far is that?"),
    )

    assert [issue.split(":")[0] for issue in repeated_questions(draft)] == ["core1"]


def test_questions_that_share_one_number_or_have_other_numbers_are_different_problems() -> None:
    draft = _draft(
        "lesson-note",
        core1=_asking("What is half of 10?", "A step is 60 cm; 1,000 steps. How far?"),
        evaluation=_asking("Is 10 even?", "A step is 60 cm; 8,315 steps. How far?"),
    )

    assert repeated_questions(draft) == []


def test_the_same_question_twice_in_one_step_or_distinct_questions_is_not_repeated() -> None:
    draft = _draft("lesson-note", core1=_asking("Q one", "Q one"), evaluation=_asking("Q two"))

    assert repeated_questions(draft) == []


def _worked(*lines: str) -> JsonObject:
    return {
        "worked_examples": [
            {
                "problem": "A step is 60 cm; 8,000 steps. Estimate the distance.",
                "solution": [{"working": line, "commentary": "c"} for line in lines],
                "answer": "x",
            }
        ]
    }


def test_a_note_that_asks_for_an_estimate_with_no_rounding_shown_or_practised_is_sent_back() -> (
    None
):
    draft = _draft(
        "lesson-note",
        core1={
            **_worked("$0.6 \\times 8000 = 4800$ m", "$4800$ m $= 4.8$ km"),
            **_asking("Find 0.6 x 4000 m"),
        },
        evaluation=_asking("A step is 60 cm; 8,315 steps. Approximately how far is the school?"),
    )

    issues = rounding_taught(draft)

    assert [issue.split(":")[0] for issue in issues] == ["core1", "core1"]
    assert "no worked example shows it" in issues[0]
    assert "no question before it practises" in issues[1]


def test_rounding_shown_in_a_worked_example_and_practised_before_the_evaluation_passes() -> None:
    draft = _draft(
        "lesson-note",
        core1={
            **_worked("$4.8$ km $\\approx 5$ km", "round to the nearest kilometre"),
            **_asking("Estimate 70 cm x 8,000 steps, rounding to the nearest km."),
        },
        evaluation=_asking("A step is 60 cm; 8,315 steps. Approximately how far is the school?"),
    )

    assert rounding_taught(draft) == []


def test_round_as_a_preposition_in_a_question_is_not_a_request_to_round() -> None:
    algebra = _draft(
        "lesson-note",
        core1=_asking("Put brackets round the first two terms of 3a + 2a - 4."),
        evaluation=_asking("The minus sign turns every sign inside the bracket round. Simplify."),
    )

    assert rounding_taught(algebra) == []


def test_a_note_that_never_asks_for_rounding_needs_none() -> None:
    plain = _draft("lesson-note", core1=_asking("What is 1/4 + 2/4?"), evaluation=_asking("Q"))

    assert rounding_taught(plain) == []


def _payload(**parts: JsonObject) -> dict[str, object]:
    sections = [{"unit_id": step, "label": step, "part": part} for step, part in parts.items()]
    return {"draft": {"type": "lesson-note", "sections": sections}, "source": None}


_ENOUGH = {"teaching_points": ["Place value of a digit depends on its position. " * 8]}


def test_a_step_with_too_little_to_teach_from_is_sent_back() -> None:
    faults = review(_payload(core1={"teaching_points": ["Place value."]}))

    assert len(faults) == 1
    assert faults[0].startswith("core1: the note holds 12 characters of text; add substance")


def test_a_step_that_leaves_a_second_thought_a_false_rule_or_a_wrong_rounding_is_sent_back() -> (
    None
):
    thoughts = {"teaching_points": [*_ENOUGH["teaching_points"], "Wait, that is not right."]}
    rule = {"teaching_points": [*_ENOUGH["teaching_points"], "The larger unit name wins."]}
    rounding = {"teaching_points": [*_ENOUGH["teaching_points"], "Round 7,500 to 7,000."]}

    assert "second thought" in review(_payload(core1=thoughts))[0]
    assert "larger unit name or leading digit" in review(_payload(core1=rule))[0]
    assert "7,500 rounds to 8,000" in review(_payload(core1=rounding))[0]


def test_a_note_with_enough_in_each_step_has_no_fault() -> None:
    assert review(_payload(core1=_ENOUGH, evaluation=_ENOUGH)) == []
