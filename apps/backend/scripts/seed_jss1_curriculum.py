"""Seed JSS1 Mathematics curriculum and syllabus data from processed JSON.

Loads themes, topics, subtopics (with full NERDC design fields),
scheme-of-work weeks, lesson periods, reference material metadata,
knowledge components, and sample students.

Usage:
    cd apps/backend
    uv run python scripts/seed_jss1_curriculum.py
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import uuid
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias, TypedDict, cast

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.default_school import ensure_default_school
from app.db.metadata import target_metadata  # noqa: F401
from app.shared.ids import PublicIdPrefix, new_public_id

if TYPE_CHECKING:
    from app.domains.curriculum.models.curriculum import (
        CurriculumGrade,
        CurriculumSubject,
        CurriculumTerm,
        CurriculumTrack,
    )

# The four curriculum catalogs are the same shape (a unique ``name``), which is what lets
# one loop seed them all: the union types both ``model.name`` and the row it reads back.
CatalogModel: TypeAlias = (
    "type[CurriculumSubject] | type[CurriculumGrade] | type[CurriculumTrack] | type[CurriculumTerm]"
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger(__name__)

DATASET = Path(__file__).resolve().parents[3] / "dataset" / "processed"
GRADE = "JSS1"
SUBJECT = "Mathematics"
SUBJECT_CODE = "MATH"
TRACK = "General"
YEAR = "2024/2025"
TEXTBOOK_SOURCE_ID = "siyavula-jss1-math"
SCHOOL_NAME = "Plan-to-Tutor Research School"
SCHOOL_CODE = "PTRS"


class SchemeBreakdownItem(TypedDict):
    title: str
    subtopic_id: str


class SchemeWeek(TypedDict, total=False):
    week: int
    breakdown: list[SchemeBreakdownItem]
    _topic_keys: list[str]
    _label: str
    _title: str


def load_json_rows(path: Path) -> list[dict[str, Any]]:
    """Load a dataset file whose top level must be a JSON array of objects."""
    raw_data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw_data, list):
        raise ValueError(f"Expected a list-based dataset: {path}")
    return cast(list[dict[str, Any]], raw_data)


def load_scheme_data() -> dict[str, list[SchemeWeek]]:
    raw_data = json.loads(
        (DATASET / "scheme-of-work" / "jss1_scheme.json").read_text(encoding="utf-8")
    )
    if not isinstance(raw_data, dict):
        raise ValueError("Expected dict-based scheme-of-work dataset.")
    return cast(dict[str, list[SchemeWeek]], raw_data)


_TERM_ORDER = {"First Term": 1, "Second Term": 2, "Third Term": 3}


def build_subtopic_schedule(
    scheme_data: dict[str, list[SchemeWeek]],
    topics_data: list[dict[str, Any]],
) -> dict[str, tuple[str, int]]:
    """Map every subtopic_id to a valid (term, week) from the scheme of work.

    A ClassSession needs a non-empty term and a week >= 1 (SessionPlan rejects
    term="" / week=0), so each session must carry its scheme slot. Resolution
    order, most to least specific:

      1. the subtopic's own first scheme appearance;
      2. else its topic's earliest scheme slot (some subtopics aren't listed
         individually but their topic is);
      3. else carry forward the previous topic's slot in canonical topic order,
         so a topic the scheme omits entirely still lands in a valid in-sequence
         week instead of week 0.
    """
    subtopic_slot: dict[str, tuple[str, int]] = {}
    for term, weeks in scheme_data.items():
        for week in weeks:
            for item in week.get("breakdown", []):
                subtopic_id = item.get("subtopic_id")
                if subtopic_id:
                    subtopic_slot.setdefault(subtopic_id, (term, int(week["week"])))

    subtopic_topic: dict[str, str] = {}
    for entry in topics_data:
        for subtopic in entry.get("subtopics", []):
            subtopic_topic[subtopic["subtopic_id"]] = entry["topic_key"]

    def slot_key(slot: tuple[str, int]) -> tuple[int, int]:
        return (_TERM_ORDER[slot[0]], slot[1])

    topic_slot: dict[str, tuple[str, int]] = {}
    for subtopic_id, slot in subtopic_slot.items():
        topic_key = subtopic_topic.get(subtopic_id)
        if topic_key and (
            topic_key not in topic_slot or slot_key(slot) < slot_key(topic_slot[topic_key])
        ):
            topic_slot[topic_key] = slot

    schedule: dict[str, tuple[str, int]] = {}
    last_slot: tuple[str, int] = ("First Term", 1)
    for entry in topics_data:
        topic_key = entry["topic_key"]
        resolved = topic_slot.get(topic_key, last_slot)
        last_slot = resolved
        for subtopic in entry.get("subtopics", []):
            subtopic_id = subtopic["subtopic_id"]
            schedule[subtopic_id] = subtopic_slot.get(subtopic_id, resolved)
    return schedule


async def _delete_experiment_rows_for_workspace_ids(
    db: AsyncSession,
    *,
    workspace_ids: Sequence[uuid.UUID],
) -> None:
    if not workspace_ids:
        return

    from app.domains.evaluation.infrastructure.models import EvaluationPacket
    from app.domains.experiments.infrastructure.models import (
        Experiment,
        ExperimentConditionRun,
        ExperimentExecution,
        ExperimentFocalCase,
    )

    experiment_ids = list(
        (
            await db.execute(
                select(Experiment.id).where(Experiment.teacher_workspace_id.in_(workspace_ids))
            )
        ).scalars()
    )
    if not experiment_ids:
        return

    execution_ids = list(
        (
            await db.execute(
                select(ExperimentExecution.id).where(
                    ExperimentExecution.experiment_db_id.in_(experiment_ids)
                )
            )
        ).scalars()
    )
    if execution_ids:
        await db.execute(
            delete(EvaluationPacket).where(EvaluationPacket.execution_db_id.in_(execution_ids))
        )
        await db.execute(
            delete(ExperimentConditionRun).where(
                ExperimentConditionRun.execution_db_id.in_(execution_ids)
            )
        )
        await db.execute(
            delete(ExperimentFocalCase).where(
                ExperimentFocalCase.execution_db_id.in_(execution_ids)
            )
        )
        await db.execute(
            delete(ExperimentExecution).where(ExperimentExecution.id.in_(execution_ids))
        )

    await db.execute(delete(Experiment).where(Experiment.id.in_(experiment_ids)))


async def _purge_noncanonical_ptrs_jss1_teaching_rows(
    db: AsyncSession,
    *,
    class_id: uuid.UUID,
    canonical_course_id: uuid.UUID,
) -> None:
    from app.domains.school.models.subject_offerings import TermClassSubject
    from app.domains.teaching.models import (
        LessonDelivery,
        LessonPeriod,
        SchemeOfWork,
        TeacherWorkspace,
    )

    contaminated_tcs_ids = list(
        (
            await db.execute(
                select(TermClassSubject.id).where(
                    TermClassSubject.class_id == class_id,
                    TermClassSubject.course_id != canonical_course_id,
                )
            )
        ).scalars()
    )
    if not contaminated_tcs_ids:
        return

    workspace_ids = list(
        (
            await db.execute(
                select(TeacherWorkspace.id).where(
                    TeacherWorkspace.term_class_subject_id.in_(contaminated_tcs_ids)
                )
            )
        ).scalars()
    )
    scheme_ids = list(
        (
            await db.execute(
                select(SchemeOfWork.id).where(
                    SchemeOfWork.term_class_subject_id.in_(contaminated_tcs_ids)
                )
            )
        ).scalars()
    )
    period_ids = list(
        (
            await db.execute(
                select(LessonPeriod.id).where(LessonPeriod.scheme_of_work_id.in_(scheme_ids))
            )
        ).scalars()
    )

    await _delete_experiment_rows_for_workspace_ids(db, workspace_ids=workspace_ids)

    if workspace_ids:
        await db.execute(
            delete(LessonDelivery).where(LessonDelivery.teacher_workspace_id.in_(workspace_ids))
        )
        await db.execute(delete(TeacherWorkspace).where(TeacherWorkspace.id.in_(workspace_ids)))

    if period_ids:
        await db.execute(
            delete(LessonDelivery).where(LessonDelivery.lesson_period_id.in_(period_ids))
        )
        await db.execute(delete(LessonPeriod).where(LessonPeriod.id.in_(period_ids)))

    if scheme_ids:
        await db.execute(delete(SchemeOfWork).where(SchemeOfWork.id.in_(scheme_ids)))

    await db.execute(delete(TermClassSubject).where(TermClassSubject.id.in_(contaminated_tcs_ids)))


async def seed_jss1(db: AsyncSession) -> None:
    """Seed JSS1 Mathematics curriculum and supporting data."""
    from app.domains.curriculum.models.curriculum import (
        ClassSession,
        CurriculumGrade,
        CurriculumSubject,
        CurriculumSubtopic,
        CurriculumTerm,
        CurriculumTopic,
        CurriculumTrack,
        ReferenceMaterial,
    )
    from app.domains.curriculum.models.themes import CurriculumTheme
    from app.domains.learners.models import LearnerProfile
    from app.domains.school.models.core import (
        AcademicYear,
        GradeLevel,
        Subject,
    )
    from app.domains.school.models.structure import (
        Class,
        Course,
        School,
    )
    from app.domains.school.models.subject_offerings import TermClassSubject
    from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace
    from app.domains.users.models import User

    # ── 0. Curriculum catalogs (FK-hardening targets) ──
    # curriculum_topics/* now carry FKs onto the subject/grade/term catalogs;
    # on a fresh database those rows must exist BEFORE any topic insert (the
    # backfill script scripts/seed_curriculum_subject_grade_term_catalogs.py
    # only derives catalogs from existing data). The "" term is the documented
    # sentinel for scheme-slot-resolved topics (see module docstring).
    # Get-or-create each catalog row via the ORM (the ``name`` column is unique).
    # The model's ``default=uuid.uuid4`` mints the id and the ``Uuid`` type stores
    # it as ``CHAR(32)``.
    catalog_seeds: list[tuple[CatalogModel, str]] = [
        (CurriculumSubject, SUBJECT),
        (CurriculumGrade, GRADE),
        (CurriculumTrack, TRACK),
    ]
    catalog_seeds += [
        (CurriculumTerm, term_name) for term_name in ("", "First Term", "Second Term", "Third Term")
    ]
    for model, name in catalog_seeds:
        existing = await db.scalar(select(model).where(model.name == name))
        if existing is None:
            db.add(model(name=name))
    await db.flush()

    # ── Load JSON data ──
    themes_data = load_json_rows(DATASET / "curriculum" / "jss1_themes.json")
    topics_data = load_json_rows(DATASET / "curriculum" / "jss1_topics_enriched.json")
    scheme_data = load_scheme_data()
    # ── 1. Academic year ──
    ay = await db.scalar(select(AcademicYear).where(AcademicYear.name == YEAR))
    if not ay:
        ay = AcademicYear(
            name=YEAR,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 7, 31),
            is_current=True,
        )
        db.add(ay)
        await db.flush()
    logger.info("Academic year: %s", ay.name)

    # ── 2. Grade level ──
    grade = await db.scalar(select(GradeLevel).where(GradeLevel.name == GRADE))
    if not grade:
        grade = GradeLevel(name=GRADE, sequence=1)
        db.add(grade)
        await db.flush()

    # ── 3. Subject ──
    subj = await db.scalar(select(Subject).where(Subject.code == SUBJECT_CODE))
    if not subj:
        subj = Subject(
            name=SUBJECT,
            code=SUBJECT_CODE,
            category="Science",
            is_compulsory=True,
            is_trade=False,
        )
        db.add(subj)
        await db.flush()
    else:
        subj.name = SUBJECT
        subj.category = "Science"
        subj.is_compulsory = True
        subj.is_trade = False

    # ── 4. Course ──
    course = await db.scalar(
        select(Course).where(
            Course.subject_id == subj.id,
            Course.grade_level_id == grade.id,
        )
    )
    if not course:
        course = Course(
            name=f"{GRADE} {SUBJECT}",
            subject_id=subj.id,
            grade_level_id=grade.id,
        )
        db.add(course)
        await db.flush()
    else:
        course.name = f"{GRADE} {SUBJECT}"

    # ── 4b. School ──
    school = await db.scalar(select(School).where(School.code == SCHOOL_CODE))
    if not school:
        school = School(name=SCHOOL_NAME, code=SCHOOL_CODE)
        db.add(school)
        await db.flush()
    else:
        school.name = SCHOOL_NAME

    # ── 5. Class ──
    klass = await db.scalar(
        select(Class).where(
            Class.name == GRADE,
            Class.grade_level_id == grade.id,
            Class.school_id == school.id,
        )
    )
    if not klass:
        klass = await db.scalar(
            select(Class).where(
                Class.name == GRADE,
                Class.grade_level_id == grade.id,
            )
        )
        if klass:
            klass.school_id = school.id
        else:
            klass = Class(name=GRADE, grade_level_id=grade.id, school_id=school.id)
            db.add(klass)
            await db.flush()

    await _purge_noncanonical_ptrs_jss1_teaching_rows(
        db,
        class_id=klass.id,
        canonical_course_id=course.id,
    )

    # ── 6. Terms ──
    from app.domains.school.models.core import Term

    term_names = ["First Term", "Second Term", "Third Term"]
    term_dates = [
        (date(2024, 9, 16), date(2024, 12, 13)),
        (date(2025, 1, 6), date(2025, 3, 28)),
        (date(2025, 4, 28), date(2025, 7, 18)),
    ]
    for tname, (tstart, tend) in zip(term_names, term_dates, strict=False):
        existing_term = await db.scalar(
            select(Term).where(
                Term.name == tname,
                Term.academic_year_id == ay.id,
            )
        )
        if existing_term is None:
            db.add(
                Term(
                    name=tname,
                    academic_year_id=ay.id,
                    start_date=tstart,
                    end_date=tend,
                    is_current=(tname == "First Term"),
                )
            )
    await db.flush()

    # ── 7. Themes ──
    theme_map: dict[str, uuid.UUID] = {}
    for t in themes_data:
        existing = await db.scalar(
            select(CurriculumTheme).where(CurriculumTheme.theme_key == t["key"])
        )
        if not existing:
            ct = CurriculumTheme(theme_key=t["key"], title=t["title"])
            db.add(ct)
            await db.flush()
            theme_map[t["key"]] = ct.id
        else:
            existing.title = t["title"]
            theme_map[t["key"]] = existing.id
    logger.info("Themes: %d", len(theme_map))

    # ── 8. Topics + subtopics ──
    canonical_subtopic_ids: set[str] = set()
    subtopic_count = 0
    for entry in topics_data:
        topic_key = entry["topic_key"]
        topic_row = await db.scalar(
            select(CurriculumTopic).where(CurriculumTopic.topic_key == topic_key)
        )
        if not topic_row:
            # Derive general objectives from subtopic performance_objectives
            gen_objs: list[str] = []
            for st in entry.get("subtopics", []):
                for po in st.get("performance_objectives", []):
                    if po not in gen_objs:
                        gen_objs.append(po)
            topic_row = CurriculumTopic(
                topic_key=topic_key,
                subject=SUBJECT,
                track=TRACK,
                grade=GRADE,
                term="",
                week=0,
                topic=entry["topic"],
                general_objectives=gen_objs,
                theme_id=theme_map.get(entry["theme_key"]),
            )
            db.add(topic_row)
            await db.flush()
        else:
            topic_row.subject = SUBJECT
            topic_row.track = TRACK
            topic_row.grade = GRADE
            topic_row.topic = entry["topic"]
            topic_row.theme_id = theme_map.get(entry["theme_key"])

        for st in entry["subtopics"]:
            canonical_subtopic_ids.add(st["subtopic_id"])
            subtopic_row = await db.scalar(
                select(CurriculumSubtopic).where(
                    CurriculumSubtopic.subtopic_id == st["subtopic_id"]
                )
            )
            if not subtopic_row:
                subtopic_row = CurriculumSubtopic(
                    subtopic_id=st["subtopic_id"],
                    topic_key=topic_key,
                    title=st["title"],
                    performance_objectives=st.get("performance_objectives"),
                    teacher_activities=st.get("teacher_activities"),
                    student_activities=st.get("student_activities"),
                    teaching_learning_materials=st.get("teaching_learning_materials"),
                    evaluation_guide=st.get("evaluation_guide"),
                )
                db.add(subtopic_row)
                subtopic_count += 1
            else:
                subtopic_row.topic_key = topic_key
                subtopic_row.title = st["title"]
                subtopic_row.performance_objectives = st.get("performance_objectives")
                subtopic_row.teacher_activities = st.get("teacher_activities")
                subtopic_row.student_activities = st.get("student_activities")
                subtopic_row.teaching_learning_materials = st.get("teaching_learning_materials")
                subtopic_row.evaluation_guide = st.get("evaluation_guide")
    await db.flush()
    logger.info(
        "Topics: %d, Subtopics: %d",
        len(topics_data),
        subtopic_count,
    )

    # ── 9. Class sessions (one per subtopic) ──
    # Each session carries its scheme-of-work slot; an empty term / week 0 makes
    # the session ungenerable (SessionPlan requires term != "" and week >= 1).
    session_schedule = build_subtopic_schedule(scheme_data, topics_data)
    session_count = 0
    for entry in topics_data:
        for seq, st in enumerate(entry["subtopics"], 1):
            sid = f"session-{st['subtopic_id']}"
            term_value, week_value = session_schedule[st["subtopic_id"]]
            existing_session = await db.scalar(
                select(ClassSession).where(ClassSession.session_id == sid)
            )
            if not existing_session:
                db.add(
                    ClassSession(
                        session_id=sid,
                        topic_key=entry["topic_key"],
                        subtopic_id=st["subtopic_id"],
                        subject=SUBJECT,
                        track=TRACK,
                        grade=GRADE,
                        term=term_value,
                        week=week_value,
                        day_index=seq,
                        sequence_in_topic=seq,
                        duration_minutes=40,
                        session_objectives=st.get("performance_objectives", []),
                    )
                )
                session_count += 1
            else:
                existing_session.topic_key = entry["topic_key"]
                existing_session.subtopic_id = st["subtopic_id"]
                existing_session.subject = SUBJECT
                existing_session.track = TRACK
                existing_session.grade = GRADE
                existing_session.term = term_value
                existing_session.week = week_value
                existing_session.session_objectives = st.get("performance_objectives", [])
    await db.flush()
    logger.info("Class sessions: %d", session_count)

    # ── 10. Scheme of Work per term ──
    # Build subtopic_id → topic_key and topic_key → name lookups
    subtopic_to_topic: dict[str, str] = {}
    topic_name_map: dict[str, str] = {}
    for t in topics_data:
        topic_name_map[t["topic_key"]] = t["topic"]
        for st in t.get("subtopics", []):
            subtopic_to_topic[st["subtopic_id"]] = t["topic_key"]

    # Pre-compute week titles: "Topic - N" when a topic
    # spans multiple weeks, plain topic name otherwise.
    topic_week_count: dict[str, int] = {}
    for weeks in scheme_data.values():
        for wk in weeks:
            breakdown = wk.get("breakdown", [])
            for breakdown_item in breakdown:
                subtopic_id = breakdown_item.get("subtopic_id")
                if subtopic_id not in canonical_subtopic_ids:
                    raise ValueError(
                        f"Unknown canonical subtopic_id in scheme breakdown: {subtopic_id}"
                    )
            sids = [b["subtopic_id"] for b in breakdown]
            tkeys = list(
                dict.fromkeys(subtopic_to_topic[s] for s in sids if s in subtopic_to_topic)
            )
            wk["_topic_keys"] = tkeys
            label = " / ".join(topic_name_map.get(k, k) for k in tkeys)
            wk["_label"] = label
            topic_week_count.setdefault(label, 0)
            topic_week_count[label] += 1

    # Second pass: assign sequence numbers
    topic_seq: dict[str, int] = {}
    for weeks in scheme_data.values():
        for wk in weeks:
            label = wk["_label"]
            if topic_week_count[label] > 1:
                topic_seq.setdefault(label, 0)
                topic_seq[label] += 1
                wk["_title"] = f"{label} - {topic_seq[label]}"
            else:
                wk["_title"] = label

    sow_count = 0
    period_count = 0
    for term_name, weeks in scheme_data.items():
        tcs = await db.scalar(
            select(TermClassSubject).where(
                TermClassSubject.course_id == course.id,
                TermClassSubject.class_id == klass.id,
                TermClassSubject.term == term_name,
            )
        )
        if not tcs:
            tcs = TermClassSubject(
                course_id=course.id,
                class_id=klass.id,
                term=term_name,
                year=YEAR,
            )
            db.add(tcs)
            await db.flush()
        else:
            tcs.year = YEAR

        seen_week_numbers: set[int] = set()
        for wk in weeks:
            seen_week_numbers.add(int(wk["week"]))
            breakdown = wk.get("breakdown", [])
            deduped_periods: list[SchemeBreakdownItem] = []
            seen_subtopic_ids: set[str] = set()
            for item in breakdown:
                subtopic_id = item.get("subtopic_id")
                if not subtopic_id or subtopic_id in seen_subtopic_ids:
                    continue
                seen_subtopic_ids.add(subtopic_id)
                deduped_periods.append(item)

            sow = await db.scalar(
                select(SchemeOfWork).where(
                    SchemeOfWork.term_class_subject_id == tcs.id,
                    SchemeOfWork.week_number == wk["week"],
                )
            )
            if not sow:
                sow = SchemeOfWork(
                    term_class_subject_id=tcs.id,
                    week_number=wk["week"],
                    title=wk["_title"],
                    objectives={
                        "goals": [b["title"] for b in breakdown],
                    },
                )
                db.add(sow)
                await db.flush()
                sow_count += 1
            else:
                sow.title = wk["_title"]
                sow.objectives = {"goals": [item["title"] for item in breakdown]}

            existing_periods = list(
                await db.scalars(
                    select(LessonPeriod)
                    .where(LessonPeriod.scheme_of_work_id == sow.id)
                    .order_by(LessonPeriod.period_number.asc())
                )
            )
            for period_num, expected_period in enumerate(deduped_periods, start=1):
                if period_num <= len(existing_periods):
                    lesson_period = existing_periods[period_num - 1]
                    lesson_period.period_number = period_num
                    lesson_period.title = expected_period.get("title")
                    lesson_period.subtopic_id = expected_period.get("subtopic_id")
                    continue

                db.add(
                    LessonPeriod(
                        scheme_of_work_id=sow.id,
                        period_number=period_num,
                        title=expected_period.get("title"),
                        subtopic_id=expected_period.get("subtopic_id"),
                    )
                )
                period_count += 1

            if len(existing_periods) > len(deduped_periods):
                extra_period_ids = [
                    period.id for period in existing_periods[len(deduped_periods) :]
                ]
                await db.execute(delete(LessonPeriod).where(LessonPeriod.id.in_(extra_period_ids)))

        existing_weeks = list(
            await db.scalars(
                select(SchemeOfWork).where(SchemeOfWork.term_class_subject_id == tcs.id)
            )
        )
        extra_weeks = [week for week in existing_weeks if week.week_number not in seen_week_numbers]
        if extra_weeks:
            extra_week_ids = [week.id for week in extra_weeks]
            await db.execute(
                delete(LessonPeriod).where(LessonPeriod.scheme_of_work_id.in_(extra_week_ids))
            )
            await db.execute(delete(SchemeOfWork).where(SchemeOfWork.id.in_(extra_week_ids)))
    await db.flush()
    logger.info(
        "Scheme weeks: %d, Lesson periods: %d",
        sow_count,
        period_count,
    )

    # ── 11. Reference material (Siyavula textbook) ──
    ref_mat = await db.scalar(
        select(ReferenceMaterial).where(ReferenceMaterial.source_id == TEXTBOOK_SOURCE_ID)
    )
    if not ref_mat:
        # Collect all topic keys covered by the textbook
        all_topic_keys = [t["topic_key"] for t in topics_data]
        ref_mat = ReferenceMaterial(
            source_id=TEXTBOOK_SOURCE_ID,
            type="textbook",
            title="Siyavula JSS1 Mathematics",
            subject=SUBJECT,
            track=TRACK,
            grade=GRADE,
            license="CC-BY",
            topics=all_topic_keys,
            chunk_refs=[],
        )
        db.add(ref_mat)
        await db.flush()
    else:
        ref_mat.subject = SUBJECT
        ref_mat.track = TRACK
        ref_mat.grade = GRADE
        ref_mat.title = "Siyavula JSS1 Mathematics"

    logger.info(
        "Skipping textbook section and mapping seed. "
        "Record-level textbook seeding now runs through the dedicated textbook scripts."
    )

    # ── 14. Knowledge components ──
    from app.domains.curriculum.models.knowledge_components import (
        KnowledgeComponent,
    )

    known_subtopics = {
        str(subtopic.get("subtopic_id"))
        for topic in topics_data
        for subtopic in topic.get("subtopics", [])
        if isinstance(subtopic, dict) and subtopic.get("subtopic_id")
    }

    kc_data = load_json_rows(DATASET / "curriculum" / "jss1_knowledge_components.json")
    kc_count = 0
    kc_skipped = 0
    for kc in kc_data:
        if kc["subtopic_id"] not in known_subtopics:
            kc_skipped += 1
            continue
        existing_kc = await db.scalar(
            select(KnowledgeComponent).where(KnowledgeComponent.kc_code == kc["kc_code"])
        )
        if existing_kc is None:
            db.add(
                KnowledgeComponent(
                    kc_code=kc["kc_code"],
                    subtopic_id=kc["subtopic_id"],
                    description=kc["description"],
                    bloom_level=kc["bloom_level"],
                )
            )
            kc_count += 1
    await db.flush()
    logger.info(
        "Knowledge components: %d (skipped %d orphaned)",
        kc_count,
        kc_skipped,
    )

    # ── 15. Seed teacher + workspace ──
    # The canonical teacher persona — scripts/seed_minimal_users.py grants the
    # casbin role for this login (idempotent on the existing user).
    teacher_auth = "code|teacher-1"
    teacher = await db.scalar(select(User).where(User.auth_id == teacher_auth))
    if not teacher:
        teacher = User(
            auth_id=teacher_auth,
            email="teacher-1@seed.local",
            full_name="Teacher One",
            role="teacher",
        )
        db.add(teacher)
        await db.flush()
        await db.flush()

    for term_name in ("First Term", "Second Term", "Third Term"):
        term_class_subject = await db.scalar(
            select(TermClassSubject).where(
                TermClassSubject.course_id == course.id,
                TermClassSubject.class_id == klass.id,
                TermClassSubject.term == term_name,
            )
        )
        if term_class_subject is None:
            continue

        workspace = await db.scalar(
            select(TeacherWorkspace).where(
                TeacherWorkspace.teacher_id == teacher.id,
                TeacherWorkspace.term_class_subject_id == term_class_subject.id,
            )
        )
        if workspace is None:
            db.add(
                TeacherWorkspace(
                    teacher_id=teacher.id,
                    term_class_subject_id=term_class_subject.id,
                    is_primary=(term_name == "First Term"),
                )
            )
            continue

        workspace.is_primary = term_name == "First Term"

    # ── 16. Sample JSS1 students ──
    student_names = [
        "Adebayo Oluwaseun",
        "Chidinma Okafor",
        "Fatimah Ibrahim",
        "Emeka Nwankwo",
        "Aisha Mohammed",
        "Chukwuemeka Obi",
        "Ngozi Eze",
        "Oluwadamilola Adeyemi",
        "Hauwa Abdullahi",
        "Ifeanyi Okoro",
    ]
    student_count = 0
    for name in student_names:
        existing_learner = await db.scalar(
            select(LearnerProfile).where(LearnerProfile.full_name == name)
        )
        if existing_learner is None:
            db.add(
                LearnerProfile(
                    student_id=new_public_id(PublicIdPrefix.LEARNER),
                    full_name=name,
                    grade=GRADE,
                    track=TRACK,
                    class_id=klass.id,
                    language_level="simple",
                    pace_preference="moderate",
                    time_budget_minutes=40,
                )
            )
            student_count += 1
    await db.flush()
    logger.info("Students: %d", student_count)

    await db.commit()
    logger.info("JSS1 Mathematics curriculum seeded.")


async def main() -> None:
    from app.db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        await ensure_default_school(session=db)
        await seed_jss1(db)


if __name__ == "__main__":
    asyncio.run(main())
