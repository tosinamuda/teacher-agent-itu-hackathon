"""Classwork that is not multiple choice: a teacher's marks become the learner's diagnostic.

The marks are the study's own for Week 9, simplification of algebraic expressions: ST-STUDY-03
(two of the three marked questions right, one left unmarked) and ST-STUDY-06 (none right).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.domains.assessments.application.marked_work import marked_work_results
from app.domains.assessments.onbehalf_schemas import MarkedWork, OnBehalfResponseRequest
from app.domains.learner_state.application.service import LearnerStateService
from app.shared.json_types import JsonObject

OBJECTIVE = "lo-t2w09-01"


def _work(question: str, mark: str, **fields: object) -> MarkedWork:
    return MarkedWork(
        lesson_objective_id=OBJECTIVE,
        question=question,
        model_answer="the key",
        mark=mark,  # type: ignore[arg-type]
        **fields,  # type: ignore[arg-type]
    )


def _objective(results: JsonObject) -> JsonObject:
    objectives = results["objectives"]
    assert isinstance(objectives, list) and len(objectives) == 1
    objective = objectives[0]
    assert isinstance(objective, dict)
    return objective


def test_marks_give_the_objective_a_score_out_of_the_questions_marked() -> None:
    results = marked_work_results(
        [
            _work("$4n + 3n \\times 10$", "incorrect", misconception_code="drops_variable"),
            _work("$32 + 8x \\div 2$", "unmarked"),
            _work("$3 \\times 5x + 4x \\div 2$", "correct"),
            _work("$36y \\div 6 + y + 2 \\times 4y$", "correct"),
        ]
    )

    objective = _objective(results)
    assert (objective["score"], objective["max_score"]) == (2, 3)


def test_the_working_and_misconception_of_a_missed_question_are_kept_as_evidence() -> None:
    results = marked_work_results(
        [
            _work(
                "$4n + 3n \\times 10$",
                "incorrect",
                working="$7n \\times 10 = 70n$",
                misconception_code="adds_before_multiplying",
                misconception_why="Adds 4n and 3n before multiplying by 10.",
            ),
            _work("$32 + 8x \\div 2$", "correct", working="$32 + 4x$"),
        ]
    )

    objective = _objective(results)
    assert objective["misconception_code"] == "adds_before_multiplying"
    assert objective["misconception_description"] == "Adds 4n and 3n before multiplying by 10."
    assert objective["evidence"] == [
        {
            "stem": "$4n + 3n \\times 10$",
            "options": {},
            "correct_option": "the key",
            "chosen_option": "$7n \\times 10 = 70n$",
            "misconception_code": "adds_before_multiplying",
        }
    ]


def test_a_learner_with_no_question_right_is_in_the_remediate_band() -> None:
    results = marked_work_results(
        [_work(f"question {n}", "incorrect", misconception_code="slip") for n in range(4)]
    )

    state = LearnerStateService().build(
        student_id="ST-1", student_profile=object(), diagnostic_results=results
    )

    assert [found.band for found in state.objective_states] == ["remediate"]
    assert state.objective_states[0].misconception_code == "slip"


@pytest.mark.parametrize(
    ("correct", "marked", "band"),
    [(4, 4, "extend"), (2, 3, "reinforce"), (2, 4, "reinforce"), (1, 4, "remediate")],
)
def test_the_band_follows_the_share_of_marked_questions_right(
    correct: int, marked: int, band: str
) -> None:
    marks = ["correct"] * correct + ["incorrect"] * (marked - correct) + ["unmarked"]
    results = marked_work_results([_work(f"q{n}", mark) for n, mark in enumerate(marks)])

    state = LearnerStateService().build(
        student_id="ST-1", student_profile=object(), diagnostic_results=results
    )

    assert [found.band for found in state.objective_states] == [band]


def test_an_entry_holds_exactly_one_kind_of_result() -> None:
    with pytest.raises(ValidationError, match="exactly one"):
        OnBehalfResponseRequest(student_id="ST-1")
    with pytest.raises(ValidationError, match="exactly one"):
        OnBehalfResponseRequest(
            student_id="ST-1",
            marked_work=[_work("q", "correct")],
            objective_scores=[{"lesson_objective_id": OBJECTIVE, "score": 1, "max_score": 2}],  # type: ignore[list-item]
        )


def test_an_entry_with_every_question_unmarked_is_refused() -> None:
    with pytest.raises(ValidationError, match="mark at least one question"):
        OnBehalfResponseRequest(student_id="ST-1", marked_work=[_work("q", "unmarked")])


def test_a_misconception_is_named_in_snake_case() -> None:
    with pytest.raises(ValidationError):
        _work("q", "incorrect", misconception_code="Adds before multiplying")
