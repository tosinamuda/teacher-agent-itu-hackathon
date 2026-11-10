"""A learner's note is released only while the class note it was made from stands approved."""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.made_from import made_from
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.wiring import build_artefact_service
from app.domains.artefacts.types.post_class_review_pack.infrastructure.learner_pack_readiness import (  # noqa: E501
    SqlAlchemyLearnerPackReadiness,
)
from tests.test_learner_pack_gate import _approve, _lesson, _submit

PLAN = "LPV-CV1"
STUDENT = "ST-CV1"


async def _learner_note(db: AsyncSession, class_pack: Artefact, *, made_from_it: bool) -> None:
    db.add(
        Artefact(
            artefact_id="AT-learner-cv",
            artefact_type="post_class_review_pack",
            scope="learner_level",
            plan_version_id=PLAN,
            student_id=STUDENT,
            manifest={"steps": []},
            artefact_refs=(
                {"made_from": made_from(class_pack.artefact_id, class_pack.version)}
                if made_from_it
                else {}
            ),
            review_status=ArtefactReviewStatus.APPROVED,
        )
    )
    await db.flush()


async def _released(db: AsyncSession) -> list[str]:
    rows = await build_artefact_service().list_artefacts_for_student(
        db=db,
        student_id=STUDENT,
        limit=10,
        artefact_type=ArtefactType.POST_CLASS_REVIEW_PACK,
        review_status="approved",
    )
    return [row.artefact_id for row in rows]


async def _revise(db: AsyncSession, class_pack: Artefact) -> None:
    """A teacher's revision rewrites the class note in place: a new version, pending again."""
    class_pack.version += 1
    class_pack.review_status = ArtefactReviewStatus.PENDING
    await db.flush()


@pytest.mark.asyncio
async def test_a_note_is_released_while_its_class_version_stands_and_withheld_once_it_changes(
    db: AsyncSession,
) -> None:
    class_pack = await _lesson(db, PLAN, STUDENT)
    await _submit(db, PLAN, STUDENT)
    await _approve(db, class_pack)
    await _learner_note(db, class_pack, made_from_it=True)
    assert await _released(db) == ["AT-learner-cv"]

    await _revise(db, class_pack)
    assert await _released(db) == []

    await _approve(db, class_pack)
    assert await _released(db) == []


@pytest.mark.asyncio
async def test_a_learner_made_from_an_old_version_waits_for_a_note_from_the_new_one(
    db: AsyncSession,
) -> None:
    readiness = SqlAlchemyLearnerPackReadiness()
    class_pack = await _lesson(db, PLAN, STUDENT)
    await _submit(db, PLAN, STUDENT)
    await _approve(db, class_pack)
    await _learner_note(db, class_pack, made_from_it=True)
    assert await readiness.waiting_learners(db, PLAN) == []

    await _revise(db, class_pack)
    await _approve(db, class_pack)

    assert await readiness.waiting_learners(db, PLAN) == [STUDENT]


@pytest.mark.asyncio
async def test_a_note_that_records_no_source_is_released_as_it_always_was(
    db: AsyncSession,
) -> None:
    class_pack = await _lesson(db, PLAN, STUDENT)
    await _approve(db, class_pack)
    await _learner_note(db, class_pack, made_from_it=False)

    await _revise(db, class_pack)

    assert await _released(db) == ["AT-learner-cv"]


def test_a_learners_note_records_the_class_note_version_it_was_made_from() -> None:
    from types import SimpleNamespace

    from app.domains.artefacts.types.post_class_review_pack.application.grounding import Grounding
    from app.domains.artefacts.types.post_class_review_pack.application.student_pack_service import (  # noqa: E501
        StudentPackGenerationService,
    )
    from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import (
        ExpertSources,
    )

    service = StudentPackGenerationService(
        base_generator=object(),  # type: ignore[arg-type]
        learner_personaliser=object(),  # type: ignore[arg-type]
        lesson_notes=object(),  # type: ignore[arg-type]
    )
    generated = SimpleNamespace(validation=None, request=SimpleNamespace(units=[]))
    specification = SimpleNamespace(kind="post_class_review_pack", revision=1)

    refs = service._learner_refs(
        specification,  # type: ignore[arg-type]
        Grounding(ExpertSources.TEXTBOOK, None),
        generated,  # type: ignore[arg-type]
        SimpleNamespace(artefact_id="AT-class", version=3),  # type: ignore[arg-type]
    )

    assert refs["made_from"] == {"artefact_id": "AT-class", "version": 3}
    assert refs["review"]["checks"] == []
