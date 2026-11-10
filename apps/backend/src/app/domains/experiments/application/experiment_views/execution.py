"""One execution's rows, rendered for the dashboard.

An execution is read as a whole — its condition runs, focal cases and packets —
because the dashboard shows them together and nothing here writes.
"""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.evaluation.infrastructure.models import EvaluationPacket
from app.domains.experiments.api.schemas import (
    EvaluationPacketResponse,
    ExperimentConditionRunResponse,
    ExperimentExecutionResponse,
    ExperimentFocalCaseResponse,
)
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.lookups import execution_or_error
from app.domains.experiments.domain import (
    ConditionCode,
    FocalCaseType,
    Hypothesis,
    PacketStatus,
)
from app.domains.experiments.domain.records import ExecutionRecord
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.learner_state.domain.models import misconception_codes_for_snapshot


class ExperimentExecutionViewReader(Protocol):
    """Rows rendered together for one execution dashboard response."""

    async def get_execution(self, execution_id: str) -> ExperimentExecution | None: ...

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> list[ExperimentConditionRun]: ...

    async def list_focal_cases(self, execution_db_id: uuid.UUID) -> list[ExperimentFocalCase]: ...

    async def list_packets(self, execution_db_id: uuid.UUID) -> list[EvaluationPacket]: ...

    async def current_artefacts_by_condition_run(
        self, run_ids: list[str]
    ) -> dict[str, Artefact]: ...


class ExperimentExecutionViewQuery:
    """Finished execution-detail query injected by the execution route."""

    def __init__(self, reader: ExperimentExecutionViewReader) -> None:
        self.reader = reader

    async def build_detail(self, *, execution_id: str) -> ExperimentExecutionResponse:
        return await build_execution_detail_view(self.reader, execution_id=execution_id)


async def build_execution_detail_view(
    experiments: ExperimentExecutionViewReader,
    *,
    execution_id: str,
) -> ExperimentExecutionResponse:
    """Fetch one execution + its rows + render the ``ExperimentExecutionResponse``."""
    execution = await execution_or_error(experiments, execution_id)
    experiment = await experiments.get_experiment_by_db_id(execution.experiment_db_id)
    if experiment is None:
        raise ExperimentApplicationError(404, "experiment_not_found")
    return await execution_payload(
        experiments, experiment_id=experiment.experiment_id, execution=execution
    )


async def execution_payload(
    experiments: ExperimentExecutionViewReader,
    *,
    experiment_id: str,
    execution: ExecutionRecord,
) -> ExperimentExecutionResponse:
    """Fetch an execution's rows (runs + focal cases + packets) and render the response."""
    condition_runs = await experiments.list_condition_runs(execution.id)
    focal_cases = await experiments.list_focal_cases(execution.id)
    packets = await experiments.list_packets(execution.id)
    # Each run's current pack id, resolved via the back-pointer (one query).
    packs = await experiments.current_artefacts_by_condition_run(
        [run.experiment_condition_run_id for run in condition_runs]
    )
    pack_ids = {run_id: artefact.artefact_id for run_id, artefact in packs.items()}
    return execution_response(
        experiment_id=experiment_id,
        execution=execution,
        condition_runs=condition_runs,
        focal_cases=focal_cases,
        packets=packets,
        pack_ids=pack_ids,
    )


def render_evaluation_packet_response(packet: EvaluationPacket) -> EvaluationPacketResponse:
    """Render an ``EvaluationPacket`` ORM row to the API ``EvaluationPacketResponse`` DTO."""
    return EvaluationPacketResponse(
        evaluation_packet_id=packet.evaluation_packet_id,
        packet_code=packet.packet_code,
        hypothesis=Hypothesis(packet.hypothesis),
        status=PacketStatus(packet.status),
        primary_condition_run_id=packet.primary_condition_run_id,
        experiment_focal_case_id=packet.experiment_focal_case_id,
        export_refs=packet.export_refs,
        condition_run_ids=list(packet.condition_run_ids),
    )


def execution_response(
    *,
    experiment_id: str,
    execution: ExecutionRecord,
    condition_runs: list,
    focal_cases: list,
    packets: list,
    pack_ids: dict[str, str],
) -> ExperimentExecutionResponse:
    """Render an execution + its condition runs / focal cases / packets to the response DTO.

    ``pack_ids`` maps each run's business id to its current pack artefact id
    (resolved via the back-pointer); the response's ``artefact_id`` field reads
    from it rather than a stored column on the run.
    """
    return ExperimentExecutionResponse(
        execution_id=execution.execution_id,
        experiment_id=experiment_id,
        hypothesis=Hypothesis(execution.hypothesis),
        attempt_number=execution.attempt_number,
        status=execution.status,
        runtime_snapshot=execution.runtime_snapshot,
        error_message=execution.error_message,
        error_category=execution.error_category,
        created_at=execution.created_at,
        updated_at=execution.updated_at,
        condition_runs=[
            ExperimentConditionRunResponse(
                experiment_condition_run_id=run.experiment_condition_run_id,
                hypothesis=Hypothesis(run.hypothesis),
                condition_code=ConditionCode(run.condition_code),
                learner_id=run.student_id,
                artefact_plan_id=run.artefact_plan_id,
                artefact_build_job_id=run.artefact_build_job_id,
                artefact_id=pack_ids.get(run.experiment_condition_run_id),
                status=run.status,
                error_message=run.error_message,
            )
            for run in condition_runs
        ],
        focal_cases=[
            ExperimentFocalCaseResponse(
                experiment_focal_case_id=focal_case.experiment_focal_case_id,
                learner_id=focal_case.student_id,
                focal_case_type=FocalCaseType(focal_case.focal_case_type),
                misconception_codes=misconception_codes_for_snapshot(
                    focal_case.learner_state_snapshot
                ),
                learner_state_snapshot=focal_case.learner_state_snapshot,
                selection_metadata=focal_case.selection_metadata,
            )
            for focal_case in focal_cases
        ],
        packets=[render_evaluation_packet_response(packet) for packet in packets],
    )
