"""Which revision packs are the lesson's own, rather than an experiment's research outputs."""

from __future__ import annotations

from sqlalchemy import ColumnElement, Select, and_, exists, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact

#: The one experiment condition whose pack the lesson's teacher reviews. The other conditions'
#: packs, and the personalised packs an experiment run writes, are research outputs.
TEACHER_REVIEWED_CONDITION = "C4"


def _teacher_reviewed(artefact: type[Artefact]) -> ColumnElement[bool]:
    return artefact.condition_run.has(condition_code=TEACHER_REVIEWED_CONDITION)


def is_the_lessons_pack() -> ColumnElement[bool]:
    """A revision pack the lesson's teacher reviews and its learners may receive.

    For a lesson its experiment ran on, the class pack is the C4 run's; a class pack made
    outside the experiment for that lesson does not replace it. Otherwise the class pack is
    the one made for the lesson. A learner's pack is theirs unless an experiment run wrote it.
    """
    c4_pack = aliased(Artefact)
    lesson_has_c4_pack = exists().where(
        c4_pack.plan_version_id == Artefact.plan_version_id,
        c4_pack.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value,
        c4_pack.scope == ArtefactScope.CLASS_LEVEL.value,
        _teacher_reviewed(c4_pack),
    )
    return or_(
        _teacher_reviewed(Artefact),
        and_(
            Artefact.experiment_condition_run_id.is_(None),
            or_(Artefact.scope != ArtefactScope.CLASS_LEVEL.value, ~lesson_has_c4_pack),
        ),
    )


def _lessons_class_packs(plan_version_id: str, *, lock: bool) -> Select[tuple[Artefact]]:
    query = (
        select(Artefact)
        .where(Artefact.plan_version_id == plan_version_id)
        .where(Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value)
        .where(Artefact.scope == ArtefactScope.CLASS_LEVEL.value)
        .where(is_the_lessons_pack())
        .where(Artefact.review_status != ArtefactReviewStatus.REJECTED)
        .order_by(Artefact.created_at.desc(), Artefact.id.desc())
    )
    return query.with_for_update() if lock else query


async def the_lessons_class_pack(
    db: AsyncSession, plan_version_id: str, *, lock: bool = False
) -> Artefact | None:
    """The class pack the teacher reviews: the approved one, else the newest still pending.

    ``lock=True`` makes it a current (``FOR UPDATE``) read, for the re-check after the plan
    version's lock is held: under REPEATABLE READ a plain snapshot read would miss a pack a
    rival worker committed while this one waited, and the loser would make a duplicate.
    """
    packs = list((await db.execute(_lessons_class_packs(plan_version_id, lock=lock))).scalars())
    approved = [pack for pack in packs if pack.review_status == ArtefactReviewStatus.APPROVED]
    return next(iter(approved or packs), None)


async def the_lessons_approved_class_pack(
    db: AsyncSession, plan_version_id: str
) -> Artefact | None:
    """The class pack a learner's pack is made from: only one the teacher has approved."""
    query = _lessons_class_packs(plan_version_id, lock=False).where(
        Artefact.review_status == ArtefactReviewStatus.APPROVED
    )
    return (await db.execute(query.limit(1))).scalars().first()
