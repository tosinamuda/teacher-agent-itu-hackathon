"""Execution creation stages one attempt; the launch that calls it owns the commit."""

from __future__ import annotations

import uuid
from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.application.create_execution import create_execution
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.domain import ExecutionStatus, Hypothesis
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from tests.launch_collaborators import FakeLaunchStore


class _RecordingSession:
    def __init__(self) -> None:
        self.events: list[tuple[str, object] | str] = []

    def add(self, row: object) -> None:
        self.events.append(("add", row))

    async def flush(self) -> None:
        self.events.append("flush")

    async def refresh(self, row: object) -> None:
        self.events.append(("refresh", row))

    async def commit(self) -> None:
        raise AssertionError("repository must not commit")

    async def rollback(self) -> None:
        raise AssertionError("repository must not roll back")


@pytest.mark.asyncio
async def test_repository_stages_and_flushes_execution_without_transaction_control() -> None:
    session = _RecordingSession()
    repository = ExperimentRepository(cast(AsyncSession, session))
    execution = object()

    result = await repository.stage_execution(execution)  # type: ignore[arg-type]

    assert result is execution
    assert session.events == [("add", execution), "flush", ("refresh", execution)]


@pytest.mark.asyncio
async def test_create_execution_stages_created_attempt_without_ending_transaction() -> None:
    store = FakeLaunchStore()
    experiment_db_id = uuid.uuid4()

    execution = await create_execution(
        store,  # type: ignore[arg-type]
        experiment_db_id=experiment_db_id,
        hypothesis=Hypothesis.H1,
        runtime_snapshot={"trigger": "test"},
    )

    assert store.staged == [execution]
    assert execution.experiment_db_id == experiment_db_id
    assert execution.attempt_number == 1
    assert execution.status is ExecutionStatus.CREATED
    assert store.events == ["stage"]


@pytest.mark.asyncio
async def test_attempt_conflict_rolls_back_through_the_store() -> None:
    store = FakeLaunchStore(conflict=True)

    with pytest.raises(ExperimentApplicationError) as raised:
        await create_execution(
            store,  # type: ignore[arg-type]
            experiment_db_id=uuid.uuid4(),
            hypothesis=Hypothesis.H2,
            runtime_snapshot=None,
        )

    assert raised.value.status_code == 409
    assert raised.value.detail == "generation_already_in_progress"
    assert store.events == ["stage", "rollback"]
