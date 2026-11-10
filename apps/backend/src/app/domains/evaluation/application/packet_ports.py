"""Read-only role ports for packet queues and packet details."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.domains.evaluation.application.peer_ports import PackArtefactsPort
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
    RaterAssignment,
)
from app.domains.experiments.application.experiment_context_service import ExperimentContext
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)


class PacketExperimentContext(Protocol):
    async def get_experiment_context(self, *, experiment: Experiment) -> ExperimentContext: ...


class PacketQueueData(Protocol):
    async def get_rater(self, *, rater_id: str) -> EvaluationRater | None: ...

    async def list_packets(self, *, hypothesis: str) -> list[EvaluationPacket]: ...

    async def list_ratings_for_packets(
        self, *, evaluation_packet_db_ids: list[uuid.UUID], rater_db_id: uuid.UUID
    ) -> list[EvaluationRating]: ...

    async def list_assignments_for_rater(
        self, *, rater_db_id: uuid.UUID
    ) -> list[RaterAssignment]: ...


class PacketQueueExperiments(Protocol):
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


class H1PacketDetailData(Protocol):
    async def get_rater(self, *, rater_id: str) -> EvaluationRater | None: ...

    async def get_packet(self, *, evaluation_packet_id: str) -> EvaluationPacket | None: ...

    async def get_rating(
        self, *, evaluation_packet_db_id: uuid.UUID, rater_db_id: uuid.UUID
    ) -> EvaluationRating | None: ...

    async def list_packets(self, *, hypothesis: str) -> list[EvaluationPacket]: ...


class H1PacketDetailExperiments(Protocol):
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


class H2PacketDetailData(Protocol):
    async def get_rater(self, *, rater_id: str) -> EvaluationRater | None: ...

    async def get_packet(self, *, evaluation_packet_id: str) -> EvaluationPacket | None: ...

    async def get_rating(
        self, *, evaluation_packet_db_id: uuid.UUID, rater_db_id: uuid.UUID
    ) -> EvaluationRating | None: ...


class H2PacketDetailExperiments(Protocol):
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


@dataclass(frozen=True)
class PacketQueueDependencies:
    data: PacketQueueData
    experiments: PacketQueueExperiments
    context: PacketExperimentContext
    artefacts: PackArtefactsPort


@dataclass(frozen=True)
class H1PacketDetailDependencies:
    data: H1PacketDetailData
    experiments: H1PacketDetailExperiments
    context: PacketExperimentContext
    artefacts: PackArtefactsPort


@dataclass(frozen=True)
class H2PacketDetailDependencies:
    data: H2PacketDetailData
    experiments: H2PacketDetailExperiments
    context: PacketExperimentContext
    artefacts: PackArtefactsPort
