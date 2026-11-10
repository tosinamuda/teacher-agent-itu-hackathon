from __future__ import annotations

from collections.abc import Callable, Hashable, Sequence
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.service import ArtefactApplicationService
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact


@dataclass
class ArtefactLifecycleError(Exception):
    status_code: int
    detail: str


def _current_version_per(
    artefacts: list[Artefact], *, key: Callable[[Artefact], Hashable]
) -> list[Artefact]:
    """Keep only the newest artefact per ``key`` — the "keep versions" current-pack view.

    A (student, lesson) may have several pack rows (each regeneration is a new version
    kept for provenance); the teacher/student UI shows only the current = latest one.
    The input MUST be ``created_at``-descending, so the first row seen per key is newest.
    """
    seen: set[Hashable] = set()
    current: list[Artefact] = []
    for artefact in artefacts:
        artefact_key = key(artefact)
        if artefact_key in seen:
            continue
        seen.add(artefact_key)
        current.append(artefact)
    return current


class ArtefactLifecycleManager:
    """Read/approve/export operations over artefacts.

    Generation runs directly through the spec pipeline
    (``StudentPackGenerationService`` / the experiment runner), so there is no
    build-job orchestration here.
    """

    def __init__(self, artefact_service: ArtefactApplicationService) -> None:
        self.artefact_service = artefact_service

    async def get_artefact(
        self,
        *,
        db: AsyncSession,
        artefact_id: str,
    ) -> Artefact:
        artefact = await self.artefact_service.get_artefact(db=db, artefact_id=artefact_id)
        if artefact is None:
            raise ArtefactLifecycleError(404, "artefact_not_found")
        return artefact

    async def list_learner_artefacts(
        self,
        *,
        db: AsyncSession,
        learner_id: str | None,
        plan_version_id: str | None,
        limit: int,
        review_status: str | None = None,
    ) -> list[Artefact]:
        if learner_id:
            rows = await self.artefact_service.list_artefacts_for_student(
                db=db,
                student_id=learner_id,
                limit=limit,
                review_status=review_status,
            )
            # Keep-versions: show one current pack per lesson, newest wins.
            return _current_version_per(rows, key=lambda a: a.plan_version_id)
        if plan_version_id:
            artefact = await self.artefact_service.get_latest_class_level_artefact(
                db=db,
                plan_version_id=plan_version_id,
            )
            return [artefact] if artefact is not None else []
        return []

    async def list_pending_learner_packs(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str | None,
        limit: int,
        owned_plan_version_ids: Sequence[str] | None = None,
        review_status: ArtefactReviewStatus = ArtefactReviewStatus.PENDING,
    ) -> list[Artefact]:
        rows = await self.artefact_service.list_pending_learner_artefacts(
            db=db,
            plan_version_id=plan_version_id,
            limit=limit,
            owned_plan_version_ids=owned_plan_version_ids,
            review_status=review_status,
        )
        # Keep-versions: the teacher reviews the current (latest) pending pack per
        # (student, lesson); older superseded pending versions don't clutter the queue.
        return _current_version_per(rows, key=lambda a: (a.student_id, a.plan_version_id))

    async def approve_artefact(
        self,
        *,
        db: AsyncSession,
        artefact_id: str,
        reviewed_by: str | None,
        expected_version: int | None = None,
    ) -> Artefact:
        artefact = await self.get_artefact(db=db, artefact_id=artefact_id)
        return await self.artefact_service.approve_artefact(
            db=db,
            artefact=artefact,
            reviewed_by=reviewed_by,
            expected_version=expected_version,
        )

    async def reject_artefact(
        self,
        *,
        db: AsyncSession,
        artefact_id: str,
        reviewed_by: str | None,
        reason: str,
        expected_version: int | None = None,
    ) -> None:
        artefact = await self.get_artefact(db=db, artefact_id=artefact_id)
        await self.artefact_service.reject_artefact(
            db=db,
            artefact=artefact,
            reviewed_by=reviewed_by,
            reason=reason,
            expected_version=expected_version,
        )

    async def export_artefact(
        self,
        *,
        db: AsyncSession,
        artefact_id: str,
    ) -> Artefact:
        artefact = await self.get_artefact(db=db, artefact_id=artefact_id)
        return await self.artefact_service.export_review_pack(db=db, artefact=artefact)

    async def resolve_download_manifest_path(
        self,
        *,
        db: AsyncSession,
        artefact_id: str,
    ) -> tuple[Artefact, str]:
        artefact = await self.get_artefact(db=db, artefact_id=artefact_id)
        return await self.artefact_service.resolve_manifest_path(db=db, artefact=artefact)
