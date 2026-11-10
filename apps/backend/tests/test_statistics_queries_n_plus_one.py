"""Regression guard: statistics queries must not fan out over executions.

The previous shape (per-execution ``list_packets`` + per-execution
``list_condition_runs``) was textbook N+1 — query count grew linearly with
``len(executions)`` even though the result set was the same. The fix lifts
those into batched ``list_packets_for_executions`` /
``list_condition_runs_for_executions`` repository methods. This test pins
the new contract: both repository methods are called exactly ONCE
regardless of execution count.

The assertion uses a fake repository that records per-method call counts;
it doesn't need a live DB. The point is the SHAPE of the calls, not the
SQL — anyone refactoring back to a per-execution loop in the future
fails this test loudly.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any, cast

import pytest

from app.domains.evaluation.application.experiment_statistics import (
    ExperimentStatisticsData,
    ExperimentStatisticsDependencies,
    ExperimentStatisticsReader,
    experiment_statistics,
)
from app.domains.evaluation.application.investigation_rollup import (
    InvestigationRollupData,
    InvestigationRollupDependencies,
    InvestigationRollupExperiments,
    investigation_results_rollup,
)
from app.domains.evaluation.application.ratings_summary import (
    RatingsSummaryData,
    RatingsSummaryDependencies,
    RatingsSummaryExperiments,
    experiment_ratings_summary,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)


@dataclass
class _FakeExperimentRepository:
    """Records method-call counts; returns minimal fixtures.

    Only the caller-owned methods used by the query are implemented, so adding
    a dependency surfaces here rather than silently reaching a mega-port.
    """

    experiment: Experiment
    executions: list[ExperimentExecution]
    condition_runs_by_execution: dict[uuid.UUID, list[ExperimentConditionRun]]
    calls: dict[str, int] = field(default_factory=dict)

    def _tick(self, name: str) -> None:
        self.calls[name] = self.calls.get(name, 0) + 1

    async def get_experiment(self, experiment_id: str) -> Experiment | None:
        self._tick("get_experiment")
        return self.experiment if experiment_id == self.experiment.experiment_id else None

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]:
        self._tick("list_executions_for_experiment")
        return list(self.executions)

    async def list_packets_for_executions(
        self, *, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[Any]:
        self._tick("list_packets_for_executions")
        return []

    async def list_condition_runs_for_executions(
        self, *, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentConditionRun]:
        self._tick("list_condition_runs_for_executions")
        return [
            run
            for execution_db_id in execution_db_ids
            for run in self.condition_runs_by_execution.get(execution_db_id, [])
        ]

    async def list_packets(self, execution_db_id: uuid.UUID) -> list[Any]:
        # ANY call to this is a regression — the N+1 we just retired.
        self._tick("list_packets__NPLUSONE_REGRESSION")
        return []

    async def list_condition_runs(self, execution_db_id: uuid.UUID) -> list[ExperimentConditionRun]:
        # Same — any call here is the per-execution N+1 we retired.
        self._tick("list_condition_runs__NPLUSONE_REGRESSION")
        return []


class _FakeEvaluationRepository:
    """Minimal: ``_experiment_packets_and_ratings`` only calls ``list_all_ratings_for_packets``."""

    def __init__(self) -> None:
        self.calls: dict[str, int] = {}

    async def list_all_ratings_for_packets(
        self, *, evaluation_packet_db_ids: Sequence[uuid.UUID]
    ) -> list[Any]:
        self.calls["list_all_ratings_for_packets"] = (
            self.calls.get("list_all_ratings_for_packets", 0) + 1
        )
        return []

    async def list_audit_items_for_executions(
        self, *, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[Any]:
        self.calls["list_audit_items_for_executions"] = (
            self.calls.get("list_audit_items_for_executions", 0) + 1
        )
        return []

    async def list_audit_ratings_for_items(
        self, *, audit_item_db_ids: Sequence[uuid.UUID]
    ) -> list[Any]:
        self.calls["list_audit_ratings_for_items"] = (
            self.calls.get("list_audit_ratings_for_items", 0) + 1
        )
        return []


def _make_repos(n_executions: int) -> tuple[_FakeExperimentRepository, _FakeEvaluationRepository]:
    experiment_id = "EXP-test"
    experiment = Experiment(
        id=uuid.uuid4(),
        experiment_id=experiment_id,
        experiment_code="EXP-TEST-001",
        teacher_workspace_id=uuid.uuid4(),
        plan_version_id="LPV-test",
        focal_learner_ids=[],
    )
    executions = [
        ExperimentExecution(
            id=uuid.uuid4(),
            execution_id=f"EXE-{index}",
            experiment_db_id=experiment.id,
            hypothesis="H1",
            attempt_number=1,
        )
        for index in range(n_executions)
    ]
    return (
        _FakeExperimentRepository(
            experiment=experiment,
            executions=executions,
            condition_runs_by_execution={},
        ),
        _FakeEvaluationRepository(),
    )


@pytest.mark.parametrize("n_executions", [1, 5, 20])
@pytest.mark.asyncio
async def test_experiment_ratings_summary_is_constant_queries(n_executions: int) -> None:
    """Repository call count must NOT grow with execution count.

    Calls per run:
    - ``get_experiment``               × 1
    - ``list_executions_for_experiment`` × 1
    - ``list_packets_for_executions``  × 1  (batched — was N before)
    - ``list_condition_runs_for_executions`` × 0 (no synthetic ratings → branch
      that triggers ``_packet_condition_codes`` doesn't fire here)
    - ``list_all_ratings_for_packets`` × 1
    """
    experiment_repo, evaluation_repo = _make_repos(n_executions)
    dependencies = RatingsSummaryDependencies(
        ratings=cast(RatingsSummaryData, evaluation_repo),
        experiments=cast(RatingsSummaryExperiments, experiment_repo),
    )
    await experiment_ratings_summary(dependencies, experiment_id="EXP-test")

    # Per-execution methods MUST NOT have been called.
    assert experiment_repo.calls.get("list_packets__NPLUSONE_REGRESSION", 0) == 0, (
        "list_packets() called per-execution — the N+1 returned. "
        f"call counts: {experiment_repo.calls}"
    )
    assert experiment_repo.calls.get("list_condition_runs__NPLUSONE_REGRESSION", 0) == 0, (
        "list_condition_runs() called per-execution — the N+1 returned. "
        f"call counts: {experiment_repo.calls}"
    )
    # Batched method called exactly once.
    assert experiment_repo.calls.get("list_packets_for_executions") == 1
    # Outer wrapper queries called exactly once each.
    assert experiment_repo.calls.get("get_experiment") == 1
    assert experiment_repo.calls.get("list_executions_for_experiment") == 1
    assert evaluation_repo.calls.get("list_all_ratings_for_packets") == 1


@pytest.mark.parametrize("n_executions", [1, 5, 20])
@pytest.mark.asyncio
async def test_experiment_statistics_is_constant_queries(n_executions: int) -> None:
    experiment_repo, evaluation_repo = _make_repos(n_executions)
    dependencies = ExperimentStatisticsDependencies(
        data=cast(ExperimentStatisticsData, evaluation_repo),
        experiments=cast(ExperimentStatisticsReader, experiment_repo),
    )

    await experiment_statistics(dependencies, "EXP-test")

    assert experiment_repo.calls == {
        "get_experiment": 1,
        "list_executions_for_experiment": 1,
        "list_packets_for_executions": 1,
        "list_condition_runs_for_executions": 1,
    }
    assert evaluation_repo.calls == {
        "list_all_ratings_for_packets": 1,
        "list_audit_items_for_executions": 1,
        "list_audit_ratings_for_items": 1,
    }


class _FakeInvestigationExperiments:
    def __init__(self, n_experiments: int) -> None:
        self.investigation = SimpleNamespace(id=uuid.uuid4(), investigation_id="INV-test")
        self.experiments = [
            SimpleNamespace(id=uuid.uuid4(), experiment_id=f"EXP-{index}")
            for index in range(n_experiments)
        ]
        self.executions = [
            SimpleNamespace(
                id=uuid.uuid4(),
                experiment_db_id=experiment.id,
            )
            for experiment in self.experiments
        ]
        self.calls: dict[str, int] = {}

    def _tick(self, name: str) -> None:
        self.calls[name] = self.calls.get(name, 0) + 1

    async def get_investigation(self, investigation_id: str) -> Any:
        self._tick("get_investigation")
        return self.investigation

    async def list_experiments_for_investigation(self, investigation_db_id: uuid.UUID) -> list[Any]:
        self._tick("list_experiments_for_investigation")
        return self.experiments

    async def list_executions_for_experiments(
        self, experiment_db_ids: Sequence[uuid.UUID]
    ) -> list[Any]:
        self._tick("list_executions_for_experiments")
        return self.executions

    async def list_packets_for_executions(
        self, *, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[Any]:
        self._tick("list_packets_for_executions")
        return []


@pytest.mark.parametrize("n_experiments", [1, 5, 20])
@pytest.mark.asyncio
async def test_investigation_rollup_is_constant_queries(n_experiments: int) -> None:
    experiment_data = _FakeInvestigationExperiments(n_experiments)
    evaluation_data = _FakeEvaluationRepository()
    dependencies = InvestigationRollupDependencies(
        ratings=cast(InvestigationRollupData, evaluation_data),
        experiments=cast(InvestigationRollupExperiments, experiment_data),
    )

    await investigation_results_rollup(dependencies, investigation_id="INV-test")

    assert experiment_data.calls == {
        "get_investigation": 1,
        "list_experiments_for_investigation": 1,
        "list_executions_for_experiments": 1,
        "list_packets_for_executions": 1,
    }
    assert evaluation_data.calls == {"list_all_ratings_for_packets": 1}
