from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.ports import Approval
from app.domains.artefacts.core.domain.made_from import made_from_of
from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import (
    Artefact,
    ArtefactPlan,
    ContentApproval,
)
from app.shared.ids import PublicIdPrefix, new_public_id


class ArtefactRepository:
    async def save_plan(self, db: AsyncSession, plan: ArtefactPlan) -> ArtefactPlan:
        db.add(plan)
        await db.commit()
        await db.refresh(plan)
        return plan

    async def save_plans(
        self,
        db: AsyncSession,
        *,
        plans: list[ArtefactPlan],
    ) -> None:
        db.add_all(plans)
        await db.commit()

    async def get_plan(
        self,
        db: AsyncSession,
        artefact_plan_id: str,
    ) -> ArtefactPlan | None:
        result = await db.execute(
            select(ArtefactPlan).filter(ArtefactPlan.artefact_plan_id == artefact_plan_id)
        )
        return result.scalars().first()

    async def get_latest_plan(
        self,
        db: AsyncSession,
        *,
        artefact_type: ArtefactType,
        scope: ArtefactScope,
        plan_version_id: str,
        student_id: str | None = None,
        experiment_condition_run_id: str | None = None,
    ) -> ArtefactPlan | None:
        stmt = (
            select(ArtefactPlan)
            .filter(ArtefactPlan.artefact_type == artefact_type.value)
            .filter(ArtefactPlan.scope == scope.value)
            .filter(ArtefactPlan.plan_version_id == plan_version_id)
        )
        if student_id is None:
            stmt = stmt.filter(ArtefactPlan.student_id.is_(None))
        else:
            stmt = stmt.filter(ArtefactPlan.student_id == student_id)
        if experiment_condition_run_id is None:
            stmt = stmt.filter(ArtefactPlan.experiment_condition_run_id.is_(None))
        else:
            stmt = stmt.filter(
                ArtefactPlan.experiment_condition_run_id == experiment_condition_run_id
            )
        result = await db.execute(stmt.order_by(ArtefactPlan.created_at.desc()))
        return result.scalars().first()

    async def save_artefact(self, db: AsyncSession, artefact: Artefact) -> Artefact:
        db.add(artefact)
        await db.commit()
        await db.refresh(artefact)
        return artefact

    async def get_artefact(self, db: AsyncSession, artefact_id: str) -> Artefact | None:
        result = await db.execute(select(Artefact).filter(Artefact.artefact_id == artefact_id))
        return result.scalars().first()

    async def get_artefact_for_update(self, db: AsyncSession, artefact_id: str) -> Artefact | None:
        """Row-lock + return the artefact, to serialize approve vs in-place revise.

        Both the teacher-approve path and a revision turn do a read-modify-write on the same
        row's ``review_status``/``manifest``. Taking ``FOR UPDATE`` (+ ``populate_existing`` so a
        caller's already-loaded snapshot refreshes to the locked DB state) makes those
        transitions serialize, instead of last-writer-wins clobbering a manifest or stamping
        an approval onto content the approver never saw / silently undoing an approval.
        """
        result = await db.execute(
            select(Artefact)
            .filter(Artefact.artefact_id == artefact_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return result.scalars().first()

    def record_approval(
        self, db: AsyncSession, *, artefact_id: str, approved_version: int, approved_by: str | None
    ) -> None:
        """Add one approval to the session; the caller's commit writes it with the approval."""
        db.add(
            ContentApproval(
                approval_id=new_public_id(PublicIdPrefix.CONTENT_APPROVAL),
                artefact_id=artefact_id,
                approved_version=approved_version,
                approved_by=approved_by,
            )
        )

    async def list_approvals(self, db: AsyncSession, artefact_id: str) -> list[Approval]:
        """A content item's approvals, oldest first."""
        result = await db.execute(
            select(ContentApproval)
            .where(ContentApproval.artefact_id == artefact_id)
            .order_by(ContentApproval.approved_at, ContentApproval.id)
        )
        return [
            Approval(
                approval_id=row.approval_id,
                approved_version=row.approved_version,
                approved_by=row.approved_by,
                approved_at=row.approved_at,
            )
            for row in result.scalars()
        ]

    async def current_artefacts_by_condition_run(
        self, db: AsyncSession, run_ids: Sequence[str]
    ) -> dict[str, Artefact]:
        """Map each condition-run business id to its CURRENT pack artefact.

        Resolves via the single stored link — ``Artefact.experiment_condition_run_id``
        (the back-pointer from an output to the run that produced it). A run may
        own more than one artefact version (e.g. a regenerated C4 pack), so this
        is deliberately 1-or-many-safe: the **approved** version wins; absent an
        approved one, the **latest by created_at**. One query for the whole set,
        so callers avoid an N+1 over their condition runs.
        """
        ids = [run_id for run_id in run_ids if run_id]
        if not ids:
            return {}
        result = await db.execute(
            select(Artefact)
            .where(Artefact.experiment_condition_run_id.in_(ids))
            .order_by(Artefact.created_at.asc())
        )
        by_run: dict[str, list[Artefact]] = defaultdict(list)
        for artefact in result.scalars().all():
            run_id = artefact.experiment_condition_run_id
            if run_id is not None:
                by_run[run_id].append(artefact)
        chosen: dict[str, Artefact] = {}
        for run_id, artefacts in by_run.items():
            approved = [
                a for a in artefacts if a.review_status == ArtefactReviewStatus.APPROVED.value
            ]
            # `artefacts` is created_at-ascending, so [-1] is the latest of the pool.
            chosen[run_id] = (approved or artefacts)[-1]
        return chosen

    async def current_artefact_for_condition_run(
        self, db: AsyncSession, run_id: str
    ) -> Artefact | None:
        """The single current pack artefact for one condition run (see bulk variant)."""
        return (await self.current_artefacts_by_condition_run(db, [run_id])).get(run_id)

    async def list_artefacts_for_student(
        self,
        db: AsyncSession,
        *,
        artefact_type: ArtefactType,
        student_id: str,
        limit: int,
        review_status: str | None = None,
    ) -> list[Artefact]:
        stmt = (
            select(Artefact)
            .filter(Artefact.artefact_type == artefact_type.value)
            .filter(Artefact.student_id == student_id)
        )
        if review_status is not None:
            stmt = stmt.filter(Artefact.review_status == review_status)
        result = await db.execute(stmt.order_by(Artefact.created_at.desc()).limit(limit))
        return await self._made_from_a_current_version(db, list(result.scalars().all()))

    async def _made_from_a_current_version(
        self, db: AsyncSession, artefacts: list[Artefact]
    ) -> list[Artefact]:
        """Drop a note made from a version of another note that is no longer its approved one.

        A learner's note is released only while the class note it adapts stands approved at the
        version it was made from. A revised class note is a new version and pending, so notes made
        from the old one wait for the new version's notes.
        """
        sources = {m[0] for a in artefacts if (m := made_from_of(a.artefact_refs)) is not None}
        if not sources:
            return artefacts
        rows = await db.execute(
            select(Artefact.artefact_id, Artefact.version, Artefact.review_status).where(
                Artefact.artefact_id.in_(sources)
            )
        )
        current = {
            artefact_id: version
            for artefact_id, version, status in rows.all()
            if status == ArtefactReviewStatus.APPROVED
        }
        return [
            a
            for a in artefacts
            if (m := made_from_of(a.artefact_refs)) is None or current.get(m[0]) == m[1]
        ]

    async def list_pending_learner_artefacts(
        self,
        db: AsyncSession,
        *,
        artefact_type: ArtefactType,
        plan_version_id: str | None,
        limit: int,
        owned_plan_version_ids: Sequence[str] | None = None,
        review_status: ArtefactReviewStatus = ArtefactReviewStatus.PENDING,
    ) -> list[Artefact]:
        stmt = (
            select(Artefact)
            .filter(Artefact.artefact_type == artefact_type.value)
            .filter(Artefact.scope == ArtefactScope.LEARNER_LEVEL.value)
            .filter(Artefact.review_status == review_status)
            # Production queue only: an experiment's own plan_version shares the
            # lesson_period (so it resolves as teacher-owned), but artefacts born
            # from an experiment condition run are NOT the teacher's production
            # packs and must never surface in their review queue.
            .filter(Artefact.experiment_condition_run_id.is_(None))
        )
        if plan_version_id:
            stmt = stmt.filter(Artefact.plan_version_id == plan_version_id)
        # Scope to a teacher's own classes (None = research-manager, sees all).
        # An empty list means "owns nothing" → no rows, which is correct.
        if owned_plan_version_ids is not None:
            stmt = stmt.filter(Artefact.plan_version_id.in_(owned_plan_version_ids))
        result = await db.execute(stmt.order_by(Artefact.created_at.desc()).limit(limit))
        return list(result.scalars().all())

    async def get_latest_artefact_for_plan_version(
        self,
        db: AsyncSession,
        *,
        artefact_type: ArtefactType,
        scope: ArtefactScope,
        plan_version_id: str,
    ) -> Artefact | None:
        result = await db.execute(
            select(Artefact)
            .filter(Artefact.artefact_type == artefact_type.value)
            .filter(Artefact.scope == scope.value)
            .filter(Artefact.plan_version_id == plan_version_id)
            .order_by(Artefact.created_at.desc())
        )
        return result.scalars().first()
