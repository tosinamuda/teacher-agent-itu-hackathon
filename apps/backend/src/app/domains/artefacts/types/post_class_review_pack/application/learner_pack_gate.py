"""When a learner's personalised pack may be made: only once both of its inputs hold.

A learner's pack adapts the lesson's class pack to what the learner's marked work showed, so
it waits for two things: the teacher's approval of the class pack, and the learner's complete
evidence (the marked responses, and the post-class survey where the flow collects one). A
submission that arrives first waits; the class pack's approval releases every learner whose
evidence is already in. Nothing else queues a learner's generation.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.types.post_class_review_pack.application.generation_job_service import (
    StudentPackGenerationJobService,
)

if TYPE_CHECKING:
    from app.domains.artefacts.core.infrastructure.models import Artefact

logger = logging.getLogger(__name__)


class LearnerPackReadiness(Protocol):
    """The two facts the gate needs, and the learners it has kept waiting."""

    async def class_pack_approved(self, db: AsyncSession, plan_version_id: str) -> bool: ...

    async def evidence_complete(
        self, db: AsyncSession, *, student_id: str, plan_version_id: str
    ) -> bool: ...

    async def waiting_learners(self, db: AsyncSession, plan_version_id: str) -> list[str]: ...


class LearnerPackGate:
    """Queue a learner's pack only when the class pack is approved and the evidence is in."""

    def __init__(
        self, readiness: LearnerPackReadiness, jobs: StudentPackGenerationJobService
    ) -> None:
        self.readiness = readiness
        self.jobs = jobs

    async def request(self, db: AsyncSession, *, student_id: str, plan_version_id: str) -> bool:
        """Queue this learner's pack if the gate is open; report whether a job was queued."""
        if not await self.readiness.class_pack_approved(db, plan_version_id):
            return False
        if not await self.readiness.evidence_complete(
            db, student_id=student_id, plan_version_id=plan_version_id
        ):
            return False
        job = await self.jobs.enqueue(db, student_id=student_id, plan_version_id=plan_version_id)
        return job is not None

    async def release_waiting(self, db: AsyncSession, plan_version_id: str) -> list[str]:
        """Queue every learner who was waiting on the class pack; return those queued."""
        if not await self.readiness.class_pack_approved(db, plan_version_id):
            return []
        queued = []
        for student_id in await self.readiness.waiting_learners(db, plan_version_id):
            job = await self.jobs.enqueue(
                db, student_id=student_id, plan_version_id=plan_version_id
            )
            if job is not None:
                queued.append(student_id)
        return queued

    async def after_approval(self, db: AsyncSession, artefact: Artefact) -> None:
        """A class pack's approval opens the gate for the learners already waiting on it.

        Runs after the approval has committed, so a failure here leaves the approval standing;
        the teacher's regenerate action reaches any learner it missed.
        """
        if artefact.artefact_type != ArtefactType.POST_CLASS_REVIEW_PACK.value:
            return
        if artefact.scope != ArtefactScope.CLASS_LEVEL.value:
            return
        try:
            await self.release_waiting(db, artefact.plan_version_id)
        except Exception:  # noqa: BLE001 - the approval has committed; never undo it
            logger.exception("releasing learners failed after approving %s", artefact.artefact_id)
