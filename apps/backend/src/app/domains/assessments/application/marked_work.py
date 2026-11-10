"""A student's marked classwork, as the diagnostic results a student's own answers would give.

A teacher marks work that is not multiple choice: each question has a model answer, and the
student's working is marked correct or incorrect, with the misconception it shows when it is
incorrect. The marks give the same objective scores and missed-question evidence as a student's
answers to a class test, so the learner state and the note written from it read them alike.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domains.assessments.application.scoring import score_objective_diagnostic
from app.domains.assessments.onbehalf_schemas import MarkedWork
from app.domains.assessments.schemas import (
    ExitAssessmentItemResponse,
    ExitAssessmentObjectiveSurvey,
    ExitAssessmentSessionSurvey,
)
from app.shared.json_types import JsonObject


def marked_work_results(
    work: Sequence[MarkedWork],
    survey: list[ExitAssessmentObjectiveSurvey] | None = None,
    session_survey: ExitAssessmentSessionSurvey | None = None,
) -> JsonObject:
    """The diagnostic results of ``work``; a question left unmarked counts for nothing."""
    responses = [
        ExitAssessmentItemResponse(
            lesson_objective_id=entry.lesson_objective_id,
            is_correct=entry.mark == "correct",
            misconception_code=entry.misconception_code,
            misconception_why=entry.misconception_why,
            stem=entry.question,
            correct_option=entry.model_answer,
            chosen_option=entry.working,
        )
        for entry in work
        if entry.mark != "unmarked"
    ]
    results = score_objective_diagnostic(responses, survey, session_survey).model_dump(
        mode="json", exclude_none=True
    )
    # The scores keep only the missed questions; the marked work keeps every one, so the teacher
    # can read what the learner wrote on each.
    results["marked_work"] = [
        entry.model_dump(mode="json", exclude_none=True)
        for entry in work
        if entry.mark != "unmarked"
    ]
    return results
