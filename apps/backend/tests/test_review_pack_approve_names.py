"""Approving a student's revision note answers with the student's name, as reading it does."""

from __future__ import annotations

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.api.schemas import ApprovePackRequest
from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.api.routes import (
    approve_review_pack,
    get_review_pack,
)
from app.domains.learners.models import LearnerProfile
from app.shared.auth import ROLE_RESEARCH_MANAGER, Actor


@pytest.mark.asyncio
async def test_the_approved_note_names_its_student(db: AsyncSession) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            LearnerProfile(
                student_id="ST-NAMED", full_name="Ada Obi", grade="JSS1", track="General"
            ),
            Artefact(
                artefact_id="AT-NAMED",
                artefact_type=ArtefactType.POST_CLASS_REVIEW_PACK.value,
                scope=ArtefactScope.LEARNER_LEVEL.value,
                plan_version_id="LPV-NAMED",
                student_id="ST-NAMED",
                manifest={},
                review_status=ArtefactReviewStatus.PENDING,
            ),
        ]
    )
    await db.commit()

    researcher = Actor(role=ROLE_RESEARCH_MANAGER, auth_id="code|researcher")
    read = await get_review_pack("AT-NAMED", actor=researcher, db=db)
    approved = await approve_review_pack(
        "AT-NAMED",
        ApprovePackRequest(expected_version=read.version),
        actor=researcher,
        db=db,
    )

    assert (read.learner_name, approved.learner_name) == ("Ada Obi", "Ada Obi")
    assert approved.review_status == ArtefactReviewStatus.APPROVED
