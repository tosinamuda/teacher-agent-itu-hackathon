"""H1/H2 and source-audit statistics query for one experiment."""

from __future__ import annotations

import uuid
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.domains.evaluation.application.constants import _SOURCE_AUDIT_CRITERION_IDS
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.rating_metrics import is_synthetic, mean_score
from app.domains.evaluation.application.reporting_queries import (
    _build_h1,
    _build_h2,
    _inter_rater,
    _underpowered_notes,
)
from app.domains.evaluation.application.result_schemas import (
    ExperimentStatistics,
    SourceAuditDescriptives,
)
from app.domains.evaluation.infrastructure.models import (
    EvaluationAuditItem,
    EvaluationAuditRating,
    EvaluationPacket,
    EvaluationRating,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.domains.experiments.review_pack_study.conditions.profiles import (
    condition_codes,
    h1_main_condition_codes,
)
from app.shared.experiment_enums import Hypothesis


class ExperimentStatisticsData(Protocol):
    async def list_all_ratings_for_packets(
        self, *, evaluation_packet_db_ids: list[uuid.UUID]
    ) -> list[EvaluationRating]: ...

    async def list_audit_items_for_executions(
        self, *, execution_db_ids: list[uuid.UUID]
    ) -> list[EvaluationAuditItem]: ...

    async def list_audit_ratings_for_items(
        self, *, audit_item_db_ids: list[uuid.UUID]
    ) -> list[EvaluationAuditRating]: ...


class ExperimentStatisticsReader(Protocol):
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
class ExperimentStatisticsDependencies:
    data: ExperimentStatisticsData
    experiments: ExperimentStatisticsReader


async def experiment_statistics(
    dependencies: ExperimentStatisticsDependencies,
    experiment_id: str,
) -> ExperimentStatistics:
    experiment = await dependencies.experiments.get_experiment(experiment_id)
    if experiment is None:
        raise EvaluationApplicationError(404, "experiment_not_found")
    executions = await dependencies.experiments.list_executions_for_experiment(experiment.id)
    execution_ids = [execution.id for execution in executions]
    packets = await dependencies.experiments.list_packets_for_executions(
        execution_db_ids=execution_ids
    )
    condition_runs = await dependencies.experiments.list_condition_runs_for_executions(
        execution_db_ids=execution_ids
    )
    run_code = {run.experiment_condition_run_id: run.condition_code for run in condition_runs}
    all_ratings = await dependencies.data.list_all_ratings_for_packets(
        evaluation_packet_db_ids=[packet.id for packet in packets]
    )
    expert_ratings = [rating for rating in all_ratings if not is_synthetic(rating)]
    synthetic_basis = not expert_ratings and any(is_synthetic(rating) for rating in all_ratings)
    ratings = expert_ratings or [rating for rating in all_ratings if is_synthetic(rating)]
    packet_code = {packet.id: run_code.get(packet.primary_condition_run_id) for packet in packets}
    packet_focal = {packet.id: packet.experiment_focal_case_id for packet in packets}
    condition_scores: dict[str, list[float]] = defaultdict(list)
    for rating in ratings:
        code = packet_code.get(rating.evaluation_packet_db_id)
        if code:
            condition_scores[code].append(float(rating.overall_score))

    h1_codes = [code.value for code in h1_main_condition_codes()]
    h2_codes = [code.value for code in condition_codes(Hypothesis.H2)]
    h1, h1_count = _build_h1(ratings, condition_scores, packet_code, h1_codes)
    h2, h2_count = _build_h2(ratings, condition_scores, packet_code, packet_focal, h2_codes)
    inter_rater = _inter_rater(ratings)
    source_audit = await _source_audit_descriptives(dependencies.data, execution_ids=execution_ids)
    return ExperimentStatistics.model_validate(
        {
            "experiment_id": experiment_id,
            "synthetic": synthetic_basis,
            "h1": h1,
            "h2": h2,
            "source_audit": source_audit,
            "inter_rater": inter_rater,
            "notes": _underpowered_notes(synthetic_basis, h1_count, h2_count, inter_rater),
        }
    )


async def _source_audit_descriptives(
    data: ExperimentStatisticsData,
    *,
    execution_ids: list[uuid.UUID],
) -> SourceAuditDescriptives:
    items = await data.list_audit_items_for_executions(execution_db_ids=execution_ids)
    ratings = await data.list_audit_ratings_for_items(audit_item_db_ids=[item.id for item in items])
    criteria = {
        criterion_id: {"fail": 0, "partial": 0, "pass": 0}  # nosec B105
        for criterion_id in _SOURCE_AUDIT_CRITERION_IDS
    }
    bucket = {0: "fail", 1: "partial", 2: "pass"}
    scores: list[float] = []
    for rating in ratings:
        scores.append(float(rating.source_grounding_score))
        for criterion_id in _SOURCE_AUDIT_CRITERION_IDS:
            value = int(getattr(rating, criterion_id))
            if value in bucket:
                criteria[criterion_id][bucket[value]] += 1
    return SourceAuditDescriptives.model_validate(
        {
            "n_items": len(items),
            "n_ratings": len(ratings),
            "mean_score": mean_score(scores),
            "criteria": criteria,
        }
    )
