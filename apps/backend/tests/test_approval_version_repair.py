"""An approved artefact's version is the version its approval names."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact, ContentApproval
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from migrations.data.approval_version_repair import repair_approval_versions


def _note(
    artefact_id: str, *, version: int, status: ArtefactReviewStatus, plan: str = "LPV-R1"
) -> Artefact:
    return Artefact(
        artefact_id=artefact_id,
        artefact_type=ArtefactType.LESSON_NOTE.value,
        scope="class_level",
        plan_version_id=plan,
        manifest={},
        version=version,
        review_status=status,
    )


def _approval(artefact_id: str, approved_version: int) -> ContentApproval:
    return ContentApproval(
        approval_id=f"CA-{artefact_id}-{approved_version}",
        artefact_id=artefact_id,
        approved_version=approved_version,
        approved_by="Teacher One",
    )


async def _versions(db: AsyncSession) -> dict[str, int]:
    rows = await db.execute(
        select(Artefact.artefact_id, Artefact.version).where(
            Artefact.plan_version_id.in_(["LPV-R1", "LPV-CONCLUDED"])
        )
    )
    return {artefact_id: version for artefact_id, version in rows.all()}


@pytest.mark.asyncio
async def test_only_an_approval_s_extra_version_is_taken_off(db: AsyncSession) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            _note("AT-bumped", version=3, status=ArtefactReviewStatus.APPROVED),
            _approval("AT-bumped", 1),
            _approval("AT-bumped", 2),
            _note("AT-repaired", version=2, status=ArtefactReviewStatus.APPROVED),
            _approval("AT-repaired", 2),
            _note("AT-revised", version=3, status=ArtefactReviewStatus.PENDING),
            _approval("AT-revised", 1),
            _note("AT-unapproved", version=2, status=ArtefactReviewStatus.APPROVED),
            PlanVersion(
                version_id="LPV-CONCLUDED",
                plan_id="P-CONCLUDED",
                source_type="study_import",
                concluded_at=datetime.now(timezone.utc),
            ),
            _note(
                "AT-concluded",
                version=3,
                status=ArtefactReviewStatus.APPROVED,
                plan="LPV-CONCLUDED",
            ),
            _approval("AT-concluded", 2),
        ]
    )
    await db.flush()
    connection = await db.connection()

    assert await connection.run_sync(repair_approval_versions, dry_run=True) == 1
    assert await connection.run_sync(repair_approval_versions) == 1
    assert await connection.run_sync(repair_approval_versions) == 0

    db.expire_all()
    assert await _versions(db) == {
        "AT-bumped": 2,
        "AT-repaired": 2,
        "AT-revised": 3,
        "AT-unapproved": 2,
        "AT-concluded": 3,
    }
