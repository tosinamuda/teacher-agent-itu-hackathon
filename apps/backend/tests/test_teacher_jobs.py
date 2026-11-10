"""A teacher's long generations run as jobs the page follows, and only they may follow them."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.content_engine.infrastructure.plan_generator import DraftedPlan
from app.domains.experiments import jobs as experiment_jobs
from app.domains.experiments.infrastructure.models import Experiment
from app.infra.jobs.kinds import AUTHOR_EXPERIMENT_PLAN
from app.infra.jobs.models import Job
from app.infra.jobs.queue import JobQueue
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from tests.queued_jobs import run_queued_job

pytestmark = pytest.mark.asyncio

TEACHER = Actor(role="teacher", auth_id="code|teacher-1", full_name="Teacher One")
OTHER_TEACHER = Actor(role="teacher", auth_id="code|teacher-2", full_name="Teacher Two")
ADMIN = Actor(role="admin", auth_id="code|admin", full_name="Admin")
MANAGER = Actor(role="research_manager", auth_id="code|researcher", full_name="Researcher")
ANONYMOUS = Actor(role="anonymous", auth_id="anonymous")


class _Caller:
    def __init__(self) -> None:
        self.actor = TEACHER


@pytest_asyncio.fixture
async def http(db: AsyncSession, monkeypatch) -> AsyncIterator[tuple[AsyncClient, _Caller]]:  # type: ignore[no-untyped-def]
    async def _allow(*_args, **_kwargs) -> None:
        """The Casbin layer has its own tests in ``test_authz.py``."""

    async def _db() -> AsyncIterator[AsyncSession]:
        yield db

    caller = _Caller()
    monkeypatch.setattr(authz, "enforce", _allow)
    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_actor] = lambda: caller.actor
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client, caller
    finally:
        app.dependency_overrides.clear()


async def _job_asked_for_by(db: AsyncSession, actor: Actor) -> str:
    job_id = JobQueue(db).add(
        AUTHOR_EXPERIMENT_PLAN, "EXP-1", subject="EXP-1", requested_by=actor.auth_id
    )
    await db.flush()
    return job_id


async def test_whoever_asked_for_a_job_follows_it_and_no_other_teacher_does(http, db) -> None:  # type: ignore[no-untyped-def]
    client, caller = http
    job_id = await _job_asked_for_by(db, TEACHER)

    mine = await client.get(f"/jobs/{job_id}")
    caller.actor = OTHER_TEACHER
    theirs = await client.get(f"/jobs/{job_id}")
    caller.actor = ADMIN
    operator = await client.get(f"/jobs/{job_id}")
    caller.actor = ANONYMOUS
    nobody = await client.get(f"/jobs/{job_id}")

    assert (mine.status_code, mine.json()["state"]) == (200, "queued")
    assert theirs.status_code == 404
    assert operator.status_code == 200
    assert nobody.status_code == 403


async def test_a_reloaded_page_finds_the_job_it_started(http, db) -> None:  # type: ignore[no-untyped-def]
    client, caller = http
    job_id = await _job_asked_for_by(db, TEACHER)
    params = {"kind": AUTHOR_EXPERIMENT_PLAN, "subject": "EXP-1"}

    found = (await client.get("/jobs", params=params)).json()
    caller.actor = OTHER_TEACHER
    not_theirs = (await client.get("/jobs", params=params)).json()

    assert found["job_id"] == job_id
    assert not_theirs is None


async def _experiment(db: AsyncSession, *, lesson: uuid.UUID | None) -> str:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    experiment_id = f"EXP-{uuid.uuid4().hex[:8]}"
    db.add(
        Experiment(
            id=uuid.uuid4(),
            experiment_id=experiment_id,
            experiment_code=f"JOBS-{uuid.uuid4().hex[:8]}",
            investigation_db_id=uuid.uuid4(),
            teacher_workspace_id=uuid.uuid4(),
            lesson_period_id=lesson,
        )
    )
    await db.flush()
    return experiment_id


async def _jobs(db: AsyncSession) -> int:
    return (await db.execute(select(func.count()).select_from(Job))).scalar_one()


async def test_an_experiment_with_no_lesson_is_refused_at_once(http, db) -> None:  # type: ignore[no-untyped-def]
    client, caller = http
    caller.actor = MANAGER
    experiment_id = await _experiment(db, lesson=None)

    refused = await client.post(f"/experiments/{experiment_id}/plan")

    assert (refused.status_code, refused.json()["detail"]) == (409, "experiment_lesson_missing")
    assert await _jobs(db) == 0


async def test_the_experiment_s_plan_is_drafted_and_bound_by_its_job(http, db, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    client, caller = http
    caller.actor = MANAGER
    lesson = uuid.uuid4()
    experiment_id = await _experiment(db, lesson=lesson)
    db.add_all(
        [
            LessonPlan(
                plan_id="LP-DRAFTED",
                lesson_period_id=lesson,
                title="Drafted",
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
            PlanVersion(
                version_id="LPV-DRAFTED",
                plan_id="LP-DRAFTED",
                source_type="experiment_generated",
                session_plan={},
                status=PlanVersionStatus.DRAFT,
            ),
        ]
    )
    await db.flush()

    class _Drafter:
        async def draft(self, db, *, session_id, for_teacher):  # type: ignore[no-untyped-def]
            assert (session_id, for_teacher) == (str(lesson), None)
            return DraftedPlan("LP-DRAFTED", "LPV-DRAFTED")

    monkeypatch.setattr(experiment_jobs, "build_plan_generator", lambda: _Drafter())

    queued = await client.post(f"/experiments/{experiment_id}/plan")
    assert queued.status_code == 202, queued.text
    done = await run_queued_job(db, monkeypatch, queued.json()["job_id"])

    assert done == {"experiment_id": experiment_id, "plan_version_id": "LPV-DRAFTED"}
    bound = await db.scalar(
        select(Experiment.plan_version_id).where(Experiment.experiment_id == experiment_id)
    )
    assert bound == "LPV-DRAFTED"
