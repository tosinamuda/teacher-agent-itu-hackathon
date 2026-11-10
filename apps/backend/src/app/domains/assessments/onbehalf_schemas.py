"""On-behalf student-response entry schemas (FD-04).

A researcher/teacher records a student's classwork results without a student
login. They provide ONE of: the option the student chose per item (full signal:
score + chosen-distractor misconception), per-objective aggregate scores (score-only:
band, misconception N/A), or the marks on the student's worked answers (the question,
the model answer, the working, the mark, and the misconception it shows).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.domains.assessments.schemas import (
    ExitAssessmentAnswer,
    ExitAssessmentObjectiveSurvey,
    ExitAssessmentSessionSurvey,
)


class ManualObjectiveScore(BaseModel):
    """Score-only fallback: an objective's correct count out of its total."""

    lesson_objective_id: str = Field(..., min_length=1)
    score: int = Field(..., ge=0)
    max_score: int = Field(..., gt=0)


class MarkedWork(BaseModel):
    """One question of the classwork, and how a teacher marked a student's work on it.

    The classwork is not multiple choice: the student wrote their working, and the teacher
    marked it against the model answer. A question left ``unmarked`` counts for nothing.
    """

    lesson_objective_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    model_answer: str = ""
    mark: Literal["correct", "incorrect", "unmarked"]
    working: str = ""
    # Which mistake the working shows, as a short snake_case name, and the teacher's words for it.
    misconception_code: str | None = Field(default=None, pattern=r"^[a-z][a-z0-9_]*$")
    misconception_why: str | None = None


class OnBehalfResponseRequest(BaseModel):
    student_id: str = Field(..., min_length=1)
    answers: list[ExitAssessmentAnswer] = Field(default_factory=list)
    objective_scores: list[ManualObjectiveScore] = Field(default_factory=list)
    marked_work: list[MarkedWork] = Field(default_factory=list)
    survey: list[ExitAssessmentObjectiveSurvey] = Field(default_factory=list)
    session_survey: ExitAssessmentSessionSurvey | None = None
    # Optional photo of the student's original marked answer sheet.
    provenance_attachment_id: str | None = None

    @model_validator(mode="after")
    def _exactly_one_mode(self) -> OnBehalfResponseRequest:
        given = [bool(self.answers), bool(self.objective_scores), bool(self.marked_work)]
        if given.count(True) != 1:
            raise ValueError("provide exactly one of answers, objective_scores or marked_work")
        if self.marked_work and all(entry.mark == "unmarked" for entry in self.marked_work):
            raise ValueError("mark at least one question")
        return self


# --- Context (the entry form's prerequisites) ---


class OnBehalfObjective(BaseModel):
    lesson_objective_id: str
    objective_text: str | None = None


class OnBehalfItem(BaseModel):
    """An item to record the student's choice against.

    No answer key: the transcriber copies what the student picked; the server grades.
    """

    item_id: str
    lesson_objective_id: str | None = None
    stem: str
    options: dict[str, str]


class OnBehalfContextResponse(BaseModel):
    plan_version_id: str
    subject: str | None = None
    topic: str | None = None
    subtopic: str | None = None
    objectives: list[OnBehalfObjective] = Field(default_factory=list)
    items: list[OnBehalfItem] = Field(default_factory=list)
    # Students who already have a submission for this lesson (so the picker can
    # skip them — re-entry is rejected to protect their evidence).
    submitted_student_ids: list[str] = Field(default_factory=list)


class OnBehalfResponseResult(BaseModel):
    diagnostic_id: str
    student_id: str
    plan_version_id: str
    objectives_scored: int
