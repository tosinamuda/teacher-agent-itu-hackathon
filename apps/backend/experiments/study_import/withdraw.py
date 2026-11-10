"""Remove every row the study import wrote, so a corrected import can replace it.

A concluded study is never edited in place: the app refuses any flush that would change it.
Correcting an import is instead a withdrawal and a fresh import in one transaction, done by
explicit deletes of exactly what the import wrote. The school, its class, the study teacher
and the teacher's workspaces stay: the import finds them again rather than making new ones.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.models import Artefact, ContentApproval
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.assessments.models import (
    StudyClassworkAnswer,
    StudyClassworkQuestion,
    StudyClassworkScript,
)
from app.domains.evaluation.infrastructure.models import EvaluationRater
from app.domains.evaluation.infrastructure.study_rating_models import (
    StudyComparativeJudgement,
    StudyCriterionScore,
    StudyRatingDocument,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
    Investigation,
)
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from app.domains.experiments.infrastructure.study_transcript_models import StudyTranscript
from app.domains.learners.models import LearnerProfile
from app.domains.teaching.models import LessonPeriod, SchemeOfWork
from experiments.study_import.lessons import learner_id, plan_version_id
from experiments.study_import.raters import RATER_ID_PREFIX
from experiments.study_import.runs import INVESTIGATION_ID


async def _ids(db: AsyncSession, query: Select[tuple[Any]]) -> list[Any]:
    return list((await db.execute(query)).scalars())


async def withdraw_study(db: AsyncSession) -> None:
    """Delete the imported study, children before parents; the caller commits or rolls back."""
    versions = await _ids(
        db,
        select(PlanVersion.version_id).where(
            PlanVersion.version_id.startswith(plan_version_id(""))
        ),
    )
    plans = await _ids(db, select(PlanVersion.plan_id).where(PlanVersion.version_id.in_(versions)))
    periods = await _ids(
        db, select(LessonPlan.lesson_period_id).where(LessonPlan.plan_id.in_(plans))
    )
    weeks = await _ids(
        db, select(LessonPeriod.scheme_of_work_id).where(LessonPeriod.id.in_(periods))
    )
    notes = select(Artefact.artefact_id).where(Artefact.plan_version_id.in_(versions))
    investigation = select(Investigation.id).where(
        Investigation.investigation_id == INVESTIGATION_ID
    )
    experiments = select(Experiment.id).where(Experiment.investigation_db_id.in_(investigation))
    executions = select(ExperimentExecution.id).where(
        ExperimentExecution.experiment_db_id.in_(experiments)
    )
    for statement in (
        delete(StudyCriterionScore).where(StudyCriterionScore.artefact_id.in_(notes)),
        delete(StudyComparativeJudgement).where(StudyComparativeJudgement.artefact_a_id.in_(notes)),
        delete(StudyRatingDocument).where(StudyRatingDocument.artefact_a_id.in_(notes)),
        delete(EvaluationRater).where(
            EvaluationRater.origin == "study_record",
            EvaluationRater.rater_id.startswith(RATER_ID_PREFIX),
        ),
        delete(ContentApproval).where(ContentApproval.artefact_id.in_(notes)),
        delete(Artefact).where(Artefact.plan_version_id.in_(versions)),
        delete(ExperimentConditionRun).where(
            ExperimentConditionRun.execution_db_id.in_(executions)
        ),
        delete(ExperimentFocalCase).where(ExperimentFocalCase.execution_db_id.in_(executions)),
        delete(ExperimentExecution).where(ExperimentExecution.experiment_db_id.in_(experiments)),
        delete(Experiment).where(Experiment.investigation_db_id.in_(investigation)),
        delete(Investigation).where(Investigation.investigation_id == INVESTIGATION_ID),
        delete(StudyImport).where(StudyImport.investigation_id == INVESTIGATION_ID),
        delete(StudyClassworkAnswer).where(StudyClassworkAnswer.plan_version_id.in_(versions)),
        delete(StudyClassworkScript).where(StudyClassworkScript.plan_version_id.in_(versions)),
        delete(StudyClassworkQuestion).where(StudyClassworkQuestion.plan_version_id.in_(versions)),
        delete(StudyTranscript).where(StudyTranscript.plan_version_id.in_(versions)),
        delete(PlanVersion).where(PlanVersion.version_id.in_(versions)),
        delete(LessonPlan).where(LessonPlan.plan_id.in_(plans)),
        delete(LessonPeriod).where(LessonPeriod.id.in_(periods)),
        delete(SchemeOfWork).where(SchemeOfWork.id.in_(weeks)),
        delete(LearnerProfile).where(LearnerProfile.student_id.startswith(learner_id(""))),
    ):
        await db.execute(statement.execution_options(synchronize_session=False))
