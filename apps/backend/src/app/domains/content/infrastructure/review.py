"""The approval gate, the class test's release, and the revision conversation, as adapters."""

from __future__ import annotations

from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.executor import RevisionExecutor
from app.domains.artefact_revision.application.service import (
    ArtefactRevisionService,
    ChatRecord,
    RevisionRecord,
)
from app.domains.artefacts.core.application.build_jobs import ArtefactLifecycleError
from app.domains.artefacts.core.application.service import ArtefactApplicationError
from app.domains.artefacts.core.infrastructure.wiring import build_lifecycle_manager
from app.domains.assessments.application.service import (
    AssessmentApplicationError,
    AssessmentApplicationService,
)
from app.domains.content.application.errors import ContentError
from app.shared.json_types import JsonObject


class LifecycleApprover:
    """The artefact core's approval: a version check, then a kept approval."""

    async def approve(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        expected_version: int | None,
        approved_by: str | None,
    ) -> None:
        try:
            await build_lifecycle_manager().approve_artefact(
                db=db,
                artefact_id=content_id,
                reviewed_by=approved_by,
                expected_version=expected_version,
            )
        except (ArtefactLifecycleError, ArtefactApplicationError) as error:
            raise ContentError(error.status_code, error.detail) from error

    async def reject(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        expected_version: int | None,
        rejected_by: str | None,
        reason: str,
    ) -> None:
        try:
            await build_lifecycle_manager().reject_artefact(
                db=db,
                artefact_id=content_id,
                reviewed_by=rejected_by,
                reason=reason,
                expected_version=expected_version,
            )
        except (ArtefactLifecycleError, ArtefactApplicationError) as error:
            raise ContentError(error.status_code, error.detail) from error


class AssessmentRelease:
    """Sends the class test to its students, as the assessment workflow always has."""

    async def release(self, db: AsyncSession, *, plan_version_id: str, released_by: str) -> None:
        try:
            await AssessmentApplicationService().release_assessment(
                db=db, plan_version_id=plan_version_id, released_by=released_by
            )
        except AssessmentApplicationError as error:
            raise ContentError(error.status_code, error.detail) from error


class RevisionConversation:
    """The existing revision conversation; building it opens the executors' models.

    ``engine_executor`` builds the executor that revises content the engine built, and
    ``plan_executor`` the one that revises a lesson plan.
    """

    def __init__(
        self,
        engine_executor: Callable[[], RevisionExecutor],
        plan_executor: Callable[[], RevisionExecutor],
    ) -> None:
        self._engine_executor = engine_executor
        self._plan_executor = plan_executor

    def _service(self) -> ArtefactRevisionService:
        from app.domains.artefact_revision.infrastructure.wiring import (
            build_artefact_revision_service,
        )

        return build_artefact_revision_service(
            fallback=self._engine_executor(), plans=self._plan_executor()
        )

    async def revise(
        self,
        db: AsyncSession,
        *,
        stored_type: str,
        subject_id: str,
        feedback: str,
        requested_by: str | None,
        highlight: JsonObject | None = None,
        chat_id: str | None = None,
    ) -> RevisionRecord:
        service = self._service()
        try:
            thread_id = (
                (
                    await service.chat_of(
                        db=db, artefact_type=stored_type, subject_id=subject_id, chat_id=chat_id
                    )
                ).chat_id
                if chat_id is not None
                else (
                    await service.get_or_create_thread(
                        db=db,
                        artefact_type=stored_type,
                        subject_id=subject_id,
                        created_by=requested_by,
                    )
                ).revision_thread_id
            )
            turn, _outcome = await service.submit_turn(
                db=db,
                thread_id=thread_id,
                instruction=feedback,
                highlight=highlight,
            )
        except ArtefactRevisionError as error:
            raise ContentError(error.status_code, error.detail) from error
        return RevisionRecord(
            turn_number=turn.turn_number,
            instruction=turn.instruction,
            summary=turn.summary,
            result_version_id=turn.result_version_id,
            created_at=turn.created_at,
            highlight=turn.highlight,
        )

    async def history(
        self, db: AsyncSession, *, stored_type: str, subject_id: str
    ) -> list[RevisionRecord]:
        from app.domains.artefact_revision.application.service import ArtefactRevisionService

        # Reading history needs no executor, so no model is opened for it.
        return await ArtefactRevisionService(()).history(
            db=db, artefact_type=stored_type, subject_id=subject_id
        )

    async def chats(
        self, db: AsyncSession, *, stored_type: str, subject_id: str
    ) -> list[ChatRecord]:
        # Reading chats needs no executor, so no model is opened for it.
        return await ArtefactRevisionService(()).chats(
            db=db, artefact_type=stored_type, subject_id=subject_id
        )

    async def new_chat(
        self,
        db: AsyncSession,
        *,
        stored_type: str,
        subject_id: str,
        requested_by: str | None,
        title: str | None,
    ) -> ChatRecord:
        service = self._service()
        try:
            return await service.create_chat(
                db=db,
                artefact_type=stored_type,
                subject_id=subject_id,
                created_by=requested_by,
                title=title,
            )
        except ArtefactRevisionError as error:
            raise ContentError(error.status_code, error.detail) from error

    async def chat(
        self, db: AsyncSession, *, stored_type: str, subject_id: str, chat_id: str
    ) -> ChatRecord:
        try:
            return await ArtefactRevisionService(()).chat_of(
                db=db, artefact_type=stored_type, subject_id=subject_id, chat_id=chat_id
            )
        except ArtefactRevisionError as error:
            raise ContentError(error.status_code, error.detail) from error
