"""Assessment domain schemas — exit-ticket submissions + MCQ exit assessment."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field

from app.shared.json_types import JsonObject
from app.shared.schema_base import UtcDatetime

SignalLevel = Literal["low", "medium", "high"]

# Legacy 3-bucket survey answers normalise onto the canonical 1-5 scale
# (learner-model spec: Confidence/Difficulty(s,o) ∈ {1..5}).
_LEGACY_SIGNAL_TO_SCALE = {"low": 2, "medium": 3, "high": 4}


def _coerce_survey_scale(value: object) -> object:
    """Accept legacy "low/medium/high" strings and map them onto 1-5."""
    if isinstance(value, str):
        return _LEGACY_SIGNAL_TO_SCALE.get(value, value)
    return value


SurveyScale = Annotated[int, BeforeValidator(_coerce_survey_scale), Field(ge=1, le=5)]


class ExitTicketSubmissionCreateRequest(BaseModel):
    student_id: str = Field(..., min_length=1)
    plan_version_id: str = Field(..., min_length=1)
    results: JsonObject
    diagnostic_id: str | None = Field(default=None, min_length=1)


class ExitTicketSubmissionResponse(BaseModel):
    diagnostic_id: str
    student_id: str
    plan_version_id: str
    created_at: UtcDatetime | None = None
    #: The answers are in and the survey is still to come.
    survey_pending: bool = False


# --- Internal scoring contract (built server-side after MCQ grading) ---


class ExitAssessmentItemResponse(BaseModel):
    """One graded item (server-derived from the student's selected option).

    The item fields (stem/options/correct/chosen) ride along so the scorer can
    record option-level answer evidence in the diagnostic results — the input
    that lets P1 defuse the learner's actual chosen distractor.
    """

    lesson_objective_id: str = Field(..., min_length=1)
    item_id: str | None = None
    is_correct: bool
    misconception_code: str | None = None
    stem: str | None = None
    options: dict[str, str] | None = None
    correct_option: str | None = None
    chosen_option: str | None = None
    # The teacher's own words for the misconception, where they gave them.
    misconception_why: str | None = None


class ExitAssessmentObjectiveSurvey(BaseModel):
    """Per-objective post-class survey: Confidence + Difficulty on a 1-5 scale.

    Learner-model spec: Confidence(s,o) ("How sure are you that you can do this by
    yourself?") and Difficulty(s,o) ("How difficult was this for you?") are asked
    PER learning objective. Legacy low/medium/high answers coerce onto the scale.
    """

    lesson_objective_id: str = Field(..., min_length=1)
    confidence: SurveyScale | None = None
    perceived_difficulty: SurveyScale | None = None


class ExitAssessmentSessionSurvey(BaseModel):
    """Session-level survey: Interest + Affect, asked once for the whole subtopic.

    Learner-model spec: Interest(s,σ) ("How interested were you in today's topic?")
    and Affect(s,σ) ("How did you feel at the end of the lesson?"), both 1-5.
    """

    interest: SurveyScale | None = None
    affect: SurveyScale | None = None


# --- Student-facing MCQ submission ---


class ExitAssessmentAnswer(BaseModel):
    """One MCQ answer: the option key the student selected."""

    item_id: str = Field(..., min_length=1)
    selected_option: str = Field(..., min_length=1)


class ExitAssessmentSubmitRequest(BaseModel):
    """Student submits selected MCQ options; the server grades them (correctness.

    + misconception from the chosen distractor) and scores the diagnostic.
    """

    student_id: str = Field(..., min_length=1)
    plan_version_id: str = Field(..., min_length=1)
    answers: list[ExitAssessmentAnswer] = Field(..., min_length=1)
    survey: list[ExitAssessmentObjectiveSurvey] = Field(default_factory=list)
    # Session-level Interest + Affect (asked once per subtopic session).
    session_survey: ExitAssessmentSessionSurvey | None = None
    diagnostic_id: str | None = Field(default=None, min_length=1)
    # True = the survey arrives in a follow-up call (two-step student flow);
    # defer pack generation until it lands. One-shot callers (synthetic class,
    # offline imports) leave this False and keep the original behaviour.
    survey_pending: bool = False


class ExitAssessmentSurveyAttachRequest(BaseModel):
    """Step 2 of the student flow: attach the post-class survey to a diagnostic.

    The answers were already graded; this completes the evidence (per-objective
    Confidence/Difficulty + session Interest/Affect) and triggers pack generation.
    """

    survey: list[ExitAssessmentObjectiveSurvey] = Field(default_factory=list)
    session_survey: ExitAssessmentSessionSurvey | None = None


# --- Question serving (no answers / misconceptions exposed) ---


class ExitAssessmentObjectiveQuestions(BaseModel):
    lesson_objective_id: str
    objective_text: str | None = None
    items: list[JsonObject] = Field(default_factory=list)


class ExitAssessmentQuestionsResponse(BaseModel):
    plan_version_id: str
    subject: str | None = None
    topic: str | None = None
    subtopic: str | None = None
    objectives: list[ExitAssessmentObjectiveQuestions] = Field(default_factory=list)


class AssessmentStatusResponse(BaseModel):
    """Per-lesson assessment state for the teacher's lesson-prep queue."""

    plan_version_id: str
    has_assessment: bool
    released: bool
