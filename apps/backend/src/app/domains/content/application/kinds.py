"""How each content type is read and decided on: one registered handler per type.

Most content is an artefact row, approved through the artefact gate and revised in place.
The class test's questions live with grading, its conversation is keyed by its plan version,
and approving it sends it to students. A lesson plan lives in its own tables: approving it
freezes its latest version, and revising it adds a version.
"""

from __future__ import annotations

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.ports import Approval, ContentApprovals
from app.domains.content.application.errors import ContentError
from app.domains.content.application.records import (
    ClassTestQuestions,
    ContentRecord,
    ContentRecords,
)
from app.domains.content.application.review import Approver, ClassTestRelease
from app.domains.content.domain.types import Level
from app.shared.json_types import JsonObject

APPROVED = "approved"
REJECTED = "rejected"


class ContentKind(Protocol):
    """One content type's reading and decisions."""

    async def body(self, db: AsyncSession, record: ContentRecord) -> JsonObject: ...

    async def approve(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        approved_by: str,
    ) -> None: ...

    async def reject(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        rejected_by: str,
        reason: str,
    ) -> None:
        """Reject a pending version, or withdraw an approved one, or raise when that is refused."""
        ...

    async def approvals(self, db: AsyncSession, record: ContentRecord) -> list[Approval]: ...

    def revision_subject(self, record: ContentRecord) -> str:
        """What the revision conversation is keyed by."""
        ...

    def refuse_revision(self, record: ContentRecord) -> None:
        """Raise when the content can no longer be revised."""
        ...

    async def revised(self, db: AsyncSession, record: ContentRecord) -> None:
        """Whatever the revision conversation itself does not record."""
        ...


class ArtefactContent:
    """Content stored as an artefact: its manifest is its body, the artefact gate approves it."""

    def __init__(self, approver: Approver, approvals: ContentApprovals) -> None:
        self._approver = approver
        self._approvals = approvals

    async def body(self, db: AsyncSession, record: ContentRecord) -> JsonObject:
        return record.manifest

    async def approve(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        approved_by: str,
    ) -> None:
        await self._approver.approve(
            db,
            content_id=record.content_id,
            expected_version=expected_version,
            approved_by=approved_by,
        )

    async def reject(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        rejected_by: str,
        reason: str,
    ) -> None:
        await self._approver.reject(
            db,
            content_id=record.content_id,
            expected_version=expected_version,
            rejected_by=rejected_by,
            reason=reason,
        )

    async def approvals(self, db: AsyncSession, record: ContentRecord) -> list[Approval]:
        return await self._approvals.list_approvals(db, record.content_id)

    def revision_subject(self, record: ContentRecord) -> str:
        return record.content_id

    def refuse_revision(self, record: ContentRecord) -> None:
        return None

    async def revised(self, db: AsyncSession, record: ContentRecord) -> None:
        return None


class LearnerNotes(Protocol):
    """The learners' notes made from a lesson's class note."""

    async def withdraw_for(
        self, db: AsyncSession, plan_version_id: str, *, withdrawn_by: str, reason: str
    ) -> None: ...


class RevisionNoteContent(ArtefactContent):
    """The revision note: withdrawing the class note withdraws the learner notes made from it."""

    def __init__(
        self, approver: Approver, approvals: ContentApprovals, *, learner_notes: LearnerNotes
    ) -> None:
        super().__init__(approver, approvals)
        self._learner_notes = learner_notes

    async def reject(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        rejected_by: str,
        reason: str,
    ) -> None:
        was_approved = record.review_status == APPROVED
        await super().reject(
            db, record, expected_version=expected_version, rejected_by=rejected_by, reason=reason
        )
        if was_approved and record.level is Level.CLASS:
            await self._learner_notes.withdraw_for(
                db, record.plan_version_id, withdrawn_by=rejected_by, reason=reason
            )


class ClassTestContent(ArtefactContent):
    """The class test: questions from grading, sent to students once approved."""

    def __init__(
        self,
        approver: Approver,
        approvals: ContentApprovals,
        *,
        questions: ClassTestQuestions,
        release: ClassTestRelease,
        records: ContentRecords,
    ) -> None:
        super().__init__(approver, approvals)
        self._questions = questions
        self._release = release
        self._records = records

    async def body(self, db: AsyncSession, record: ContentRecord) -> JsonObject:
        return await self._questions.content(db, record.plan_version_id)

    async def approve(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        approved_by: str,
    ) -> None:
        await super().approve(
            db, record, expected_version=expected_version, approved_by=approved_by
        )
        await self._release.release(
            db, plan_version_id=record.plan_version_id, released_by=approved_by
        )

    async def reject(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        rejected_by: str,
        reason: str,
    ) -> None:
        if record.review_status == APPROVED:
            raise ContentError(409, "class_test_already_sent_to_students")
        await super().reject(
            db, record, expected_version=expected_version, rejected_by=rejected_by, reason=reason
        )

    def revision_subject(self, record: ContentRecord) -> str:
        return record.plan_version_id

    def refuse_revision(self, record: ContentRecord) -> None:
        if record.review_status == APPROVED:
            raise ContentError(409, "class_test_already_sent_to_students")

    async def revised(self, db: AsyncSession, record: ContentRecord) -> None:
        await self._records.mark_changed(db, record.content_id)


class LessonPlanVersions(Protocol):
    """A lesson plan's versions: freezing the latest, and the ones already frozen."""

    async def freeze(
        self, db: AsyncSession, record: ContentRecord, *, approved_by: str
    ) -> None: ...

    async def close(
        self, db: AsyncSession, record: ContentRecord, *, closed_by: str, reason: str
    ) -> None: ...

    async def frozen(self, db: AsyncSession, plan_id: str) -> list[Approval]: ...


class LessonPlanContent:
    """A lesson plan: its latest version is its body; approving freezes that version."""

    def __init__(self, versions: LessonPlanVersions) -> None:
        self._versions = versions

    async def body(self, db: AsyncSession, record: ContentRecord) -> JsonObject:
        return record.manifest

    async def approve(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        approved_by: str,
    ) -> None:
        if record.review_status == APPROVED:
            raise ContentError(409, "lesson_plan_already_approved")
        if record.review_status == REJECTED:
            raise ContentError(409, "a_closed_lesson_plan_cannot_be_approved")
        if expected_version is not None and expected_version != record.version:
            raise ContentError(409, "lesson_plan_changed_since_it_was_reviewed")
        await self._versions.freeze(db, record, approved_by=approved_by)

    async def reject(
        self,
        db: AsyncSession,
        record: ContentRecord,
        *,
        expected_version: int | None,
        rejected_by: str,
        reason: str,
    ) -> None:
        if expected_version is not None and expected_version != record.version:
            raise ContentError(409, "lesson_plan_changed_since_it_was_reviewed")
        await self._versions.close(db, record, closed_by=rejected_by, reason=reason)

    async def approvals(self, db: AsyncSession, record: ContentRecord) -> list[Approval]:
        return await self._versions.frozen(db, record.content_id)

    def revision_subject(self, record: ContentRecord) -> str:
        return record.content_id

    def refuse_revision(self, record: ContentRecord) -> None:
        return None

    async def revised(self, db: AsyncSession, record: ContentRecord) -> None:
        return None
