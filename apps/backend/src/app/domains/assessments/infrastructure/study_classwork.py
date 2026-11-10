"""The study's classwork read from the tables the import wrote it to."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.application.study_classwork import (
    ClassworkAnswer,
    ClassworkQuestion,
    ClassworkScript,
    LearnerClasswork,
)
from app.domains.assessments.models import (
    StudyClassworkAnswer,
    StudyClassworkQuestion,
    StudyClassworkScript,
)


class SqlAlchemyStudyClasswork:
    async def for_learner(
        self, db: AsyncSession, plan_version_id: str, student_id: str
    ) -> LearnerClasswork:
        questions = await db.execute(
            select(StudyClassworkQuestion)
            .where(StudyClassworkQuestion.plan_version_id == plan_version_id)
            .order_by(StudyClassworkQuestion.question_n)
        )
        script = await db.scalar(
            select(StudyClassworkScript).where(
                StudyClassworkScript.plan_version_id == plan_version_id,
                StudyClassworkScript.student_id == student_id,
            )
        )
        answers = (
            await db.execute(
                select(StudyClassworkAnswer)
                .where(StudyClassworkAnswer.script_id == script.id)
                .order_by(StudyClassworkAnswer.question_n)
            )
            if script is not None
            else None
        )
        return LearnerClasswork(
            questions=[
                ClassworkQuestion(
                    n=row.question_n,
                    lesson_objective_id=row.lesson_objective_id,
                    text=row.text,
                    answer=row.answer,
                    answer_source=row.answer_source,
                )
                for row in questions.scalars()
            ],
            script=None
            if script is None or answers is None
            else ClassworkScript(
                teacher_total=script.teacher_total,
                capture_complete=script.capture_complete,
                answers=[
                    ClassworkAnswer(
                        n=row.question_n,
                        mark=row.mark,
                        uncertain=row.uncertain,
                        working=row.working,
                        misconception_code=row.misconception_code,
                        misconception_why=row.misconception_why,
                    )
                    for row in answers.scalars()
                ],
            ),
        )
