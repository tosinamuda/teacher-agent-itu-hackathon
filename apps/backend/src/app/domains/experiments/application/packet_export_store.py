"""Persistence roles participating in one packet-export transaction."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import Protocol, TypeVar

from app.domains.artefacts.core.infrastructure.models import Artefact

PacketExecution = TypeVar("PacketExecution", covariant=True)
PacketRecord = TypeVar("PacketRecord")
PacketConditionRun = TypeVar("PacketConditionRun")
PacketFocalCase = TypeVar("PacketFocalCase")


class PacketExports(Protocol[PacketExecution, PacketRecord, PacketConditionRun, PacketFocalCase]):
    """Queries and staged writes needed to replace one execution's packets."""

    async def lock_execution_by_public_id(self, execution_id: str) -> None: ...

    async def get_execution(self, execution_id: str) -> PacketExecution | None: ...

    async def list_packets(self, execution_db_id: uuid.UUID) -> list[PacketRecord]: ...

    async def list_condition_runs(
        self,
        execution_db_id: uuid.UUID,
    ) -> list[PacketConditionRun]: ...

    async def current_artefacts_by_condition_run(
        self,
        run_ids: Sequence[str],
    ) -> dict[str, Artefact]: ...

    async def count_real_ratings_for_packets(self, *, packet_ids: list[uuid.UUID]) -> int: ...

    async def delete_packets(self, *, packet_ids: list[uuid.UUID]) -> None: ...

    async def list_focal_cases(
        self,
        execution_db_id: uuid.UUID,
    ) -> list[PacketFocalCase]: ...

    async def save_packets(
        self,
        *,
        packets: list[PacketRecord],
    ) -> list[PacketRecord]: ...


class PacketExportStore(
    Protocol[PacketExecution, PacketRecord, PacketConditionRun, PacketFocalCase]
):
    """One atomic lock/check/delete/insert packet-export operation."""

    @property
    def packet_exports(
        self,
    ) -> PacketExports[PacketExecution, PacketRecord, PacketConditionRun, PacketFocalCase]: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
