"""Workflow service for the post-class review pack: visibility policy + regenerate fan-out.

Two route-facing decisions live here so the HTTP layer can stay pure transport:

- **Visibility policy** — when a learner asks for their packs the default is
  "approved only" (an unapproved pack must never reach the student); the caller
  can pass ``review_status="all"`` to opt out. The HTTP route used to encode this
  rule inline, which made it look like a transport concern; it isn't — the
  per-student gate is a domain rule of the review-pack lifecycle.
- **Regenerate fan-out** — a "regenerate" action with no ``student_id`` means
  "every student who submitted but has no pack yet"; the service expands that
  request and queues one generation job per target. The HTTP route used to do
  both the expansion and the loop; both belong here.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.build_jobs import ArtefactLifecycleManager
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.application.learner_names import (
    learner_names,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_pack_gate import (
    LearnerPackGate,
)
from app.domains.artefacts.types.post_class_review_pack.application.student_pack_service import (
    StudentPackGenerationService,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)


class ReviewPackWorkflowService:
    """Owns the learner-pack visibility policy and the per-student regenerate workflow."""

    def __init__(
        self,
        lifecycle: ArtefactLifecycleManager,
        student_pack_service: StudentPackGenerationService,
        gate: LearnerPackGate,
    ) -> None:
        self.lifecycle = lifecycle
        self.student_pack_service = student_pack_service
        self.gate = gate

    async def list_learner_packs(
        self,
        *,
        db: AsyncSession,
        learner_id: str | None,
        plan_version_id: str | None,
        review_status: str | None,
        limit: int,
    ) -> list[Artefact]:
        """List packs through the learner-facing visibility default.

        Learner queries see approved packs only unless the caller passes
        ``review_status="all"`` — the pending/in-review packs are teacher-only
        (the teacher review queue uses ``GET /pending``, not this surface).
        """
        resolved_status = self._resolve_visibility(
            learner_id=learner_id, review_status=review_status
        )
        return await self.lifecycle.list_learner_artefacts(
            db=db,
            learner_id=learner_id,
            plan_version_id=plan_version_id,
            limit=limit,
            review_status=resolved_status,
        )

    async def regenerate_packs(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        student_id: str | None = None,
    ) -> list[str]:
        """Enqueue (re)generation for one or every student that has no pack yet.

        With ``student_id`` set, queues just that student. Without it, the service
        looks up every student who submitted the lesson's exit assessment but has
        no learner-level pack and queues each one, through the same gate as a submission:
        nothing is queued before the class pack is approved or while a learner's survey is
        still due. Each enqueue creates a tracked generation job; a student already
        mid-generation is skipped (not re-queued). Returns the student ids actually queued.
        """
        targets = await self._resolve_regenerate_targets(
            db=db, plan_version_id=plan_version_id, student_id=student_id
        )
        queued: list[str] = []
        for target_student_id in targets:
            if await self.gate.request(
                db, student_id=target_student_id, plan_version_id=plan_version_id
            ):
                queued.append(target_student_id)
        return queued

    async def generation_statuses(
        self, *, db: AsyncSession, plan_version_id: str
    ) -> list[tuple[StudentPackGeneration, str]]:
        """The current generation attempt per student for this lesson, with student names.

        Backs the teacher's generation queue: each student's latest attempt (queued /
        running / succeeded / failed) so the UI can show "generating…" / "failed → retry"
        rather than only "no pack yet". Returns ``(job, full_name)`` pairs.
        """
        jobs = await self.gate.jobs.latest_statuses(db, plan_version_id=plan_version_id)
        if not jobs:
            return []
        names = await learner_names(db, [job.student_id for job in jobs])
        return [(job, names[job.student_id]) for job in jobs]

    @staticmethod
    def _resolve_visibility(*, learner_id: str | None, review_status: str | None) -> str | None:
        """Apply the learner-facing visibility default policy.

        - ``review_status="all"`` → no filter (caller opts into seeing every state)
        - learner query with no explicit ``review_status`` → ``"approved"``
        - everything else passes through unchanged
        """
        if review_status == "all":
            return None
        if learner_id and review_status is None:
            return "approved"
        return review_status

    async def _resolve_regenerate_targets(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        student_id: str | None,
    ) -> list[str]:
        if student_id:
            return [student_id]
        rows = await self.student_pack_service.list_students_missing_pack(
            db=db, plan_version_id=plan_version_id
        )
        return [row["student_id"] for row in rows]
