"""Writing a lesson plan, from a teacher's document or from the curriculum, as a job."""

from __future__ import annotations

from app.db.session import AsyncSessionLocal
from app.domains.content.domain.types import BuiltIn
from app.domains.content.infrastructure.wiring import build_content_engine, build_plan_generator
from app.domains.content_engine.infrastructure.engine import Request
from app.domains.experiments.application.experiment_authoring import bind_experiment_plan_version
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)
from app.shared.json_types import JsonObject


async def import_lesson_plan(
    session_id: str,
    document: str,
    for_teacher: str | None = None,
    experiment_id: str | None = None,
) -> JsonObject:
    """Write the plan and save it as a draft for the teacher; bind it to the experiment named.

    Says where the plan is.
    """
    imported = await build_content_engine().build(
        Request(type=BuiltIn.LESSON_PLAN.value, session_id=session_id, source=document),
        for_teacher=for_teacher,
    )
    if experiment_id is not None:
        async with AsyncSessionLocal() as db:
            await bind_experiment_plan_version(
                SqlAlchemyExperimentStore(db),
                experiment_id=experiment_id,
                plan_version_id=imported.saved_as,
            )
    return {"plan_version_id": imported.saved_as, "summary": imported.summary}


async def generate_lesson_plan(session_id: str, for_teacher: str | None = None) -> JsonObject:
    """Write the lesson's plan from the curriculum and the textbook, and say where it is."""
    async with AsyncSessionLocal() as db:
        drafted = await build_plan_generator().draft(
            db, session_id=session_id, for_teacher=for_teacher
        )
    return {"plan_id": drafted.plan_id, "version_id": drafted.version_id}
