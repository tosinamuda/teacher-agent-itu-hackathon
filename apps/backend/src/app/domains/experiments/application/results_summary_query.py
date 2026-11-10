"""Results summary — flatten an execution's runs/cases/packets into a dashboard DTO.

The summary is a read-side presentation of one execution: condition runs (with
status counts), focal cases, and packets, rolled into ``ExperimentResultSummary``
for the experiment-detail view. Distinct from CRUD, execution lifecycle, packet
export, and the C4 governance summary — those each own their own concern.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import Protocol

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.evaluation.infrastructure.models import EvaluationPacket
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.result_schemas import ExperimentResultSummary
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.learner_state.domain.models import misconception_codes_for_snapshot


class ResultsSummaryReader(Protocol):
    """Rows flattened into an execution results summary."""

    async def get_execution(self, execution_id: str) -> ExperimentExecution | None: ...

    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> list[ExperimentConditionRun]: ...

    async def list_focal_cases(self, execution_db_id: uuid.UUID) -> list[ExperimentFocalCase]: ...

    async def list_packets(self, execution_db_id: uuid.UUID) -> list[EvaluationPacket]: ...

    async def current_artefacts_by_condition_run(
        self, run_ids: Sequence[str]
    ) -> dict[str, Artefact]: ...


class ExperimentResultsSummaryQuery:
    """Own the execution-results summary DTO (read-only, presentation-shaped)."""

    def __init__(self, repository: ResultsSummaryReader) -> None:
        self.repository = repository

    async def build_results_summary(
        self,
        *,
        experiment_id: str | None = None,
        execution_id: str | None = None,
    ) -> ExperimentResultSummary:
        """Flatten one execution's runs + focal cases + packets into the dashboard DTO.

        Pass ``execution_id`` to pin a specific execution; otherwise the latest
        execution for ``experiment_id`` is used.
        """
        execution = await self._resolve_execution(
            experiment_id=experiment_id,
            execution_id=execution_id,
        )
        condition_runs = await self.repository.list_condition_runs(execution.id)
        focal_cases = await self.repository.list_focal_cases(execution.id)
        packets = await self.repository.list_packets(execution.id)
        # Each run's current pack id via the back-pointer (one query).
        packs = await self.repository.current_artefacts_by_condition_run(
            [run.experiment_condition_run_id for run in condition_runs]
        )
        pack_ids = {run_id: artefact.artefact_id for run_id, artefact in packs.items()}

        status_counts: dict[str, int] = {}
        for run in condition_runs:
            status_counts[run.status] = status_counts.get(run.status, 0) + 1

        summary = {
            "execution_id": execution.execution_id,
            "hypothesis": execution.hypothesis,
            "attempt_number": execution.attempt_number,
            "status": execution.status,
            "condition_run_count": len(condition_runs),
            "focal_case_count": len(focal_cases),
            "packet_count": len(packets),
            "status_counts": status_counts,
            "condition_runs": [
                {
                    "experiment_condition_run_id": run.experiment_condition_run_id,
                    "condition_code": run.condition_code,
                    "status": run.status,
                    "learner_id": run.student_id,
                    "artefact_plan_id": run.artefact_plan_id,
                    "artefact_build_job_id": run.artefact_build_job_id,
                    "artefact_id": pack_ids.get(run.experiment_condition_run_id),
                    "error_message": run.error_message,
                }
                for run in condition_runs
            ],
            "focal_cases": [
                {
                    "experiment_focal_case_id": focal_case.experiment_focal_case_id,
                    "learner_id": focal_case.student_id,
                    "focal_case_type": focal_case.focal_case_type,
                    "misconception_codes": misconception_codes_for_snapshot(
                        focal_case.learner_state_snapshot
                    ),
                }
                for focal_case in focal_cases
            ],
            "packets": [
                {
                    "evaluation_packet_id": packet.evaluation_packet_id,
                    "packet_code": packet.packet_code,
                    "status": packet.status,
                    "primary_condition_run_id": packet.primary_condition_run_id,
                    "experiment_focal_case_id": packet.experiment_focal_case_id,
                    "condition_run_ids": list(packet.condition_run_ids),
                }
                for packet in packets
            ],
        }
        return ExperimentResultSummary.model_validate(summary)

    async def _resolve_execution(
        self,
        *,
        experiment_id: str | None,
        execution_id: str | None,
    ) -> ExperimentExecution:
        """Pin a specific execution by id, or fall back to the latest for the experiment."""
        if execution_id is not None:
            execution = await self.repository.get_execution(execution_id)
            if execution is None:
                raise ExperimentApplicationError(404, "execution_not_found")
            return execution
        if experiment_id is None:
            raise ExperimentApplicationError(422, "experiment_or_execution_required")
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        executions = await self.repository.list_executions_for_experiment(experiment.id)
        if not executions:
            raise ExperimentApplicationError(404, "experiment_execution_not_found")
        return executions[0]
