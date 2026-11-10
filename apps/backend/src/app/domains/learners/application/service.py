from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.curriculum.domain.subject_offerings import validate_student_subject_profile
from app.domains.learners.infrastructure.repository import LearnerRepository
from app.domains.learners.models.learner import LearnerProfile
from app.domains.learners.schemas import LearnerCreateRequest, LearnerUpdateRequest
from app.shared.ids import PublicIdPrefix, new_public_id


# Not frozen: Python sets __traceback__ on an exception as it passes through a context manager.
@dataclass(eq=False)
class LearnerApplicationError(Exception):
    status_code: int
    detail: object


class LearnerApplicationService:
    def __init__(self, repository: LearnerRepository | None = None) -> None:
        self.repository = repository or LearnerRepository()

    async def create_learner(
        self,
        *,
        db: AsyncSession,
        payload: LearnerCreateRequest,
    ) -> LearnerProfile:
        existing_learner = await self.repository.get_learner_by_code(db, payload.code)
        if existing_learner is not None:
            raise LearnerApplicationError(409, "learner_code_exists")

        validation_errors = validate_student_subject_profile(
            field_of_study=payload.field_of_study,
            trade_subject=payload.trade_subject,
            field_core_subjects=payload.field_core_subjects,
        )
        if validation_errors:
            raise LearnerApplicationError(422, {"errors": validation_errors})

        learner = LearnerProfile(
            student_id=new_public_id(PublicIdPrefix.LEARNER),
            code=payload.code,
            full_name=payload.full_name,
            grade=payload.grade,
            track=payload.track,
            class_id=self._optional_uuid(payload.class_id),
            field_of_study=payload.field_of_study,
            trade_subject=payload.trade_subject,
            field_core_subjects=payload.field_core_subjects,
            language_level=payload.language_level,
            pace_preference=payload.pace_preference,
            time_budget_minutes=payload.time_budget_minutes,
        )
        try:
            return await self.repository.save_learner(db, learner)
        except IntegrityError as exc:
            # Concurrent create took the same code (unique) between check and
            # insert — surface the intended 409.
            await db.rollback()
            raise LearnerApplicationError(409, "learner_code_exists") from exc

    async def list_learners(
        self,
        *,
        db: AsyncSession,
        grade: str | None,
        track: str | None,
        class_id: str | None,
        field_of_study: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[tuple[LearnerProfile, str | None]], int]:
        return await self.repository.list_learners(
            db,
            grade=grade,
            track=track,
            # Coerce str → uuid.UUID before it reaches the UUID-column filter: a bare
            # str crashes on MySQL ('str' object has no attribute 'hex'), same class as
            # the create/update paths which already use _optional_uuid. 422 on bad input.
            class_id=self._optional_uuid(class_id),
            field_of_study=field_of_study,
            page=page,
            page_size=page_size,
        )

    async def get_learner(
        self,
        *,
        db: AsyncSession,
        learner_id: str,
    ) -> tuple[LearnerProfile, str | None]:
        learner_row = await self.repository.get_learner_by_id_or_code(db, learner_id)
        if learner_row is None:
            raise LearnerApplicationError(404, "learner_not_found")
        return learner_row

    async def update_learner(
        self,
        *,
        db: AsyncSession,
        learner_id: str,
        payload: LearnerUpdateRequest,
    ) -> LearnerProfile:
        learner = await self.repository.get_learner_by_id(db, learner_id)
        if learner is None:
            raise LearnerApplicationError(404, "learner_not_found")

        next_field_of_study = (
            payload.field_of_study if payload.field_of_study is not None else learner.field_of_study
        )
        next_trade_subject = (
            payload.trade_subject if payload.trade_subject is not None else learner.trade_subject
        )
        next_field_core_subjects = (
            payload.field_core_subjects
            if payload.field_core_subjects is not None
            else learner.field_core_subjects
        )
        validation_errors = validate_student_subject_profile(
            field_of_study=next_field_of_study,
            trade_subject=next_trade_subject,
            field_core_subjects=next_field_core_subjects,
        )
        if validation_errors:
            raise LearnerApplicationError(422, {"errors": validation_errors})

        if payload.full_name is not None:
            learner.full_name = payload.full_name
        if payload.code is not None:
            learner.code = payload.code
        if payload.grade is not None:
            learner.grade = payload.grade
        if payload.track is not None:
            learner.track = payload.track
        if payload.class_id is not None:
            learner.class_id = self._optional_uuid(payload.class_id)
        if payload.field_of_study is not None:
            learner.field_of_study = payload.field_of_study
        if payload.trade_subject is not None:
            learner.trade_subject = payload.trade_subject
        if payload.field_core_subjects is not None:
            learner.field_core_subjects = payload.field_core_subjects
        if payload.language_level is not None:
            learner.language_level = payload.language_level
        if payload.pace_preference is not None:
            learner.pace_preference = payload.pace_preference
        if payload.time_budget_minutes is not None:
            learner.time_budget_minutes = payload.time_budget_minutes

        return await self.repository.save_learner(db, learner)

    def _optional_uuid(self, value: str | None) -> uuid.UUID | None:
        if value is None:
            return None
        try:
            return uuid.UUID(value)
        except ValueError as exc:
            raise LearnerApplicationError(422, {"errors": ["class_id_invalid"]}) from exc
