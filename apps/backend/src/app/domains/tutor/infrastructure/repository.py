from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.events.models.events import Event


class TutorRepository:
    async def get_review_pack(
        self,
        db: AsyncSession,
        artefact_id: str,
    ) -> Artefact | None:
        result = await db.execute(
            select(Artefact)
            .filter(Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value)
            .filter(Artefact.artefact_id == artefact_id)
        )
        return result.scalars().first()

    async def save_event(self, db: AsyncSession, event: Event) -> Event:
        db.add(event)
        await db.commit()
        return event
