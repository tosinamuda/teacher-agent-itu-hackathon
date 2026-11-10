"""GET the MSc study's ratings of one revision note."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.evaluation.api.deps import study_ratings_reader
from app.domains.evaluation.application.study_ratings import StudyRatingsReader
from app.domains.evaluation.domain.study_instrument import (
    COMPARISON,
    H1_CRITERIA,
    H2_CRITERIA,
    SCALE,
    Criterion,
)
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(prefix="/evaluation/study-ratings", tags=["evaluation"])


class CriterionScoreResponse(BaseModel):
    rater: str
    packet: str
    objective_index: int
    lesson_objective_id: str
    objective_text: str | None
    criterion_id: str
    score: int
    comment: str | None


class ComparativeJudgementResponse(BaseModel):
    rater: str
    packet: str
    shown_as: str
    other_note_id: str
    objective_index: int
    lesson_objective_id: str | None
    objective_text: str | None
    criterion_id: str
    choice: str
    favoured_condition: str | None
    comment: str | None


class StudyRatingsTallyResponse(BaseModel):
    plan_version_id: str
    scores: int
    judgements: int
    raters: int


class RatingDocumentResponse(BaseModel):
    rater: str
    rater_name: str
    packet: str
    shown_as: str | None
    state: str
    marks: int
    rows_unanswered: int
    date_completed: str | None
    closing_comment: str | None


class StudyRatingsResponse(BaseModel):
    scores: list[CriterionScoreResponse]
    judgements: list[ComparativeJudgementResponse]
    documents: list[RatingDocumentResponse]


class CriterionResponse(BaseModel):
    id: str
    name: str
    question: str
    descriptors: list[str]
    notes: list[str]
    better: str


class InstrumentResponse(BaseModel):
    scale: list[tuple[int, str]]
    comparison: list[str]
    part_1: list[CriterionResponse]
    part_2: list[CriterionResponse]


def _criteria(criteria: tuple[Criterion, ...]) -> list[CriterionResponse]:
    return [
        CriterionResponse(
            id=c.id,
            name=c.name,
            question=c.question,
            descriptors=list(c.descriptors),
            notes=list(c.notes),
            better=c.better,
        )
        for c in criteria
    ]


@router.get("/instrument", response_model=InstrumentResponse)
async def study_instrument(
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> InstrumentResponse:
    """The rating instrument as the raters read it: criteria, questions, and scale wording."""
    return InstrumentResponse(
        scale=list(SCALE),
        comparison=list(COMPARISON),
        part_1=_criteria(H1_CRITERIA),
        part_2=_criteria(H2_CRITERIA),
    )


@router.get("/tally", response_model=list[StudyRatingsTallyResponse])
async def study_ratings_tally(
    plan_version_id: list[str] = Query(..., min_length=1),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
    reader: StudyRatingsReader = Depends(study_ratings_reader),
    db: AsyncSession = Depends(get_db),
) -> list[StudyRatingsTallyResponse]:
    """How many study ratings each lesson's notes hold; a lesson with none is left out."""
    tallies = await reader.tally(db, plan_version_id)
    return [StudyRatingsTallyResponse(**asdict(tally)) for tally in tallies]


@router.get("", response_model=StudyRatingsResponse)
async def study_ratings_of_a_note(
    note: str = Query(..., min_length=1, description="The revision note's content id."),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
    reader: StudyRatingsReader = Depends(study_ratings_reader),
    db: AsyncSession = Depends(get_db),
) -> StudyRatingsResponse:
    """Every study rating of the note: Part 1 scores, or Part 2 judgements it was one side of."""
    ratings = await reader.for_note(db, note)
    return StudyRatingsResponse(
        scores=[CriterionScoreResponse(**asdict(score)) for score in ratings.scores],
        judgements=[ComparativeJudgementResponse(**asdict(j)) for j in ratings.judgements],
        documents=[RatingDocumentResponse(**asdict(d)) for d in ratings.documents],
    )
