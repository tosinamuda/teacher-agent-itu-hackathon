"""Curriculum query routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.curriculum.application.service import CurriculumApplicationService

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


@router.get("/topics")
async def list_topics(
    subject: str | None = None,
    track: str | None = None,
    grade: str | None = None,
    term: str | None = None,
    week: int | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, object]]:
    service = CurriculumApplicationService()
    topics = await service.list_topics(
        db=db,
        subject=subject,
        track=track,
        grade=grade,
        term=term,
        week=week,
        limit=limit,
    )
    return [
        {
            "topic_key": topic.topic_key,
            "subject": topic.subject,
            "track": topic.track,
            "grade": topic.grade,
            "term": topic.term,
            "week": topic.week,
            "topic": topic.topic,
            "general_objectives": topic.general_objectives,
        }
        for topic in topics
    ]


@router.get("/sessions")
async def list_sessions(
    subject: str | None = None,
    track: str | None = None,
    grade: str | None = None,
    term: str | None = None,
    week: int | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, object]]:
    service = CurriculumApplicationService()
    sessions = await service.list_sessions(
        db=db,
        subject=subject,
        track=track,
        grade=grade,
        term=term,
        week=week,
        limit=limit,
    )
    return [
        {
            "session_id": session.session_id,
            "subject": session.subject,
            "track": session.track,
            "grade": session.grade,
            "term": session.term,
            "week": session.week,
            "day_index": session.day_index,
            "topic_key": session.topic_key,
            "subtopic_id": session.subtopic_id,
            "subtopic_title": subtopic.title,
            "session_objectives": session.session_objectives,
        }
        for session, subtopic in sessions
    ]
