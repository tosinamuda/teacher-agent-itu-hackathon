"""What each teacher has switched, kept by the teacher's sign-in."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.infrastructure.models import TeacherPreferenceRecord


class TeacherPreferences:
    async def _record(self, db: AsyncSession, auth_id: str) -> TeacherPreferenceRecord | None:
        return (
            await db.execute(
                select(TeacherPreferenceRecord).where(TeacherPreferenceRecord.auth_id == auth_id)
            )
        ).scalar_one_or_none()

    async def _record_for(self, db: AsyncSession, auth_id: str) -> TeacherPreferenceRecord:
        record = await self._record(db, auth_id)
        if record is None:
            record = TeacherPreferenceRecord(auth_id=auth_id, hidden_types=[])
            db.add(record)
        return record

    async def hidden(self, db: AsyncSession, auth_id: str) -> set[str]:
        """The optional types this teacher has switched off."""
        record = await self._record(db, auth_id)
        return set(record.hidden_types or []) if record else set()

    async def set_material(self, db: AsyncSession, auth_id: str, type: str, enabled: bool) -> None:
        record = await self._record_for(db, auth_id)
        hidden = set(record.hidden_types or [])
        record.hidden_types = sorted(hidden - {type} if enabled else hidden | {type})
        await db.flush()
