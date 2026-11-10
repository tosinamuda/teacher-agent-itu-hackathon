"""A student's submission says whether its survey is still to come, so the page can resume it."""

from __future__ import annotations

from app.domains.assessments.api.routes import _submission_response
from app.domains.assessments.models import ExitTicketSubmission


def _submission(*, survey_pending: bool) -> ExitTicketSubmission:
    return ExitTicketSubmission(
        diagnostic_id="DG-1",
        student_id="ST-1",
        plan_version_id="LPV-1",
        survey_pending=survey_pending,
    )


def test_a_submission_awaiting_its_survey_says_so() -> None:
    assert _submission_response(_submission(survey_pending=True)).survey_pending is True
    assert _submission_response(_submission(survey_pending=False)).survey_pending is False
