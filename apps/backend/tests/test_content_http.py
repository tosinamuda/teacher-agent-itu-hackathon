"""End to end over HTTP: the /content routes, the production permission table, the database.

Only the two things that cannot run in a test are stood in for: the language model (a
writer and a question generator that return fixed content) and the class-and-subject
ownership lookup. Everything else — routing, authentication by role, the Casbin policy the
seed writes, services, persistence, approvals and the class test's release — is real.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass

import casbin
import pytest
import pytest_asyncio
from casbin.persist.adapters.string_adapter import StringAdapter
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, text, update

from app.db.deps import get_db
from app.domains.artefact_revision.application.lesson_note_executor import (
    LessonNoteRevisionExecutor,
)
from app.domains.artefact_revision.application.service import ArtefactRevisionService
from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.core.infrastructure.specifications import (
    SqlAlchemyContentSpecifications,
)
from app.domains.artefacts.lesson_note.application.draft import (
    DraftLessonNote,
    NoteLesson,
    NoteStepInput,
)
from app.domains.artefacts.lesson_note.application.service import LessonNoteService
from app.domains.artefacts.lesson_note.domain.note import NoteSection, NoteStepDraft
from app.domains.artefacts.lesson_note.infrastructure.repository import (
    SqlAlchemyLessonNotes,
)
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.assessments.application.diagnostic_generator import DiagnosticMCQItem
from app.domains.assessments.application.diagnostic_service import DiagnosticGenerationService
from app.domains.assessments.infrastructure.repository import ClassTestMaterials
from app.domains.content.api import routes as content_routes
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.infrastructure import generators
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.teaching.models.syllabus import LessonPeriod
from app.infra.jobs.models import Job
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from migrations.data.casbin_policy_seed import _CAPABILITY_POLICIES
from migrations.data.content_registry_seed import seed_content_registry
from tests.plugin_folder import implementing_plan, read_plugin
from tests.queued_jobs import run_queued_job

PLAN = "LPV-HTTP-1"
TEACHER = uuid.UUID(int=701)
OTHER_TEACHER = uuid.UUID(int=702)
RESEARCHER = uuid.UUID(int=703)
SESSION_PLAN = {
    "subject": "Mathematics",
    "grade": "JSS1",
    "topic": "Order of operations",
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lop01", "objective_text": "Use the order of operations"}
    ],
    "steps": [
        {"step_id": "s1", "step_kind": "core", "lesson_objective_id": "lop01", "title": "BODMAS"}
    ],
}


@dataclass
class _Caller:
    actor: Actor


def _actor(user_id: uuid.UUID | None, role: str) -> Actor:
    return Actor(
        role=role,
        auth_id=f"code|{user_id}",
        teacher_id=user_id,
        email=None,
        full_name={TEACHER: "Teacher One", RESEARCHER: "Researcher"}.get(user_id),  # type: ignore[arg-type]
    )


class _Writer:
    async def write(
        self, *, brief: ArtefactSpec, lesson: NoteLesson, step: NoteStepInput, draw: int = 0
    ) -> NoteStepDraft:
        return NoteStepDraft(
            title=step.title,
            teaching_points=["Brackets first, then multiplication, then addition."],
            board_summary="B, then × and ÷, then + and −.",
        )


class _Reviser:
    async def revise(
        self,
        *,
        brief: ArtefactSpec,
        current_sections: list[NoteSection],
        highlighted_section: str,
        instruction: str,
    ) -> tuple[list[NoteSection], str]:
        return list(current_sections), f"Applied: {instruction}"


class _Questions:
    async def generate(self, *, brief: ArtefactSpec, **_: object) -> list[DiagnosticMCQItem]:
        return [
            DiagnosticMCQItem(
                stem="2 + 3 × 4 = ?",
                options={"A": "20", "B": "14", "C": "24", "D": "9"},
                correct_option="B",
                distractor_misconceptions={"A": "add_before_multiply", "C": "x", "D": "y"},
                difficulty="easy",
            )
        ]


def _policy() -> str:
    rows = [f"p, {role}, {obj}, {act}, allow" for role, obj, act in _CAPABILITY_POLICIES]
    rows += [
        f"g, {TEACHER}, teacher",
        f"g, {OTHER_TEACHER}, teacher",
        f"g, {RESEARCHER}, researcher",
    ]
    return "\n".join(rows)


@pytest_asyncio.fixture
async def client(db, monkeypatch) -> AsyncIterator[tuple[AsyncClient, _Caller]]:  # type: ignore[no-untyped-def]
    enforcer = casbin.Enforcer(authz.MODEL_PATH, StringAdapter(_policy()))

    async def _enforcer() -> casbin.Enforcer:
        return enforcer

    async def _owns(db, *, teacher_id: uuid.UUID, plan_version_id: str) -> bool:  # type: ignore[no-untyped-def]
        return teacher_id == TEACHER and plan_version_id == PLAN

    monkeypatch.setattr(authz, "get_enforcer", _enforcer)
    monkeypatch.setattr(content_routes, "teacher_owns_plan_version", _owns)
    monkeypatch.setattr(
        generators,
        "build_lesson_note_service",
        lambda: LessonNoteService(
            SqlAlchemyLessonNotes(),
            DraftLessonNote(_Writer()),
            SqlAlchemyContentSpecifications(),
        ),
    )
    monkeypatch.setattr(
        generators,
        "build_diagnostic_service",
        lambda: DiagnosticGenerationService(
            generator=_Questions(),  # type: ignore[arg-type]
            specifications=SqlAlchemyContentSpecifications(),
            materials=ClassTestMaterials(),
        ),
    )
    monkeypatch.setattr(
        "app.domains.artefact_revision.infrastructure.wiring.build_artefact_revision_service",
        lambda fallback=None, plans=None: ArtefactRevisionService(
            (
                LessonNoteRevisionExecutor(
                    SqlAlchemyLessonNotes(), _Reviser(), SqlAlchemyContentSpecifications()
                ),
            ),
            fallback=fallback,
        ),
    )

    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    period_id = uuid.uuid4()
    db.add_all(
        [
            LessonPeriod(
                id=period_id, scheme_of_work_id=uuid.uuid4(), period_number=1, subtopic_id="sub-1"
            ),
            LessonPlan(
                plan_id="P-HTTP-1",
                lesson_period_id=period_id,
                title="Order of operations",
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
            PlanVersion(
                version_id=PLAN,
                plan_id="P-HTTP-1",
                source_type="experiment_manual",
                session_plan=SESSION_PLAN,
                status=PlanVersionStatus.APPROVED,
            ),
        ]
    )
    await db.flush()
    connection = await db.connection()
    await connection.run_sync(seed_content_registry)

    caller = _Caller(_actor(TEACHER, "teacher"))

    async def _db() -> AsyncIterator:
        yield db

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_actor] = lambda: caller.actor
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
            yield http, caller
    finally:
        app.dependency_overrides.clear()


async def _make(http, db, monkeypatch, body: dict) -> dict:  # type: ignore[no-untyped-def]
    """Ask for content as the page does, then run the job it queued; the content it made."""
    queued = await http.post("/content", json=body)
    assert queued.status_code == 202, queued.text
    made = await run_queued_job(db, monkeypatch, queued.json()["job_id"])
    return (await http.get(f"/content/{made['content_id']}")).json()


@pytest.mark.asyncio
async def test_a_teacher_generates_revises_and_approves_content_over_http(
    client, db, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    http, caller = client

    types = (await http.get("/content/types")).json()
    assert sorted(t["type"] for t in types) == [
        "class-test",
        "exam-questions",
        "lesson-note",
        "lesson-plan",
        "revision-note",
    ]
    assert {t["type"]: t["spec"]["revision"] for t in types} == {
        "class-test": 1,
        "exam-questions": 2,
        "lesson-note": 1,
        "lesson-plan": 7,
        "revision-note": 1,
    }

    draft = await _make(http, db, monkeypatch, {"plan_version_id": PLAN, "type": "lesson-note"})
    assert (draft["review_status"], draft["version"]) == ("pending", 1)
    assert draft["provenance"] == {
        "origin": "generated",
        "specification": {"kind": "lesson_note", "revision": 1},
        "generator": {"harness": "dspy-pipeline", "schema": "code", "ref": "builtin"},
    }
    assert draft["content"]["sections"][0]["body"].startswith("#### BODMAS")

    test = await _make(http, db, monkeypatch, {"plan_version_id": PLAN, "type": "class-test"})
    assert test["type"] == "class-test"
    assert [item["stem"] for item in test["content"]["items"]] == ["2 + 3 × 4 = ?"]

    listed = (await http.get("/content", params={"plan_version_id": PLAN})).json()
    assert {m["type"] for m in listed} == {"lesson-plan", "lesson-note", "class-test"}

    revised = await http.post(
        f"/content/{draft['id']}/revisions", json={"feedback": "Add a board diagram."}
    )
    assert revised.status_code == 201, revised.text
    assert revised.json()["summary"] == "Applied: Add a board diagram."
    history = (await http.get(f"/content/{draft['id']}/revisions")).json()
    assert [(r["turn_number"], r["feedback"]) for r in history] == [(1, "Add a board diagram.")]
    assert (await http.get(f"/content/{draft['id']}")).json()["version"] == 2

    approved = await http.post(f"/content/{draft['id']}/approvals", json={"expected_version": 2})
    assert approved.status_code == 201, approved.text
    assert approved.json()["review_status"] == "approved"
    approvals = (await http.get(f"/content/{draft['id']}/approvals")).json()
    assert [(a["approved_version"], a["approved_by"]) for a in approvals] == [(2, "Teacher One")]

    sent = await http.post(
        f"/content/{test['id']}/approvals", json={"expected_version": test["version"]}
    )
    assert sent.status_code == 201, sent.text
    released_by = (
        await db.execute(
            select(PlanVersion.assessment_released_by).where(PlanVersion.version_id == PLAN)
        )
    ).scalar_one()
    assert released_by == "Teacher One"
    locked = await http.post(f"/content/{test['id']}/revisions", json={"feedback": "Harder."})
    assert locked.status_code == 409

    refused = await http.post(
        "/content", json={"plan_version_id": PLAN, "type": "class-test", "pipeline": "2026-08-25"}
    )
    assert refused.status_code == 422
    learner_pack = await http.post(
        "/content", json={"plan_version_id": PLAN, "type": "revision-note", "level": "learner"}
    )
    assert learner_pack.status_code == 422
    for body in (
        {"type": "revision-note", "sources": "encyclopaedia"},
        {"type": "class-test", "sources": "textbook"},
    ):
        refused_sources = await http.post("/content", json={"plan_version_id": PLAN, **body})
        assert refused_sources.status_code == 422, body

    caller.actor = _actor(OTHER_TEACHER, "teacher")
    assert (await http.get(f"/content/{draft['id']}")).status_code == 403
    assert (await http.get("/content", params={"plan_version_id": PLAN})).status_code == 403
    assert (await http.get("/content")).json() == []

    caller.actor = Actor(role="anonymous", auth_id="anonymous")
    assert (await http.get("/content/types")).status_code == 403


@pytest.mark.asyncio
async def test_only_a_researcher_adds_a_spec_revision_over_http(client) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    current = (await http.get("/content/types/lesson-note")).json()["spec"]
    body = {
        key: current[key] for key in ("material", "audience", "levels", "structure", "adaptable")
    }
    body["requirements"] = ["Keep each step to one page."]

    assert (await http.post("/content/types/lesson-note/specs", json=body)).status_code == 403

    caller.actor = _actor(RESEARCHER, "research_manager")
    added = await http.post("/content/types/lesson-note/specs", json=body)
    assert added.status_code == 201, added.text
    assert added.json()["revision"] == 2
    revisions = (await http.get("/content/types/lesson-note/specs")).json()
    assert [r["revision"] for r in revisions] == [1, 2]
    assert (await http.get("/content/types/lesson-note/specs/1")).json()["requirements"] != [
        "Keep each step to one page."
    ]

    invalid = await http.post(
        "/content/types/lesson-note/specs",
        json={**body, "levels": ["class", "learner"], "adaptable": []},
    )
    assert invalid.status_code == 422


@pytest.mark.asyncio
async def test_an_approval_of_a_version_the_teacher_did_not_see_is_refused(
    client, db, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    http, _ = client
    draft = await _make(http, db, monkeypatch, {"plan_version_id": PLAN, "type": "lesson-note"})
    await http.post(f"/content/{draft['id']}/revisions", json={"feedback": "Shorter."})

    stale = await http.post(f"/content/{draft['id']}/approvals", json={"expected_version": 1})

    assert stale.status_code == 409


@pytest.mark.asyncio
async def test_a_teacher_rejects_a_note_with_a_reason_and_no_other_teacher_can(
    client, db, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    draft = await _make(http, db, monkeypatch, {"plan_version_id": PLAN, "type": "lesson-note"})
    body = {"expected_version": draft["version"], "reason": "It repeats itself."}

    caller.actor = _actor(OTHER_TEACHER, "teacher")
    refused = await http.post(f"/content/{draft['id']}/rejections", json=body)
    assert refused.status_code == 403

    caller.actor = _actor(TEACHER, "teacher")
    short = await http.post(f"/content/{draft['id']}/rejections", json={**body, "reason": "no"})
    assert short.status_code == 422
    rejected = await http.post(f"/content/{draft['id']}/rejections", json=body)
    assert rejected.status_code == 201, rejected.text
    assert (rejected.json()["review_status"], rejected.json()["review_reason"]) == (
        "rejected",
        "It repeats itself.",
    )
    again = await http.post(f"/content/{draft['id']}/rejections", json=body)
    assert (again.status_code, again.json()["detail"]) == (409, "artefact_already_rejected")


@pytest.mark.asyncio
async def test_a_teacher_approves_their_lesson_plan_as_content_and_no_one_else_can(
    client, db
) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    await db.execute(
        update(PlanVersion)
        .where(PlanVersion.version_id == PLAN)
        .values(status=PlanVersionStatus.DRAFT)
    )
    [plan] = (
        await http.get("/content", params={"plan_version_id": PLAN, "type": "lesson-plan"})
    ).json()
    assert (plan["id"], plan["version"], plan["provenance"]) == (
        "P-HTTP-1",
        1,
        {"origin": "teacher"},
    )

    caller.actor = _actor(OTHER_TEACHER, "teacher")
    refused = await http.post(f"/content/{plan['id']}/approvals", json={"expected_version": 1})
    assert refused.status_code == 403

    caller.actor = _actor(TEACHER, "teacher")
    approved = await http.post(f"/content/{plan['id']}/approvals", json={"expected_version": 1})
    assert approved.status_code == 201, approved.text
    assert approved.json()["review_status"] == "approved"
    approvals = (await http.get(f"/content/{plan['id']}/approvals")).json()
    assert [(a["id"], a["approved_version"], a["approved_by"]) for a in approvals] == [
        (PLAN, 1, "Teacher One")
    ]


@pytest.mark.asyncio
async def test_each_type_says_who_it_is_for_and_whether_a_plan_version_makes_it(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client
    types = {t["type"]: t for t in (await http.get("/content/types")).json()}

    assert {name: (t["label"], t["audience"]) for name, t in types.items()} == {
        "lesson-plan": ("Lesson plan", "teacher"),
        "lesson-note": ("Lesson note", "teacher"),
        "revision-note": ("Revision note", "learner"),
        "class-test": ("Class test", "learner"),
        "exam-questions": ("Exam questions", "learner"),
    }
    assert [name for name, t in types.items() if not t["made_from_a_plan_version"]] == [
        "lesson-plan"
    ]


@pytest.mark.asyncio
async def test_what_generation_would_refuse_is_refused_at_once_and_queues_nothing(
    client, db
) -> None:  # type: ignore[no-untyped-def]
    http, _ = client

    refused = await http.post(
        "/content", json={"plan_version_id": PLAN, "type": "lesson-note", "level": "learner"}
    )

    assert (refused.status_code, refused.json()["detail"]) == (
        422,
        "lesson-note_is_class_level_only",
    )
    assert (await db.execute(select(func.count()).select_from(Job))).scalar_one() == 0


@pytest.mark.asyncio
async def test_asking_again_while_it_is_made_follows_the_same_job(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client
    body = {"plan_version_id": PLAN, "type": "lesson-note"}

    first = (await http.post("/content", json=body)).json()["job_id"]
    again = (await http.post("/content", json=body)).json()["job_id"]
    followed = (await http.get(f"/jobs/{first}")).json()

    assert again == first
    assert (followed["kind"], followed["state"], followed["subject"]) == (
        "content.generate",
        "queued",
        f"{PLAN}:lesson-note:class",
    )


@pytest.mark.asyncio
async def test_only_a_researcher_changes_the_default_generator_and_never_a_native_one(
    client, db, tmp_path
) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    listed = {t["type"]: t for t in (await http.get("/content/types")).json()}
    notes = [g for g in listed["revision-note"]["generators"] if g["level"] == "class"]
    assert {g["ref"]: g["status"] for g in notes} == {
        "2026-09-02": "default",
        "2026-08-25": "available",
    }
    assert [g["ref"] for g in listed["lesson-plan"]["generators"]] == ["builtin"]

    catalogue = build_content_catalogue()
    own = await catalogue.current(db, "lesson-plan")
    plugin, problems = read_plugin(implementing_plan(tmp_path / "p", own))
    assert plugin is not None, problems
    await PluginInstaller(catalogue, SqlAlchemyPlugins()).install(db, plugin, "digest", "R")
    body = {"level": "class", "generator": "plan-writer"}

    forbidden = await http.put("/content/types/lesson-plan/default-generator", json=body)
    assert forbidden.status_code == 403

    caller.actor = _actor(RESEARCHER, "research_manager")
    switched = await http.put("/content/types/lesson-plan/default-generator", json=body)
    assert switched.status_code == 200, switched.text
    assert {g["ref"]: g["status"] for g in switched.json()["generators"]} == {
        "plan-writer": "default",
        "builtin": "available",
    }
    assert switched.json()["spec"]["revision"] == own.revision

    locked = await http.put(
        "/content/types/revision-note/default-generator",
        json={"level": "class", "generator": "2026-08-25"},
    )
    assert (locked.status_code, locked.json()["detail"]) == (
        409,
        "native_generator_is_locked:revision-note",
    )
    missing = await http.put(
        "/content/types/lesson-plan/default-generator", json={"generator": "nobody"}
    )
    assert missing.status_code == 422


@pytest.mark.asyncio
async def test_a_teacher_switches_an_optional_material_off_and_on_for_themselves(  # type: ignore[no-untyped-def]
    client, monkeypatch
) -> None:
    from app.domains.content.api import preference_routes
    from app.domains.content.domain import preferences

    core = frozenset({"lesson-plan", "lesson-note", "revision-note"})
    monkeypatch.setattr(preferences, "CORE_TYPES", core)
    monkeypatch.setattr(preference_routes, "CORE_TYPES", core)
    http, caller = client

    shown = await http.get("/content/preferences")
    by_type = {m["type"]: m for m in shown.json()["materials"]}
    assert by_type["lesson-note"]["core"] is True
    assert by_type["lesson-note"]["description"]
    assert {t: m["enabled"] for t, m in by_type.items() if not m["core"]} == {
        "class-test": True,
        "exam-questions": True,
    }

    off = await http.put("/content/preferences/materials/class-test", json={"enabled": False})
    assert {m["type"]: m["enabled"] for m in off.json()["materials"]}["class-test"] is False
    assert "class-test" not in {t["type"] for t in (await http.get("/content/types")).json()}
    refused = await http.post("/content", json={"plan_version_id": PLAN, "type": "class-test"})
    assert (refused.status_code, refused.json()["detail"]) == (409, "material_is_switched_off")

    caller.actor = _actor(OTHER_TEACHER, "teacher")
    assert "class-test" in {t["type"] for t in (await http.get("/content/types")).json()}

    caller.actor = _actor(TEACHER, "teacher")
    on = await http.put("/content/preferences/materials/class-test", json={"enabled": True})
    assert {m["type"]: m["enabled"] for m in on.json()["materials"]}["class-test"] is True
    assert "class-test" in {t["type"] for t in (await http.get("/content/types")).json()}


@pytest.mark.asyncio
async def test_a_core_material_cannot_be_switched_off(
    client,
) -> None:  # type: ignore[no-untyped-def]
    http, _ = client

    core = await http.put("/content/preferences/materials/lesson-note", json={"enabled": False})
    assert (core.status_code, core.json()["detail"]) == (422, "material_is_always_on")


@pytest.mark.asyncio
async def test_a_teacher_adds_a_plugin_from_the_library_and_it_becomes_a_material_they_can_turn_off(  # type: ignore[no-untyped-def]
    client,
) -> None:
    http, _ = client

    before = {
        p["folder"]: p["installed"] for p in (await http.get("/content/plugins/library")).json()
    }
    assert before["flashcards"] is False
    assert "flashcards" not in {t["type"] for t in (await http.get("/content/types")).json()}

    added = await http.post("/content/plugins/library/flashcards")
    assert added.status_code == 201, added.text
    assert [p["type"] for p in added.json()] == ["flashcards"]

    after = {
        p["folder"]: p["installed"] for p in (await http.get("/content/plugins/library")).json()
    }
    assert after["flashcards"] is True
    assert "flashcards" in {t["type"] for t in (await http.get("/content/types")).json()}
    shown = {
        m["type"]: m["enabled"]
        for m in (await http.get("/content/preferences")).json()["materials"]
    }
    assert shown["flashcards"] is True

    missing = await http.post("/content/plugins/library/nothing-here")
    assert (missing.status_code, missing.json()["detail"]) == (404, "plugin_not_in_the_library")
    outside = await http.post("/content/plugins/library/..%2Fplugins%2Fclass-test")
    assert outside.status_code in (404, 422)
