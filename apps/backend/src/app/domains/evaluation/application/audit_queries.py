"""Named read-only source-audit queries and export."""

from __future__ import annotations

from typing import Protocol

from app.shared.json_types import JsonObject


class AuditQueueReader(Protocol):
    async def list_audit_queue(self, *, rater_id: str) -> list[JsonObject]: ...


class AuditDetailReader(Protocol):
    async def get_audit_item_detail(
        self, *, audit_item_id: str, rater_id: str
    ) -> dict[str, object]: ...


class AuditExportReader(Protocol):
    async def export_source_audit_pack(self, *, experiment_id: str) -> tuple[bytes, str]: ...


async def audit_queue(reader: AuditQueueReader, *, rater_id: str) -> list[JsonObject]:
    return await reader.list_audit_queue(rater_id=rater_id)


async def audit_detail(
    reader: AuditDetailReader,
    *,
    audit_item_id: str,
    rater_id: str,
) -> dict[str, object]:
    return await reader.get_audit_item_detail(
        audit_item_id=audit_item_id,
        rater_id=rater_id,
    )


async def export_audit_pack(
    reader: AuditExportReader,
    *,
    experiment_id: str,
) -> tuple[bytes, str]:
    return await reader.export_source_audit_pack(experiment_id=experiment_id)
