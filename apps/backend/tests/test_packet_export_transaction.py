"""Transaction contracts for replacing evaluation packet sets."""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any, cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.application.packet_export_service import (
    PacketExportApplicationService,
)
from app.domains.experiments.domain import ConditionCode, Hypothesis
from app.domains.experiments.infrastructure.repository import ExperimentRepository


def _run(code: ConditionCode) -> SimpleNamespace:
    return SimpleNamespace(
        experiment_condition_run_id=f"RUN-{code.value}",
        condition_code=code.value,
    )


class _PacketExports:
    def __init__(self, *, fail_save: bool = False, packets_are_current: bool = False) -> None:
        self.execution = SimpleNamespace(id=uuid.uuid4(), hypothesis=Hypothesis.H1.value)
        self.runs = [
            _run(code)
            for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3)
        ]
        primary_runs = (
            [run.experiment_condition_run_id for run in self.runs]
            if packets_are_current
            else ["RUN-STALE"]
        )
        self.persisted_packets: list[Any] = [
            SimpleNamespace(id=uuid.uuid4(), primary_condition_run_id=run_id, created_at=index)
            for index, run_id in enumerate(primary_runs)
        ]
        self.persisted_ratings = ["synthetic-rating"]
        self.pending_delete = False
        self.pending_packets: list[Any] = []
        self.fail_save = fail_save
        self.calls: list[str] = []

    async def lock_execution_by_public_id(self, execution_id: str) -> None:
        self.calls.append(f"lock:{execution_id}")

    async def get_execution(self, execution_id: str) -> Any:
        self.calls.append(f"execution:{execution_id}")
        return self.execution

    async def list_packets(self, execution_db_id: uuid.UUID) -> list[Any]:
        self.calls.append("list_packets")
        return list(self.persisted_packets)

    async def list_condition_runs(self, execution_db_id: uuid.UUID) -> list[Any]:
        self.calls.append("list_runs")
        return self.runs

    async def current_artefacts_by_condition_run(
        self, run_ids: list[str]
    ) -> dict[str, SimpleNamespace]:
        self.calls.append("resolve_artefacts")
        return {run_id: SimpleNamespace(artefact_id=f"ART-{run_id}") for run_id in run_ids}

    async def count_real_ratings_for_packets(self, *, packet_ids: list[uuid.UUID]) -> int:
        self.calls.append("count_real_ratings")
        return 0

    async def delete_packets(self, *, packet_ids: list[uuid.UUID]) -> None:
        self.calls.append("stage_delete")
        self.pending_delete = True

    async def save_packets(self, *, packets: list[Any]) -> list[Any]:
        self.calls.append("stage_packets")
        if self.fail_save:
            raise RuntimeError("packet insert failed")
        self.pending_packets = packets
        return packets


class _RecordingSession:
    def __init__(self) -> None:
        self.added: list[Any] = []
        self.flushes = 0
        self.refreshed: list[Any] = []
        self.commits = 0

    def add_all(self, values: list[Any]) -> None:
        self.added.extend(values)

    async def flush(self) -> None:
        self.flushes += 1

    async def refresh(self, value: Any) -> None:
        self.refreshed.append(value)

    async def commit(self) -> None:
        self.commits += 1


class _PacketExportStore:
    def __init__(self, packet_exports: _PacketExports) -> None:
        self.packet_exports = packet_exports
        self.commits = 0
        self.rollbacks = 0

    async def commit(self) -> None:
        self.commits += 1
        self.packet_exports.calls.append("commit")
        if self.packet_exports.pending_delete:
            self.packet_exports.persisted_packets = []
            self.packet_exports.persisted_ratings = []
        self.packet_exports.persisted_packets.extend(self.packet_exports.pending_packets)
        self.packet_exports.pending_delete = False
        self.packet_exports.pending_packets = []

    async def rollback(self) -> None:
        self.rollbacks += 1
        self.packet_exports.calls.append("rollback")
        self.packet_exports.pending_delete = False
        self.packet_exports.pending_packets = []


@pytest.mark.asyncio
async def test_save_packets_stages_and_flushes_without_committing() -> None:
    session = _RecordingSession()
    repository = ExperimentRepository(cast(AsyncSession, session))
    packets = cast(list[Any], [object(), object()])

    result = await repository.save_packets(packets=packets)

    assert result == packets
    assert session.added == packets
    assert session.flushes == 1
    assert session.refreshed == packets
    assert session.commits == 0


@pytest.mark.asyncio
async def test_packet_replacement_commits_once_after_delete_and_insert_are_staged() -> None:
    packet_exports = _PacketExports()
    store = _PacketExportStore(packet_exports)

    packets = await PacketExportApplicationService(store).export_packets(execution_id="EXE-1")

    assert len(packets) == 4
    assert store.commits == 1
    assert store.rollbacks == 0
    assert packet_exports.calls[-3:] == ["stage_delete", "stage_packets", "commit"]
    assert packet_exports.persisted_packets == packets
    assert packet_exports.persisted_ratings == []


@pytest.mark.asyncio
async def test_failed_packet_replacement_rolls_back_delete_and_preserves_ratings() -> None:
    packet_exports = _PacketExports(fail_save=True)
    original_packets = list(packet_exports.persisted_packets)
    original_ratings = list(packet_exports.persisted_ratings)
    store = _PacketExportStore(packet_exports)

    with pytest.raises(RuntimeError, match="packet insert failed"):
        await PacketExportApplicationService(store).export_packets(execution_id="EXE-1")

    assert store.commits == 0
    assert store.rollbacks == 1
    assert packet_exports.persisted_packets == original_packets
    assert packet_exports.persisted_ratings == original_ratings
    assert packet_exports.calls[-3:] == ["stage_delete", "stage_packets", "rollback"]


@pytest.mark.asyncio
async def test_current_packet_set_commits_once_to_release_the_execution_lock() -> None:
    packet_exports = _PacketExports(packets_are_current=True)
    store = _PacketExportStore(packet_exports)

    packets = await PacketExportApplicationService(store).export_packets(execution_id="EXE-1")

    assert packets == packet_exports.persisted_packets
    assert store.commits == 1
    assert store.rollbacks == 0
    assert "stage_delete" not in packet_exports.calls
    assert "stage_packets" not in packet_exports.calls
    assert packet_exports.calls[-1] == "commit"
