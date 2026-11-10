import asyncio
from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient

from app.db.deps import get_db
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.artefacts.types.lesson_plan.api.schemas import PlanGenerateRequest
from app.domains.artefacts.types.lesson_plan.application import service as plans_application_service
from app.domains.artefacts.types.lesson_plan.application.errors import PlanValidationError
from app.domains.artefacts.types.lesson_plan.deps import (
    get_content_specifications,
    lesson_plan_service,
)
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionInfo, SessionContext
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import GeneratedLessonPlan
from app.domains.artefacts.types.lesson_plan.drafting.deps import (
    get_lesson_generation_service,
    get_session_plan_validator,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.validator_service import (
    SessionPlanValidationResult,
)
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor

client = TestClient(app)

LESSON_PERIOD = "00000000-0000-0000-0000-000000000902"
_TEST_MANAGER = Actor(role="research_manager", auth_id="code|uncle-tosin", full_name="Uncle Tosin")


async def _noop_enforce(*_args, **_kwargs) -> None:
    """Allow every call — the Casbin layer has its own tests in ``test_authz.py``."""
    return None


def _override_actor_as_manager(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Approval is gated; these are route-handler tests, so we (a) make the actor
    a manager and (b) short-circuit the Casbin enforcer (covered elsewhere), for this
    test only."""
    app.dependency_overrides[get_actor] = lambda: _TEST_MANAGER
    monkeypatch.setattr(authz, "enforce", _noop_enforce)


class DummyGenerator:
    def __init__(self, session_plan):
        self.session_plan = session_plan
        self.last_kwargs = None

    async def generate(self, *args, **kwargs):
        self.last_kwargs = kwargs
        return GeneratedLessonPlan(
            session_plan=self.session_plan,
            run_metadata={"model": "test", "prompt_inputs": {}},
        )


class SeededSpecifications:
    """The specification store as seeded, without a database."""

    async def current(self, db, kind):
        return seed_specification(kind)


class DummySchemaValidator:
    def __init__(self, schema_errors=None, context_errors=None):
        self.schema_errors = schema_errors or []
        self.context_errors = context_errors or []

    def validate(self, session_plan, session_context):
        return SessionPlanValidationResult(
            schema_errors=self.schema_errors,
            context_errors=self.context_errors,
        )


async def _fake_db():
    yield object()


def _session_context():
    return SessionContext(
        session_id="SS1-GMATH-T1-W01-S01",
        subject="Mathematics (General)",
        track="General",
        grade="SS1",
        term="First Term",
        week=1,
        day_index=1,
        topic="Revision and number bases",
        subtopic="Place value and number systems",
        duration_minutes=40,
        session_objectives=["Convert numbers between common bases"],
        general_objectives=["Convert numbers between common bases"],
        reference_materials=[],
    )


def test_the_drafting_job_has_the_engine_write_the_plan_and_says_where_it_is(monkeypatch):
    from app.domains.content_engine import jobs as engine_jobs
    from app.domains.content_engine.infrastructure.plan_generator import DraftedPlan

    asked: list[tuple[str, str | None]] = []

    class FakeGenerator:
        async def draft(self, db, *, session_id, for_teacher):  # type: ignore[no-untyped-def]
            asked.append((session_id, for_teacher))
            return DraftedPlan("LP-1", "LPV-123")

    @asynccontextmanager
    async def _no_session():  # type: ignore[no-untyped-def]
        yield object()

    monkeypatch.setattr(engine_jobs, "build_plan_generator", lambda: FakeGenerator())
    monkeypatch.setattr(engine_jobs, "AsyncSessionLocal", _no_session)

    drafted = asyncio.run(engine_jobs.generate_lesson_plan(LESSON_PERIOD, "teacher-7"))

    assert drafted == {"plan_id": "LP-1", "version_id": "LPV-123"}
    assert asked == [(LESSON_PERIOD, "teacher-7")]


def test_generate_plan_session_missing(monkeypatch):
    _override_actor_as_manager(monkeypatch)

    async def fake_build(*_):
        return None

    monkeypatch.setattr(plans_application_service, "build_session_context", fake_build)

    app.dependency_overrides[get_db] = _fake_db
    app.dependency_overrides[get_lesson_generation_service] = lambda: DummyGenerator({})
    app.dependency_overrides[get_content_specifications] = SeededSpecifications
    app.dependency_overrides[get_session_plan_validator] = lambda: DummySchemaValidator()

    response = client.post("/artefacts/lesson-plans/generate", json={"session_id": "missing"})
    assert response.status_code == 404

    app.dependency_overrides.clear()


def test_a_draft_that_breaks_the_plan_schema_is_refused(monkeypatch):
    invalid_session_plan = {"plan_id": "LP-1"}

    async def fake_build(*_):
        return _session_context()

    async def fake_persist(*_):
        return PlanVersionInfo(
            plan_id="LP-SS1-GMATH-T1-W01-S01",
            version_id="LPV-123",
            status="draft",
        )

    monkeypatch.setattr(plans_application_service, "build_session_context", fake_build)
    monkeypatch.setattr(plans_application_service, "persist_plan_version", fake_persist)

    service = lesson_plan_service(
        object(),  # type: ignore[arg-type]
        generator=DummyGenerator(invalid_session_plan),  # type: ignore[arg-type]
        validator=DummySchemaValidator(  # type: ignore[arg-type]
            schema_errors=[{"path": ["plan_id"], "message": "missing"}]
        ),
        specifications=SeededSpecifications(),  # type: ignore[arg-type]
    )

    with pytest.raises(PlanValidationError):
        asyncio.run(service.generate(PlanGenerateRequest(session_id="SS1-GMATH-T1-W01-S01")))


def test_generating_a_plan_needs_a_signed_in_author() -> None:
    """Each generation spends on the model, so an anonymous caller is refused."""
    app.dependency_overrides.clear()
    response = client.post("/artefacts/lesson-plans/generate", json={"session_id": "any"})

    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_asking_for_a_draft_queues_the_job_that_writes_it(db, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    from httpx import ASGITransport, AsyncClient
    from sqlalchemy import select

    from app.infra.jobs.models import Job

    _override_actor_as_manager(monkeypatch)

    async def fake_build(*_):
        return _session_context()

    async def _db():  # type: ignore[no-untyped-def]
        yield db

    monkeypatch.setattr(plans_application_service, "build_session_context", fake_build)
    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_lesson_generation_service] = lambda: DummyGenerator({})
    app.dependency_overrides[get_content_specifications] = SeededSpecifications
    app.dependency_overrides[get_session_plan_validator] = lambda: DummySchemaValidator()
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
            body = {"session_id": LESSON_PERIOD, "teacher_id": "teacher-7"}
            queued = await http.post("/artefacts/lesson-plans/generate", json=body)
            again = await http.post("/artefacts/lesson-plans/generate", json=body)
    finally:
        app.dependency_overrides.clear()

    assert queued.status_code == 202, queued.text
    assert again.json()["job_id"] == queued.json()["job_id"]
    job = (await db.execute(select(Job))).scalar_one()
    assert (job.kind, job.subject, job.args) == (
        "lesson_plans.generate",
        f"lesson:{LESSON_PERIOD}",
        [LESSON_PERIOD, "teacher-7"],
    )
    assert job.requested_by == "code|uncle-tosin"
