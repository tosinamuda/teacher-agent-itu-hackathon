"""Shared packet runtime resolution and narrow packet/identity lookup helpers."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.packet_ports import PacketExperimentContext

# WeasyPrint is the active renderer for the expert rater packs (HTML/CSS -> PDF):
# it renders reading-note / excerpt markdown natively and carries full Unicode, so
# no ``■`` missing-glyph boxes. The reportlab modules (``audit_pack_pdf``,
# ``h1_worksheet_pdf``) are kept in place as a fallback; ``H1_MAJOR_ISSUE_FLAGS``
# still lives in (and is imported from) ``h1_worksheet_pdf`` as its source of truth.
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRater,
)
from app.domains.experiments.application.experiment_context_service import ExperimentContext
from app.shared.session_plan_view import SessionPlanView

if TYPE_CHECKING:
    from app.domains.experiments.infrastructure.models import (
        Experiment,
        ExperimentConditionRun,
        ExperimentExecution,
        ExperimentFocalCase,
    )


@dataclass(frozen=True)
class PacketRuntimeContext:
    execution: ExperimentExecution
    experiment_context: ExperimentContext
    session_plan: SessionPlanView
    condition_runs: list[ExperimentConditionRun]
    run_by_id: dict[str, ExperimentConditionRun]
    focal_case_by_id: dict[str, ExperimentFocalCase]


class PacketRaterReader(Protocol):
    async def get_rater(self, *, rater_id: str) -> EvaluationRater | None: ...


class PacketReader(Protocol):
    async def get_packet(self, *, evaluation_packet_id: str) -> EvaluationPacket | None: ...


class PacketRuntimeExperiments(Protocol):
    async def get_execution_by_db_id(
        self, execution_db_id: uuid.UUID
    ) -> ExperimentExecution | None: ...

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> Sequence[ExperimentConditionRun]: ...

    async def list_focal_cases(
        self, execution_db_id: uuid.UUID
    ) -> Sequence[ExperimentFocalCase]: ...


class PacketRuntime:
    def __init__(
        self,
        rater_reader: PacketRaterReader,
        *,
        experiment_repository: PacketRuntimeExperiments,
        experiment_context_service: PacketExperimentContext,
    ) -> None:
        self.rater_reader = rater_reader
        self.experiment_repository = experiment_repository
        self.experiment_context_service = experiment_context_service

    async def load_packet_runtime(
        self,
        *,
        packet: EvaluationPacket,
    ) -> PacketRuntimeContext:
        execution = await self.experiment_repository.get_execution_by_db_id(
            packet.execution_db_id,
        )
        if execution is None:
            raise EvaluationApplicationError(404, "execution_not_found")
        experiment = await self.experiment_repository.get_experiment_by_db_id(
            execution.experiment_db_id,
        )
        if experiment is None:
            raise EvaluationApplicationError(404, "experiment_not_found")
        experiment_context = await self.experiment_context_service.get_experiment_context(
            experiment=experiment,
        )
        if experiment_context.plan_version is None:
            raise EvaluationApplicationError(409, "experiment_plan_not_authored")
        session_plan = SessionPlanView.model_validate(
            experiment_context.plan_version.session_plan or {}
        )
        condition_runs = list(await self.experiment_repository.list_condition_runs(execution.id))
        focal_cases = list(await self.experiment_repository.list_focal_cases(execution.id))
        return PacketRuntimeContext(
            execution=execution,
            experiment_context=experiment_context,
            session_plan=session_plan,
            condition_runs=condition_runs,
            run_by_id={
                run.experiment_condition_run_id: run
                for run in condition_runs
                if run.experiment_condition_run_id
            },
            focal_case_by_id={
                focal_case.experiment_focal_case_id: focal_case
                for focal_case in focal_cases
                if focal_case.experiment_focal_case_id
            },
        )

    async def rater_or_error(
        self,
        *,
        rater_id: str,
    ) -> EvaluationRater:
        rater = await self.rater_reader.get_rater(rater_id=rater_id)
        if rater is None:
            raise EvaluationApplicationError(404, "rater_not_found")
        return rater


async def packet_or_error(
    reader: PacketReader,
    *,
    evaluation_packet_id: str,
) -> EvaluationPacket:
    packet = await reader.get_packet(evaluation_packet_id=evaluation_packet_id)
    if packet is None:
        raise EvaluationApplicationError(404, "evaluation_packet_not_found")
    return packet
