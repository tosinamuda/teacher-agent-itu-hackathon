"""Minimal evaluation for lesson plan generator."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

from app.db.session import AsyncSessionLocal
from app.domains.artefacts.types.lesson_plan.drafting.deps import (
    get_lesson_generation_service,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.service import (
    validate_session_plan,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import (
    build_session_context,
)

load_dotenv(override=False)

BASE_DIR = Path(__file__).resolve().parents[1]


def _json_list_len(value: object) -> int:
    return len(value) if isinstance(value, list) else 0


async def main() -> None:
    session_id = os.getenv("EVAL_SESSION_ID")

    async with AsyncSessionLocal() as db:
        if session_id is None:
            result = await db.execute(
                text("SELECT session_id FROM class_sessions ORDER BY session_id LIMIT 1")
            )
            first_session = result.scalars().first()
            if first_session is None:
                raise RuntimeError("No sessions found; seed the database first.")
            session_id = first_session

        context = await build_session_context(db, session_id)
        if context is None:
            raise RuntimeError(f"Session not found: {session_id}")

        generator = get_lesson_generation_service()
        generation = await generator.generate(
            session_context={
                "session_id": context.session_id,
                "subject": context.subject,
                "track": context.track,
                "grade": context.grade,
                "term": context.term,
                "week": context.week,
                "day_index": context.day_index,
                "topic": context.topic,
                "subtopic": context.subtopic,
                "duration_minutes": context.duration_minutes,
                "session_objectives": list(context.session_objectives),
            },
            curriculum_context={
                "topic": context.topic,
                "general_objectives": list(context.general_objectives),
                "session_objectives": list(context.session_objectives),
            },
            reference_context=context.reference_materials,
        )

    errors = validate_session_plan(generation.session_plan)

    report = {
        "session_id": session_id,
        "valid_schema": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors[:5],
        "session_plan_steps": _json_list_len(generation.session_plan.get("steps")),
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
