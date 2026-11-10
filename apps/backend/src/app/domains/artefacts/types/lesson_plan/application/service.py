from __future__ import annotations

import logging
import uuid
from collections.abc import Mapping
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.domain.specification import specification_ref
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.types.lesson_plan.api.schemas import (
    ManualCurriculumObjective,
    ManualPlanContextResponse,
    PlanApproveResponse,
    PlanGenerateRequest,
    PlanGenerateResponse,
    PlanVersionSummary,
)
from app.domains.artefacts.types.lesson_plan.application.errors import (
    GenerationFailedError,
    PlanLookupNotFoundError,
    PlanNotOwnedByTeacherError,
    PlanValidationError,
    PlanVersionNotFoundError,
    SessionNotFoundError,
)
from app.domains.artefacts.types.lesson_plan.application.manual_check import check_manual_plan
from app.domains.artefacts.types.lesson_plan.application.payload_builder import (
    SessionContextPayloadBuilder,
)
from app.domains.artefacts.types.lesson_plan.application.plan_reuse import (
    ReusedPlan,
    ReuseSource,
    canonical_content,
    map_curriculum,
)
from app.domains.artefacts.types.lesson_plan.application.ports import (
    LessonPlanGeneratorPort,
    SessionPlanValidatorPort,
)
from app.domains.artefacts.types.lesson_plan.domain.lesson_document import as_document, violations
from app.domains.artefacts.types.lesson_plan.domain.plan_requirements import unmet
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    GeneratedLessonPlan,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    normalize_session_plan_payload,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    READING_A_STORED_PLAN,
    SessionPlan,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import (
    approve_plan_version,
    build_session_context,
    get_plan_row,
    latest_compiled_artefact_id,
    latest_compiled_artefact_ids,
    list_plan_version_rows,
    persist_plan_version,
    persist_revised_plan_version,
)
from app.domains.generation_log.application.recorder import log_context
from app.shared.json_types import JsonObject
from app.shared.readers import reader_for

logger = logging.getLogger(__name__)


class DiagnosticGenerator(Protocol):
    """Generates a plan version's class test."""

    async def generate_for_plan(self, *, db: AsyncSession, plan_version_id: str) -> int: ...


class LessonPlanApplicationService:
    def __init__(
        self,
        *,
        db: AsyncSession,
        generator: LessonPlanGeneratorPort,
        validator: SessionPlanValidatorPort,
        specifications: ContentSpecifications,
        diagnostic_service: DiagnosticGenerator | None = None,
    ) -> None:
        self._db = db
        self._generator = generator
        self._validator = validator
        self._specifications = specifications
        self._diagnostic_service = diagnostic_service
        self._payload_builder = SessionContextPayloadBuilder()

    async def approve(
        self,
        *,
        version_id: str,
        approved_by: str | None,
        owner_teacher_id: uuid.UUID | None = None,
        auto_generate_diagnostic: bool = True,
    ) -> PlanApproveResponse:
        """Freeze a plan version.

        If ``owner_teacher_id`` is given (the caller is a teacher) they must own
        the plan's class + subject + term; a research-manager passes None.

        ``auto_generate_diagnostic`` (default True for production) best-effort
        generates the exit assessment on approval. The experiment lesson-prep
        flow passes False so "Create the assessment" is an explicit teacher step.
        """
        if owner_teacher_id is not None:
            from app.domains.artefacts.types.lesson_plan.application.ownership import (
                teacher_owns_plan_version,
            )

            owns = await teacher_owns_plan_version(
                self._db, teacher_id=owner_teacher_id, plan_version_id=version_id
            )
            if not owns:
                raise PlanNotOwnedByTeacherError(version_id)
        plan_version = await approve_plan_version(
            self._db,
            version_id=version_id,
            approved_by=approved_by,
        )
        if plan_version is None:
            raise PlanVersionNotFoundError(version_id)
        if auto_generate_diagnostic:
            await self._auto_generate_diagnostic(plan_version.version_id)
        return PlanApproveResponse(
            plan_id=plan_version.plan_id,
            version_id=plan_version.version_id,
            status=plan_version.status,
            approved_at=plan_version.approved_at,
            approved_by=plan_version.approved_by,
        )

    async def _auto_generate_diagnostic(self, plan_version_id: str) -> None:
        """Best-effort: generate the class test on approval, before students take it.

        Never blocks approval.
        """
        if self._diagnostic_service is None:
            return
        try:
            await self._diagnostic_service.generate_for_plan(
                db=self._db, plan_version_id=plan_version_id
            )
        except Exception:  # noqa: BLE001 - diagnostic generation is best-effort
            logging.getLogger(__name__).warning(
                "diagnostic auto-generation failed for %s", plan_version_id, exc_info=True
            )

    async def has_session(self, session_id: str) -> bool:
        """Whether there is a lesson to draft a plan for."""
        return await build_session_context(self._db, session_id) is not None

    async def generate(
        self, payload: PlanGenerateRequest, *, source_type: str = "generated"
    ) -> PlanGenerateResponse:
        session_context = await build_session_context(self._db, payload.session_id)
        if session_context is None:
            raise SessionNotFoundError(payload.session_id)

        generation_payloads = self._payload_builder.build(session_context)
        specification = await self._specifications.current(self._db, ArtefactType.LESSON_PLAN.value)

        try:
            with log_context(
                kind="lesson_plan",
                correlation_id=session_context.session_id,
                session_id=session_context.session_id,
                subject=session_context.subject,
                topic=session_context.topic,
                grounding_mode=generation_payloads.grounding_mode,
            ):
                generation = await self._generator.generate(
                    session_context=generation_payloads.session_scope.model_dump(mode="json"),
                    curriculum_context=generation_payloads.curriculum_scope.model_dump(mode="json"),
                    reference_context=generation_payloads.reference_context,
                    evidence_selection_strategy=payload.evidence_selection_strategy,
                    grounding_mode=generation_payloads.grounding_mode,
                    curated_objectives=generation_payloads.curated_objectives,
                    brief=specification.brief(reader_for(session_context.grade or "")),
                )
            generation.run_metadata.update(specification_ref(specification))
        except ValueError as exc:
            logger.exception(
                "Plan generation validation error",
                extra={"session_id": session_context.session_id},
            )
            raise PlanValidationError(str(exc)) from exc
        except Exception as exc:  # pragma: no cover - safety guard
            logger.exception(
                "Plan generation failed",
                extra={"session_id": session_context.session_id},
            )
            raise GenerationFailedError from exc

        validation_result = self._validator.validate(
            generation.session_plan,
            generation_payloads.validation_scope.model_dump(mode="json"),
        )
        if validation_result.schema_errors:
            raise PlanValidationError({"errors": validation_result.schema_errors})
        if validation_result.context_errors:
            raise PlanValidationError({"context_errors": validation_result.context_errors})

        plan_version = await persist_plan_version(
            self._db,
            session_context,
            generation,
            created_by=payload.teacher_id,
            source_type=source_type,
        )
        return PlanGenerateResponse(
            plan_id=plan_version.plan_id,
            version_id=plan_version.version_id,
            session_plan=SessionPlan.model_validate(generation.session_plan),
            session_id=session_context.session_id,
            version_status=plan_version.status,
        )

    async def list_versions(
        self,
        *,
        subject: str | None,
        track: str | None,
        grade: str | None,
        term: str | None,
        week: int | None,
        session_id: str | None,
        teacher_id: str | None,
        latest_only: bool,
        limit: int,
        class_id: uuid.UUID | None = None,
    ) -> list[PlanVersionSummary]:
        rows = await list_plan_version_rows(
            self._db,
            class_id=class_id,
            subject=subject,
            track=track,
            grade=grade,
            term=term,
            week=week,
            session_id=session_id,
            teacher_id=teacher_id,
            latest_only=latest_only,
            limit=limit,
        )
        version_ids = [plan_version.version_id for plan_version, *_ in rows]
        pack_map = await latest_compiled_artefact_ids(self._db, version_ids=version_ids)

        summaries: list[PlanVersionSummary] = []
        for plan_version, plan, lesson_period, scheme, term_subject in rows:
            session_plan = plan_version.session_plan or {}
            term_val = term_subject.term if term_subject else session_plan.get("term", "Term 1")
            week_val = scheme.week_number if scheme else session_plan.get("week", 1)
            topic_val = scheme.title if scheme else session_plan.get("topic", "Legacy Topic")
            subtopic_val = (
                lesson_period.subtopic.title
                if lesson_period and lesson_period.subtopic
                else session_plan.get("subtopic", "Legacy Unit")
            )
            day_index_val = lesson_period.period_number if lesson_period else 1

            summaries.append(
                PlanVersionSummary(
                    plan_id=plan.plan_id,
                    version_id=plan_version.version_id,
                    session_id=str(plan.lesson_period_id),
                    subject=session_plan.get("subject") or plan.subject,
                    track=session_plan.get("track") or plan.track,
                    grade=session_plan.get("grade") or plan.grade,
                    term=term_val,
                    week=week_val,
                    day_index=day_index_val,
                    topic=topic_val,
                    subtopic=subtopic_val,
                    status=plan_version.status,
                    source_type=plan_version.source_type,
                    approved_at=plan_version.approved_at,
                    approved_by=plan_version.approved_by,
                    created_at=plan_version.created_at,
                    artefact_id=pack_map.get(plan_version.version_id),
                )
            )
        return summaries

    async def manual_edit(
        self,
        *,
        plan_or_version_id: str,
        edited_session_plan: JsonObject,
        owner_teacher_id: uuid.UUID | None = None,
    ) -> PlanGenerateResponse:
        """Persist a teacher's hand-edit as a new chained draft version.

        Mirrors a revision turn but with teacher-supplied content instead of an
        LLM turn. Identity + scope fields (subject / grade / term / lesson) are
        forced from the current version so an edit can only change *content*,
        never which lesson this plan is for. The full edited plan is validated
        against ``SessionPlan`` (via ``persist_revised_plan_version``); a
        structural break raises ``PlanValidationError`` (422), never a 500.
        """
        from pydantic import ValidationError

        row = await get_plan_row(self._db, plan_or_version_id=plan_or_version_id)
        if row is None:
            raise PlanLookupNotFoundError(plan_or_version_id)
        plan_version, plan = row

        if owner_teacher_id is not None:
            from app.domains.artefacts.types.lesson_plan.application.ownership import (
                teacher_owns_plan_version,
            )

            owns = await teacher_owns_plan_version(
                self._db,
                teacher_id=owner_teacher_id,
                plan_version_id=plan_version.version_id,
            )
            if not owns:
                raise PlanNotOwnedByTeacherError(plan_version.version_id)

        # Force identity/scope from the current version — a content edit can never
        # silently re-target the lesson.
        current = plan_version.session_plan or {}
        forced = dict(edited_session_plan)
        for field in (
            "plan_id",
            "session_id",
            "subject",
            "track",
            "grade",
            "term",
            "week",
            "topic",
            "subtopic",
        ):
            if field in current:
                forced[field] = current[field]

        try:
            new_version = await persist_revised_plan_version(
                self._db,
                plan_id=plan.plan_id,
                revised_session_plan=forced,
                parent_version_id=plan_version.version_id,
                run_metadata={"source": "manual_edit"},
            )
        except ValidationError as error:
            messages = [str(err.get("msg", err)) for err in error.errors()]
            raise PlanValidationError("; ".join(messages) or "invalid plan") from None

        return await self.get_plan(plan_id=new_version.version_id)

    async def manual_context(self, *, session_id: str) -> ManualPlanContextResponse:
        """Lesson identity + curriculum objectives a hand-entered plan maps onto."""
        session_context = await build_session_context(self._db, session_id)
        if session_context is None:
            raise SessionNotFoundError(session_id)
        payloads = self._payload_builder.build(session_context)
        return ManualPlanContextResponse(
            session_id=session_context.session_id,
            subject=session_context.subject,
            grade=session_context.grade,
            term=session_context.term,
            week=session_context.week,
            topic=session_context.topic,
            subtopic=session_context.subtopic,
            curriculum_objectives=[
                ManualCurriculumObjective.model_validate(objective)
                for objective in payloads.curriculum_scope.curriculum_objectives
            ],
        )

    async def create_manual(
        self,
        *,
        session_id: str,
        session_plan_content: JsonObject,
        teacher_id: str | None,
        owner_teacher_id: uuid.UUID | None = None,
        source_type: str = "manual",
        original_document_attachment_id: str | None = None,
        generator: JsonObject | None = None,
        imported_from: str | None = None,
    ) -> PlanGenerateResponse:
        """Persist a hand-entered teacher lesson plan as a new draft version.

        Lesson identity and the curriculum-objective list are forced from the
        lesson's ``SessionContext`` (the teacher supplies only content), so a
        manual plan stays bound to its real lesson and curriculum. Mirrors
        ``generate`` with teacher-supplied content in place of an LLM turn; the
        draft is frozen later via the approve endpoint. A curriculum-mapping gap
        or a structural break raises ``PlanValidationError`` (422), never a 500.

        If ``owner_teacher_id`` is given (the caller is a teacher) they must own
        the lesson's class + subject + term; a research-manager passes None and
        may author a plan for any lesson (it does the field data entry).
        """
        from pydantic import ValidationError

        session_context = await build_session_context(self._db, session_id)
        if session_context is None:
            raise SessionNotFoundError(session_id)
        if owner_teacher_id is not None:
            from app.domains.artefacts.types.lesson_plan.application.ownership import (
                teacher_owns_lesson_period,
            )

            owns = (
                session_context.lesson_period_id is not None
                and await teacher_owns_lesson_period(
                    self._db,
                    teacher_id=owner_teacher_id,
                    lesson_period_id=session_context.lesson_period_id,
                )
            )
            if not owns:
                raise PlanNotOwnedByTeacherError(session_id)
        check = check_manual_plan(session_context, session_plan_content)
        if not check.passes:
            first = next(iter(check.issues))
            raise PlanValidationError({first: check.issues[first]})
        session_plan = check.session_plan

        try:
            plan_version = await persist_plan_version(
                self._db,
                session_context,
                GeneratedLessonPlan(
                    session_plan=session_plan,
                    run_metadata={
                        "source": "manual_entry",
                        **(
                            {
                                "original_document": {
                                    "attachment_id": original_document_attachment_id
                                }
                            }
                            if original_document_attachment_id
                            else {}
                        ),
                        **({"generator": generator} if generator is not None else {}),
                        **({"imported_from": imported_from} if imported_from else {}),
                    },
                ),
                created_by=teacher_id,
                source_type=source_type,
            )
        except ValidationError as error:
            messages = [str(err.get("msg", err)) for err in error.errors()]
            raise PlanValidationError("; ".join(messages) or "invalid plan") from None

        return await self.get_plan(plan_id=plan_version.version_id)

    async def reusable_source(self, plan_or_version_id: str) -> ReuseSource:
        """A saved plan version, with the lesson it belongs to, for another lesson to reuse."""
        row = await get_plan_row(self._db, plan_or_version_id=plan_or_version_id)
        if row is None:
            raise PlanLookupNotFoundError(plan_or_version_id)
        version, plan = row
        return ReuseSource(version.session_plan or {}, version.version_id, plan.lesson_period_id)

    async def reuse_plan(
        self,
        *,
        session_id: str,
        source: JsonObject,
        chosen: Mapping[str, str],
        teacher_id: str | None,
        imported_from: str | None,
    ) -> ReusedPlan:
        """Save ``source`` as the lesson's plan, or say which objectives need a curriculum one.

        The plan keeps its content. Its field names are read as a stored plan's are, and each
        lesson objective is pointed at a curriculum objective of this lesson, by the choices made
        or by the only one the lesson has. The saved draft passes the same checks as a plan
        entered by hand, and the teacher still reviews and accepts it.
        """
        session_context = await build_session_context(self._db, session_id)
        if session_context is None:
            raise SessionNotFoundError(session_id)
        curriculum = (
            SessionContextPayloadBuilder()
            .build(session_context)
            .curriculum_scope.curriculum_objectives
        )
        mapped = map_curriculum(canonical_content(source), curriculum, chosen)
        if mapped.unmapped:
            return ReusedPlan(None, mapped.unmapped, [dict(found) for found in curriculum])
        plan = await self.create_manual(
            session_id=session_id,
            session_plan_content=mapped.content,
            teacher_id=teacher_id,
            source_type="experiment_reused",
            imported_from=imported_from,
        )
        return ReusedPlan(plan, [], [])

    async def get_plan(self, *, plan_id: str) -> PlanGenerateResponse:
        row = await get_plan_row(self._db, plan_or_version_id=plan_id)
        if row is None:
            raise PlanLookupNotFoundError(plan_id)

        plan_version, plan = row
        compiled_artefact_id = await latest_compiled_artefact_id(
            self._db,
            version_id=plan_version.version_id,
        )
        normalized = normalize_session_plan_payload(plan_version.session_plan or {})
        return PlanGenerateResponse(
            plan_id=plan_version.plan_id,
            version_id=plan_version.version_id,
            session_plan=SessionPlan.model_validate(normalized, context=READING_A_STORED_PLAN),
            session_id=str(plan.lesson_period_id),
            version_status=plan_version.status,
            closed_reason=plan_version.closed_reason,
            closed_at=plan_version.closed_at,
            compiled_artefact_id=compiled_artefact_id,
            unmet_requirements=await self._unmet_requirements(
                normalized, str(plan.lesson_period_id)
            ),
        )

    async def _unmet_requirements(self, plan: JsonObject, session_id: str) -> list[str]:
        """What the plan, as it stands, leaves of the lesson document and the plan spec."""
        session_context = await build_session_context(self._db, session_id)
        duration = session_context.duration_minutes if session_context else None
        return [*violations(as_document(plan)), *unmet(plan, duration_minutes=duration)]
