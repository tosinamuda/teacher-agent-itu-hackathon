"""Unit tests for the synthetic evaluation loop orchestrator.

Locks the order teacher-review -> export(every execution) -> rate, the graceful skip
of not-ready executions, and the aggregated result. The three collaborators (teacher,
export service, rater) are faked so the sequencing is deterministic and DB-free.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.evaluation.application import synthetic_loop as sl
from app.domains.evaluation.application.identity_ports import RaterRegistrationStore
from app.domains.experiments.application.packet_export_store import PacketExportStore
from app.domains.experiments.application.service import ExperimentApplicationError

DB = cast(AsyncSession, object())
IDENTITY_STORE = cast(RaterRegistrationStore, object())


class _FakePacketExportStore:
    def __init__(self, calls: list[str]) -> None:
        self._calls = calls

    async def rollback(self) -> None:
        self._calls.append("release_export_snapshot")


class _FakeRepo:
    def __init__(self, executions: list[SimpleNamespace]) -> None:
        self._executions = executions

    async def list_executions_for_experiment(
        self, experiment_db_id: object
    ) -> list[SimpleNamespace]:
        return self._executions


class _FakeService:
    """Stand-in for the experiment identity query used by the loop."""

    async def get_experiment(self, *, experiment_id: str) -> SimpleNamespace:
        return SimpleNamespace(id="exp-db-id")


class _FakePacketExportService:
    """Stand-in for PacketExportApplicationService: records each export and skips not-ready."""

    def __init__(self, calls: list[str]) -> None:
        self._calls = calls

    async def export_packets(self, *, execution_id: str) -> list[object]:
        self._calls.append(f"export:{execution_id}")
        if execution_id == "E-not-ready":
            raise ExperimentApplicationError(409, "execution_packets_not_ready")
        return [object(), object()]


def _patch(
    monkeypatch: pytest.MonkeyPatch,
    *,
    executions: list[str],
) -> tuple[list[str], PacketExportStore]:
    calls: list[str] = []
    exec_objs = [SimpleNamespace(execution_id=eid) for eid in executions]

    async def _review(db: AsyncSession, *, experiment_id: str, max_rounds: int, on_progress=None):  # type: ignore[no-untyped-def]
        calls.append("review")
        return {"approved": 1, "revisions": 0, "pending_reviewed": 1}

    async def _rate(  # type: ignore[no-untyped-def]
        db: AsyncSession,
        *,
        identity_store,
        experiment_id: str,
        personas=None,
        on_progress=None,
    ):
        calls.append("rate")
        return {"created": 2, "packets": 2, "personas": []}

    monkeypatch.setattr(sl, "review_experiment", _review)
    monkeypatch.setattr(sl, "rate_experiment", _rate)
    repository = _FakeRepo(exec_objs)
    monkeypatch.setattr(sl, "ExperimentRepository", lambda _db: repository)
    monkeypatch.setattr(sl, "ExperimentApplicationService", lambda _repo: _FakeService())
    monkeypatch.setattr(
        sl, "PacketExportApplicationService", lambda _repo: _FakePacketExportService(calls)
    )
    return calls, cast(PacketExportStore, _FakePacketExportStore(calls))


@pytest.mark.asyncio
async def test_loop_runs_review_then_export_all_then_rate(monkeypatch: pytest.MonkeyPatch) -> None:
    calls, packet_export_store = _patch(monkeypatch, executions=["E1", "E2"])
    result = await sl.run_synthetic_loop(
        DB,
        identity_store=IDENTITY_STORE,
        packet_export_store=packet_export_store,
        experiment_id="EXP-1",
    )
    assert calls == [
        "review",
        "release_export_snapshot",
        "export:E1",
        "export:E2",
        "rate",
    ]
    assert result["exported_packets"] == 4  # 2 executions × 2 packets
    assert result["skipped_exports"] == 0
    assert result["review"]["approved"] == 1
    assert result["rating"]["created"] == 2


@pytest.mark.asyncio
async def test_loop_skips_not_ready_execution_without_failing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls, packet_export_store = _patch(monkeypatch, executions=["E1", "E-not-ready"])
    result = await sl.run_synthetic_loop(
        DB,
        identity_store=IDENTITY_STORE,
        packet_export_store=packet_export_store,
        experiment_id="EXP-1",
    )
    # The not-ready execution is skipped, not fatal; the loop still reaches rating.
    assert calls == [
        "review",
        "release_export_snapshot",
        "export:E1",
        "export:E-not-ready",
        "rate",
    ]
    assert result["exported_packets"] == 2  # only E1
    assert result["skipped_exports"] == 1
