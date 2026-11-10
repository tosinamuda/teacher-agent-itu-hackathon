"""Verify or repair the canonical JSS1 Mathematics baseline."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import TypedDict, cast

from sqlalchemy import select

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.default_school import ensure_default_school
from app.db.metadata import target_metadata  # noqa: F401
from app.db.session import AsyncSessionLocal
from app.domains.curriculum.models.curriculum import CurriculumSubtopic, CurriculumTopic
from app.domains.curriculum.models.themes import CurriculumTheme
from app.domains.school.models import Class, School, Subject, TermClassSubject
from app.domains.school.models.structure import Course
from app.domains.teaching.models import LessonPeriod, SchemeOfWork
from app.domains.teaching.models.workspace import TeacherWorkspace
from app.domains.users.models import User
from scripts.seed_jss1_curriculum import (
    DATASET,
    GRADE,
    SCHOOL_CODE,
    SUBJECT,
    SUBJECT_CODE,
    load_json_rows,
    seed_jss1,
)


class SchemeBreakdownItem(TypedDict):
    title: str
    subtopic_id: str


class SchemeWeek(TypedDict):
    week: int
    breakdown: list[SchemeBreakdownItem]


def load_scheme_data() -> dict[str, list[SchemeWeek]]:
    raw_data = json.loads(
        (DATASET / "scheme-of-work" / "jss1_scheme.json").read_text(encoding="utf-8")
    )
    if not isinstance(raw_data, dict):
        raise ValueError("Expected dict-based scheme-of-work dataset.")
    return cast(dict[str, list[SchemeWeek]], raw_data)


def canonical_period_map() -> dict[str, dict[int, list[str]]]:
    scheme_data = load_scheme_data()
    period_map: dict[str, dict[int, list[str]]] = {}
    for term_name, weeks in scheme_data.items():
        term_periods: dict[int, list[str]] = {}
        for week in weeks:
            seen_subtopic_ids: set[str] = set()
            ordered_subtopic_ids: list[str] = []
            for breakdown_item in week.get("breakdown", []):
                subtopic_id = breakdown_item.get("subtopic_id")
                if not subtopic_id or subtopic_id in seen_subtopic_ids:
                    continue
                seen_subtopic_ids.add(subtopic_id)
                ordered_subtopic_ids.append(subtopic_id)
            term_periods[int(week["week"])] = ordered_subtopic_ids
        period_map[str(term_name)] = term_periods
    return period_map


async def verify_baseline(*, repair: bool) -> int:
    async with AsyncSessionLocal() as db:
        await ensure_default_school(session=db)
        if repair:
            await seed_jss1(db)

        issues: list[str] = []
        topics_data = load_json_rows(DATASET / "curriculum" / "jss1_topics_enriched.json")
        themes_data = load_json_rows(DATASET / "curriculum" / "jss1_themes.json")
        expected_periods = canonical_period_map()

        subject = (
            (await db.execute(select(Subject).where(Subject.code == SUBJECT_CODE)))
            .scalars()
            .first()
        )
        if subject is None:
            issues.append("Missing Mathematics subject with code MATH.")
        elif subject.name != SUBJECT:
            issues.append(
                "Wrong subject ownership for "
                f"{SUBJECT_CODE}: expected {SUBJECT}, found {subject.name}."
            )

        school = (
            (await db.execute(select(School).where(School.code == SCHOOL_CODE))).scalars().first()
        )
        if school is None:
            issues.append(f"Missing canonical school with code {SCHOOL_CODE}.")

        klass = None
        if school is not None:
            klass = (
                (
                    await db.execute(
                        select(Class).where(
                            Class.name == GRADE,
                            Class.school_id == school.id,
                        )
                    )
                )
                .scalars()
                .first()
            )
        if klass is None:
            issues.append("Missing canonical JSS1 class linked to the canonical school.")

        canonical_theme_keys = {str(theme["key"]) for theme in themes_data}
        theme_rows = (
            (
                await db.execute(
                    select(CurriculumTheme).where(
                        CurriculumTheme.theme_key.in_(canonical_theme_keys)
                    )
                )
            )
            .scalars()
            .all()
        )
        found_theme_keys = {theme.theme_key for theme in theme_rows}
        missing_theme_keys = sorted(canonical_theme_keys - found_theme_keys)
        for theme_key in missing_theme_keys:
            issues.append(f"Missing curriculum theme: {theme_key}.")

        canonical_topic_keys = {str(topic["topic_key"]) for topic in topics_data}
        topic_rows = (
            (
                await db.execute(
                    select(CurriculumTopic).where(
                        CurriculumTopic.topic_key.in_(canonical_topic_keys)
                    )
                )
            )
            .scalars()
            .all()
        )
        topic_by_key = {topic.topic_key: topic for topic in topic_rows}
        for topic in topics_data:
            topic_key = str(topic["topic_key"])
            topic_row = topic_by_key.get(topic_key)
            if topic_row is None:
                issues.append(f"Missing curriculum topic: {topic_key}.")
                continue
            if topic_row.subject != SUBJECT:
                issues.append(
                    f"Wrong subject ownership for topic {topic_key}: {topic_row.subject}."
                )
            if topic_row.theme_id is None:
                issues.append(f"Missing theme linkage for topic {topic_key}.")

        canonical_subtopic_map = {
            str(subtopic["subtopic_id"]): str(topic["topic_key"])
            for topic in topics_data
            for subtopic in topic.get("subtopics", [])
        }
        subtopic_rows = (
            (
                await db.execute(
                    select(CurriculumSubtopic).where(
                        CurriculumSubtopic.subtopic_id.in_(canonical_subtopic_map.keys())
                    )
                )
            )
            .scalars()
            .all()
        )
        subtopic_by_id = {subtopic.subtopic_id: subtopic for subtopic in subtopic_rows}
        for subtopic_id, expected_topic_key in canonical_subtopic_map.items():
            subtopic_row = subtopic_by_id.get(subtopic_id)
            if subtopic_row is None:
                issues.append(f"Missing curriculum subtopic: {subtopic_id}.")
                continue
            if subtopic_row.topic_key != expected_topic_key:
                issues.append(
                    "Wrong topic linkage for "
                    "subtopic "
                    f"{subtopic_id}: expected {expected_topic_key}, "
                    f"found {subtopic_row.topic_key}."
                )

        if subject is not None and klass is not None:
            course = (
                (
                    await db.execute(
                        select(Course).where(
                            Course.subject_id == subject.id,
                            Course.grade_level_id == klass.grade_level_id,
                        )
                    )
                )
                .scalars()
                .first()
            )
            if course is None:
                issues.append("Missing canonical JSS1 Mathematics course.")
            else:
                for term_name, weeks in expected_periods.items():
                    term_class_subject = (
                        (
                            await db.execute(
                                select(TermClassSubject).where(
                                    TermClassSubject.course_id == course.id,
                                    TermClassSubject.class_id == klass.id,
                                    TermClassSubject.term == term_name,
                                )
                            )
                        )
                        .scalars()
                        .first()
                    )
                    if term_class_subject is None:
                        issues.append(f"Missing term-class-subject row for {term_name}.")
                        continue

                    for week_number, expected_subtopic_ids in weeks.items():
                        scheme_row = (
                            (
                                await db.execute(
                                    select(SchemeOfWork).where(
                                        SchemeOfWork.term_class_subject_id == term_class_subject.id,
                                        SchemeOfWork.week_number == week_number,
                                    )
                                )
                            )
                            .scalars()
                            .first()
                        )
                        if scheme_row is None:
                            issues.append(
                                f"Missing scheme-of-work row for {term_name} week {week_number}."
                            )
                            continue

                        period_rows = (
                            (
                                await db.execute(
                                    select(LessonPeriod)
                                    .where(LessonPeriod.scheme_of_work_id == scheme_row.id)
                                    .order_by(LessonPeriod.period_number.asc())
                                )
                            )
                            .scalars()
                            .all()
                        )
                        actual_subtopic_ids = [period.subtopic_id for period in period_rows]
                        if any(subtopic_id is None for subtopic_id in actual_subtopic_ids):
                            issues.append(
                                f"Unlinked lesson period in {term_name} week {week_number}."
                            )
                        actual_clean_ids = [
                            subtopic_id for subtopic_id in actual_subtopic_ids if subtopic_id
                        ]
                        if actual_clean_ids != expected_subtopic_ids:
                            issues.append(
                                "Lesson-period linkage mismatch for "
                                f"{term_name} week {week_number}: "
                                f"expected {expected_subtopic_ids}, found {actual_clean_ids}."
                            )

        if school is not None and klass is not None:
            contamination_rows = (
                await db.execute(
                    select(User.auth_id, Subject.name, TermClassSubject.term)
                    .join(TeacherWorkspace, TeacherWorkspace.teacher_id == User.id)
                    .join(
                        TermClassSubject,
                        TermClassSubject.id == TeacherWorkspace.term_class_subject_id,
                    )
                    .join(Course, Course.id == TermClassSubject.course_id)
                    .join(Subject, Subject.id == Course.subject_id)
                    .where(
                        TermClassSubject.class_id == klass.id,
                        Subject.code != SUBJECT_CODE,
                    )
                    .order_by(User.auth_id, Subject.name, TermClassSubject.term)
                )
            ).all()
            for teacher_auth_id, subject_name, term_name in contamination_rows:
                issues.append(
                    "Non-canonical PTRS JSS1 workspace row detected for "
                    f"{teacher_auth_id}: {subject_name} / {term_name}."
                )

        if subject is not None and klass is not None:
            course = (
                (
                    await db.execute(
                        select(Course).where(
                            Course.subject_id == subject.id,
                            Course.grade_level_id == klass.grade_level_id,
                        )
                    )
                )
                .scalars()
                .first()
            )
            teacher = (
                (await db.execute(select(User).where(User.auth_id == "code|uncle-tosin")))
                .scalars()
                .first()
            )
            if course is not None and teacher is not None:
                workspace_rows = (
                    await db.execute(
                        select(TermClassSubject.term, Subject.code)
                        .join(
                            TeacherWorkspace,
                            TeacherWorkspace.term_class_subject_id == TermClassSubject.id,
                        )
                        .join(Course, Course.id == TermClassSubject.course_id)
                        .join(Subject, Subject.id == Course.subject_id)
                        .where(
                            TeacherWorkspace.teacher_id == teacher.id,
                            TermClassSubject.class_id == klass.id,
                            TermClassSubject.course_id == course.id,
                        )
                        .order_by(TermClassSubject.term.asc())
                    )
                ).all()
                expected_terms = {"First Term", "Second Term", "Third Term"}
                actual_terms = {term for term, _subject_code in workspace_rows}
                missing_terms = sorted(expected_terms - actual_terms)
                for term_name in missing_terms:
                    issues.append(
                        f"Missing canonical teacher workspace for uncle-tosin in {term_name}."
                    )
                wrong_subject_terms = [
                    term_name
                    for term_name, subject_code in workspace_rows
                    if subject_code != SUBJECT_CODE
                ]
                for term_name in wrong_subject_terms:
                    issues.append(
                        "Wrong subject on canonical teacher workspace for "
                        f"uncle-tosin in {term_name}."
                    )

        if issues:
            print("JSS1 baseline verification failed:")
            for issue in issues:
                print(f"- {issue}")
            return 1

        print("JSS1 Mathematics baseline verified.")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repair",
        action="store_true",
        help="Run the canonical JSS1 seed first, then verify.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(asyncio.run(verify_baseline(repair=parse_args().repair)))
