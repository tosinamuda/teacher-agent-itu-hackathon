"""An ended experiment's record, read from its runs, its import record and the study's ratings."""

from __future__ import annotations

import uuid

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.evaluation.application.study_results import (
    LessonResults,
    RatedScore,
    StudyResults,
    objective_means,
    part_1_means,
    part_2_counts,
)
from app.domains.evaluation.infrastructure.models import EvaluationRater
from app.domains.evaluation.infrastructure.study_rating_models import (
    StudyComparativeJudgement,
    StudyCriterionScore,
    StudyRatingDocument,
)
from app.domains.experiments.application.study_record import (
    ComparedLesson,
    DatasetRelease,
    GenerationRecord,
    LessonDesign,
    Provenance,
    RatedSet,
    RaterSchedule,
    StudyDesign,
    StudySource,
    Transcript,
)
from app.domains.experiments.domain.study_release import hub_repo
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
    Investigation,
)
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from app.domains.experiments.infrastructure.study_transcript_models import StudyTranscript

#: A note's condition and draw, through the run that wrote it.
_RUN = (
    ExperimentConditionRun,
    ExperimentConditionRun.experiment_condition_run_id == Artefact.experiment_condition_run_id,
)
_DRAW = (ExperimentExecution, ExperimentExecution.id == ExperimentConditionRun.execution_db_id)
#: The experiment, and so the lesson, a draw belongs to.
_EXPERIMENT = (Experiment, Experiment.id == ExperimentExecution.experiment_db_id)

#: What a Part 1 score is read with: the note's condition, and who scored which cell.
_SCORED = (
    ExperimentConditionRun.condition_code,
    StudyCriterionScore.criterion_id,
    StudyCriterionScore.score,
    StudyCriterionScore.artefact_id,
    StudyCriterionScore.lesson_objective_id,
    StudyCriterionScore.rater,
)


def _rated(row: Row) -> RatedScore:
    return RatedScore(
        row.condition_code,
        row.criterion_id,
        row.score,
        (row.artefact_id, row.lesson_objective_id),
        row.rater,
    )


_TRANSCRIPT_STAGES = ("teacher_record", "teacher_cleaned", "cleaning_log", "learner_script")


class SqlAlchemyStudyRecord:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def _study_source(self, investigation_db_id: uuid.UUID) -> StudySource | None:
        record = await self._db.scalar(
            select(StudyImport)
            .join(Investigation, Investigation.investigation_id == StudyImport.investigation_id)
            .where(Investigation.id == investigation_db_id)
        )
        if record is None:
            return None
        return StudySource(
            datasets=[
                DatasetRelease(hub_repo(name), pin["revision"], pin["provenance_sha256"])
                for name, pin in sorted(record.release.items())
            ],
            importer_sha256=record.importer,
            imported_at=record.imported_at,
        )

    async def provenance(
        self, *, experiment_db_id: uuid.UUID, investigation_db_id: uuid.UUID
    ) -> Provenance:
        """The release an imported study came from, and the model and prompt behind each note."""
        runs = await self._db.execute(
            select(
                ExperimentExecution.hypothesis,
                ExperimentConditionRun.model_name,
                ExperimentConditionRun.prompt_version,
                func.count(),
            )
            .join(*_DRAW)
            .where(ExperimentExecution.experiment_db_id == experiment_db_id)
            .group_by(
                ExperimentExecution.hypothesis,
                ExperimentConditionRun.model_name,
                ExperimentConditionRun.prompt_version,
            )
            .order_by(ExperimentExecution.hypothesis, ExperimentConditionRun.prompt_version)
        )
        return Provenance(
            source=await self._study_source(investigation_db_id),
            generation=[GenerationRecord(*row) for row in runs.tuples()],
        )

    async def schedule(self, plan_version_id: str) -> RaterSchedule:
        """Every set returned for the lesson's notes, and the lessons Part 2 compared."""
        rows = await self._db.execute(
            select(
                StudyRatingDocument,
                EvaluationRater.display_name,
                Artefact.student_id,
                ExperimentConditionRun.condition_code,
                ExperimentExecution.attempt_number,
            )
            .join(EvaluationRater, EvaluationRater.id == StudyRatingDocument.rater_db_id)
            .join(Artefact, Artefact.artefact_id == StudyRatingDocument.artefact_a_id)
            .outerjoin(*_RUN)
            .outerjoin(*_DRAW)
            .where(Artefact.plan_version_id == plan_version_id)
            .order_by(
                StudyRatingDocument.part, StudyRatingDocument.rater, StudyRatingDocument.packet
            )
        )
        compared = await self._db.execute(
            select(Experiment.experiment_id, Experiment.experiment_code)
            .where(
                Experiment.plan_version_id.in_(
                    select(Artefact.plan_version_id)
                    .join(
                        StudyRatingDocument,
                        StudyRatingDocument.artefact_a_id == Artefact.artefact_id,
                    )
                    .where(StudyRatingDocument.part == 2)
                )
            )
            .order_by(Experiment.experiment_code)
        )
        return RaterSchedule(
            sets=[
                RatedSet(
                    part=row.part,
                    rater=row.rater,
                    rater_name=rater_name,
                    packet=row.packet,
                    delivery_order=row.delivery_order,
                    note_id=row.artefact_a_id,
                    condition=condition,
                    draw=draw,
                    other_note_id=row.artefact_b_id,
                    learner_id=student_id if row.part == 2 else None,
                    state=row.state,
                    date_completed=row.date_completed,
                )
                for row, rater_name, student_id, condition, draw in rows.all()
            ],
            compared_lessons=[ComparedLesson(*lesson) for lesson in compared.all()],
        )

    async def results(self, plan_version_id: str) -> LessonResults:
        """The lesson's Part 1 scores by condition and its Part 2 choices, described."""
        scores = await self._db.execute(
            select(*_SCORED)
            .join(Artefact, Artefact.artefact_id == StudyCriterionScore.artefact_id)
            .join(*_RUN)
            .where(Artefact.plan_version_id == plan_version_id)
        )
        judgements = await self._db.execute(
            select(
                StudyComparativeJudgement.criterion_id,
                StudyComparativeJudgement.choice,
                StudyComparativeJudgement.favoured_condition,
            )
            .join(Artefact, Artefact.artefact_id == StudyComparativeJudgement.artefact_a_id)
            .where(Artefact.plan_version_id == plan_version_id)
        )
        return LessonResults(
            part_1=part_1_means(_rated(row) for row in scores.all()),
            part_2=part_2_counts(
                (criterion, choice, favoured or "neither")
                for criterion, choice, favoured in judgements.tuples()
            ),
        )

    async def _objective_texts(self, plan_version_ids: set[str]) -> dict[str, str]:
        plans = await self._db.execute(
            select(PlanVersion.session_plan).where(PlanVersion.version_id.in_(plan_version_ids))
        )
        return {
            str(objective["lesson_objective_id"]): str(objective.get("objective_text") or "")
            for (plan,) in plans.tuples()
            for objective in (plan or {}).get("lesson_plan_objectives") or []
        }

    async def _study_scores(self, investigation: uuid.UUID) -> list[Row]:
        """Every Part 1 score in the study, with the lesson and condition of the note it rated."""
        return list(
            (
                await self._db.execute(
                    select(Experiment.experiment_code, Artefact.plan_version_id, *_SCORED)
                    .join(Artefact, Artefact.artefact_id == StudyCriterionScore.artefact_id)
                    .join(*_RUN)
                    .join(*_DRAW)
                    .join(*_EXPERIMENT)
                    .where(Experiment.investigation_db_id == investigation)
                )
            ).all()
        )

    async def _study_judgements(self, investigation: uuid.UUID) -> list[tuple[str, str, str]]:
        """Every Part 2 judgement in the study, by criterion, choice and the note it favoured."""
        rows = await self._db.execute(
            select(
                StudyComparativeJudgement.criterion_id,
                StudyComparativeJudgement.choice,
                StudyComparativeJudgement.favoured_condition,
            )
            .join(Artefact, Artefact.artefact_id == StudyComparativeJudgement.artefact_a_id)
            .join(*_RUN)
            .join(*_DRAW)
            .join(*_EXPERIMENT)
            .where(Experiment.investigation_db_id == investigation)
        )
        return [(criterion, choice, favoured or "neither") for criterion, choice, favoured in rows]

    async def study_results(self, investigation_id: str) -> StudyResults | None:
        """The study's ratings across its lessons, each note placed by the run that wrote it."""
        investigation = await self._db.scalar(
            select(Investigation.id).where(Investigation.investigation_id == investigation_id)
        )
        if investigation is None:
            return None
        scores = await self._study_scores(investigation)
        texts = await self._objective_texts({row.plan_version_id for row in scores})
        return StudyResults(
            part_1=part_1_means(_rated(row) for row in scores),
            objectives=objective_means(
                (
                    (row.experiment_code, row.lesson_objective_id, row.condition_code, row.score)
                    for row in scores
                ),
                texts,
            ),
            part_2=part_2_counts(await self._study_judgements(investigation)),
        )

    async def transcripts(self, plan_version_id: str) -> list[Transcript]:
        """The lesson's published transcripts, in the order they were made, then each script."""
        rows = await self._db.execute(
            select(StudyTranscript).where(StudyTranscript.plan_version_id == plan_version_id)
        )
        ordered = sorted(
            rows.scalars(), key=lambda row: (_TRANSCRIPT_STAGES.index(row.kind), row.source_path)
        )
        return [
            Transcript(row.kind, row.student_id, row.pages, row.header, row.body, row.source_path)
            for row in ordered
        ]

    async def _h1_runs(self, investigation: uuid.UUID) -> list[tuple[str, int, str]]:
        """Each class note of the study: its lesson, draw and condition."""
        rows = await self._db.execute(
            select(
                Experiment.experiment_id,
                ExperimentExecution.attempt_number,
                ExperimentConditionRun.condition_code,
            )
            .select_from(ExperimentConditionRun)
            .join(*_DRAW)
            .join(*_EXPERIMENT)
            .where(Experiment.investigation_db_id == investigation)
            .where(ExperimentExecution.hypothesis == "H1")
        )
        return list(rows.tuples())

    async def _learners(self, investigation: uuid.UUID) -> dict[str, int]:
        """How many focal learners each of the study's lessons has."""
        rows = await self._db.execute(
            select(Experiment.experiment_id, func.count())
            .select_from(ExperimentFocalCase)
            .join(
                ExperimentExecution, ExperimentExecution.id == ExperimentFocalCase.execution_db_id
            )
            .join(*_EXPERIMENT)
            .where(Experiment.investigation_db_id == investigation)
            .group_by(Experiment.experiment_id)
        )
        return {experiment_id: int(count) for experiment_id, count in rows.tuples()}

    async def _rating_sets(self, investigation: uuid.UUID) -> list[tuple[str, int, str]]:
        """Each returned rating set of the study: its lesson, part and rater."""
        rows = await self._db.execute(
            select(Experiment.experiment_id, StudyRatingDocument.part, StudyRatingDocument.rater)
            .select_from(StudyRatingDocument)
            .join(Artefact, Artefact.artefact_id == StudyRatingDocument.artefact_a_id)
            .join(*_RUN)
            .join(*_DRAW)
            .join(*_EXPERIMENT)
            .where(Experiment.investigation_db_id == investigation)
        )
        return list(rows.tuples())

    async def design(self, investigation_id: str) -> StudyDesign | None:
        """The study's shape: each lesson's objectives, notes, learners and rating sets."""
        investigation = await self._db.scalar(
            select(Investigation.id).where(Investigation.investigation_id == investigation_id)
        )
        if investigation is None:
            return None
        lessons = await self._db.execute(
            select(Experiment.experiment_id, PlanVersion.session_plan)
            .join(PlanVersion, PlanVersion.version_id == Experiment.plan_version_id)
            .where(Experiment.investigation_db_id == investigation)
            .order_by(Experiment.experiment_code)
        )
        runs = await self._h1_runs(investigation)
        learners = await self._learners(investigation)
        sets = await self._rating_sets(investigation)

        def sets_of(experiment_id: str, part: int) -> int:
            return sum(1 for row in sets if row[0] == experiment_id and row[1] == part)

        return StudyDesign(
            lessons=[
                LessonDesign(
                    experiment_id=experiment_id,
                    objectives=len((plan or {}).get("lesson_plan_objectives") or []),
                    class_notes=sum(1 for run in runs if run[0] == experiment_id),
                    learners=learners.get(experiment_id, 0),
                    part_1_sets=sets_of(experiment_id, 1),
                    part_2_sets=sets_of(experiment_id, 2),
                )
                for experiment_id, plan in lessons.tuples()
            ],
            conditions=sorted({condition for _, _, condition in runs}),
            draws=max((draw for _, draw, _ in runs), default=0),
            raters=len({rater for _, _, rater in sets}),
        )
