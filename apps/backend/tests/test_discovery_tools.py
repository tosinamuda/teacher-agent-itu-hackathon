"""A tools-only client can list the types, find a lesson, read it, and read a draft in part."""

from __future__ import annotations

import json
import uuid

import pytest
from mcp import Client
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content_engine.mcp.caller import as_the_app
from app.domains.content_engine.mcp.discovery_tools import MOST_LESSONS, _lessons_of
from app.domains.curriculum.models.curriculum import CurriculumSubtopic
from app.domains.school.models.structure import Class, Course
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models.syllabus import LessonPeriod, SchemeOfWork
from app.domains.teaching.models.workspace import TeacherWorkspace
from tests.content_engine_support import PLAN, TYPE, part, seed_lesson, server_over

pytestmark = pytest.mark.asyncio


async def _teach(db: AsyncSession, teacher_id: uuid.UUID, topics: list[str]) -> list[uuid.UUID]:
    """A teacher with a class, and a lesson period for each topic, one per week."""
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    course_id, class_id, tcs_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    db.add_all(
        [
            Course(
                id=course_id,
                name="JSS1 Mathematics",
                subject_id=uuid.uuid4(),
                grade_level_id=uuid.uuid4(),
            ),
            Class(id=class_id, name="JSS1A", school_id=uuid.uuid4(), grade_level_id=uuid.uuid4()),
            TermClassSubject(
                id=tcs_id, course_id=course_id, class_id=class_id, term="First Term", year="2026"
            ),
            TeacherWorkspace(teacher_id=teacher_id, term_class_subject_id=tcs_id),
        ]
    )
    periods: list[uuid.UUID] = []
    for week, topic in enumerate(topics, start=1):
        week_id, period_id = uuid.uuid4(), uuid.uuid4()
        subtopic_id = f"sub-{teacher_id.hex[:6]}-{week}"
        db.add_all(
            [
                CurriculumSubtopic(
                    subtopic_id=subtopic_id,
                    topic_key="topic-x",
                    title=topic,
                    performance_objectives=[],
                ),
                SchemeOfWork(
                    id=week_id, term_class_subject_id=tcs_id, week_number=week, title=f"W{week}"
                ),
                LessonPeriod(
                    id=period_id,
                    scheme_of_work_id=week_id,
                    period_number=1,
                    title=None,
                    subtopic_id=subtopic_id,
                ),
            ]
        )
        periods.append(period_id)
    await db.flush()
    return periods


async def test_a_teachers_lessons_are_found_in_the_order_taught(db: AsyncSession) -> None:
    teacher = uuid.uuid4()
    periods = await _teach(db, teacher, ["Trillions", "LCM of whole numbers"])
    await _teach(db, uuid.uuid4(), ["Someone else's topic"])

    found = await _lessons_of(db, teacher, None)

    assert [lesson["lesson_id"] for lesson in found] == [str(p) for p in periods]
    assert found[1] == {
        "lesson_id": str(periods[1]),
        "course": "JSS1 Mathematics",
        "class": "JSS1A",
        "term": "First Term",
        "year": "2026",
        "week": 2,
        "week_title": "W2",
        "period": 1,
        "topic": "LCM of whole numbers",
        "plan_id": None,
    }


async def test_every_word_of_the_query_must_match(db: AsyncSession) -> None:
    teacher = uuid.uuid4()
    periods = await _teach(db, teacher, ["Trillions", "LCM of whole numbers"])

    assert [x["lesson_id"] for x in await _lessons_of(db, teacher, "lcm week 2")] == [
        str(periods[1])
    ]
    assert await _lessons_of(db, teacher, "lcm trillions") == []
    assert len(await _lessons_of(db, teacher, "jss1a")) == 2


async def test_no_more_lessons_than_the_limit_are_returned(db: AsyncSession) -> None:
    teacher = uuid.uuid4()
    await _teach(db, teacher, [f"Topic {n}" for n in range(MOST_LESSONS + 5)])

    assert len(await _lessons_of(db, teacher, None)) == MOST_LESSONS


async def test_the_lesson_of_a_draft_is_read_with_a_tool_as_with_the_resource(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            draft = json.loads(started.content[0].text)  # type: ignore[union-attr]
            by_tool = await client.call_tool("read_lesson", {"draft_id": draft["draft_id"]})
            by_resource = await client.read_resource(draft["lesson_uri"])

    assert json.loads(by_tool.content[0].text) == json.loads(  # type: ignore[union-attr]
        by_resource.contents[0].text  # type: ignore[union-attr]
    )


async def test_a_draft_is_read_in_part_when_fields_are_named(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            draft_id = json.loads(started.content[0].text)["draft_id"]  # type: ignore[union-attr]
            await client.call_tool(
                "add_part", {"draft_id": draft_id, "unit_id": "s1", "part": part("A")}
            )
            whole = await client.call_tool("read_draft", {"draft_id": draft_id})
            some = await client.call_tool(
                "read_draft", {"draft_id": draft_id, "fields": ["missing", "issues"]}
            )

    assert set(json.loads(some.content[0].text)) == {"draft_id", "missing", "issues"}  # type: ignore[union-attr]
    assert "part_schemas" in json.loads(whole.content[0].text)  # type: ignore[union-attr]
    assert len(some.content[0].text) < len(whole.content[0].text) / 4  # type: ignore[union-attr]


async def test_the_types_are_listed_with_what_they_are_made_from_and_whether_they_are_drafted(
    db,  # type: ignore[no-untyped-def]
) -> None:
    await seed_lesson(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            listed = await client.call_tool("list_content_types", {})

    types = {t["type"]: t for t in json.loads(listed.content[0].text)["types"]}  # type: ignore[union-attr]
    assert types[TYPE]["draftable"] is True
    assert types[TYPE]["made_from"] == "plan_version_id"
    assert types["lesson-plan"]["made_from"] == "session_id"
    assert types["lesson-plan"]["draftable"] is True
    assert types["class-test"]["draftable"] is False
    assert "material" in types[TYPE]
