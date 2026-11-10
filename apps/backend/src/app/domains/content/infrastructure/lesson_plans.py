"""Lesson plans as content: a plan is the item, its versions are its versions.

A plan's latest version is what the teacher reviews; approving freezes that version, and a
revision adds the next one, so a plan's version is how many versions it has. Who made the
plan is read from its first version: a revision does not change who made it.
"""

from __future__ import annotations

from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.ports import Approval
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import (
    approve_plan_version,
    close_plan_version,
)
from app.domains.content.application.errors import ContentError
from app.domains.content.application.records import ContentRecord
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.experiments.domain.types import ExperimentLifecycleStatus
from app.domains.experiments.infrastructure.models import Experiment

#: Who made a plan, by how its first version was written.
_ORIGIN = {
    "generated": "generated",
    "experiment_generated": "generated",
    "manual": "teacher",
    "experiment_manual": "teacher",
    "experiment_reused": "teacher",
    "document_import": "teacher",
    "study_record": "study_record",
}


def _current(versions: list[PlanVersion]) -> PlanVersion:
    """The version a plan is read as: its newest live one, else its newest."""
    live = [version for version in versions if version.status.is_live]
    return (live or versions)[-1]


def _review_status(current: PlanVersion) -> str:
    if current.status == PlanVersionStatus.APPROVED:
        return "approved"
    return "pending" if current.status.is_live else "rejected"


def _record(versions: list[PlanVersion]) -> ContentRecord:
    first, latest = versions[0], _current(versions)
    origin = _ORIGIN.get(first.source_type)
    return ContentRecord(
        content_id=latest.plan_id,
        type=BuiltIn.LESSON_PLAN.value,
        kind=ArtefactType.LESSON_PLAN.value,
        level=Level.CLASS,
        plan_version_id=latest.version_id,
        student_id=None,
        version=len(versions),
        review_status=_review_status(latest),
        review_reason=None if latest.status.is_live else latest.closed_reason,
        created_at=latest.created_at,
        provenance={
            **({"origin": origin} if origin else {}),
            **(
                {"generator": made_by}
                if (made_by := (latest.run_metadata or {}).get("generator"))
                else {}
            ),
        },
        manifest=latest.session_plan or {},
        read_only=any(version.concluded_at is not None for version in versions),
    )


async def _versions_of(db: AsyncSession, plan_ids: set[str]) -> list[list[PlanVersion]]:
    rows = await db.execute(
        select(PlanVersion)
        .where(PlanVersion.plan_id.in_(plan_ids))
        .order_by(PlanVersion.created_at, PlanVersion.id)
    )
    by_plan: dict[str, list[PlanVersion]] = defaultdict(list)
    for version in rows.scalars():
        by_plan[version.plan_id].append(version)
    return list(by_plan.values())


class LessonPlanRecords:
    """Lesson plans read from their own tables."""

    async def get(self, db: AsyncSession, plan_id: str) -> ContentRecord | None:
        versions = await _versions_of(db, {plan_id})
        return _record(versions[0]) if versions else None

    async def find(self, db: AsyncSession, *, plan_version_id: str | None) -> list[ContentRecord]:
        """The plan a version belongs to, or every plan."""
        query = select(PlanVersion.plan_id).distinct()
        if plan_version_id is not None:
            query = query.where(PlanVersion.version_id == plan_version_id)
        plan_ids = set((await db.execute(query)).scalars())
        return [_record(versions) for versions in await _versions_of(db, plan_ids)]


class PlanVersionFreezer:
    """Freezes a plan's latest version; a plan's approvals are its frozen versions."""

    async def freeze(self, db: AsyncSession, record: ContentRecord, *, approved_by: str) -> None:
        await approve_plan_version(db, version_id=record.plan_version_id, approved_by=approved_by)

    async def close(
        self, db: AsyncSession, record: ContentRecord, *, closed_by: str, reason: str
    ) -> None:
        """Discard the draft a plan is at, or take back the approval it is at.

        A version a running study froze stays approved: its record is the study's.
        """
        current = (await _versions_of(db, {record.content_id}) or [[]])[0]
        version = _current(current) if current else None
        if version is None or not version.status.is_live:
            raise ContentError(409, "lesson_plan_is_already_closed")
        if version.status == PlanVersionStatus.APPROVED and await _frozen_into_a_study(db, version):
            raise ContentError(409, "lesson_plan_is_frozen_into_a_running_study")
        await close_plan_version(
            db,
            version_id=version.version_id,
            status=(
                PlanVersionStatus.WITHDRAWN
                if version.status == PlanVersionStatus.APPROVED
                else PlanVersionStatus.REJECTED
            ),
            closed_by=closed_by,
            reason=reason,
        )

    async def frozen(self, db: AsyncSession, plan_id: str) -> list[Approval]:
        versions = (await _versions_of(db, {plan_id}) or [[]])[0]
        return [
            Approval(
                approval_id=version.version_id,
                approved_version=number,
                approved_by=version.approved_by,
                approved_at=version.approved_at,
            )
            for number, version in enumerate(versions, start=1)
            if version.status == PlanVersionStatus.APPROVED and version.approved_at is not None
        ]


async def _frozen_into_a_study(db: AsyncSession, version: PlanVersion) -> bool:
    running = await db.scalar(
        select(Experiment.id)
        .where(Experiment.plan_version_id == version.version_id)
        .where(Experiment.lifecycle_status != ExperimentLifecycleStatus.ENDED)
        .limit(1)
    )
    return running is not None
