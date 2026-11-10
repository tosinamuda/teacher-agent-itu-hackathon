"""The lesson-plan side of a drafted plan: the lesson, its checks, and saving the plan.

A plan written from a document or from the curriculum is saved exactly as a teacher's own plan
is, so it passes the same checks and becomes a draft the teacher approves. A plan the app
writes from the curriculum is also held to the lesson-plan spec's requirements.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.application.errors import PlanValidationError
from app.domains.artefacts.types.lesson_plan.application.manual_check import check_manual_plan
from app.domains.artefacts.types.lesson_plan.application.payload_builder import (
    SessionContextPayloadBuilder,
)
from app.domains.artefacts.types.lesson_plan.deps import lesson_plan_service
from app.domains.artefacts.types.lesson_plan.domain.plan_sections import (
    carry_figures,
    split_plan,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    normalize_session_plan_payload,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import (
    build_session_context,
    get_plan_row,
    persist_revised_plan_version,
)
from app.domains.content_engine.application.planning_ports import (
    PlanLesson,
    PlanRecord,
    PlanRefusedError,
)
from app.domains.content_engine.infrastructure.plan_grounding import grounding_of
from app.shared.json_types import JsonObject


class LessonPlanning:
    async def lesson(self, db: AsyncSession, session_id: str) -> PlanLesson | None:
        context = await build_session_context(db, session_id)
        if context is None:
            return None
        payloads = SessionContextPayloadBuilder().build(context)
        return PlanLesson(
            session_id=session_id,
            facts={
                "subject": context.subject,
                "grade": context.grade,
                "term": context.term,
                "week": context.week,
                "topic": context.topic,
                "subtopic": context.subtopic,
                "duration_minutes": context.duration_minutes,
            },
            curriculum_objectives=list(payloads.curriculum_scope.curriculum_objectives),
            grounding=grounding_of(payloads),
        )

    async def current(self, db: AsyncSession, plan_id: str) -> PlanRecord | None:
        row = await get_plan_row(db, plan_or_version_id=plan_id)
        if row is None or row[1].lesson_period_id is None:
            return None
        version, plan = row
        lesson, sections = split_plan(normalize_session_plan_payload(version.session_plan or {}))
        return PlanRecord(
            plan_id=plan.plan_id,
            session_id=str(plan.lesson_period_id),
            version_id=version.version_id,
            lesson=lesson,
            sections=sections,
            concluded=version.concluded_at is not None,
        )

    async def issues(
        self, db: AsyncSession, session_id: str, content: JsonObject, *, strict: bool
    ) -> JsonObject:
        context = await build_session_context(db, session_id)
        if context is None:
            return {"lesson": f"there is no lesson {session_id}"}
        return check_manual_plan(context, content, strict=strict).issues

    async def save(
        self,
        db: AsyncSession,
        session_id: str,
        content: JsonObject,
        author: str | None,
        *,
        source_type: str,
        generator: JsonObject,
    ) -> str:
        try:
            saved = await lesson_plan_service(db).create_manual(
                session_id=session_id,
                session_plan_content=content,
                teacher_id=author,
                source_type=source_type,
                generator=generator,
            )
        except PlanValidationError as error:
            detail = error.detail
            issues: JsonObject = (
                {str(check): found for check, found in detail.items()}
                if isinstance(detail, dict)
                else {"plan": str(detail)}
            )
            raise PlanRefusedError(issues) from error
        return saved.version_id

    async def revise(
        self,
        db: AsyncSession,
        plan_id: str,
        session_id: str,
        content: JsonObject,
        *,
        generator: JsonObject,
    ) -> str:
        context = await build_session_context(db, session_id)
        row = await get_plan_row(db, plan_or_version_id=plan_id)
        if context is None or row is None:
            raise PlanRefusedError({"plan": f"there is no plan {plan_id}"})
        version = row[0]
        saved = normalize_session_plan_payload(version.session_plan or {})
        checked = check_manual_plan(context, carry_figures(saved, content), strict=True)
        if checked.issues:
            raise PlanRefusedError(checked.issues)
        if split_plan(saved) == split_plan(checked.session_plan):
            return version.version_id
        revised = await persist_revised_plan_version(
            db,
            plan_id=plan_id,
            revised_session_plan=checked.session_plan,
            parent_version_id=version.version_id,
            run_metadata={"revised_by": "engine", "generator": generator},
        )
        return revised.version_id
