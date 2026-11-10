"""The MSc study's ratings of one revision note, as its raters recorded them."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class CriterionScore:
    """Part 1: a rater's 1–5 on one criterion for one of the note's objectives."""

    rater: str
    packet: str
    objective_index: int
    lesson_objective_id: str
    #: The objective as the lesson plan words it, which the scoring page named.
    objective_text: str | None
    criterion_id: str
    score: int
    comment: str | None


@dataclass(frozen=True)
class ComparativeJudgement:
    """Part 2: a rater's choice between this note and the learner's other one."""

    rater: str
    packet: str
    #: Where this note sat in front of the rater, A or B.
    shown_as: str
    other_note_id: str
    #: The objective's number among those the set compared, not in the lesson.
    objective_index: int
    lesson_objective_id: str | None
    objective_text: str | None
    criterion_id: str
    choice: str
    favoured_condition: str | None
    comment: str | None


@dataclass(frozen=True)
class RatingDocument:
    """A returned rating document that rated the note: when, and the rater's closing comment."""

    rater: str
    #: The rater's profile, e.g. "Study rater 2".
    rater_name: str
    packet: str
    #: Where the note sat in a Part 2 comparison, A or B; none for Part 1.
    shown_as: str | None
    #: ``complete``, ``partial`` or ``untouched``.
    state: str
    marks: int
    rows_unanswered: int
    date_completed: str | None
    closing_comment: str | None


@dataclass(frozen=True)
class StudyRatings:
    scores: list[CriterionScore]
    judgements: list[ComparativeJudgement]
    documents: list[RatingDocument]


@dataclass(frozen=True)
class StudyRatingsTally:
    """How much the study's raters recorded about one lesson's revision notes."""

    plan_version_id: str
    scores: int
    judgements: int
    raters: int


class StudyRatingsReader(Protocol):
    async def for_note(self, db: AsyncSession, note_id: str) -> StudyRatings: ...

    async def tally(
        self, db: AsyncSession, plan_version_ids: list[str]
    ) -> list[StudyRatingsTally]: ...
