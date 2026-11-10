"""Unit tests for the H1 packet export (experiments service).

June-5 settled design: a teacher-validation-gated condition (C4) is **separate
teacher-governance evidence, not an H1 rater packet**. These prove — without a DB
— that `_export_h1_packets` ships exactly the main comparison conditions (C0-C3)
and never C4, regardless of C4's approval state, and that `_packets_match_execution`
treats the C0-C3 set as the complete current set (so C4 approval never triggers a
re-export). `C4` remains generated/gated; it just does not enter the rater queue.

A run's pack is no longer a stored id on the run — it's resolved via the
back-pointer and passed into these methods as a ``pack_ids`` map (run id ->
current artefact id). "Generated" therefore means "present in ``pack_ids``".
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import cast

import pytest

from app.domains.experiments.application.packet_export_service import (
    PacketExportApplicationService,
    _h1_condition_is_teacher_gated,
)
from app.domains.experiments.application.packet_export_store import PacketExportStore
from app.domains.experiments.domain.types import Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import condition_codes

H1_CODES = [code.value for code in condition_codes(Hypothesis.H1)]


class FakeRepo:
    """Minimal repository: just a packet sink (resolution is passed in)."""

    def __init__(self) -> None:
        self.saved_packets: list[object] | None = None

    async def save_packets(self, *, packets: list[object]) -> list[object]:
        self.saved_packets = packets
        return packets


class FakeStore:
    def __init__(self, packet_exports: FakeRepo) -> None:
        self.packet_exports = packet_exports

    async def commit(self) -> None:
        return None

    async def rollback(self) -> None:
        return None


def _run(code: str) -> SimpleNamespace:
    return SimpleNamespace(experiment_condition_run_id=f"run:{code}", condition_code=code)


ALL_RUNS = [_run(code) for code in H1_CODES]


def _pack_ids(generated: set[str]) -> dict[str, str]:
    """Map each generated condition's run id to its current pack artefact id."""
    return {f"run:{code}": f"art:{code}" for code in generated}


def _service() -> tuple[PacketExportApplicationService, FakeRepo]:
    repo = FakeRepo()
    service = PacketExportApplicationService(cast(PacketExportStore, FakeStore(repo)))
    return service, repo


def test_c4_is_the_only_teacher_gated_h1_condition() -> None:
    assert _h1_condition_is_teacher_gated("C4") is True
    for code in ("C0", "C1", "C2", "C3"):
        assert _h1_condition_is_teacher_gated(code) is False


@pytest.mark.asyncio
async def test_export_excludes_unapproved_c4_and_ships_c0_to_c3() -> None:
    service, repo = _service()
    execution = SimpleNamespace(id=uuid.uuid4(), hypothesis="H1")
    packets = await service._export_h1_packets(
        execution=cast("object", execution),
        condition_runs=ALL_RUNS,
        pack_ids=_pack_ids({"C0", "C1", "C2", "C3", "C4"}),
    )
    exported_codes = {packet.export_refs["condition_code"] for packet in packets}
    assert exported_codes == {"C0", "C1", "C2", "C3"}  # C4 is governance, not a packet
    assert repo.saved_packets is not None and len(repo.saved_packets) == 4


@pytest.mark.asyncio
async def test_export_excludes_c4_even_when_approved() -> None:
    # C4 is teacher-governance evidence, never an H1 rater packet — even approved.
    service, _ = _service()
    execution = SimpleNamespace(id=uuid.uuid4(), hypothesis="H1")
    packets = await service._export_h1_packets(
        execution=cast("object", execution),
        condition_runs=ALL_RUNS,
        pack_ids=_pack_ids({"C0", "C1", "C2", "C3", "C4"}),
    )
    exported_codes = {packet.export_refs["condition_code"] for packet in packets}
    assert exported_codes == {"C0", "C1", "C2", "C3"}


def test_packets_match_treats_deferred_c4_as_complete() -> None:
    # With C4 deferred, a 4-packet (C0-C3) export is the *current* complete set:
    # the idempotency check must return True so export is not re-run forever.
    service, _ = _service()
    execution = SimpleNamespace(hypothesis="H1")
    packets = [
        SimpleNamespace(primary_condition_run_id=f"run:{code}") for code in ("C0", "C1", "C2", "C3")
    ]
    assert (
        service._packets_match_execution(
            execution=cast("object", execution),
            condition_runs=ALL_RUNS,
            packets=packets,
            pack_ids=_pack_ids({"C0", "C1", "C2", "C3", "C4"}),
        )
        is True
    )


def test_packets_match_true_regardless_of_c4_approval() -> None:
    # C4 is never an H1 packet, so its approval does not make the C0-C3 set stale:
    # the idempotency check stays True (no spurious re-export when C4 is approved).
    service, _ = _service()
    execution = SimpleNamespace(hypothesis="H1")
    packets = [
        SimpleNamespace(primary_condition_run_id=f"run:{code}") for code in ("C0", "C1", "C2", "C3")
    ]
    assert (
        service._packets_match_execution(
            execution=cast("object", execution),
            condition_runs=ALL_RUNS,
            packets=packets,
            pack_ids=_pack_ids({"C0", "C1", "C2", "C3", "C4"}),
        )
        is True
    )


def test_packets_match_false_when_ungated_condition_missing() -> None:
    # An ungated condition (C2) not yet generated -> absent from pack_ids -> incomplete.
    service, _ = _service()
    execution = SimpleNamespace(hypothesis="H1")
    packets = [
        SimpleNamespace(primary_condition_run_id=f"run:{code}") for code in ("C0", "C1", "C3", "C4")
    ]
    assert (
        service._packets_match_execution(
            execution=cast("object", execution),
            condition_runs=ALL_RUNS,
            packets=packets,
            pack_ids=_pack_ids({"C0", "C1", "C3", "C4"}),  # no C2
        )
        is False
    )
