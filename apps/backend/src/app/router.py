"""Every route the API serves, gathered from the domains in one router."""

from __future__ import annotations

from fastapi import APIRouter

from app.domains.artefact_revision.api import routes as artefact_revision
from app.domains.artefacts.core.api import routes as artefacts
from app.domains.assessments.api import routes as assessments
from app.domains.assessments.api import study_classwork
from app.domains.attachments.api import routes as attachments
from app.domains.content.api import chat_routes as content_chats
from app.domains.content.api import file_routes as content_files
from app.domains.content.api import plugin_routes as content_plugins
from app.domains.content.api import preference_routes as content_preferences
from app.domains.content.api import routes as content
from app.domains.content.api import skill_routes as content_skills
from app.domains.content_engine.api import routes as plan_imports
from app.domains.curriculum.api import routes as curriculum
from app.domains.evaluation.api import routes as evaluation
from app.domains.evaluation.api import study_ratings
from app.domains.events.api import routes as events
from app.domains.events.api import summary_routes as event_summaries
from app.domains.experiments.api import investigation_routes as investigations
from app.domains.experiments.api import record_routes as experiment_records
from app.domains.experiments.api import routes as experiments
from app.domains.expert_content.api import routes as expert_content
from app.domains.figures.api import routes as figures
from app.domains.jobs.api import routes as jobs
from app.domains.learners.api import routes as learners
from app.domains.ops.api import routes as ops
from app.domains.school.api import routes as school
from app.domains.teaching.api import routes as teaching
from app.domains.tutor.api import routes as tutor
from app.domains.users.api import routes as users

#: In the order they are matched. Order matters only where paths overlap: investigations
#: come before experiments, so /experiments/investigations reaches its own route first.
_DOMAIN_ROUTERS: tuple[APIRouter, ...] = (
    users.router,
    assessments.router,
    attachments.router,
    artefacts.router,
    artefact_revision.router,
    # Before content: its /content/{content_id} would otherwise take /content/skills and /plugins.
    content_skills.router,
    content_plugins.router,
    content_preferences.router,
    content_chats.router,
    content_files.router,
    content.router,
    plan_imports.router,
    curriculum.router,
    evaluation.router,
    study_ratings.router,
    figures.router,
    study_classwork.router,
    events.router,
    event_summaries.router,
    expert_content.router,
    investigations.router,
    experiments.router,
    experiment_records.router,
    jobs.router,
    learners.router,
    ops.router,
    school.router,
    teaching.router,
    tutor.router,
)

api_router = APIRouter()
for _domain_router in _DOMAIN_ROUTERS:
    api_router.include_router(_domain_router)


@api_router.get("/")
async def root() -> dict[str, str]:
    return {"message": "Backend API is running"}


@api_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
