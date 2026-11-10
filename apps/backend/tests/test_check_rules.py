"""The rules of each content type find the faults a program can check in a draft."""

from __future__ import annotations

from app.domains.content_engine.rules import RULES
from app.shared.json_types import JsonObject

LONG = "Place value of a digit depends on its position in the number. " * 6


def _payload(source: JsonObject | None = None, **parts: JsonObject) -> JsonObject:
    sections = [{"unit_id": step, "label": step, "part": part} for step, part in parts.items()]
    return {"draft": {"type": "t", "sections": sections}, "source": source}


def test_a_thin_lesson_note_step_and_a_question_asked_twice_are_sent_back() -> None:
    asked = {"questions_for_the_class": [{"question": "What is 1/4 + 2/4?"}]}

    faults = RULES["check_lesson_note"](
        _payload(core1={**asked, "teaching_points": [LONG]}, evaluation=asked)
    )

    assert [fault.split(":")[0] for fault in faults] == ["evaluation", "core1"]
    assert "add substance" in faults[0]
    assert "is also asked in evaluation" in faults[1]


def test_a_thin_revision_note_section_is_sent_back() -> None:
    part = {
        "explanation": "Short.",
        "worked_examples": [{"problem": "1 + 1"}],
        "practice": [{"question": "q"}, {"question": "q"}],
    }

    faults = RULES["check_revision_note"](_payload(s1=part))

    assert [fault.split(";")[0].split(":")[1].strip() for fault in faults] == [
        "the explanation holds 6 characters",
        "give at least 2 worked examples, from simple to harder",
        "give at least 3 practice questions, each with its answer and a worked solution "
        "where the answer alone would not show the method",
        "two practice questions are the same",
    ]


def test_a_class_test_question_that_cannot_be_graded_or_is_below_its_scale_is_sent_back() -> None:
    question = {
        "stem": "Which is larger?",
        "options": {"a": "5", "b": "5", "c": "7", "d": "9"},
        "correct_option": "C",
        "distractors": [{"option": "A", "misconception_code": "Bad Code"}],
    }
    source: JsonObject = {"objectives_by_step": {"s1": "Compare numbers up to billions"}}

    faults = RULES["check_class_test"](_payload(source, s1={"questions": [question]}))

    assert faults == [
        "s1 question 1: the options must differ and the correct option must be one of A-D",
        "s1 question 1: give a misconception code for each wrong option: A, B, D",
        "s1 question 1: the misconception code 'Bad Code' for A is snake_case",
        "s1: the objective names numbers as large as 'Compare numbers up to billions': "
        "use that size in at least one question",
    ]


def test_a_well_formed_class_test_has_no_fault() -> None:
    question = {
        "stem": "What is 4 + 5?",
        "options": {"a": "8", "b": "9", "c": "10", "d": "11"},
        "correct_option": "B",
        "distractors": [
            {"option": option, "misconception_code": f"slip_{option.lower()}"} for option in "ACD"
        ],
    }

    assert RULES["check_class_test"](_payload(s1={"questions": [question]})) == []


def test_a_slide_without_speaker_notes_is_sent_back_when_the_draft_has_no_source() -> None:
    slide = {"title": "Adding", "points": [{"point": "A point"}], "speaker_notes": ""}

    faults = RULES["check_slide_deck"](_payload(core={"slides": [slide]}))

    assert faults == [
        "core: slide 1 needs speaker notes: what the teacher says and asks while it is up"
    ]
