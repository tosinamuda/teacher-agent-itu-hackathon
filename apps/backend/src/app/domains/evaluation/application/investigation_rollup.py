"""Evaluation-results rollup query for one investigation."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.rating_metrics import is_synthetic, mean_score
from app.domains.evaluation.application.result_schemas import InvestigationResultsRollup
from app.domains.evaluation.infrastructure.models import EvaluationPacket, EvaluationRating
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentExecution,
    Investigation,
)
from app.shared.json_types import JsonObject


class InvestigationRollupData(Protocol):
    async def list_all_ratings_for_packets(
        self, *, evaluation_packet_db_ids: list[uuid.UUID]
    ) -> list[EvaluationRating]: ...


class InvestigationRollupExperiments(Protocol):
    async def get_investigation(self, investigation_id: str) -> Investigation | None: ...

    async def list_experiments_for_investigation(
        self, investigation_db_id: uuid.UUID
    ) -> Sequence[Experiment]: ...

    async def list_executions_for_experiments(
        self, experiment_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentExecution]: ...

    async def list_packets_for_executions(
        self, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[EvaluationPacket]: ...


@dataclass(frozen=True)
class InvestigationRollupDependencies:
    ratings: InvestigationRollupData
    experiments: InvestigationRollupExperiments


@dataclass(frozen=True)
class _InvestigationRows:
    experiments: list[Experiment]
    packets: list[EvaluationPacket]
    ratings: list[EvaluationRating]
    experiment_id_by_packet: dict[uuid.UUID, str]


@dataclass(frozen=True)
class _RollupTotals:
    per_experiment: list[JsonObject]
    rated_packet_count: int
    scores: list[float]
    rater_ids: set[object]


async def investigation_results_rollup(
    dependencies: InvestigationRollupDependencies,
    *,
    investigation_id: str,
) -> InvestigationResultsRollup:
    rows = await _load_investigation_rows(dependencies, investigation_id=investigation_id)
    packets_by_experiment, ratings_by_experiment = _group_rows(rows)
    totals = _rollup_totals(
        rows.experiments,
        packets_by_experiment=packets_by_experiment,
        ratings_by_experiment=ratings_by_experiment,
    )
    return InvestigationResultsRollup.model_validate(
        {
            "investigation_id": investigation_id,
            "experiment_count": len(rows.experiments),
            "packet_count": len(rows.packets),
            "rated_packet_count": totals.rated_packet_count,
            "total_ratings": len(totals.scores),
            "distinct_raters": len(totals.rater_ids),
            "mean_overall": mean_score(totals.scores),
            "per_experiment": totals.per_experiment,
        }
    )


async def _load_investigation_rows(
    dependencies: InvestigationRollupDependencies,
    *,
    investigation_id: str,
) -> _InvestigationRows:
    investigation = await dependencies.experiments.get_investigation(investigation_id)
    if investigation is None:
        raise EvaluationApplicationError(404, "investigation_not_found")
    experiments = list(
        await dependencies.experiments.list_experiments_for_investigation(investigation.id)
    )
    executions = await dependencies.experiments.list_executions_for_experiments(
        [experiment.id for experiment in experiments]
    )
    experiment_by_id = {experiment.id: experiment for experiment in experiments}
    experiment_id_by_execution = {
        execution.id: experiment_by_id[execution.experiment_db_id].experiment_id
        for execution in executions
        if execution.experiment_db_id in experiment_by_id
    }
    packets = await dependencies.experiments.list_packets_for_executions(
        execution_db_ids=[execution.id for execution in executions]
    )
    experiment_id_by_packet = {
        packet.id: experiment_id_by_execution[packet.execution_db_id]
        for packet in packets
        if packet.execution_db_id in experiment_id_by_execution
    }
    expert_ratings = [
        rating
        for rating in await dependencies.ratings.list_all_ratings_for_packets(
            evaluation_packet_db_ids=[packet.id for packet in packets]
        )
        if not is_synthetic(rating)
    ]
    return _InvestigationRows(
        experiments=experiments,
        packets=packets,
        ratings=expert_ratings,
        experiment_id_by_packet=experiment_id_by_packet,
    )


def _group_rows(
    rows: _InvestigationRows,
) -> tuple[
    dict[str, list[EvaluationPacket]],
    dict[str, list[EvaluationRating]],
]:
    packets_by_experiment: dict[str, list[EvaluationPacket]] = {
        experiment.experiment_id: [] for experiment in rows.experiments
    }
    ratings_by_experiment: dict[str, list[EvaluationRating]] = {
        experiment.experiment_id: [] for experiment in rows.experiments
    }
    for packet in rows.packets:
        public_id = rows.experiment_id_by_packet.get(packet.id)
        if public_id is not None:
            packets_by_experiment[public_id].append(packet)
    for rating in rows.ratings:
        public_id = rows.experiment_id_by_packet.get(rating.evaluation_packet_db_id)
        if public_id is not None:
            ratings_by_experiment[public_id].append(rating)
    return packets_by_experiment, ratings_by_experiment


def _rollup_totals(
    experiments: list[Experiment],
    *,
    packets_by_experiment: dict[str, list[EvaluationPacket]],
    ratings_by_experiment: dict[str, list[EvaluationRating]],
) -> _RollupTotals:
    per_experiment: list[JsonObject] = []
    all_scores: list[float] = []
    rated_packet_count = 0
    rater_ids: set[object] = set()
    for experiment in experiments:
        public_id = experiment.experiment_id
        experiment_packets = packets_by_experiment[public_id]
        experiment_ratings = ratings_by_experiment[public_id]
        scores = [rating.overall_score for rating in experiment_ratings]
        rated_ids = {rating.evaluation_packet_db_id for rating in experiment_ratings}
        rated_packet_count += len(rated_ids)
        all_scores.extend(scores)
        rater_ids.update(rating.rater_db_id for rating in experiment_ratings)
        per_experiment.append(
            {
                "experiment_id": public_id,
                "packet_count": len(experiment_packets),
                "rated_packet_count": len(rated_ids),
                "total_ratings": len(experiment_ratings),
                "mean_overall": mean_score(scores),
            }
        )

    return _RollupTotals(
        per_experiment=per_experiment,
        rated_packet_count=rated_packet_count,
        scores=all_scores,
        rater_ids=rater_ids,
    )
