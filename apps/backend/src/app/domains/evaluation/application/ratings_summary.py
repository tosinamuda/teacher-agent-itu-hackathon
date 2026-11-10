"""Rating-progress query for one experiment."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.rating_metrics import is_synthetic, mean_score
from app.domains.evaluation.application.result_schemas import ExperimentRatingsSummary
from app.domains.evaluation.infrastructure.models import EvaluationPacket, EvaluationRating
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.shared.experiment_enums import Hypothesis
from app.shared.json_types import JsonObject


class RatingsSummaryData(Protocol):
    async def list_all_ratings_for_packets(
        self, *, evaluation_packet_db_ids: list[uuid.UUID]
    ) -> list[EvaluationRating]: ...


class RatingsSummaryExperiments(Protocol):
    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def list_packets_for_executions(
        self, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[EvaluationPacket]: ...

    async def list_condition_runs_for_executions(
        self, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentConditionRun]: ...


@dataclass(frozen=True)
class RatingsSummaryDependencies:
    ratings: RatingsSummaryData
    experiments: RatingsSummaryExperiments


@dataclass(frozen=True)
class _RatingsSummaryRows:
    executions: list[ExperimentExecution]
    packets: list[EvaluationPacket]
    expert: list[EvaluationRating]
    synthetic: list[EvaluationRating]


async def experiment_ratings_summary(
    dependencies: RatingsSummaryDependencies,
    *,
    experiment_id: str,
) -> ExperimentRatingsSummary:
    """Compute expert rating progress and the labelled synthetic rehearsal block."""
    rows = await _load_summary_rows(dependencies, experiment_id=experiment_id)
    synthetic = await _synthetic_summary(dependencies, rows=rows)
    return ExperimentRatingsSummary.model_validate(
        {
            "experiment_id": experiment_id,
            "packet_count": len(rows.packets),
            "rated_packet_count": len({rating.evaluation_packet_db_id for rating in rows.expert}),
            "total_ratings": len(rows.expert),
            "distinct_raters": len({rating.rater_db_id for rating in rows.expert}),
            "mean_overall": mean_score([rating.overall_score for rating in rows.expert]),
            "by_hypothesis": _ratings_by_hypothesis(rows),
            "synthetic": synthetic,
        }
    )


async def _load_summary_rows(
    dependencies: RatingsSummaryDependencies,
    *,
    experiment_id: str,
) -> _RatingsSummaryRows:
    experiment = await dependencies.experiments.get_experiment(experiment_id)
    if experiment is None:
        raise EvaluationApplicationError(404, "experiment_not_found")
    executions = await dependencies.experiments.list_executions_for_experiment(experiment.id)
    packets = await dependencies.experiments.list_packets_for_executions(
        execution_db_ids=[execution.id for execution in executions]
    )
    all_ratings = await dependencies.ratings.list_all_ratings_for_packets(
        evaluation_packet_db_ids=[packet.id for packet in packets]
    )
    return _RatingsSummaryRows(
        executions=executions,
        packets=packets,
        expert=[rating for rating in all_ratings if not is_synthetic(rating)],
        synthetic=[rating for rating in all_ratings if is_synthetic(rating)],
    )


def _ratings_by_hypothesis(rows: _RatingsSummaryRows) -> dict[str, JsonObject]:
    by_hypothesis: dict[str, JsonObject] = {}
    for hypothesis in (Hypothesis.H1.value, Hypothesis.H2.value):
        scores = [rating.overall_score for rating in rows.expert if rating.hypothesis == hypothesis]
        hypothesis_packets = [packet for packet in rows.packets if packet.hypothesis == hypothesis]
        by_hypothesis[hypothesis] = {
            "packet_count": len(hypothesis_packets),
            "rating_count": len(scores),
            "mean_overall": mean_score(scores),
        }

    return by_hypothesis


async def _synthetic_summary(
    dependencies: RatingsSummaryDependencies,
    *,
    rows: _RatingsSummaryRows,
) -> JsonObject | None:
    if not rows.synthetic:
        return None
    condition_runs = await dependencies.experiments.list_condition_runs_for_executions(
        execution_db_ids=[execution.id for execution in rows.executions]
    )
    run_code = {run.experiment_condition_run_id: run.condition_code for run in condition_runs}
    packet_code = {
        packet.id: run_code.get(packet.primary_condition_run_id) for packet in rows.packets
    }
    by_condition: dict[str, list[float]] = {}
    for rating in rows.synthetic:
        code = packet_code.get(rating.evaluation_packet_db_id)
        if code:
            by_condition.setdefault(code, []).append(rating.overall_score)
    return {
        "rating_count": len(rows.synthetic),
        "rated_packet_count": len({rating.evaluation_packet_db_id for rating in rows.synthetic}),
        "distinct_raters": len({rating.rater_db_id for rating in rows.synthetic}),
        "mean_overall": mean_score([rating.overall_score for rating in rows.synthetic]),
        "by_condition": {code: mean_score(scores) for code, scores in sorted(by_condition.items())},
    }
