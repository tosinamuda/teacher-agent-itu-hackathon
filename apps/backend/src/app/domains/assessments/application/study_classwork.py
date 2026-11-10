"""A learner's MSc-study classwork: marked by the teacher, coded by the researcher."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class ClassworkQuestion:
    n: int
    lesson_objective_id: str
    text: str
    answer: str | None
    answer_source: str | None


@dataclass(frozen=True)
class ClassworkAnswer:
    n: int
    mark: str
    uncertain: bool
    working: str
    misconception_code: str | None
    misconception_why: str | None


@dataclass(frozen=True)
class ClassworkScript:
    teacher_total: str
    capture_complete: bool
    answers: list[ClassworkAnswer]


@dataclass(frozen=True)
class LearnerClasswork:
    """The lesson's questions and the learner's script, if they sat it."""

    questions: list[ClassworkQuestion]
    script: ClassworkScript | None


class StudyClassworkReader(Protocol):
    async def for_learner(
        self, db: AsyncSession, plan_version_id: str, student_id: str
    ) -> LearnerClasswork: ...
