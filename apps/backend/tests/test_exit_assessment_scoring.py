"""No-LLM tests for the exit-assessment -> objective-indexed diagnostic bridge.

Proves the connection: graded student responses score into the exact results
shape, and that shape derives the correct objective bands via LearnerStateService
(the input that drives P1 personalisation).
"""

from __future__ import annotations

from app.domains.assessments.application.scoring import (
    attach_survey_to_results,
    score_objective_diagnostic,
)
from app.domains.assessments.schemas import (
    ExitAssessmentItemResponse,
    ExitAssessmentObjectiveSurvey,
    ExitAssessmentSessionSurvey,
)
from app.domains.learner_state.application.service import LearnerStateService


def _responses() -> list[ExitAssessmentItemResponse]:
    return [
        # lop01: 1/4 correct, a missed item flags the misconception -> remediate
        ExitAssessmentItemResponse(lesson_objective_id="lop01", is_correct=True),
        ExitAssessmentItemResponse(
            lesson_objective_id="lop01",
            is_correct=False,
            misconception_code="area-perimeter-confusion",
        ),
        ExitAssessmentItemResponse(lesson_objective_id="lop01", is_correct=False),
        ExitAssessmentItemResponse(lesson_objective_id="lop01", is_correct=False),
        # lop02: 4/4 correct -> extend
        ExitAssessmentItemResponse(lesson_objective_id="lop02", is_correct=True),
        ExitAssessmentItemResponse(lesson_objective_id="lop02", is_correct=True),
        ExitAssessmentItemResponse(lesson_objective_id="lop02", is_correct=True),
        ExitAssessmentItemResponse(lesson_objective_id="lop02", is_correct=True),
    ]


def test_scoring_produces_objective_indexed_results() -> None:
    # Legacy 3-bucket answers coerce onto the canonical 1-5 scale (low→2, high→4).
    survey = [
        ExitAssessmentObjectiveSurvey(lesson_objective_id="lop01", confidence="low"),
        ExitAssessmentObjectiveSurvey(lesson_objective_id="lop02", confidence="high"),
    ]
    results = score_objective_diagnostic(_responses(), survey).model_dump(
        mode="json", exclude_none=True
    )
    by_id = {o["lesson_objective_id"]: o for o in results["objectives"]}
    assert by_id["lop01"] == {
        "lesson_objective_id": "lop01",
        "score": 1,
        "max_score": 4,
        "confidence": "low",
        "confidence_score": 2,
        "misconception_code": "area-perimeter-confusion",
        # The fixture responses carry no item fields -> no answer evidence.
        "evidence": [],
    }
    assert by_id["lop02"]["score"] == 4 and by_id["lop02"]["max_score"] == 4
    assert by_id["lop02"]["confidence"] == "high"
    assert by_id["lop02"]["confidence_score"] == 4
    # mastered objective carries no misconception even if one was passed on a correct item
    assert "misconception_code" not in by_id["lop02"]


def test_numeric_survey_scores_bucket_and_session_block_persists() -> None:
    # Spec survey: 1-5 per objective + session-level interest/affect.
    survey = [
        ExitAssessmentObjectiveSurvey(
            lesson_objective_id="lop01", confidence=1, perceived_difficulty=5
        ),
        ExitAssessmentObjectiveSurvey(
            lesson_objective_id="lop02", confidence=5, perceived_difficulty=3
        ),
    ]
    session = ExitAssessmentSessionSurvey(interest=2, affect=4)
    results = score_objective_diagnostic(_responses(), survey, session).model_dump(
        mode="json", exclude_none=True
    )
    by_id = {o["lesson_objective_id"]: o for o in results["objectives"]}
    assert by_id["lop01"]["confidence"] == "low" and by_id["lop01"]["confidence_score"] == 1
    assert (
        by_id["lop01"]["perceived_difficulty"] == "high" and by_id["lop01"]["difficulty_score"] == 5
    )
    assert by_id["lop02"]["confidence"] == "high"
    assert by_id["lop02"]["perceived_difficulty"] == "medium"
    assert results["session"] == {"interest": 2, "affect": 4}


def test_misconception_description_derived_from_code() -> None:
    # No description is authored anywhere — learner state derives readable prose
    # from the snake_case distractor code so it is never shown as "none recorded".
    results = score_objective_diagnostic(_responses()).model_dump(mode="json", exclude_none=True)
    state = LearnerStateService().build(
        student_id="s1", student_profile=object(), diagnostic_results=results
    )
    by_id = {o.lesson_objective_id: o for o in state.objective_states}
    assert by_id["lop01"].misconception_description == "Area-perimeter-confusion"


def test_session_survey_lands_on_learner_state() -> None:
    session = ExitAssessmentSessionSurvey(interest=1, affect=2)
    results = score_objective_diagnostic(_responses(), None, session).model_dump(
        mode="json", exclude_none=True
    )
    state = LearnerStateService().build(
        student_id="s1", student_profile=object(), diagnostic_results=results
    )
    assert state.session_survey is not None
    assert state.session_survey.interest == 1
    assert state.session_survey.affect == 2


def test_scored_results_drive_correct_bands() -> None:
    results = score_objective_diagnostic(_responses()).model_dump(mode="json", exclude_none=True)
    state = LearnerStateService().build(
        student_id="s1", student_profile=object(), diagnostic_results=results
    )
    by_id = {o.lesson_objective_id: o for o in state.objective_states}
    assert by_id["lop01"].band == "remediate"  # 0.25
    assert by_id["lop01"].misconception_code == "area-perimeter-confusion"
    assert by_id["lop02"].band == "extend"  # 1.0


def test_misconception_is_the_mode_of_chosen_distractors() -> None:
    # Miscon(s,o) = mode of the chosen-distractor codes; ties break first-seen.
    responses = [
        ExitAssessmentItemResponse(
            lesson_objective_id="lop01", is_correct=False, misconception_code="off_by_one"
        ),
        ExitAssessmentItemResponse(
            lesson_objective_id="lop01", is_correct=False, misconception_code="sign_error"
        ),
        ExitAssessmentItemResponse(
            lesson_objective_id="lop01", is_correct=False, misconception_code="sign_error"
        ),
        ExitAssessmentItemResponse(lesson_objective_id="lop01", is_correct=True),
    ]
    results = score_objective_diagnostic(responses).model_dump(mode="json", exclude_none=True)
    assert results["objectives"][0]["misconception_code"] == "sign_error"


def test_attach_survey_merges_into_graded_results() -> None:
    # Two-step flow: grade first (no survey), attach the survey after. Scores and
    # misconceptions stay untouched; survey fields + session block fill in.
    graded = score_objective_diagnostic(_responses()).model_dump(mode="json", exclude_none=True)
    assert "confidence_score" not in graded["objectives"][0]

    merged = attach_survey_to_results(
        graded,
        [
            ExitAssessmentObjectiveSurvey(
                lesson_objective_id="lop01", confidence=2, perceived_difficulty=5
            )
        ],
        ExitAssessmentSessionSurvey(interest=4, affect=1),
    )
    by_id = {o["lesson_objective_id"]: o for o in merged["objectives"]}
    assert by_id["lop01"]["score"] == graded["objectives"][0]["score"]
    assert by_id["lop01"]["misconception_code"] == "area-perimeter-confusion"
    assert by_id["lop01"]["confidence_score"] == 2
    assert by_id["lop01"]["confidence"] == "low"
    assert by_id["lop01"]["difficulty_score"] == 5
    assert by_id["lop01"]["perceived_difficulty"] == "high"
    # lop02 had no survey entry -> untouched.
    assert "confidence_score" not in by_id["lop02"]
    assert merged["session"] == {"interest": 4, "affect": 1}


def test_missed_items_record_answer_evidence() -> None:
    # Wrong answers carry the question + chosen distractor into the results
    # (the P1 prompt's evidence items); correct answers record no evidence.
    responses = [
        ExitAssessmentItemResponse(
            lesson_objective_id="lop01",
            is_correct=False,
            misconception_code="sign_error",
            stem="What is -3 + 5?",
            options={"A": "2", "B": "-2", "C": "8"},
            correct_option="A",
            chosen_option="B",
        ),
        ExitAssessmentItemResponse(
            lesson_objective_id="lop01",
            is_correct=True,
            stem="What is -1 + 1?",
            options={"A": "0", "B": "2"},
            correct_option="A",
            chosen_option="A",
        ),
    ]
    results = score_objective_diagnostic(responses).model_dump(mode="json", exclude_none=True)
    evidence = results["objectives"][0]["evidence"]
    assert evidence == [
        {
            "stem": "What is -3 + 5?",
            "options": {"A": "2", "B": "-2", "C": "8"},
            "correct_option": "A",
            "chosen_option": "B",
            "misconception_code": "sign_error",
        }
    ]

    # attach_survey (two-step flow) must not disturb the recorded evidence.
    merged = attach_survey_to_results(
        results,
        [ExitAssessmentObjectiveSurvey(lesson_objective_id="lop01", confidence=4)],
        None,
    )
    assert merged["objectives"][0]["evidence"] == evidence
    assert merged["objectives"][0]["confidence_score"] == 4


def test_full_mastery_has_no_misconception() -> None:
    results = score_objective_diagnostic(
        [
            ExitAssessmentItemResponse(
                lesson_objective_id="lop01",
                is_correct=True,
                misconception_code="should-be-ignored",
            )
        ]
    ).model_dump(mode="json", exclude_none=True)
    assert "misconception_code" not in results["objectives"][0]
