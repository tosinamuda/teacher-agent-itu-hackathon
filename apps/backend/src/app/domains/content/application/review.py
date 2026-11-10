"""The teacher's two decisions on content: approve it, or revise it with feedback."""

from __future__ import annotations

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.service import ChatRecord, RevisionRecord
from app.shared.json_types import JsonObject


class Approver(Protocol):
    """Approves content at the version the teacher saw, keeps the approval, and keeps a refusal."""

    async def approve(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        expected_version: int | None,
        approved_by: str | None,
    ) -> None: ...

    async def reject(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        expected_version: int | None,
        rejected_by: str | None,
        reason: str,
    ) -> None:
        """Reject a pending version, or withdraw an approved one."""
        ...


class ClassTestRelease(Protocol):
    """Sends a class test to its students."""

    async def release(
        self, db: AsyncSession, *, plan_version_id: str, released_by: str
    ) -> None: ...


class Revisions(Protocol):
    """The revision conversation, addressed by a stored type and the subject it revises."""

    async def revise(
        self,
        db: AsyncSession,
        *,
        stored_type: str,
        subject_id: str,
        feedback: str,
        requested_by: str | None,
        highlight: JsonObject | None = None,
        chat_id: str | None = None,
    ) -> RevisionRecord: ...

    async def history(
        self, db: AsyncSession, *, stored_type: str, subject_id: str
    ) -> list[RevisionRecord]: ...

    async def chats(
        self, db: AsyncSession, *, stored_type: str, subject_id: str
    ) -> list[ChatRecord]: ...

    async def new_chat(
        self,
        db: AsyncSession,
        *,
        stored_type: str,
        subject_id: str,
        requested_by: str | None,
        title: str | None,
    ) -> ChatRecord: ...

    async def chat(
        self, db: AsyncSession, *, stored_type: str, subject_id: str, chat_id: str
    ) -> ChatRecord: ...
