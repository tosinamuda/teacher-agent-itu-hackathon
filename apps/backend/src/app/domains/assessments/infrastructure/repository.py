from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.curriculum.models.knowledge_components import KnowledgeComponent
from app.domains.learners.models import LearnerProfile
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject

_SUBTOPIC_SQL = text(
    """
    select lp.subtopic_id as subtopic_id
    from plan_versions pv
    join lesson_plans lpn on lpn.plan_id = pv.plan_id
    join lesson_periods lp on lp.id = lpn.lesson_period_id
    where pv.version_id = :version_id
    """
)


class AssessmentRepository:
    async def get_exit_ticket_items(
        self,
        db: AsyncSession,
        plan_version_id: str,
    ) -> list[ExitTicketItem]:
        result = await db.execute(
            select(ExitTicketItem)
            .filter(ExitTicketItem.plan_version_id == plan_version_id)
            .order_by(
                ExitTicketItem.lesson_objective_id,
                ExitTicketItem.created_at,
                ExitTicketItem.id,
            )
        )
        return list(result.scalars().all())

    async def item_counts_by_objective(
        self,
        db: AsyncSession,
        plan_version_id: str,
    ) -> dict[str | None, int]:
        """How many exit-ticket items each objective has (drives the coverage report)."""
        result = await db.execute(
            select(ExitTicketItem.lesson_objective_id, func.count())
            .where(ExitTicketItem.plan_version_id == plan_version_id)
            .group_by(ExitTicketItem.lesson_objective_id)
        )
        return {row[0]: int(row[1]) for row in result.all()}

    async def has_student_responses(self, db: AsyncSession, plan_version_id: str) -> bool:
        """True if any student has answered this plan's items (blocks destructive re-entry)."""
        count = await db.scalar(
            select(func.count())
            .select_from(StudentItemResponse)
            .join(ExitTicketItem, ExitTicketItem.id == StudentItemResponse.item_id)
            .where(ExitTicketItem.plan_version_id == plan_version_id)
        )
        return bool(count)

    async def resolve_subtopic_id(self, db: AsyncSession, plan_version_id: str) -> str | None:
        """The lesson's subtopic_id for a plan version (the exit-ticket FK), or None."""
        row = (await db.execute(_SUBTOPIC_SQL, {"version_id": plan_version_id})).first()
        return row[0] if row else None

    async def list_knowledge_components(
        self,
        db: AsyncSession,
        subtopic_id: str,
    ) -> list[KnowledgeComponent]:
        """Knowledge components for a subtopic (the optional per-item KC tag options)."""
        result = await db.execute(
            select(KnowledgeComponent)
            .where(KnowledgeComponent.subtopic_id == subtopic_id)
            .order_by(KnowledgeComponent.kc_code)
        )
        return list(result.scalars().all())

    async def plan_versions_with_items(
        self,
        db: AsyncSession,
        plan_version_ids: Sequence[str],
    ) -> set[str]:
        """One query: which of the given plan_versions already have an assessment."""
        if not plan_version_ids:
            return set()
        result = await db.execute(
            select(ExitTicketItem.plan_version_id)
            .where(ExitTicketItem.plan_version_id.in_(plan_version_ids))
            .distinct()
        )
        return set(result.scalars().all())

    async def released_plan_versions(
        self,
        db: AsyncSession,
        plan_version_ids: Sequence[str],
    ) -> set[str]:
        """One query: which of the given plan_versions have their assessment released."""
        if not plan_version_ids:
            return set()
        result = await db.execute(
            select(PlanVersion.version_id).where(
                PlanVersion.version_id.in_(plan_version_ids),
                PlanVersion.assessment_released_at.is_not(None),
            )
        )
        return set(result.scalars().all())

    async def is_assessment_released(self, db: AsyncSession, plan_version_id: str) -> bool:
        """Whether the teacher has released this lesson's assessment to students."""
        result = await db.execute(
            select(PlanVersion.assessment_released_at).where(
                PlanVersion.version_id == plan_version_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def set_assessment_released(
        self, db: AsyncSession, *, plan_version_id: str, released_by: str | None
    ) -> bool:
        """Mark the assessment released. Returns False if the plan version is unknown."""
        plan_version = (
            await db.execute(select(PlanVersion).where(PlanVersion.version_id == plan_version_id))
        ).scalar_one_or_none()
        if plan_version is None:
            return False
        from datetime import datetime, timezone

        plan_version.assessment_released_at = datetime.now(timezone.utc)
        plan_version.assessment_released_by = released_by
        await db.commit()
        return True

    async def get_student(
        self,
        db: AsyncSession,
        student_id: str,
    ) -> LearnerProfile | None:
        result = await db.execute(
            select(LearnerProfile).filter(LearnerProfile.student_id == student_id)
        )
        return result.scalars().first()

    async def get_plan_version(
        self,
        db: AsyncSession,
        plan_version_id: str,
    ) -> PlanVersion | None:
        result = await db.execute(
            select(PlanVersion).filter(PlanVersion.version_id == plan_version_id)
        )
        return result.scalars().first()

    async def get_submission_by_diagnostic_id(
        self,
        db: AsyncSession,
        diagnostic_id: str,
    ) -> ExitTicketSubmission | None:
        result = await db.execute(
            select(ExitTicketSubmission).filter(ExitTicketSubmission.diagnostic_id == diagnostic_id)
        )
        return result.scalars().first()

    async def get_submission_by_diagnostic_id_for_update(
        self,
        db: AsyncSession,
        diagnostic_id: str,
    ) -> ExitTicketSubmission | None:
        """Row-lock + return the submission, to serialize survey-attach writes to results JSON.

        attach_exit_assessment_survey does a read-modify-write on the ``results`` JSON; two
        concurrent attaches off the same snapshot would lose one survey. FOR UPDATE (+
        populate_existing to refresh a cached row) makes the second attach build on the first's
        committed survey rather than clobber it.
        """
        result = await db.execute(
            select(ExitTicketSubmission)
            .filter(ExitTicketSubmission.diagnostic_id == diagnostic_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return result.scalars().first()

    async def submission_exists_for_student_plan(
        self,
        db: AsyncSession,
        *,
        student_id: str,
        plan_version_id: str,
    ) -> bool:
        """True if this learner already has a submission for this lesson (one per pair)."""
        result = await db.execute(
            select(ExitTicketSubmission.id)
            .filter(
                ExitTicketSubmission.student_id == student_id,
                ExitTicketSubmission.plan_version_id == plan_version_id,
            )
            .limit(1)
        )
        return result.scalars().first() is not None

    async def submitted_student_ids(self, db: AsyncSession, plan_version_id: str) -> set[str]:
        """Students who already have a submission for this lesson (on-behalf skip set)."""
        result = await db.execute(
            select(ExitTicketSubmission.student_id)
            .where(ExitTicketSubmission.plan_version_id == plan_version_id)
            .distinct()
        )
        return set(result.scalars().all())

    async def list_submissions_for_student(
        self,
        db: AsyncSession,
        student_id: str,
    ) -> list[ExitTicketSubmission]:
        result = await db.execute(
            select(ExitTicketSubmission)
            .filter(ExitTicketSubmission.student_id == student_id)
            .order_by(ExitTicketSubmission.created_at.desc())
        )
        return list(result.scalars().all())

    async def save_submission(
        self,
        db: AsyncSession,
        submission: ExitTicketSubmission,
    ) -> ExitTicketSubmission:
        db.add(submission)
        await db.commit()
        await db.refresh(submission)
        return submission


class ClassTestMaterials:
    """The class test's material record: one per plan version, its content read from the items.

    The items in ``exit_ticket_items`` stay the only copy of the questions, because grading
    and students' answers depend on them. The record is what the materials API, the approval
    log and the revision history address.
    """

    async def ensure(self, db: AsyncSession, *, plan_version_id: str, source: str) -> Artefact:
        """Create the record, or mark a changed set of questions as a new version of it.

        Joins the caller's transaction; the caller commits it with the items.
        """
        released = (
            await db.execute(
                select(PlanVersion.assessment_released_at).where(
                    PlanVersion.version_id == plan_version_id
                )
            )
        ).scalar_one_or_none() is not None
        status = ArtefactReviewStatus.APPROVED if released else ArtefactReviewStatus.PENDING
        record = (
            await db.execute(
                select(Artefact)
                .where(Artefact.artefact_type == ArtefactType.DIAGNOSTIC.value)
                .where(Artefact.plan_version_id == plan_version_id)
                .with_for_update()
            )
        ).scalar_one_or_none()
        manifest: JsonObject = {"plan_version_id": plan_version_id, "source": source}
        if record is None:
            record = Artefact(
                artefact_id=new_public_id(PublicIdPrefix.ARTEFACT),
                artefact_type=ArtefactType.DIAGNOSTIC.value,
                scope=ArtefactScope.CLASS_LEVEL.value,
                plan_version_id=plan_version_id,
                manifest=manifest,
                review_status=status,
            )
            db.add(record)
            return record
        record.manifest = manifest
        record.review_status = status
        record.version = record.version + 1
        return record
