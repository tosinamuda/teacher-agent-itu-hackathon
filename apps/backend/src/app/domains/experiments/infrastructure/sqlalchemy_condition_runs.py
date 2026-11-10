"""SQLAlchemy persistence for condition-run records and review artefacts."""

from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.application.materialisation import (
    ReviewPackArtefactWriter,
    ReviewPackMaterialisation,
)
from app.domains.experiments.domain.types import (
    ConditionCode,
    ConditionRunStatus,
)
from app.domains.experiments.infrastructure.models import ExperimentConditionRun
from app.domains.experiments.review_pack_study.condition_runs.records import (
    CompletedConditionRun,
    FailedConditionRun,
)
from app.infra.dspy_lm import active_model_name
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.time import utc_now

from .generated_review_pack_record import generated_pack_record


class SqlAlchemyConditionRuns:
    """Persist and query one session's condition runs; the store ends the write."""

    def __init__(self, session: AsyncSession, artefacts: ReviewPackArtefactWriter) -> None:
        self._db = session
        self._artefacts = artefacts

    async def record(
        self,
        *,
        completed: Sequence[CompletedConditionRun],
        failed: Sequence[FailedConditionRun],
    ) -> None:
        """Stage every generated and failed run; the store's commit makes them durable."""
        await self.save_completed(records=completed)
        await self.save_failed(records=failed)

    async def save_completed(
        self,
        *,
        records: Sequence[CompletedConditionRun],
    ) -> list[ExperimentConditionRun]:
        """Stage a complete condition batch inside one SAVEPOINT."""
        runs: list[ExperimentConditionRun] = []
        async with self._db.begin_nested():
            for record in records:
                runs.append(self.add_completed(record=record))
            await self._db.flush()
            for run, record in zip(runs, records, strict=True):
                self._stage_artefact(run=run, record=record)
        return runs

    def add_completed(
        self,
        *,
        record: CompletedConditionRun,
    ) -> ExperimentConditionRun:
        """Stage one successful run and its linked artefact."""
        validation = record.result.validation
        status = (
            ConditionRunStatus.SUCCEEDED
            if validation is None or validation.passed
            else ConditionRunStatus.NEEDS_REVIEW
        )
        run = ExperimentConditionRun(
            experiment_condition_run_id=new_public_id(PublicIdPrefix.EXPERIMENT_CONDITION_RUN),
            execution_db_id=record.execution_db_id,
            focal_case_db_id=record.focal_case_db_id,
            hypothesis=record.hypothesis.value,
            condition_code=record.condition_code.value,
            student_id=record.student_id,
            status=status,
            error_message=None,
            condition_profile=record.profile.model_dump(mode="json"),
            validation_result=(validation.model_dump(mode="json") if validation else None),
            generated_pack=generated_pack_record(record.result),
            model_name=active_model_name(),
            prompt_version=record.result.prompt_provenance.composite_fingerprint,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self._db.add(run)
        return run

    def _stage_artefact(
        self,
        *,
        run: ExperimentConditionRun,
        record: CompletedConditionRun,
    ) -> None:
        self._artefacts.stage(
            ReviewPackMaterialisation(
                condition_run_id=run.experiment_condition_run_id,
                plan_version_id=record.plan_version_id,
                scope=record.scope,
                learner_id=record.student_id,
                result=record.result,
                requires_teacher_review=record.profile.teacher_validation.enabled,
                artefact_refs=record.artefact_refs,
            )
        )

    async def save_failed(
        self,
        *,
        records: Sequence[FailedConditionRun],
    ) -> list[ExperimentConditionRun]:
        """Stage every failed condition inside one SAVEPOINT."""
        runs: list[ExperimentConditionRun] = []
        async with self._db.begin_nested():
            for record in records:
                runs.append(self.add_failed(record=record))
        return runs

    def add_failed(
        self,
        *,
        record: FailedConditionRun,
    ) -> ExperimentConditionRun:
        """Stage a failed condition run without an artefact."""
        run = ExperimentConditionRun(
            experiment_condition_run_id=new_public_id(PublicIdPrefix.EXPERIMENT_CONDITION_RUN),
            execution_db_id=record.execution_db_id,
            focal_case_db_id=record.focal_case_db_id,
            hypothesis=record.hypothesis.value,
            condition_code=record.condition_code.value,
            student_id=record.student_id,
            status=ConditionRunStatus.FAILED,
            error_message=(record.error or "generation failed")[:2000],
            condition_profile=record.profile.model_dump(mode="json"),
            validation_result=None,
            generated_pack=None,
            model_name=active_model_name(),
            prompt_version=None,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self._db.add(run)
        return run

    async def find(
        self,
        *,
        execution_db_id: uuid.UUID,
        condition_code: ConditionCode,
    ) -> ExperimentConditionRun | None:
        """Return one condition run for an execution, if present."""
        return (
            (
                await self._db.execute(
                    select(ExperimentConditionRun).where(
                        ExperimentConditionRun.execution_db_id == execution_db_id,
                        ExperimentConditionRun.condition_code == condition_code.value,
                    )
                )
            )
            .scalars()
            .first()
        )

    async def has_failures(
        self,
        *,
        execution_db_id: uuid.UUID,
    ) -> bool:
        """Whether an execution still contains a failed condition."""
        failed = (
            (
                await self._db.execute(
                    select(ExperimentConditionRun.id).where(
                        ExperimentConditionRun.execution_db_id == execution_db_id,
                        ExperimentConditionRun.status == ConditionRunStatus.FAILED,
                    )
                )
            )
            .scalars()
            .first()
        )
        return failed is not None

    async def replace_family(
        self,
        *,
        execution_db_id: uuid.UUID,
        condition_codes: Sequence[ConditionCode],
        records: Sequence[CompletedConditionRun],
    ) -> None:
        """Atomically replace one owning condition and every fork of it."""
        values = [code.value for code in condition_codes]
        async with self._db.begin_nested():
            stale = (
                (
                    await self._db.execute(
                        select(ExperimentConditionRun).where(
                            ExperimentConditionRun.execution_db_id == execution_db_id,
                            ExperimentConditionRun.condition_code.in_(values),
                        )
                    )
                )
                .scalars()
                .all()
            )
            for run in stale:
                await self._db.delete(run)
            await self._db.flush()
            replacement_runs = [self.add_completed(record=record) for record in records]
            await self._db.flush()
            for run, record in zip(replacement_runs, records, strict=True):
                self._stage_artefact(run=run, record=record)
