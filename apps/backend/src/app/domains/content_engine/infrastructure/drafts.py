"""Drafts in the ``content_drafts`` table."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.parts import Unit
from app.domains.content_engine.domain.draft import Draft, DraftStatus
from app.domains.content_engine.domain.lesson import LessonUnit
from app.domains.content_engine.infrastructure.models import ContentDraftRecord
from app.shared.ids import PublicIdPrefix, new_public_id


def _draft(row: ContentDraftRecord) -> Draft:
    return Draft(
        draft_id=row.draft_id,
        type=row.type,
        kind=row.kind,
        spec_revision=row.spec_revision,
        plan_version_id=row.plan_version_id,
        session_id=row.session_id,
        unit=Unit(row.unit),
        units=tuple(
            LessonUnit(unit["unit_id"], unit["label"], Unit(unit["unit"])) for unit in row.units
        ),
        source=row.source,
        parts=dict(row.parts),
        status=DraftStatus(row.status),
        saved_as=row.saved_as,
        created_by=row.created_by,
        author=row.author,
        student_id=row.student_id,
    )


class SqlAlchemyDrafts:
    def new_id(self) -> str:
        return new_public_id(PublicIdPrefix.CONTENT_DRAFT)

    async def add(self, db: AsyncSession, draft: Draft) -> None:
        db.add(
            ContentDraftRecord(
                draft_id=draft.draft_id,
                type=draft.type,
                kind=draft.kind,
                spec_revision=draft.spec_revision,
                plan_version_id=draft.plan_version_id,
                session_id=draft.session_id,
                source=draft.source,
                unit=draft.unit.value,
                units=[
                    {"unit_id": u.unit_id, "label": u.label, "unit": u.unit.value}
                    for u in draft.units
                ],
                parts=draft.parts,
                status=draft.status.value,
                saved_as=draft.saved_as,
                created_by=draft.created_by,
                author=draft.author,
                student_id=draft.student_id,
            )
        )
        await db.flush()

    async def get(self, db: AsyncSession, draft_id: str, *, for_update: bool) -> Draft | None:
        query = select(ContentDraftRecord).where(ContentDraftRecord.draft_id == draft_id)
        if for_update:
            query = query.with_for_update().execution_options(populate_existing=True)
        row = await db.scalar(query)
        return _draft(row) if row is not None else None

    async def latest_open(self, db: AsyncSession, type_: str, session_id: str) -> Draft | None:
        """The newest draft of this type still being written for the lesson, if any."""
        row = await db.scalar(
            select(ContentDraftRecord)
            .where(
                ContentDraftRecord.type == type_,
                ContentDraftRecord.session_id == session_id,
                ContentDraftRecord.status == DraftStatus.OPEN.value,
            )
            .order_by(ContentDraftRecord.created_at.desc())
            .limit(1)
        )
        return _draft(row) if row is not None else None

    async def save(self, db: AsyncSession, draft: Draft) -> None:
        row = await db.scalar(
            select(ContentDraftRecord).where(ContentDraftRecord.draft_id == draft.draft_id)
        )
        if row is None:
            raise LookupError(f"content_draft_not_found:{draft.draft_id}")
        row.parts = dict(draft.parts)
        row.status = draft.status.value
        row.saved_as = draft.saved_as
        await db.flush()
