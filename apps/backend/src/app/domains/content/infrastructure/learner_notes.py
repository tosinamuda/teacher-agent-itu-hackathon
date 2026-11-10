"""The learners' revision notes made from a class note, withdrawn when the class note is."""

from __future__ import annotations

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.shared.time import utc_now


class LearnerNotes:
    async def withdraw_for(
        self, db: AsyncSession, plan_version_id: str, *, withdrawn_by: str, reason: str
    ) -> None:
        """Reject every learner's note for the lesson that is not already rejected."""
        await db.execute(
            update(Artefact)
            .where(Artefact.plan_version_id == plan_version_id)
            .where(Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value)
            .where(Artefact.scope == ArtefactScope.LEARNER_LEVEL.value)
            .where(Artefact.experiment_condition_run_id.is_(None))
            .where(Artefact.review_status != ArtefactReviewStatus.REJECTED)
            .values(
                review_status=ArtefactReviewStatus.REJECTED,
                reviewed_at=utc_now(),
                reviewed_by=withdrawn_by,
                review_reason=f"The class revision note was withdrawn: {reason}"[:512],
            )
        )
        await db.commit()
