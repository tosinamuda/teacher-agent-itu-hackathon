"""Regression guard: ``list_experiment_views`` must NOT
fan out per experiment.

Before this fix the LIST path called ``build_experiment_view`` once per
experiment, which itself made ~10 queries per experiment (context lookups,
executions, focal-learner candidates, C4 approval). For 11 experiments
that was ~110 round-trips.

After the fix the LIST path uses ``experiment_list_loader.load_experiment_list``
to batch every lookup into ``IN(...)`` queries, then assembles each
``ExperimentResponse`` in-memory. This test pins the new shape: the per-
experiment lookups MUST NOT be called, and the batched lookups MUST be
called exactly once each, regardless of N.

The fake repository implements both old per-experiment methods (renamed
with ``__NPLUSONE_REGRESSION`` so a regression fails loudly) and the new
batched ones. The test runs with N ∈ {1, 5, 20} experiments.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, cast

import pytest

from app.domains.experiments.api.schemas import ExperimentResponse
from app.domains.experiments.application.experiment_list_loader import ExperimentListReader
from app.domains.experiments.application.experiment_views import list_experiment_views
from app.domains.experiments.application.experiment_views.experiment import (
    ExperimentEvaluationModeReader,
)
from app.domains.experiments.application.filters import ExperimentListFilters
from app.domains.experiments.application.lesson_notes import LessonNotesReader
from app.domains.experiments.application.service import ExperimentApplicationQueries
from app.domains.experiments.domain import Hypothesis
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentExecution,
)


@dataclass
class _FakeRepo:
    """Records per-method call counts and returns minimal fixtures.

    Implements every method ``list_experiment_views`` (via the loader)
    touches, plus the OLD per-experiment methods so any regression is
    visible as a ``..._NPLUSONE_REGRESSION`` counter.
    """

    experiments: list[Experiment]
    calls: dict[str, int] = field(default_factory=dict)

    def _tick(self, name: str) -> None:
        self.calls[name] = self.calls.get(name, 0) + 1

    # ----- Filter-driven list -----
    async def list_experiments(self, *, filters: Any) -> list[Experiment]:
        self._tick("list_experiments")
        return list(self.experiments)

    async def evaluation_modes_for_experiments(
        self, experiment_db_ids: Sequence[uuid.UUID]
    ) -> dict[uuid.UUID, str]:
        self._tick("evaluation_modes_for_experiments")
        return {}

    # ----- Batched lookups the new prefetch uses (each called exactly once) -----
    async def list_workspaces_by_ids(self, workspace_ids: Sequence[uuid.UUID]) -> list[Any]:
        self._tick("list_workspaces_by_ids")
        return []

    async def list_plan_version_plans_by_ids(self, plan_version_ids: Sequence[str]) -> list[Any]:
        self._tick("list_plan_version_plans_by_ids")
        return []

    async def list_lesson_periods_by_ids(self, lesson_period_ids: Sequence[uuid.UUID]) -> list[Any]:
        self._tick("list_lesson_periods_by_ids")
        return []

    async def count_learners_per_class(
        self, *, class_ids: Sequence[uuid.UUID]
    ) -> dict[uuid.UUID, int]:
        self._tick("count_learners_per_class")
        return {}

    async def count_diagnostics_per_class_plan(
        self, *, pairs: Sequence[tuple[uuid.UUID, str]]
    ) -> dict[tuple[uuid.UUID, str], int]:
        self._tick("count_diagnostics_per_class_plan")
        return {}

    async def list_executions_for_experiments(
        self, *, experiment_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentExecution]:
        self._tick("list_executions_for_experiments")
        return []

    async def list_condition_runs_for_executions(
        self, *, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[Any]:
        self._tick("list_condition_runs_for_executions")
        return []

    async def current_artefacts_by_condition_run(self, run_ids: Sequence[str]) -> dict[str, Any]:
        # Bulk resolver (one query for the whole set) — constant, not per-run.
        self._tick("current_artefacts_by_condition_run")
        return {}

    async def latest_lesson_notes(self, plan_version_ids: Sequence[str]) -> dict[str, Any]:
        self._tick("latest_lesson_notes")
        return {}

    # ----- Old per-experiment methods — ANY call here is a regression -----
    async def get_workspace(self, workspace_id: uuid.UUID) -> Any:
        self._tick("get_workspace__NPLUSONE_REGRESSION")
        return None

    async def get_plan_version_plan(self, *, plan_version_id: str) -> tuple[Any, Any] | None:
        self._tick("get_plan_version_plan__NPLUSONE_REGRESSION")
        return None

    async def get_lesson_period(self, lesson_period_id: uuid.UUID) -> Any:
        self._tick("get_lesson_period__NPLUSONE_REGRESSION")
        return None

    async def count_learners_for_class(self, *, class_id: uuid.UUID) -> int:
        self._tick("count_learners_for_class__NPLUSONE_REGRESSION")
        return 0

    async def count_diagnostics_for_class_plan(
        self, *, class_id: uuid.UUID, plan_version_id: str
    ) -> int:
        self._tick("count_diagnostics_for_class_plan__NPLUSONE_REGRESSION")
        return 0

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]:
        self._tick("list_executions_for_experiment__NPLUSONE_REGRESSION")
        return []

    async def list_condition_runs(self, execution_db_id: uuid.UUID) -> list[Any]:
        self._tick("list_condition_runs__NPLUSONE_REGRESSION")
        return []

    async def list_all_learners_for_class(self, *, class_id: uuid.UUID) -> list[Any]:
        # Called per-class with focal selections only — fine when zero experiments
        # have focal learners (which is the default in this test). If we add a
        # parametrise variant with focal learners, this becomes a per-class call.
        self._tick("list_all_learners_for_class")
        return []

    async def latest_diagnostic_per_student(
        self, *, student_ids: Sequence[str], plan_version_id: str
    ) -> dict[str, Any]:
        self._tick("latest_diagnostic_per_student")
        return {}


@pytest.mark.parametrize("n_experiments", [1, 5, 20])
@pytest.mark.asyncio
async def test_list_experiment_views_is_constant_queries(n_experiments: int) -> None:
    """Query count must NOT grow with experiment count."""
    experiments = [
        Experiment(
            id=uuid.uuid4(),
            experiment_id=f"EXP-{i}",
            experiment_code=f"EXP-TEST-{i:03d}",
            teacher_workspace_id=uuid.uuid4(),
            plan_version_id=f"LPV-test-{i}",
            focal_learner_ids=[],
        )
        for i in range(n_experiments)
    ]
    repo = _FakeRepo(experiments=experiments)
    responses = await list_experiment_views(
        cast(ExperimentApplicationQueries, repo),
        cast(ExperimentListReader, repo),
        cast(ExperimentEvaluationModeReader, repo),
        cast(LessonNotesReader, repo),
        filters=ExperimentListFilters(limit=200),
    )

    # No experiments will fully assemble (fake repo returns empty for every
    # lookup so each experiment's workspace/plan-version is missing →
    # experiment_list_assembly.loaded_experiment returns None → response is
    # dropped). What matters for THIS test is the call SHAPE.
    assert isinstance(responses, list)
    for response in responses:
        assert isinstance(response, ExperimentResponse)

    # Per-experiment methods MUST NOT have been called.
    regressed = {k: v for k, v in repo.calls.items() if "__NPLUSONE_REGRESSION" in k}
    assert not regressed, (
        f"Per-experiment methods were called — N+1 regression. counts: {repo.calls}"
    )

    # Batched methods are called exactly the expected number of times,
    # regardless of N.
    assert repo.calls.get("list_experiments") == 1
    assert repo.calls.get("evaluation_modes_for_experiments") == 1
    assert repo.calls.get("list_workspaces_by_ids") == 1
    assert repo.calls.get("list_plan_version_plans_by_ids") == 1
    assert repo.calls.get("count_learners_per_class") == 1
    assert repo.calls.get("count_diagnostics_per_class_plan") == 1
    assert repo.calls.get("list_executions_for_experiments") == 1
    assert repo.calls.get("list_condition_runs_for_executions") == 1
    assert repo.calls.get("latest_lesson_notes") == 1
    # list_lesson_periods_by_ids is also called exactly once (with an empty
    # list when no plan_version_plans returned, but still issued once).
    assert repo.calls.get("list_lesson_periods_by_ids") == 1

    # NO experiment had focal learners in this test → focal-learner state
    # load is a no-op (zero calls to list_all_learners_for_class and
    # latest_diagnostic_per_student).
    assert repo.calls.get("list_all_learners_for_class", 0) == 0
    assert repo.calls.get("latest_diagnostic_per_student", 0) == 0


@pytest.mark.parametrize("n_experiments_with_focals", [1, 5])
@pytest.mark.asyncio
async def test_list_experiment_views_focal_learner_calls_bounded(
    n_experiments_with_focals: int,
) -> None:
    """Focal-learner lookups are bounded by distinct (class, plan_version) pairs.

    With ``n`` experiments all sharing one plan_version and one class,
    ``list_all_learners_for_class`` is called exactly once (one class) and
    ``latest_diagnostic_per_student`` is called exactly once (one
    plan_version).
    """
    shared_workspace_id = uuid.uuid4()
    shared_plan_version = "LPV-test"
    experiments = [
        Experiment(
            id=uuid.uuid4(),
            experiment_id=f"EXP-{i}",
            experiment_code=f"EXP-TEST-{i:03d}",
            teacher_workspace_id=shared_workspace_id,
            plan_version_id=shared_plan_version,
            focal_learner_ids=[f"S-{i}-{j}" for j in range(2)],
        )
        for i in range(n_experiments_with_focals)
    ]
    repo = _FakeRepo(experiments=experiments)

    # Fake repo returns empty workspaces by default. To trigger the focal
    # path, we need a workspace with a term_class_subject. Patch the
    # workspaces_by_ids return to include one.
    @dataclass
    class _FakeTCS:
        class_id: uuid.UUID = field(default_factory=uuid.uuid4)

    @dataclass
    class _FakeWorkspace:
        id: uuid.UUID
        term_class_subject: Any

    shared_tcs = _FakeTCS()
    fake_workspace = _FakeWorkspace(id=shared_workspace_id, term_class_subject=shared_tcs)

    async def _workspaces_with_one(workspace_ids: Sequence[uuid.UUID]) -> list[Any]:
        repo.calls["list_workspaces_by_ids"] = repo.calls.get("list_workspaces_by_ids", 0) + 1
        return [fake_workspace]

    repo.list_workspaces_by_ids = _workspaces_with_one  # type: ignore[method-assign]
    await list_experiment_views(
        cast(ExperimentApplicationQueries, repo),
        cast(ExperimentListReader, repo),
        cast(ExperimentEvaluationModeReader, repo),
        cast(LessonNotesReader, repo),
        filters=ExperimentListFilters(limit=200),
    )

    # ONE class, ONE plan_version, regardless of n_experiments_with_focals → 1 call each.
    assert repo.calls.get("list_all_learners_for_class") == 1
    assert repo.calls.get("latest_diagnostic_per_student") == 1

    # NO regression
    regressed = {k: v for k, v in repo.calls.items() if "__NPLUSONE_REGRESSION" in k}
    assert not regressed, (
        f"Per-experiment methods were called — N+1 regression. counts: {repo.calls}"
    )


# Silence unused-import warning in test file (Hypothesis is documentation that we know about it).
_ = Hypothesis
