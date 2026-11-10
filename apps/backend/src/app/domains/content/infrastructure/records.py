"""Content read from where each type is stored, and a class test's questions from its items."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import ColumnElement, Select, and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.concluded_record import is_concluded
from app.domains.artefact_revision.application.diagnostic_executor import (
    build_diagnostic_payload,
)
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    is_the_lessons_pack,
    the_lessons_class_pack,
)
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.content.application.records import ContentRecord
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.lesson_plans import LessonPlanRecords
from app.domains.content.infrastructure.models import ContentTypeRecord
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.experiments.domain.types import ExperimentLifecycleStatus
from app.domains.experiments.infrastructure.models import Experiment
from app.shared.json_types import JsonObject

_PROVENANCE_KEYS = ("origin", "specification", "pipeline", "generator")
_REVISION_PACK = ArtefactType.POST_CLASS_REVIEW_PACK.value


def _is_the_lessons_content() -> ColumnElement[bool]:
    """Made for the lesson, not by an experiment's research runs."""
    return or_(
        and_(Artefact.artefact_type == _REVISION_PACK, is_the_lessons_pack()),
        and_(
            Artefact.artefact_type != _REVISION_PACK,
            Artefact.experiment_condition_run_id.is_(None),
        ),
    )


def _review_of(refs: JsonObject) -> JsonObject | None:
    review = refs.get("review")
    return review if isinstance(review, dict) else None


def _record(artefact: Artefact, concluded_at: datetime | None, slug: str) -> ContentRecord:
    refs = artefact.artefact_refs or {}
    return ContentRecord(
        content_id=artefact.artefact_id,
        type=slug,
        kind=artefact.artefact_type,
        level=Level.of(artefact.scope),
        plan_version_id=artefact.plan_version_id,
        student_id=artefact.student_id,
        version=artefact.version,
        review_status=ArtefactReviewStatus(artefact.review_status).value,
        created_at=artefact.created_at,
        provenance={key: refs[key] for key in _PROVENANCE_KEYS if key in refs},
        manifest=artefact.manifest or {},
        read_only=concluded_at is not None,
        review_reason=artefact.review_reason,
        review=_review_of(refs),
    )


def _content_rows() -> Select[tuple[Artefact, datetime | None, str]]:
    """Artefact rows of a registered type: nothing else in the table is content."""
    return (
        select(Artefact, PlanVersion.concluded_at, ContentTypeRecord.slug)
        .join(ContentTypeRecord, ContentTypeRecord.kind == Artefact.artefact_type)
        .outerjoin(PlanVersion, PlanVersion.version_id == Artefact.plan_version_id)
        .where(ContentTypeRecord.slug != BuiltIn.LESSON_PLAN.value)
        .where(_is_the_lessons_content())
    )


class _ArtefactRecords:
    """The content stored as artefact rows."""

    async def get(self, db: AsyncSession, content_id: str) -> ContentRecord | None:
        row = (
            await db.execute(_content_rows().where(Artefact.artefact_id == content_id))
        ).one_or_none()
        return _record(*row) if row is not None else None

    async def find(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str | None,
        type: str | None,
        level: Level | None,
        student_id: str | None,
    ) -> list[ContentRecord]:
        query = _content_rows()
        if type is not None:
            query = query.where(ContentTypeRecord.slug == type)
        if plan_version_id is not None:
            query = query.where(Artefact.plan_version_id == plan_version_id)
        if level is not None:
            query = query.where(Artefact.scope == level.stored_as.value)
        if student_id is not None:
            query = query.where(Artefact.student_id == student_id)
        rows = await db.execute(query.order_by(Artefact.created_at.desc(), Artefact.id.desc()))
        return [_record(*row) for row in rows.all()]

    async def mark_changed(self, db: AsyncSession, content_id: str) -> None:
        artefact = (
            await db.execute(
                select(Artefact).where(Artefact.artefact_id == content_id).with_for_update()
            )
        ).scalar_one()
        artefact.version = artefact.version + 1
        artefact.review_status = ArtefactReviewStatus.PENDING
        await db.commit()

    async def record_generator(
        self, db: AsyncSession, content_id: str, generator: JsonObject
    ) -> None:
        artefact = (
            await db.execute(
                select(Artefact).where(Artefact.artefact_id == content_id).with_for_update()
            )
        ).scalar_one_or_none()
        if artefact is None or "generator" in (artefact.artefact_refs or {}):
            return
        artefact.artefact_refs = {**(artefact.artefact_refs or {}), "generator": generator}
        await db.commit()


class SqlAlchemyContentRecords:
    """Every content type, wherever it is stored."""

    def __init__(self) -> None:
        self._artefacts = _ArtefactRecords()
        self._plans = LessonPlanRecords()

    async def get(self, db: AsyncSession, content_id: str) -> ContentRecord | None:
        found = await self._artefacts.get(db, content_id)
        return found if found is not None else await self._plans.get(db, content_id)

    async def find(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str | None,
        type: str | None,
        level: Level | None,
        student_id: str | None,
    ) -> list[ContentRecord]:
        found: list[ContentRecord] = []
        if type != BuiltIn.LESSON_PLAN.value:
            found += await self._artefacts.find(
                db, plan_version_id=plan_version_id, type=type, level=level, student_id=student_id
            )
        if (
            type in (None, BuiltIn.LESSON_PLAN.value)
            and level in (None, Level.CLASS)
            and not student_id
        ):
            found += await self._plans.find(db, plan_version_id=plan_version_id)
        return sorted(found, key=_newest_first)

    async def mark_changed(self, db: AsyncSession, content_id: str) -> None:
        await self._artefacts.mark_changed(db, content_id)

    async def record_generator(
        self, db: AsyncSession, content_id: str, generator: JsonObject
    ) -> None:
        await self._artefacts.record_generator(db, content_id, generator)

    async def concluded(self, db: AsyncSession, plan_version_id: str) -> bool:
        return await is_concluded(db, plan_version_id)

    async def plan_refusal(self, db: AsyncSession, plan_version_id: str) -> str | None:
        version = (
            await db.execute(select(PlanVersion).where(PlanVersion.version_id == plan_version_id))
        ).scalar_one_or_none()
        if version is None:
            return None
        if version.status != PlanVersionStatus.APPROVED:
            return "lesson_plan_not_approved"
        newer = await db.scalar(
            select(PlanVersion.id)
            .where(PlanVersion.plan_id == version.plan_id)
            .where(PlanVersion.status == PlanVersionStatus.APPROVED)
            .where(PlanVersion.created_at > version.created_at)
            .limit(1)
        )
        return "a_newer_plan_version_is_approved" if newer is not None else None

    async def class_pack_awaits_its_experiment(
        self, db: AsyncSession, plan_version_id: str
    ) -> bool:
        running = await db.scalar(
            select(Experiment.id)
            .where(Experiment.plan_version_id == plan_version_id)
            .where(Experiment.lifecycle_status != ExperimentLifecycleStatus.ENDED)
            .limit(1)
        )
        return running is not None and await the_lessons_class_pack(db, plan_version_id) is None

    async def has_class_revision_note(self, db: AsyncSession, plan_version_id: str) -> bool:
        return await the_lessons_class_pack(db, plan_version_id) is not None

    async def class_test_answered(self, db: AsyncSession, plan_version_id: str) -> bool:
        answered = await db.scalar(
            select(StudentItemResponse.id)
            .join(ExitTicketItem, ExitTicketItem.id == StudentItemResponse.item_id)
            .where(ExitTicketItem.plan_version_id == plan_version_id)
            .limit(1)
        )
        return answered is not None


def _newest_first(record: ContentRecord) -> tuple[bool, float]:
    created = record.created_at.timestamp() if record.created_at is not None else 0.0
    return (record.created_at is None, -created)


class ClassTestItems:
    """A class test's questions, as the revision conversation already assembles them."""

    async def content(self, db: AsyncSession, plan_version_id: str) -> JsonObject:
        return await build_diagnostic_payload(db, plan_version_id)
