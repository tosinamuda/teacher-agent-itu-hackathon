"""The learner-pack gate's facts, read from the lesson's packs and the learners' submissions."""

from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.made_from import made_from_of
from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_approved_class_pack,
)
from app.domains.assessments.models import ExitTicketSubmission


def _complete_submissions(plan_version_id: str) -> Select[tuple[str]]:
    return select(ExitTicketSubmission.student_id).where(
        ExitTicketSubmission.plan_version_id == plan_version_id,
        ExitTicketSubmission.survey_pending.is_(False),
    )


class SqlAlchemyLearnerPackReadiness:
    """Whether the class pack is approved, whose evidence is complete, and who is waiting."""

    async def class_pack_approved(self, db: AsyncSession, plan_version_id: str) -> bool:
        return await the_lessons_approved_class_pack(db, plan_version_id) is not None

    async def evidence_complete(
        self, db: AsyncSession, *, student_id: str, plan_version_id: str
    ) -> bool:
        query = _complete_submissions(plan_version_id).where(
            ExitTicketSubmission.student_id == student_id
        )
        return (await db.execute(query.limit(1))).first() is not None

    async def waiting_learners(self, db: AsyncSession, plan_version_id: str) -> list[str]:
        """Learners with complete evidence and no pack made from the class note's version."""
        class_pack = await the_lessons_approved_class_pack(db, plan_version_id)
        current = (class_pack.artefact_id, class_pack.version) if class_pack else None
        packs = await db.execute(
            select(Artefact.student_id, Artefact.artefact_refs).where(
                Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value,
                Artefact.scope == ArtefactScope.LEARNER_LEVEL.value,
                Artefact.plan_version_id == plan_version_id,
            )
        )
        served = {
            student
            for student, refs in packs.all()
            if (m := made_from_of(refs)) is None or m == current
        }
        submitted = (await db.execute(_complete_submissions(plan_version_id))).scalars()
        return sorted(set(submitted) - served)
