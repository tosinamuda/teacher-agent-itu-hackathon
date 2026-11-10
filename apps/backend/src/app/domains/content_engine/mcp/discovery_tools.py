"""Tools that find a teacher's lessons, list the types, and read a lesson, for a tools-only client.

A client that reads MCP resources can read ``content-types://``, ``lesson-period://`` and
``lesson://``. A model in a host that passes only tools to it has no other way to learn what can
be written, to find a lesson to write for, or to read what it is about, so these say the same
things as tools.
"""

from __future__ import annotations

from collections.abc import Callable

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ToolError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import LessonPlan
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content_engine.application.drafting import DraftingService
from app.domains.content_engine.mcp.caller import caller, permit, permit_planning
from app.domains.content_engine.mcp.refusals import Sessions, refusing
from app.domains.content_engine.mcp.views import Payload, as_payload
from app.domains.curriculum.models.curriculum import CurriculumSubtopic
from app.domains.school.models.structure import Class, Course
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models.syllabus import LessonPeriod, SchemeOfWork
from app.domains.teaching.models.workspace import TeacherWorkspace
from app.shared.json_types import JsonObject

#: The most lessons one search returns.
MOST_LESSONS = 25


async def _lessons_of(db: AsyncSession, teacher_id: object, query: str | None) -> list[JsonObject]:
    """The lessons of the teacher's classes that the query names, in the order they are taught."""
    plan = (
        select(LessonPlan.lesson_period_id, func.max(LessonPlan.plan_id).label("plan_id"))
        .group_by(LessonPlan.lesson_period_id)
        .subquery()
    )
    stmt = (
        select(
            LessonPeriod.id,
            LessonPeriod.period_number,
            SchemeOfWork.week_number,
            SchemeOfWork.title,
            CurriculumSubtopic.title,
            Course.name,
            Class.name,
            TermClassSubject.term,
            TermClassSubject.year,
            plan.c.plan_id,
        )
        .select_from(TeacherWorkspace)
        .join(
            SchemeOfWork,
            SchemeOfWork.term_class_subject_id == TeacherWorkspace.term_class_subject_id,
        )
        .join(LessonPeriod, LessonPeriod.scheme_of_work_id == SchemeOfWork.id)
        .join(TermClassSubject, TermClassSubject.id == SchemeOfWork.term_class_subject_id)
        .join(Course, Course.id == TermClassSubject.course_id)
        .join(Class, Class.id == TermClassSubject.class_id)
        .outerjoin(CurriculumSubtopic, CurriculumSubtopic.subtopic_id == LessonPeriod.subtopic_id)
        .outerjoin(plan, plan.c.lesson_period_id == LessonPeriod.id)
        .where(TeacherWorkspace.teacher_id == teacher_id)
        .order_by(TermClassSubject.year, TermClassSubject.term, SchemeOfWork.week_number)
    )
    wanted = (query or "").casefold().split()
    found: list[JsonObject] = []
    for row in (await db.execute(stmt)).all():
        (period_id, period, week, week_title, topic, course, classroom, term, year, plan_id) = row
        lesson: JsonObject = {
            "lesson_id": str(period_id),
            "course": course,
            "class": classroom,
            "term": term,
            "year": year,
            "week": week,
            "week_title": week_title,
            "period": period,
            "topic": topic,
            "plan_id": plan_id,
        }
        said = [*(str(value) for value in lesson.values() if value is not None)]
        text = " ".join([*said, f"week {week}", f"period {period}"]).casefold()
        if all(word in text for word in wanted):
            found.append(lesson)
    return found[:MOST_LESSONS]


def add_discovery_tools(
    server: MCPServer,
    drafting: Callable[[], DraftingService],
    catalogue: Callable[[], ContentCatalogue],
    sessions: Sessions,
) -> None:
    @server.tool()
    async def list_content_types(ctx: Context) -> Payload:
        """The types of content there are, and which can be drafted with these tools.

        Each has the type to give start_draft, what it is, who it is for, and what it is made
        from: a lesson's session_id (a lesson plan) or a plan_version_id (the rest). Read a
        type's whole spec and part schema from the content-type:// resource, or from the brief
        start_draft returns.
        """
        async with sessions() as db:
            await refusing(permit(db, await caller(db, ctx.headers), "read"))
            service = drafting()
            return {
                "types": [
                    {
                        "type": t.slug,
                        "label": t.label,
                        "material": spec.material,
                        "audience": t.audience.value,
                        "made_from": "plan_version_id"
                        if t.made_from_a_plan_version
                        else "session_id",
                        "draftable": await service.drafts(db, t),
                    }
                    for t, spec in await catalogue().types(db)
                ]
            }

    @server.tool()
    async def find_lessons(ctx: Context, query: str | None = None) -> Payload:
        """The lessons of the caller's own classes, in the order they are taught.

        Give words of what you look for, such as a topic, a week or a class; every word must
        match. Each lesson has a lesson_id, which is the session_id that start_draft takes to
        write a lesson plan, and a plan_id when it already has a plan, which is the content_id
        of that plan.
        """
        async with sessions() as db:
            signed_in = await caller(db, ctx.headers)
            actor = signed_in.actor
            if actor is None or actor.teacher_id is None:
                raise ToolError("only a teacher has lessons of their own to find")
            await refusing(permit(db, signed_in, "read"))
            lessons = await _lessons_of(db, actor.teacher_id, query)
        return {"count": len(lessons), "lessons": [*lessons]}

    @server.tool()
    async def read_lesson(draft_id: str, ctx: Context) -> Payload:
        """What a writer may read about the lesson a draft is for.

        It is what the draft's lesson_uri holds: for a lesson plan, the lesson's subject, topic
        and curriculum objectives; for other types, the lesson's plan and approved note.
        """
        async with sessions() as db:
            signed_in = await caller(db, ctx.headers)
            view = await refusing(drafting().read(db, draft_id=draft_id, by=signed_in.by))
            draft = view.draft
            if draft.session_id is not None:
                await refusing(permit_planning(db, signed_in, draft.session_id))
                lesson = await refusing(drafting().lesson_period(db, draft.session_id))
            elif draft.plan_version_id is not None:
                await refusing(permit(db, signed_in, "read", plan_version_id=draft.plan_version_id))
                lesson = await refusing(drafting().lesson(db, draft.plan_version_id))
            else:
                raise ToolError("the draft is not for a lesson")
            return as_payload(lesson)
