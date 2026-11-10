"""A lesson note carries no record ids and no second thoughts, and a naira escape decodes."""

from __future__ import annotations

import asyncio

import pytest

from app.domains.artefacts.lesson_note.application.draft import DraftLessonNote
from app.domains.artefacts.lesson_note.domain.note import NoteStepDraft
from app.shared.llm_text import decode_llm_json_escapes
from app.shared.note_text import corrects_itself, states_false_size_rule, without_record_ids
from app.shared.session_plan_view import SessionPlanView
from tests.test_lesson_note import LESSON_NOTE, SESSION_PLAN


@pytest.mark.parametrize(
    ("text", "clean"),
    [
        (
            "Demonstrate the rule with a worked example taken from record ch01‑b044‑i01.",
            "Demonstrate the rule with a worked example taken from the textbook.",
        ),
        (
            "Work through the textbook example (record ch01‑b043) step by step.",
            "Work through the textbook example step by step.",
        ),
        (
            "Give the practice exercise (ch01-b044-i03): arrange 3 billion.",
            "Give the practice exercise: arrange 3 billion.",
        ),
        ("See ch01-b044-i01 for more.", "See the textbook for more."),
        ("A plain sentence with no record.", "A plain sentence with no record."),
    ],
)
def test_the_plans_record_ids_are_taken_out_and_the_sentence_still_reads(
    text: str, clean: str
) -> None:
    assert without_record_ids(text) == clean


@pytest.mark.parametrize(
    "text",
    [
        "6 > 3? Wait, this contradicts the digit comparison.",
        "Actually, we made a mistake: we should compare from the left.",
        "Let me recompute the total.",
        "Oops, the tens digit decides.",
    ],
)
def test_a_note_that_corrects_itself_is_recognised(text: str) -> None:
    assert corrects_itself(text)


@pytest.mark.parametrize(
    "text",
    [
        "Wait for the class to copy the board.",
        "Compare digits from the left.",
        "Actually 5 is odd.",
    ],
)
def test_ordinary_text_is_not_taken_for_a_second_thought(text: str) -> None:
    assert not corrects_itself(text)


def test_a_naira_escape_typed_inside_a_formula_is_the_naira_sign() -> None:
    assert decode_llm_json_escapes(r"$1{,}148 \text{ billion}\;(=₦1{,}148)$") == (
        r"$1{,}148 \text{ billion}\;(=₦1{,}148)$"
    )
    assert decode_llm_json_escapes(r"$a \times b$") == r"$a \times b$"


class _Redrawing:
    """Leaves a second thought in the first draw of each step and a clean note in the next."""

    def __init__(self) -> None:
        self.draws: list[int] = []

    async def write(self, *, brief, lesson, step, draw: int = 0) -> NoteStepDraft:  # type: ignore[no-untyped-def]
        self.draws.append(draw)
        text = "Actually, we made a mistake here." if draw == 0 else "Compare digits from the left."
        return NoteStepDraft(
            title=step.title,
            teaching_points=[text, "See record ch01‑b044‑i01."],
            board_summary="Left to right.",
        )


def test_the_pipeline_draws_a_step_again_while_it_corrects_itself_and_drops_record_ids() -> None:
    writer = _Redrawing()

    note = asyncio.run(
        DraftLessonNote(writer).draft(
            plan=SessionPlanView.model_validate(SESSION_PLAN),
            plan_version_id="LPV-N1",
            specification=LESSON_NOTE,
        )
    )

    assert sorted(set(writer.draws)) == [0, 1]
    for section in note.sections:
        assert "Actually" not in section.body
        assert "ch01" not in section.body and "See the textbook." in section.body


@pytest.mark.parametrize(
    "text",
    [
        "Each unit is 1,000 times the previous, so the larger unit guarantees a larger number.",
        "The number with the bigger unit is automatically larger.",
        "The larger group wins; if equal, compare the next group.",
        "The number with the bigger leading digit is larger.",
    ],
)
def test_a_false_rule_for_comparing_sizes_is_recognised(text: str) -> None:
    assert states_false_size_rule(text)


@pytest.mark.parametrize(
    "text",
    [
        "Convert both to billions, then the number with more digits is larger.",
        "A larger unit is worth 1,000 of the one before it.",
        "0.08 trillion is less than 800 billion.",
    ],
)
def test_a_correct_statement_about_units_is_not_taken_for_the_false_rule(text: str) -> None:
    assert not states_false_size_rule(text)
