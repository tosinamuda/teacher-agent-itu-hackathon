"""Structural contract for the conditioned-execution store roles."""

from __future__ import annotations

from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)


def test_worker_roles_share_adapters_without_exposing_one_mega_role() -> None:
    store = SqlAlchemyExperimentStore(cast(AsyncSession, object()))

    assert store.execution_lifecycle is store.h1_inputs
    assert store.h1_inputs is store.h2_inputs
    assert store.h2_inputs is store.focal_cases
    assert store.focal_cases is store.execution_progress
    assert store.condition_runs is store.condition_recovery
