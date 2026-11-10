"""Engine-built content, stored as class-level artefacts like every other content type."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import get_plan_row
from app.domains.content_engine.application.drafting_ports import StoredContent
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject


class SqlAlchemyEngineContent:
    async def get(self, db: AsyncSession, content_id: str) -> StoredContent | None:
        artefact = await db.scalar(select(Artefact).where(Artefact.artefact_id == content_id))
        if artefact is None:
            return None
        recorded = (artefact.artefact_refs or {}).get("specification")
        revision = recorded.get("revision") if isinstance(recorded, dict) else None
        return StoredContent(
            content_id=artefact.artefact_id,
            kind=artefact.artefact_type,
            plan_version_id=artefact.plan_version_id,
            manifest=artefact.manifest or {},
            spec_revision=revision if isinstance(revision, int) else None,
        )

    async def add(
        self,
        db: AsyncSession,
        *,
        kind: str,
        plan_version_id: str,
        manifest: JsonObject,
        refs: JsonObject,
    ) -> str:
        artefact = Artefact(
            artefact_id=new_public_id(PublicIdPrefix.ARTEFACT),
            artefact_type=kind,
            scope=ArtefactScope.CLASS_LEVEL.value,
            plan_version_id=plan_version_id,
            manifest=manifest,
            artefact_refs=refs,
            review_status=ArtefactReviewStatus.PENDING,
        )
        db.add(artefact)
        await db.flush()
        return artefact.artefact_id

    async def replace(self, db: AsyncSession, content_id: str, manifest: JsonObject) -> None:
        artefact = await db.scalar(
            select(Artefact)
            .where(Artefact.artefact_id == content_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        if artefact is None:
            raise LookupError(f"content_not_found:{content_id}")
        if artefact.manifest == manifest:
            return
        artefact.manifest = manifest
        artefact.review_status = ArtefactReviewStatus.PENDING
        artefact.version = artefact.version + 1
        await db.flush()


class SqlAlchemyPlanContent:
    """Lesson plans read as content: the plan's latest version, for the lesson period it is for."""

    async def get(self, db: AsyncSession, content_id: str) -> StoredContent | None:
        row = await get_plan_row(db, plan_or_version_id=content_id)
        if row is None or row[1].lesson_period_id is None:
            return None
        version, plan = row
        return StoredContent(
            content_id=plan.plan_id,
            kind=ArtefactType.LESSON_PLAN.value,
            plan_version_id=version.version_id,
            manifest=version.session_plan or {},
            spec_revision=None,
            session_id=str(plan.lesson_period_id),
        )
