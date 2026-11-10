from __future__ import annotations

import uuid
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

from app.domains.learner_state.domain.models import ObjectiveBand
from app.shared.json_types import JsonObject
from app.shared.schema_base import StrictRequest, UtcDatetime


class TeachingWorkspaceResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    term_class_subject_id: uuid.UUID
    class_id: uuid.UUID | None = None
    class_name: str | None = None
    school_id: uuid.UUID | None = None
    school_name: str | None = None
    name: str
    subject_name: str | None
    subject_code: str | None
    grade_level: str | None
    term: str | None
    is_primary: bool
    teacher_id: str
    settings: JsonObject | None = None
    created_at: UtcDatetime | None = None


class LessonPeriodResponse(BaseModel):
    id: uuid.UUID
    scheme_of_work_id: uuid.UUID
    period_number: int
    title: str | None = None
    subtopic_id: str | None
    subtopic_title: str | None = None


class SchemeOfWorkResponse(BaseModel):
    id: uuid.UUID
    term_class_subject_id: uuid.UUID
    week_number: int
    starts_on: date | None = None
    title: str
    objectives: JsonObject | None
    lesson_periods: list[LessonPeriodResponse] = Field(default_factory=list)


class TermClassSubjectResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    term: str
    year: str
    weeks: list[SchemeOfWorkResponse] = Field(default_factory=list)
    current_week_number: int | None = None
    created_at: UtcDatetime | None


class SchemeOfWorkUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    objectives: JsonObject | None = None


class LessonPeriodCreateRequest(BaseModel):
    period_number: int = Field(..., ge=1)
    subtopic_id: str = Field(..., min_length=1)


class LessonPeriodUpdateRequest(BaseModel):
    subtopic_id: str | None = Field(default=None, min_length=1)
    period_number: int | None = Field(default=None, ge=1)


class LastClassTestResponse(BaseModel):
    lesson_title: str
    band: ObjectiveBand
    correct: int | None
    out_of: int | None
    taken_at: UtcDatetime


class ClassLearnerResponse(BaseModel):
    student_id: str
    full_name: str
    last_test: LastClassTestResponse | None
    notes_to_review: int = 0
    notes_approved: int = 0


class ClassLearnersResponse(BaseModel):
    learners: list[ClassLearnerResponse]


class LearnerTestResponse(BaseModel):
    lesson_period_id: uuid.UUID
    lesson_title: str
    band: ObjectiveBand
    correct: int | None
    out_of: int | None
    taken_at: UtcDatetime
    #: Who entered the results when the learner did not answer themselves.
    entered_by: str | None = None


class LearnerObjectiveResponse(BaseModel):
    objective_text: str
    lesson_period_id: uuid.UUID
    lesson_title: str
    band: ObjectiveBand
    correct: int | None
    out_of: int | None


class LearnerLessonResponse(BaseModel):
    lesson_period_id: uuid.UUID
    lesson_title: str
    correct: int | None = None
    out_of: int | None = None
    band: ObjectiveBand | None = None
    revision_note: Literal["to_review", "approved", "waiting_for_test", "not_made"]
    """`waiting_for_test` while the learner has not sat the lesson's class test."""
    revision_note_id: str | None = None


class LearnerResultsResponse(BaseModel):
    student_id: str
    full_name: str
    tests: list[LearnerTestResponse]
    """Newest first."""
    objectives: list[LearnerObjectiveResponse]
    """Weakest first."""
    lessons: list[LearnerLessonResponse] = Field(default_factory=list)
    """Every lesson with a plan: those with a test, newest first, then the rest as taught."""


class LessonReviewResponse(BaseModel):
    lesson_period_id: uuid.UUID
    plans_to_approve: int
    materials_to_review: int
    notes_to_review: int
    oldest_kind: str
    """`plan`, or the type of the material that has waited longest."""
    waiting_since: UtcDatetime


class LessonReviewsResponse(BaseModel):
    """The lessons with something waiting for the teacher; the others are left out."""

    lessons: list[LessonReviewResponse]


class StudySourceResponse(BaseModel):
    """A lesson of the evaluation whose marked classwork can be brought into another lesson."""

    plan_version_id: str
    lesson_title: str
    learners: int
    #: Whether the lesson's approved plan has every objective the marks were written against.
    fits: bool = True
    #: The evaluation lesson's approved lesson note, when it has one.
    lesson_note_id: str | None = None
    #: Whether that note has a section for every step of the lesson's approved plan.
    note_fits: bool = False


class StudyObjectiveResultResponse(BaseModel):
    lesson_objective_id: str
    objective_text: str
    band: ObjectiveBand
    correct: int
    out_of: int
    misconceptions: list[str]


class StudyLearnerResultResponse(BaseModel):
    student_id: str
    full_name: str
    #: The total the teacher wrote on the script, such as `1/4`.
    teacher_total: str
    band: ObjectiveBand
    correct: int
    out_of: int
    objectives: list[StudyObjectiveResultResponse]


class StudyResultsRequest(StrictRequest):
    from_plan_version_id: str = Field(..., min_length=1)


class StudyResultsResponse(BaseModel):
    """The evaluation's class results on a lesson; empty until they are imported."""

    imported: bool
    learners: list[StudyLearnerResultResponse]


class StandInPairRequest(StrictRequest):
    """A class learner who takes the marks of one learner of the study."""

    student_id: str = Field(..., min_length=1)
    study_student_id: str = Field(..., min_length=1)


class StandInRequest(StrictRequest):
    pairs: list[StandInPairRequest] = Field(..., min_length=1, max_length=12)


class StandInResponse(BaseModel):
    """The class learners whose results were made from study marks, so their notes are queued."""

    made: list[StandInPairRequest]


class StartOverResponse(BaseModel):
    """What clearing a lesson would remove, or did; the rows by table, and why it may not be."""

    counts: dict[str, int]
    blocked: list[str] = Field(default_factory=list)


class LearnerAnswerResponse(BaseModel):
    objective_text: str
    question: str
    #: What the learner chose or wrote.
    student_answer: str
    #: The right option or the model answer, when there is one.
    correct_answer: str
    correct: bool
    #: The mistake the answer shows, when it was wrong and one was named.
    misconception: str | None = None


class LearnerAnswersResponse(BaseModel):
    """A learner's answers on one lesson, and how much of them is kept."""

    #: `answers` (every class test answer), `marked_work` (every marked question), `missed_only`
    #: (only the questions they got wrong were kept) or `none`.
    source: Literal["answers", "marked_work", "missed_only", "none"]
    answers: list[LearnerAnswerResponse] = Field(default_factory=list)
