"""The evaluation's marked classwork, read for a lesson, and copied onto another plan."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
    PlanVersionObjective,
)
from app.domains.assessments.models import (
    StudyClassworkAnswer,
    StudyClassworkQuestion,
    StudyClassworkScript,
)
from app.domains.assessments.models.exit_ticket import ExitTicketSubmission
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.assessments.onbehalf_schemas import MarkedWork
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.learners.models.learner import LearnerProfile
from app.domains.teaching.domain.study_results import MarkedAnswer, MarkedScript
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace


@dataclass(frozen=True)
class StudySource:
    plan_version_id: str
    lesson_title: str
    learners: int


class StudyResultsRepository:
    async def sources(self, db: AsyncSession) -> list[StudySource]:
        """The evaluation's own lessons with marked scripts, with how many learners.

        A lesson is the evaluation's when one of its experiments was run on that plan version, so
        a lesson the marks were only copied onto is not listed.
        """
        rows = (
            await db.execute(
                select(
                    StudyClassworkScript.plan_version_id,
                    LessonPlan.title,
                    func.count(StudyClassworkScript.student_id.distinct()),
                )
                .join(PlanVersion, PlanVersion.version_id == StudyClassworkScript.plan_version_id)
                .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
                .where(StudyClassworkScript.plan_version_id.in_(select(Experiment.plan_version_id)))
                .group_by(StudyClassworkScript.plan_version_id, LessonPlan.title)
                .order_by(StudyClassworkScript.plan_version_id)
            )
        ).all()
        return [StudySource(version, title, learners) for version, title, learners in rows]

    async def lesson_in_workspace(
        self, db: AsyncSession, workspace_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> bool:
        found = await db.execute(
            select(LessonPeriod.id)
            .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
            .join(
                TeacherWorkspace,
                TeacherWorkspace.term_class_subject_id == SchemeOfWork.term_class_subject_id,
            )
            .where(TeacherWorkspace.id == workspace_id, LessonPeriod.id == lesson_period_id)
        )
        return found.scalar_one_or_none() is not None

    async def approved_version_of(
        self, db: AsyncSession, lesson_period_id: uuid.UUID
    ) -> str | None:
        """The newest approved plan version of the lesson."""
        return (
            await db.execute(
                select(PlanVersion.version_id)
                .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
                .where(
                    LessonPlan.lesson_period_id == lesson_period_id,
                    PlanVersion.status == PlanVersionStatus.APPROVED,
                )
                .order_by(PlanVersion.created_at.desc())
                .limit(1)
            )
        ).scalar_one_or_none()

    async def version_with_results(
        self, db: AsyncSession, lesson_period_id: uuid.UUID
    ) -> str | None:
        """The plan version of the lesson that has marked scripts, if any."""
        return (
            await db.execute(
                select(StudyClassworkScript.plan_version_id)
                .join(PlanVersion, PlanVersion.version_id == StudyClassworkScript.plan_version_id)
                .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
                .where(LessonPlan.lesson_period_id == lesson_period_id)
                .limit(1)
            )
        ).scalar_one_or_none()

    async def has_scripts(self, db: AsyncSession, plan_version_id: str) -> bool:
        found = await db.execute(
            select(StudyClassworkScript.id)
            .where(StudyClassworkScript.plan_version_id == plan_version_id)
            .limit(1)
        )
        return found.scalar_one_or_none() is not None

    async def scripts(self, db: AsyncSession, plan_version_id: str) -> list[MarkedScript]:
        """Each learner's marked script for the plan version, with the objective of each answer."""
        objective_of = {
            n: objective
            for n, objective in (
                await db.execute(
                    select(
                        StudyClassworkQuestion.question_n,
                        StudyClassworkQuestion.lesson_objective_id,
                    ).where(StudyClassworkQuestion.plan_version_id == plan_version_id)
                )
            ).all()
        }
        rows = (
            await db.execute(
                select(
                    StudyClassworkScript.id,
                    StudyClassworkScript.student_id,
                    LearnerProfile.full_name,
                    StudyClassworkScript.teacher_total,
                )
                .join(LearnerProfile, LearnerProfile.student_id == StudyClassworkScript.student_id)
                .where(StudyClassworkScript.plan_version_id == plan_version_id)
            )
        ).all()
        answers = (
            await db.execute(
                select(
                    StudyClassworkAnswer.script_id,
                    StudyClassworkAnswer.question_n,
                    StudyClassworkAnswer.mark,
                    StudyClassworkAnswer.misconception_code,
                ).where(StudyClassworkAnswer.plan_version_id == plan_version_id)
            )
        ).all()
        by_script: dict[uuid.UUID, list[MarkedAnswer]] = {}
        for script_id, n, mark, code in answers:
            if n in objective_of:
                by_script.setdefault(script_id, []).append(
                    MarkedAnswer(objective_of[n], mark, code)
                )
        return [
            MarkedScript(student_id, name, total, by_script.get(script_id, []))
            for script_id, student_id, name, total in rows
        ]

    async def marked_work(
        self, db: AsyncSession, plan_version_id: str, student_id: str
    ) -> list[MarkedWork]:
        """One learner's marked classwork for the plan version, question by question."""
        questions = {
            n: (objective, text, answer)
            for n, objective, text, answer in (
                await db.execute(
                    select(
                        StudyClassworkQuestion.question_n,
                        StudyClassworkQuestion.lesson_objective_id,
                        StudyClassworkQuestion.text,
                        StudyClassworkQuestion.answer,
                    ).where(StudyClassworkQuestion.plan_version_id == plan_version_id)
                )
            ).all()
        }
        rows = (
            await db.execute(
                select(
                    StudyClassworkAnswer.question_n,
                    StudyClassworkAnswer.mark,
                    StudyClassworkAnswer.working,
                    StudyClassworkAnswer.misconception_code,
                    StudyClassworkAnswer.misconception_why,
                )
                .join(
                    StudyClassworkScript, StudyClassworkScript.id == StudyClassworkAnswer.script_id
                )
                .where(
                    StudyClassworkScript.plan_version_id == plan_version_id,
                    StudyClassworkScript.student_id == student_id,
                )
                .order_by(StudyClassworkAnswer.question_n)
            )
        ).all()
        return [
            MarkedWork(
                lesson_objective_id=questions[n][0],
                question=questions[n][1],
                model_answer=questions[n][2] or "",
                mark=mark,
                working=working or "",
                misconception_code=code,
                misconception_why=why,
            )
            for n, mark, working, code, why in rows
            if n in questions
        ]

    async def is_evaluation_version(self, db: AsyncSession, plan_version_id: str) -> bool:
        """Whether the plan version is one the evaluation ran an experiment on."""
        found = await db.execute(
            select(Experiment.id).where(Experiment.plan_version_id == plan_version_id).limit(1)
        )
        return found.scalar_one_or_none() is not None

    async def approved_note(
        self, db: AsyncSession, plan_version_id: str
    ) -> tuple[str, set[str]] | None:
        """The plan version's approved lesson note: its id and the steps it has a section for."""
        row = (
            await db.execute(
                select(Artefact.artefact_id, Artefact.manifest)
                .where(
                    Artefact.plan_version_id == plan_version_id,
                    Artefact.artefact_type == "lesson_note",
                    Artefact.review_status == "approved",
                )
                .order_by(Artefact.version.desc())
                .limit(1)
            )
        ).first()
        if row is None:
            return None
        sections = row.manifest.get("sections") if isinstance(row.manifest, dict) else None
        steps = {
            str(section["step_id"])
            for section in (sections if isinstance(sections, list) else [])
            if isinstance(section, dict) and section.get("step_id") and section.get("body")
        }
        return row.artefact_id, steps

    async def plan_step_ids(self, db: AsyncSession, plan_version_id: str) -> set[str]:
        """The plan's steps that have something to teach, so a note needs a section for each."""
        plan = (
            await db.execute(
                select(PlanVersion.session_plan).where(PlanVersion.version_id == plan_version_id)
            )
        ).scalar_one_or_none()
        steps = plan.get("steps") if isinstance(plan, dict) else None
        return {
            str(step["step_id"])
            for step in (steps if isinstance(steps, list) else [])
            if isinstance(step, dict)
            and step.get("step_id")
            and step.get("step_kind") != "evaluation"
        }

    async def submission_results(
        self, db: AsyncSession, plan_version_id: str, student_id: str
    ) -> dict[str, object] | None:
        """The results a learner's submission for the plan version holds."""
        results = (
            await db.execute(
                select(ExitTicketSubmission.results).where(
                    ExitTicketSubmission.plan_version_id == plan_version_id,
                    ExitTicketSubmission.student_id == student_id,
                )
            )
        ).scalar_one_or_none()
        return results if isinstance(results, dict) else None

    async def item_responses(
        self, db: AsyncSession, plan_version_id: str, student_id: str
    ) -> list[tuple[str | None, str, dict[str, str], str, str, bool, str | None]]:
        """A learner's answers to the class test items.

        Each row is objective, stem, options, right option, chosen option, whether it was right,
        and the mistake the choice shows.
        """
        rows = (
            await db.execute(
                select(
                    ExitTicketItem.lesson_objective_id,
                    ExitTicketItem.stem,
                    ExitTicketItem.options,
                    ExitTicketItem.correct_option,
                    StudentItemResponse.choice,
                    StudentItemResponse.is_correct,
                    ExitTicketItem.option_misconceptions,
                )
                .join(StudentItemResponse, StudentItemResponse.item_id == ExitTicketItem.id)
                .where(
                    ExitTicketItem.plan_version_id == plan_version_id,
                    StudentItemResponse.student_id == student_id,
                )
                .order_by(ExitTicketItem.created_at)
            )
        ).all()
        return [
            (
                objective,
                stem,
                options if isinstance(options, dict) else {},
                correct,
                choice,
                bool(is_right),
                (mistakes or {}).get(choice) if isinstance(mistakes, dict) else None,
            )
            for objective, stem, options, correct, choice, is_right, mistakes in rows
        ]

    async def learner_name(self, db: AsyncSession, student_id: str) -> str:
        """The name of a learner of the evaluation, as their marks are listed."""
        name = (
            await db.execute(
                select(LearnerProfile.full_name).where(LearnerProfile.student_id == student_id)
            )
        ).scalar_one_or_none()
        return name or student_id

    async def objective_ids(self, db: AsyncSession, plan_version_id: str) -> set[str]:
        return set(
            (
                await db.execute(
                    select(PlanVersionObjective.lesson_objective_id).where(
                        PlanVersionObjective.plan_version_id == plan_version_id
                    )
                )
            ).scalars()
        )

    async def question_objectives(self, db: AsyncSession, plan_version_id: str) -> set[str]:
        return set(
            (
                await db.execute(
                    select(StudyClassworkQuestion.lesson_objective_id)
                    .where(StudyClassworkQuestion.plan_version_id == plan_version_id)
                    .distinct()
                )
            ).scalars()
        )

    async def objective_texts(self, db: AsyncSession, plan_version_id: str) -> dict[str, str]:
        rows = (
            await db.execute(
                select(
                    PlanVersionObjective.lesson_objective_id, PlanVersionObjective.objective_text
                ).where(PlanVersionObjective.plan_version_id == plan_version_id)
            )
        ).all()
        return {objective: text for objective, text in rows}

    async def copy(self, db: AsyncSession, from_version: str, to_version: str) -> int:
        """Copy the marked classwork of one plan version onto another; the number of scripts."""
        questions = (
            await db.execute(
                select(StudyClassworkQuestion).where(
                    StudyClassworkQuestion.plan_version_id == from_version
                )
            )
        ).scalars()
        for question in questions:
            db.add(
                StudyClassworkQuestion(
                    plan_version_id=to_version,
                    assessed_set=question.assessed_set,
                    question_n=question.question_n,
                    lesson_objective_id=question.lesson_objective_id,
                    text=question.text,
                    answer=question.answer,
                    answer_source=question.answer_source,
                )
            )
        scripts = list(
            (
                await db.execute(
                    select(StudyClassworkScript).where(
                        StudyClassworkScript.plan_version_id == from_version
                    )
                )
            ).scalars()
        )
        copies: dict[uuid.UUID, StudyClassworkScript] = {}
        for script in scripts:
            copy = StudyClassworkScript(
                id=uuid.uuid4(),
                plan_version_id=to_version,
                student_id=script.student_id,
                teacher_total=script.teacher_total,
                capture_complete=script.capture_complete,
            )
            copies[script.id] = copy
            db.add(copy)
        await db.flush()
        answers = (
            await db.execute(
                select(StudyClassworkAnswer).where(
                    StudyClassworkAnswer.plan_version_id == from_version
                )
            )
        ).scalars()
        for answer in answers:
            db.add(
                StudyClassworkAnswer(
                    script_id=copies[answer.script_id].id,
                    plan_version_id=to_version,
                    question_n=answer.question_n,
                    mark=answer.mark,
                    uncertain=answer.uncertain,
                    working=answer.working,
                    misconception_code=answer.misconception_code,
                    misconception_why=answer.misconception_why,
                )
            )
        await db.flush()
        return len(copies)
