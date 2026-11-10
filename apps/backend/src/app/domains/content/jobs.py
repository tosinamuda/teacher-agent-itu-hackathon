"""Generating content of any type as a job."""

from __future__ import annotations

from app.db.session import AsyncSessionLocal
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.domain.types import Level
from app.domains.content.infrastructure.wiring import build_content_service
from app.shared.json_types import JsonObject


def generation_subject(plan_version_id: str, type: str, level: Level) -> str:
    """What one generation acts on: asking again for the same one follows the same job."""
    return f"{plan_version_id}:{type}:{level.value}"


async def generate_content(
    plan_version_id: str,
    type: str,
    level: str,
    pipeline: str | None = None,
    sources: str | None = None,
    instructions: str | None = None,
) -> JsonObject:
    """Make the content, and say where it is."""
    async with AsyncSessionLocal() as db:
        item = await build_content_service().generate(
            db,
            plan_version_id=plan_version_id,
            type=type,
            level=Level(level),
            choices=GenerationChoices(
                pipeline=pipeline, sources=sources, instructions=instructions
            ),
        )
    return {"content_id": item.record.content_id}
