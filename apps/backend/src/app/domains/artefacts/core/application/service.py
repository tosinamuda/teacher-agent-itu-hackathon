from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.ports import (
    ApprovalFollowUp,
    ArtefactReadPort,
    ContentApprovals,
    ReviewPackExportPort,
)
from app.domains.artefacts.core.domain.types import (
    DEFAULT_ARTEFACT_TYPE,
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.shared.time import utc_now

MANIFEST_PATH_KEY = "manifest_path"


@dataclass
class ArtefactApplicationError(Exception):
    status_code: int
    detail: str


class ArtefactApplicationService:
    """Read/approve/export operations over persisted artefacts. Artefact *generation*.

    lives in the spec pipeline (StudentPackGenerationService / the experiment runner),
    not here — there is no build-job rendering path.
    """

    def __init__(
        self,
        repository: ArtefactReadPort,
        artefact_store: ReviewPackExportPort,
        *,
        approvals: ContentApprovals,
        after_approval: ApprovalFollowUp | None = None,
    ) -> None:
        self.repository = repository
        self.artefact_store = artefact_store
        self.approvals = approvals
        self.after_approval = after_approval

    async def get_artefact(
        self,
        *,
        db: AsyncSession,
        artefact_id: str,
    ) -> Artefact | None:
        return await self.repository.get_artefact(db, artefact_id)

    async def list_artefacts_for_student(
        self,
        *,
        db: AsyncSession,
        student_id: str,
        limit: int,
        artefact_type: ArtefactType = DEFAULT_ARTEFACT_TYPE,
        review_status: str | None = None,
    ) -> list[Artefact]:
        return await self.repository.list_artefacts_for_student(
            db,
            artefact_type=artefact_type,
            student_id=student_id,
            limit=limit,
            review_status=review_status,
        )

    async def list_pending_learner_artefacts(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str | None,
        limit: int,
        artefact_type: ArtefactType = DEFAULT_ARTEFACT_TYPE,
        owned_plan_version_ids: Sequence[str] | None = None,
        review_status: ArtefactReviewStatus = ArtefactReviewStatus.PENDING,
    ) -> list[Artefact]:
        return await self.repository.list_pending_learner_artefacts(
            db,
            artefact_type=artefact_type,
            plan_version_id=plan_version_id,
            limit=limit,
            owned_plan_version_ids=owned_plan_version_ids,
            review_status=review_status,
        )

    async def approve_artefact(
        self,
        *,
        db: AsyncSession,
        artefact: Artefact,
        reviewed_by: str | None,
        expected_version: int | None = None,
    ) -> Artefact:
        # Re-read the row FOR UPDATE before mutating so the approval serializes against a
        # concurrent in-place revise: otherwise approve mutated a (possibly stale) snapshot and
        # could clobber a just-revised manifest or stamp APPROVED on content it never saw.
        target = await self.repository.get_artefact_for_update(db, artefact.artefact_id) or artefact
        # Optimistic concurrency: if the caller says which version it reviewed and the row has
        # moved on (a revise landed since they loaded it), refuse — the lock alone only stops a
        # torn write, not a blind approve of content the teacher never saw.
        if expected_version is not None and target.version != expected_version:
            await db.rollback()
            raise ArtefactApplicationError(409, "artefact_changed")
        # An approval changes no content, so it mints no version: the approved version is the
        # one the teacher read. Under the lock, a second approval of it is refused instead.
        if target.review_status == ArtefactReviewStatus.APPROVED:
            await db.rollback()
            raise ArtefactApplicationError(409, "artefact_already_approved")
        self.approvals.record_approval(
            db,
            artefact_id=target.artefact_id,
            approved_version=target.version,
            approved_by=reviewed_by,
        )
        target.review_status = ArtefactReviewStatus.APPROVED
        target.reviewed_at = utc_now()
        target.reviewed_by = reviewed_by
        await db.commit()
        await db.refresh(target)
        if self.after_approval is not None:
            await self.after_approval.after_approval(db, target)
        return target

    async def reject_artefact(
        self,
        *,
        db: AsyncSession,
        artefact: Artefact,
        reviewed_by: str | None,
        reason: str,
        expected_version: int | None = None,
    ) -> None:
        """Reject a pending version, or withdraw an approved one, and keep the teacher's reason."""
        target = await self.repository.get_artefact_for_update(db, artefact.artefact_id) or artefact
        if expected_version is not None and target.version != expected_version:
            await db.rollback()
            raise ArtefactApplicationError(409, "artefact_changed")
        if target.review_status == ArtefactReviewStatus.REJECTED:
            await db.rollback()
            raise ArtefactApplicationError(409, "artefact_already_rejected")
        target.review_status = ArtefactReviewStatus.REJECTED
        target.reviewed_at = utc_now()
        target.reviewed_by = reviewed_by
        target.review_reason = reason
        await db.commit()

    async def get_latest_class_level_artefact(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        artefact_type: ArtefactType = DEFAULT_ARTEFACT_TYPE,
    ) -> Artefact | None:
        return await self.repository.get_latest_artefact_for_plan_version(
            db,
            artefact_type=artefact_type,
            scope=ArtefactScope.CLASS_LEVEL,
            plan_version_id=plan_version_id,
        )

    async def export_review_pack(self, *, db: AsyncSession, artefact: Artefact) -> Artefact:
        # The export adds where it wrote to what the artefact records, such as its grounding.
        artefact.artefact_refs = {
            **(artefact.artefact_refs or {}),
            **self.artefact_store.export_review_pack(artefact.artefact_id, artefact.manifest),
        }
        await db.commit()
        await db.refresh(artefact)
        return artefact

    async def resolve_manifest_path(
        self,
        *,
        db: AsyncSession,
        artefact: Artefact,
    ) -> tuple[Artefact, str]:
        manifest_path = self._existing_manifest_path(artefact)
        if manifest_path is None:
            artefact = await self.export_review_pack(db=db, artefact=artefact)
            manifest_path = self._existing_manifest_path(artefact)
        if manifest_path is None:
            raise ArtefactApplicationError(500, "export_failed")
        return artefact, manifest_path

    def _existing_manifest_path(self, artefact: Artefact) -> str | None:
        if not artefact.artefact_refs:
            return None
        manifest_path = artefact.artefact_refs.get(MANIFEST_PATH_KEY)
        if not manifest_path:
            return None
        if not Path(str(manifest_path)).exists():
            return None
        return str(manifest_path)
