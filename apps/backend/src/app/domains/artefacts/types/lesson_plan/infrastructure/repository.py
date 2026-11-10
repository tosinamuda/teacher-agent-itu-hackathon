from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import cast as typing_cast

import sqlalchemy as sa
from sqlalchemy import case, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import (
    PlanVersionInfo,
    PlanVersionStatus,
    SessionContext,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import GeneratedLessonPlan
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import SessionPlan
from app.domains.artefacts.types.lesson_plan.infrastructure.curriculum_objectives import (
    ensure_curriculum_objectives,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
    PlanVersionObjective,
)
from app.domains.curriculum.models.curriculum import (
    ClassSession,
    CurriculumSubtopic,
    CurriculumTopic,
    ReferenceMaterial,
)
from app.domains.curriculum.models.themes import CurriculumTheme
from app.domains.expert_content.models import (
    AoTextbookLinkage,
    AoTextbookObjectiveLink,
    AoTextbookRecordLink,
    TextbookRecord,
)
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models import LessonPeriod, SchemeOfWork
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject, JsonValue

PlanVersionRow = tuple[
    PlanVersion,
    LessonPlan,
    LessonPeriod | None,
    SchemeOfWork | None,
    TermClassSubject | None,
]


def _summarize_textbook_title(record: TextbookRecord) -> str:
    heading = ""
    if isinstance(record.heading_path, list) and record.heading_path:
        heading = " > ".join(str(part) for part in record.heading_path if part)
    elif isinstance(record.heading_path, dict):
        heading = str(record.heading_path.get("label") or record.heading_path.get("title") or "")

    title_parts = [part for part in [record.chapter_title, heading] if part]
    if title_parts:
        return " - ".join(title_parts)
    if record.chapter_title:
        return record.chapter_title
    if heading:
        return heading
    return record.record_type.replace("_", " ").title()


def _textbook_record_ref(record: TextbookRecord, subtopic_id: str) -> JsonObject:
    """Shape a TextbookRecord into the reference dict the pipeline consumes."""
    content = (record.content_text or "").strip()
    retrieval_text = (
        record.retrieval_text or record.content_text or record.prompt_text or ""
    ).strip()
    return {
        "title": _summarize_textbook_title(record),
        "section_ref": record.record_id,
        "record_id": record.record_id,
        "content": content,
        "prompt_text": (record.prompt_text or "").strip(),
        "answer_text": (record.answer_text or "").strip(),
        "retrieval_text": retrieval_text,
        "record_type": record.record_type,
        "primary_subtopic_id": record.primary_subtopic_id,
        "matched_subtopic_id": subtopic_id,
        "source_html_path": record.source_html_path,
        "source_anchor_id": record.source_anchor_id,
        "asset_refs": record.asset_refs,
        "is_primary": True,
    }


async def _load_ao_linkage_references(
    db: AsyncSession,
    subtopic_id: str,
) -> tuple[str, list[JsonObject]]:
    """Load expert-validated AO->textbook links for a subtopic.

    Returns (grounding_mode, references). grounding_mode is "manual_linkage"
    when a linkage row exists for the subtopic, otherwise "curriculum_only"
    (the caller cold-starts from curriculum text). References are de-duplicated
    by record_id, ordered shared-foundation first then by atomic-objective and
    link order, so the curated scope replaces BM25 ranking.
    """
    linkage = (
        (
            await db.execute(
                select(AoTextbookLinkage).filter(AoTextbookLinkage.subtopic_id == subtopic_id)
            )
        )
        .scalars()
        .first()
    )
    if linkage is None:
        return "curriculum_only", []

    ordered_record_ids: list[str] = []
    seen: set[str] = set()

    shared = linkage.shared_foundation_record_ids
    if isinstance(shared, list):
        for record_id in shared:
            record_id = str(record_id or "").strip()
            if record_id and record_id not in seen:
                seen.add(record_id)
                ordered_record_ids.append(record_id)

    link_rows = (
        (
            await db.execute(
                select(AoTextbookRecordLink)
                .join(
                    AoTextbookObjectiveLink,
                    (AoTextbookRecordLink.subtopic_id == AoTextbookObjectiveLink.subtopic_id)
                    & (AoTextbookRecordLink.ao_id == AoTextbookObjectiveLink.ao_id),
                )
                .filter(AoTextbookRecordLink.subtopic_id == subtopic_id)
                .order_by(
                    AoTextbookObjectiveLink.ao_order,
                    AoTextbookRecordLink.link_order,
                )
            )
        )
        .scalars()
        .all()
    )
    for link in link_rows:
        record_id = str(link.record_id or "").strip()
        if record_id and record_id not in seen:
            seen.add(record_id)
            ordered_record_ids.append(record_id)

    if not ordered_record_ids:
        # A linkage row with no usable textbook records (e.g. status no_records)
        # has nothing to ground on -> treat as curriculum-only (no-linkage path).
        return "curriculum_only", []

    records = (
        (
            await db.execute(
                select(TextbookRecord).filter(TextbookRecord.record_id.in_(ordered_record_ids))
            )
        )
        .scalars()
        .all()
    )
    record_by_id = {record.record_id: record for record in records}

    references = [
        _textbook_record_ref(record_by_id[record_id], subtopic_id)
        for record_id in ordered_record_ids
        if record_id in record_by_id
    ]
    return "manual_linkage", references


async def _load_curated_objectives(
    db: AsyncSession,
    subtopic_id: str,
) -> list[JsonObject]:
    """Load per-AO curated planning rows in the `build_curated_planning` shape.

    One dict per atomic objective, carrying the role-tagged record links and the
    reused assessment, so the authoritative curated path can build the lesson
    structure directly from expert curation (no LLM re-derivation). Empty when no
    linkage exists for the subtopic.
    """
    objective_rows = (
        (
            await db.execute(
                select(AoTextbookObjectiveLink)
                .filter(AoTextbookObjectiveLink.subtopic_id == subtopic_id)
                .order_by(AoTextbookObjectiveLink.ao_order)
            )
        )
        .scalars()
        .all()
    )
    if not objective_rows:
        return []

    record_links = (
        (
            await db.execute(
                select(AoTextbookRecordLink)
                .filter(AoTextbookRecordLink.subtopic_id == subtopic_id)
                .order_by(AoTextbookRecordLink.ao_id, AoTextbookRecordLink.link_order)
            )
        )
        .scalars()
        .all()
    )
    links_by_ao: dict[str, list[JsonValue]] = {}
    for link in record_links:
        links_by_ao.setdefault(link.ao_id, []).append(
            {
                "record_id": link.record_id,
                "role": link.role,
                "link_order": link.link_order,
            }
        )

    curated: list[JsonObject] = []
    for row in objective_rows:
        practice = row.practice_record_ids if isinstance(row.practice_record_ids, list) else []
        assessment = row.assessment if isinstance(row.assessment, dict) else None
        curated.append(
            {
                "ao_id": row.ao_id,
                "ao_order": row.ao_order,
                "curriculum_objective_id": row.curriculum_objective_id,
                "objective_text": row.objective_text,
                "bloom_level": row.bloom_level,
                "assessment": assessment,
                "record_links": links_by_ao.get(row.ao_id, []),
                "practice_record_ids": practice,
            }
        )
    return curated


async def build_session_context(db: AsyncSession, session_id: str) -> SessionContext | None:
    # 1. Try Legacy ClassSession (String ID)
    result = await db.execute(select(ClassSession).filter(ClassSession.session_id == session_id))
    session_row = result.scalars().first()
    if session_row:
        context = await _session_context_from_class_session(db, session_row)
        if context is not None:
            return context

    # 2. Try LessonPeriod (UUID)
    try:
        uuid_obj = uuid.UUID(session_id)
    except ValueError:
        return None
    return await _session_context_from_lesson_period(db, uuid_obj)


async def _session_context_from_class_session(
    db: AsyncSession, session_row: ClassSession
) -> SessionContext | None:
    topic_result = await db.execute(
        select(CurriculumTopic).filter(CurriculumTopic.topic_key == session_row.topic_key)
    )
    topic_row = topic_result.scalars().first()

    subtopic_result = await db.execute(
        select(CurriculumSubtopic).filter(CurriculumSubtopic.subtopic_id == session_row.subtopic_id)
    )
    subtopic_row = subtopic_result.scalars().first()
    if not (topic_row and subtopic_row):
        return None
    ref_result = await db.execute(
        select(ReferenceMaterial).filter(
            ReferenceMaterial.subject == session_row.subject,
            ReferenceMaterial.track == session_row.track,
            ReferenceMaterial.grade == session_row.grade,
        )
    )
    reference_rows = ref_result.scalars().all()
    reference_materials: list[JsonObject] = [
        typing_cast(
            JsonObject,
            {
                "source_id": ref.source_id,
                "type": ref.type,
                "title": ref.title,
                "topics": ref.topics,
                "chunk_refs": ref.chunk_refs,
            },
        )
        for ref in reference_rows
    ]

    # Load theme
    theme_title = ""
    if topic_row.theme_id:
        theme_result = await db.execute(
            select(CurriculumTheme).filter(CurriculumTheme.id == topic_row.theme_id)
        )
        theme_row = theme_result.scalars().first()
        if theme_row:
            theme_title = theme_row.title

    # Load expert-validated AO->textbook linkage (no BM25 retrieval).
    grounding_mode, textbook_refs = await _load_ao_linkage_references(
        db,
        subtopic_row.subtopic_id,
    )
    curated_objectives = (
        await _load_curated_objectives(db, subtopic_row.subtopic_id)
        if grounding_mode == "manual_linkage"
        else []
    )

    # Derive entry behaviour from previous session
    entry_behaviour: list[str] = []
    prev_result = await db.execute(
        select(ClassSession).filter(
            ClassSession.topic_key == session_row.topic_key,
            ClassSession.sequence_in_topic == session_row.sequence_in_topic - 1,
        )
    )
    prev_session = prev_result.scalars().first()
    if prev_session:
        prev_sub_result = await db.execute(
            select(CurriculumSubtopic).filter(
                CurriculumSubtopic.subtopic_id == prev_session.subtopic_id
            )
        )
        prev_sub = prev_sub_result.scalars().first()
        if prev_sub and prev_sub.performance_objectives:
            entry_behaviour = list(prev_sub.performance_objectives)

    return SessionContext(
        session_id=session_row.session_id,
        subtopic_id=session_row.subtopic_id,
        subject=session_row.subject,
        track=session_row.track,
        grade=session_row.grade,
        term=session_row.term,
        week=session_row.week,
        day_index=session_row.day_index,
        topic=topic_row.topic,
        subtopic=subtopic_row.title,
        duration_minutes=session_row.duration_minutes,
        session_objectives=list(session_row.session_objectives or []),
        general_objectives=list(topic_row.general_objectives or []),
        reference_materials=reference_materials,
        theme=theme_title,
        performance_objectives=list(subtopic_row.performance_objectives or []),
        teacher_activities=list(subtopic_row.teacher_activities or []),
        student_activities=list(subtopic_row.student_activities or []),
        instructional_materials=list(subtopic_row.teaching_learning_materials or []),
        evaluation_guide=list(subtopic_row.evaluation_guide or []),
        textbook_references=textbook_refs,
        grounding_mode=grounding_mode,
        curated_objectives=curated_objectives,
        entry_behaviour=entry_behaviour,
    )


async def _lesson_period_theme_title(db: AsyncSession, subtopic_obj: CurriculumSubtopic) -> str:
    topic_result = await db.execute(
        select(CurriculumTopic).filter(CurriculumTopic.topic_key == subtopic_obj.topic_key)
    )
    topic_row = topic_result.scalars().first()
    if not (topic_row and topic_row.theme_id):
        return ""
    theme_result = await db.execute(
        select(CurriculumTheme).filter(CurriculumTheme.id == topic_row.theme_id)
    )
    theme_row = theme_result.scalars().first()
    return theme_row.title if theme_row else ""


async def _lesson_period_entry_behaviour(db: AsyncSession, day_row: LessonPeriod) -> list[str]:
    if day_row.period_number <= 1:
        return []
    prev_period_result = await db.execute(
        select(LessonPeriod).filter(
            LessonPeriod.scheme_of_work_id == day_row.scheme_of_work_id,
            LessonPeriod.period_number == day_row.period_number - 1,
        )
    )
    prev_period = prev_period_result.scalars().first()
    if prev_period and prev_period.subtopic:
        return list(prev_period.subtopic.performance_objectives or [])
    return []


async def _session_context_from_lesson_period(
    db: AsyncSession, uuid_obj: uuid.UUID
) -> SessionContext | None:
    from app.domains.school.models.structure import Course

    day_result = await db.execute(
        select(LessonPeriod)
        .options(
            selectinload(LessonPeriod.scheme_of_work)
            .selectinload(SchemeOfWork.term_class_subject)
            .selectinload(TermClassSubject.course)
            .selectinload(Course.subject),
            selectinload(LessonPeriod.scheme_of_work)
            .selectinload(SchemeOfWork.term_class_subject)
            .selectinload(TermClassSubject.course)
            .selectinload(Course.grade_level),
        )
        .filter(LessonPeriod.id == uuid_obj)
    )
    day_row = day_result.scalars().first()

    if not day_row:
        return None

    week_row = day_row.scheme_of_work
    scheme_row = week_row.term_class_subject
    course_row = scheme_row.course
    subject_row = course_row.subject
    grade_row = course_row.grade_level

    ref_result = await db.execute(
        select(ReferenceMaterial).filter(
            ReferenceMaterial.subject == subject_row.name,
            ReferenceMaterial.grade == grade_row.name,
        )
    )
    reference_rows = ref_result.scalars().all()
    reference_materials = [
        typing_cast(
            JsonObject,
            {
                "source_id": ref.source_id,
                "type": ref.type,
                "title": ref.title,
                "topics": ref.topics,
                "chunk_refs": ref.chunk_refs,
            },
        )
        for ref in reference_rows
    ]

    objectives = []
    if week_row.objectives and isinstance(week_row.objectives, dict):
        objectives = week_row.objectives.get("goals", [])

    # Extract NERDC fields from subtopic
    subtopic_obj = day_row.subtopic
    performance_objectives: list[str] = []
    teacher_activities: list[str] = []
    student_activities: list[str] = []
    instructional_materials: list[str] = []
    evaluation_guide: list[str] = []
    textbook_refs: list[JsonObject] = []
    entry_behaviour: list[str] = []
    theme_title = ""
    grounding_mode = "curriculum_only"
    curated_objectives = []

    if subtopic_obj:
        performance_objectives = list(subtopic_obj.performance_objectives or [])
        teacher_activities = list(subtopic_obj.teacher_activities or [])
        student_activities = list(subtopic_obj.student_activities or [])
        instructional_materials = list(subtopic_obj.teaching_learning_materials or [])
        evaluation_guide = list(subtopic_obj.evaluation_guide or [])

        theme_title = await _lesson_period_theme_title(db, subtopic_obj)

        # Load expert-validated AO->textbook linkage (no BM25 retrieval).
        grounding_mode, textbook_refs = await _load_ao_linkage_references(
            db,
            subtopic_obj.subtopic_id,
        )
        if grounding_mode == "manual_linkage":
            curated_objectives = await _load_curated_objectives(db, subtopic_obj.subtopic_id)

        entry_behaviour = await _lesson_period_entry_behaviour(db, day_row)

    return SessionContext(
        session_id=str(day_row.id),
        lesson_period_id=day_row.id,
        subtopic_id=day_row.subtopic_id or "",
        subject=subject_row.name,
        track="General",
        grade=grade_row.name,
        term=scheme_row.term,
        week=week_row.week_number,
        day_index=day_row.period_number,
        topic=week_row.title,
        subtopic=(day_row.subtopic.title if day_row.subtopic else day_row.subtopic_id or ""),
        duration_minutes=45,
        session_objectives=performance_objectives,
        general_objectives=objectives,
        reference_materials=reference_materials,
        theme=theme_title,
        performance_objectives=performance_objectives,
        teacher_activities=teacher_activities,
        student_activities=student_activities,
        instructional_materials=instructional_materials,
        evaluation_guide=evaluation_guide,
        textbook_references=textbook_refs,
        grounding_mode=grounding_mode,
        curated_objectives=curated_objectives,
        entry_behaviour=entry_behaviour,
        average_age=grade_row.average_age,
    )


async def _sync_plan_version_objectives(
    db: AsyncSession,
    *,
    plan_version_id: str,
    session_plan: JsonObject,
) -> None:
    """Mirror ``session_plan.lesson_plan_objectives`` into the derived table.

    P5.6 Phase 1: the JSON stays canonical at write time. This helper UPSERTs
    one row per ``(plan_version_id, lesson_objective_id)`` pair using the
    ``uq_plan_version_objectives_pv_lop`` constraint so re-runs against an
    existing version_id repair drift rather than duplicating rows.
    """
    raw_objectives = session_plan.get("lesson_plan_objectives")
    if not isinstance(raw_objectives, list) or not raw_objectives:
        return
    for ordinal, entry in enumerate(raw_objectives, start=1):
        if not isinstance(entry, dict):
            continue
        lesson_objective_id = str(entry.get("lesson_objective_id") or "").strip()
        if not lesson_objective_id:
            continue
        objective_order_raw = entry.get("objective_order")
        if isinstance(objective_order_raw, int):
            objective_order = objective_order_raw
        elif isinstance(objective_order_raw, str) and objective_order_raw.isdigit():
            objective_order = int(objective_order_raw)
        else:
            objective_order = ordinal
        # Upsert on the ``uq_plan_version_objectives_pv_lop`` natural key via the
        # ORM (get-then-update-or-insert). The sync loop is single-threaded, so a
        # select-first is safe. ``updated_at`` carries an onupdate on the model.
        existing = (
            (
                await db.execute(
                    select(PlanVersionObjective).where(
                        PlanVersionObjective.plan_version_id == plan_version_id,
                        PlanVersionObjective.lesson_objective_id == lesson_objective_id,
                    )
                )
            )
            .scalars()
            .first()
        )
        fields = {
            "objective_text": str(entry.get("objective_text") or "").strip(),
            "objective_order": objective_order,
            "kc_type": _opt_str(entry.get("kc_type")),
            "kc_focus": _opt_str(entry.get("kc_focus")),
            "curriculum_objective_id": _opt_str(entry.get("curriculum_objective_id")),
            "curriculum_objective_text": _opt_str(entry.get("curriculum_objective_text")),
        }
        if existing is None:
            db.add(
                PlanVersionObjective(
                    plan_version_id=plan_version_id,
                    lesson_objective_id=lesson_objective_id,
                    **fields,
                )
            )
        else:
            for key, value in fields.items():
                setattr(existing, key, value)


def _opt_str(value: object) -> str | None:
    if value is None:
        return None
    text_value = str(value).strip()
    return text_value or None


async def persist_plan_version(
    db: AsyncSession,
    session_context: SessionContext,
    generation: GeneratedLessonPlan,
    created_by: str | None = None,
    source_type: str = "generated",
) -> PlanVersionInfo:
    plan_id = new_public_id(PublicIdPrefix.LESSON_PLAN)
    strict_session_plan = typing_cast(
        JsonObject,
        SessionPlan.model_validate(generation.session_plan).model_dump(
            mode="json",
            exclude_none=True,
        ),
    )

    result = await db.execute(select(LessonPlan).filter(LessonPlan.plan_id == plan_id))
    existing_plan = result.scalars().first()

    if existing_plan is None:
        if session_context.lesson_period_id is None:
            raise ValueError(
                "session_context.lesson_period_id is required to persist a lesson_plan "
                "(P5.7: every lesson_plan attaches to a real lesson_period). Build the "
                "SessionContext via the lesson_period path, not the curriculum ClassSession."
            )
        plan = LessonPlan(
            plan_id=plan_id,
            lesson_period_id=session_context.lesson_period_id,
            title=(
                f"{session_context.grade} {session_context.subject} "
                f"Week {session_context.week} Session {session_context.day_index}: "
                f"{session_context.subtopic}"
            ),
            subject=session_context.subject,
            track=session_context.track,
            grade=session_context.grade,
            created_by=created_by,
        )
        db.add(plan)
    else:
        plan = existing_plan

    version_id = new_public_id(PublicIdPrefix.LESSON_PLAN_VERSION)
    strict_session_plan["plan_id"] = plan.plan_id
    plan_version = PlanVersion(
        version_id=version_id,
        plan_id=plan.plan_id,
        source_type=source_type,
        parent_version_id=None,
        session_plan=strict_session_plan,
        run_metadata=generation.run_metadata,
    )
    db.add(plan_version)
    # Flush (not commit) so the version row exists for the objectives' FK, then sync the
    # derived objectives and commit ONCE — parent + children land atomically. Two commits
    # previously left a committed version with zero objective rows if the process died
    # between them, silently drifting the derived table from the canonical JSON.
    await db.flush()
    await ensure_curriculum_objectives(db, session_context)
    await _sync_plan_version_objectives(
        db, plan_version_id=version_id, session_plan=strict_session_plan
    )
    await db.commit()

    return PlanVersionInfo(plan_id=plan.plan_id, version_id=version_id, status=plan_version.status)


async def persist_revised_plan_version(
    db: AsyncSession,
    *,
    plan_id: str,
    revised_session_plan: JsonObject,
    parent_version_id: str,
    run_metadata: JsonObject | None = None,
    created_by: str | None = None,
) -> PlanVersionInfo:
    """Persist a new draft version of an EXISTING plan produced by a revision turn.

    Unlike ``persist_plan_version`` (which mints a new plan), this chains onto an
    existing ``plan_id`` with ``source_type="revised"`` and ``parent_version_id``
    set, so the revision history forms a parent-linked chain under one plan.
    """
    del created_by  # provenance lives on the revision turn, not a new plan row
    strict_session_plan = typing_cast(
        JsonObject,
        SessionPlan.model_validate(revised_session_plan).model_dump(
            mode="json",
            exclude_none=True,
        ),
    )
    strict_session_plan["plan_id"] = plan_id
    version_id = new_public_id(PublicIdPrefix.LESSON_PLAN_VERSION)
    plan_version = PlanVersion(
        version_id=version_id,
        plan_id=plan_id,
        source_type="revised",
        parent_version_id=parent_version_id,
        session_plan=strict_session_plan,
        run_metadata=run_metadata or {},
    )
    db.add(plan_version)
    # One transaction: flush the version row for the objectives' FK, sync, then commit
    # both together (was two commits — a crash between left an objective-less version).
    await db.flush()
    await _sync_plan_version_objectives(
        db, plan_version_id=version_id, session_plan=strict_session_plan
    )
    await db.commit()
    return PlanVersionInfo(plan_id=plan_id, version_id=version_id, status=plan_version.status)


async def approve_plan_version(
    db: AsyncSession,
    *,
    version_id: str,
    approved_by: str | None,
) -> PlanVersion | None:
    result = await db.execute(select(PlanVersion).filter(PlanVersion.version_id == version_id))
    plan_version = result.scalars().first()
    if plan_version is None:
        return None

    plan_version.status = PlanVersionStatus.APPROVED
    plan_version.approved_at = datetime.now(timezone.utc)
    plan_version.approved_by = approved_by
    await db.commit()
    await db.refresh(plan_version)
    return plan_version


async def close_plan_version(
    db: AsyncSession,
    *,
    version_id: str,
    status: PlanVersionStatus,
    closed_by: str,
    reason: str,
) -> PlanVersion | None:
    """Discard a draft (``rejected``) or take an approval back (``withdrawn``), and keep why."""
    plan_version = (
        (await db.execute(select(PlanVersion).filter(PlanVersion.version_id == version_id)))
        .scalars()
        .first()
    )
    if plan_version is None:
        return None
    plan_version.status = status
    plan_version.closed_at = datetime.now(timezone.utc)
    plan_version.closed_by = closed_by
    plan_version.closed_reason = reason[:512]
    await db.commit()
    await db.refresh(plan_version)
    return plan_version


async def list_plan_version_rows(
    db: AsyncSession,
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
) -> list[PlanVersionRow]:
    stmt = (
        select(PlanVersion, LessonPlan, LessonPeriod, SchemeOfWork, TermClassSubject)
        .join(LessonPlan, PlanVersion.plan_id == LessonPlan.plan_id)
        .outerjoin(LessonPeriod, LessonPlan.lesson_period_id == LessonPeriod.id)
        .outerjoin(SchemeOfWork, LessonPeriod.scheme_of_work_id == SchemeOfWork.id)
        .outerjoin(TermClassSubject, SchemeOfWork.term_class_subject_id == TermClassSubject.id)
    )

    if subject:
        stmt = stmt.filter(LessonPlan.subject == subject)
    if track:
        stmt = stmt.filter(LessonPlan.track == track)
    if grade:
        stmt = stmt.filter(LessonPlan.grade == grade)
    if term:
        stmt = stmt.filter(TermClassSubject.term == term)
    if week:
        stmt = stmt.filter(SchemeOfWork.week_number == week)
    if session_id:
        # The caller filter is still keyed on the public ``session_id`` name; the
        # ORM column moved to ``lesson_period_id`` (UUID) under P5.7 so we parse
        # the incoming filter as a UUID.
        try:
            stmt = stmt.filter(LessonPlan.lesson_period_id == uuid.UUID(session_id))
        except ValueError:
            # Unrecognised id → no results.
            stmt = stmt.filter(sa.false())
    if teacher_id:
        stmt = stmt.filter(LessonPlan.created_by == teacher_id)
    if class_id:
        stmt = stmt.filter(TermClassSubject.class_id == class_id)

    if latest_only:
        stmt = stmt.distinct(LessonPlan.plan_id)
        stmt = stmt.order_by(LessonPlan.plan_id, PlanVersion.created_at.desc())
    else:
        stmt = stmt.order_by(PlanVersion.created_at.desc())

    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    rows: list[PlanVersionRow] = []
    for plan_version, plan, lesson_period, scheme, term_subject in result.all():
        rows.append(
            (
                plan_version,
                plan,
                lesson_period,
                scheme,
                term_subject,
            )
        )
    return rows


async def latest_compiled_artefact_ids(
    db: AsyncSession,
    *,
    version_ids: list[str],
) -> dict[str, str]:
    if not version_ids:
        return {}

    artefacts_result = await db.execute(
        select(Artefact)
        .filter(Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value)
        .filter(Artefact.scope == ArtefactScope.CLASS_LEVEL.value)
        .filter(Artefact.plan_version_id.in_(version_ids))
        .order_by(Artefact.created_at.desc())
    )
    artefact_map: dict[str, str] = {}
    for artefact in artefacts_result.scalars().all():
        if artefact.plan_version_id not in artefact_map:
            artefact_map[artefact.plan_version_id] = artefact.artefact_id
    return artefact_map


async def get_plan_row(
    db: AsyncSession,
    *,
    plan_or_version_id: str,
) -> tuple[PlanVersion, LessonPlan] | None:
    stmt = (
        select(PlanVersion, LessonPlan)
        .join(LessonPlan, PlanVersion.plan_id == LessonPlan.plan_id)
        .filter(
            or_(
                PlanVersion.version_id == plan_or_version_id,
                PlanVersion.plan_id == plan_or_version_id,
            )
        )
        # A plan is read as its newest version that is still live; only a plan whose every
        # version was closed is read as its newest closed one.
        .order_by(
            case(
                (PlanVersion.status.in_([PlanVersionStatus.DRAFT, PlanVersionStatus.APPROVED]), 0),
                else_=1,
            ),
            PlanVersion.created_at.desc(),
        )
    )
    result = await db.execute(stmt)
    row = result.first()
    if row is None:
        return None
    return row[0], row[1]


async def latest_compiled_artefact_id(
    db: AsyncSession,
    *,
    version_id: str,
) -> str | None:
    artefact_result = await db.execute(
        select(Artefact)
        .filter(Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value)
        .filter(Artefact.scope == ArtefactScope.CLASS_LEVEL.value)
        .filter(Artefact.plan_version_id == version_id)
        .order_by(Artefact.created_at.desc())
    )
    compiled_artefact = artefact_result.scalars().first()
    if compiled_artefact is None:
        return None
    return compiled_artefact.artefact_id
