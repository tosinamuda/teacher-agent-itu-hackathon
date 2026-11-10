"""A lesson's marked classwork as the app keeps it: the questions, each script, each answer."""

from __future__ import annotations

import uuid

from app.domains.assessments.models import (
    StudyClassworkAnswer,
    StudyClassworkQuestion,
    StudyClassworkScript,
)
from experiments.h2_personalisation_eval.students import Classwork
from experiments.study_import.lessons import learner_id


def classwork_rows(
    classwork: Classwork, plan_version_id: str
) -> tuple[list[object], list[StudyClassworkAnswer]]:
    """The questions and scripts, then the answers that reference the scripts."""
    questions: list[object] = [
        StudyClassworkQuestion(
            plan_version_id=plan_version_id,
            assessed_set=classwork.assessed_set,
            question_n=question.n,
            lesson_objective_id=question.objective,
            text=question.text,
            answer=question.answer,
            answer_source=question.answer_source,
        )
        for question in classwork.questions.values()
    ]
    scripts: list[object] = []
    answers: list[StudyClassworkAnswer] = []
    for student in classwork.students:
        script = StudyClassworkScript(
            id=uuid.uuid4(),
            plan_version_id=plan_version_id,
            student_id=learner_id(student.id),
            teacher_total=student.teacher_total,
            capture_complete=student.capture_complete,
        )
        scripts.append(script)
        answers += [
            StudyClassworkAnswer(
                script_id=script.id,
                plan_version_id=plan_version_id,
                question_n=response.n,
                mark=response.mark,
                uncertain=response.uncertain,
                working=response.working,
                misconception_code=response.misconception_code,
                misconception_why=response.misconception_why,
            )
            for response in student.responses
        ]
    return [*questions, *scripts], answers
