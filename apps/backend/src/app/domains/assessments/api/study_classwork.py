"""GET one learner's classwork from the MSc study."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.assessments.infrastructure.study_classwork import SqlAlchemyStudyClasswork
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(prefix="/assessments/study-classwork", tags=["assessments"])


class QuestionResponse(BaseModel):
    n: int
    lesson_objective_id: str
    text: str
    answer: str | None
    answer_source: str | None


class AnswerResponse(BaseModel):
    n: int
    mark: str
    uncertain: bool
    working: str
    misconception_code: str | None
    misconception_why: str | None


class ScriptResponse(BaseModel):
    teacher_total: str
    capture_complete: bool
    answers: list[AnswerResponse]


class LearnerClassworkResponse(BaseModel):
    questions: list[QuestionResponse]
    script: ScriptResponse | None


@router.get("", response_model=LearnerClassworkResponse)
async def learner_classwork(
    plan_version_id: str = Query(..., min_length=1),
    student_id: str = Query(..., min_length=1),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> LearnerClassworkResponse:
    """The lesson's classwork questions, and the learner's marked script if they sat it."""
    classwork = await SqlAlchemyStudyClasswork().for_learner(db, plan_version_id, student_id)
    return LearnerClassworkResponse.model_validate(asdict(classwork))
