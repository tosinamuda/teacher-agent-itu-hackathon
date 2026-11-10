"""What a learner answered on one lesson, read from the best record that is kept of it."""

from __future__ import annotations

import uuid
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.teaching.application.sequence_service import TeachingSequenceApplicationError
from app.domains.teaching.infrastructure.study_results_repository import StudyResultsRepository
from app.domains.teaching.schemas import LearnerAnswerResponse, LearnerAnswersResponse

Source = Literal["answers", "marked_work", "missed_only", "none"]


def _text(value: object) -> str:
    return str(value) if value is not None else ""


class LearnerAnswers:
    """Reads a learner's answers from the fullest record kept.

    A class test's answers are all kept; a teacher's marked work is kept in full; otherwise only
    the questions that were missed are.
    """

    def __init__(self, repository: StudyResultsRepository | None = None) -> None:
        self._repository = repository or StudyResultsRepository()

    async def of(
        self,
        db: AsyncSession,
        workspace_id: uuid.UUID,
        lesson_period_id: uuid.UUID,
        student_id: str,
    ) -> LearnerAnswersResponse:
        if not await self._repository.lesson_in_workspace(db, workspace_id, lesson_period_id):
            raise TeachingSequenceApplicationError(404, "workspace_or_lesson_not_found")
        version = await self._repository.approved_version_of(db, lesson_period_id)
        if version is None:
            return LearnerAnswersResponse(source="none")
        texts = await self._repository.objective_texts(db, version)
        responses = await self._repository.item_responses(db, version, student_id)
        if responses:
            return LearnerAnswersResponse(
                source="answers",
                answers=[
                    LearnerAnswerResponse(
                        objective_text=texts.get(objective or "", ""),
                        question=stem,
                        student_answer=_option(options, choice),
                        correct_answer=_option(options, right),
                        correct=was_right,
                        misconception=mistake,
                    )
                    for objective, stem, options, right, choice, was_right, mistake in responses
                ],
            )
        results = await self._repository.submission_results(db, version, student_id) or {}
        return _from_results(results, texts)


def _maybe(value: object) -> str | None:
    return str(value) if value else None


def _option(options: dict[str, str], key: str) -> str:
    return f"{key}. {options[key]}" if key in options else key


def _from_results(results: dict[str, object], texts: dict[str, str]) -> LearnerAnswersResponse:
    marked = results.get("marked_work")
    if isinstance(marked, list) and marked:
        return LearnerAnswersResponse(
            source="marked_work",
            answers=[
                LearnerAnswerResponse(
                    objective_text=texts.get(_text(entry.get("lesson_objective_id")), ""),
                    question=_text(entry.get("question")),
                    student_answer=_text(entry.get("working")),
                    correct_answer=_text(entry.get("model_answer")),
                    correct=entry.get("mark") == "correct",
                    misconception=_maybe(entry.get("misconception_code")),
                )
                for entry in marked
                if isinstance(entry, dict)
            ],
        )
    answers: list[LearnerAnswerResponse] = []
    objectives = results.get("objectives")
    for objective in objectives if isinstance(objectives, list) else []:
        if not isinstance(objective, dict):
            continue
        text = texts.get(_text(objective.get("lesson_objective_id")), "")
        for item in objective.get("evidence") or []:
            if isinstance(item, dict):
                raw = item.get("options")
                options = {str(k): str(v) for k, v in raw.items()} if isinstance(raw, dict) else {}
                answers.append(
                    LearnerAnswerResponse(
                        objective_text=text,
                        question=_text(item.get("stem")),
                        student_answer=_option(options, _text(item.get("chosen_option"))),
                        correct_answer=_option(options, _text(item.get("correct_option"))),
                        correct=False,
                        misconception=_maybe(item.get("misconception_code")),
                    )
                )
    return LearnerAnswersResponse(source="missed_only" if answers else "none", answers=answers)
