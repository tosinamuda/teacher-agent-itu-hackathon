"""Over HTTP: an imported lesson's record — provenance, rater schedule and study results —
behind the researcher permission and the experiment's own authorization."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from pathlib import Path

import casbin
import pytest
import pytest_asyncio
from casbin.persist.adapters.string_adapter import StringAdapter
from httpx import ASGITransport, AsyncClient

from app.db.deps import get_db
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from experiments.study_import.dataset import ReleasedStudy
from experiments.study_import.importer import import_study
from experiments.study_import.runs import INVESTIGATION_ID
from migrations.data.casbin_policy_seed import _CAPABILITY_POLICIES
from tests.study_release import seed_curriculum, write_release

RESEARCHER = uuid.UUID(int=801)
TEACHER = uuid.UUID(int=802)
LESSON = "/experiments/EXP-STUDY-t3-w05"


def _actor(user_id: uuid.UUID, role: str) -> Actor:
    return Actor(role=role, auth_id=f"code|{user_id}", teacher_id=user_id, email=None)


@pytest_asyncio.fixture
async def http(db, monkeypatch, tmp_path: Path) -> AsyncIterator[tuple[AsyncClient, list[Actor]]]:  # type: ignore[no-untyped-def]
    policy = [f"p, {role}, {obj}, {act}, allow" for role, obj, act in _CAPABILITY_POLICIES]
    policy += [f"g, {RESEARCHER}, researcher", f"g, {TEACHER}, teacher"]
    enforcer = casbin.Enforcer(authz.MODEL_PATH, StringAdapter("\n".join(policy)))

    async def _enforcer() -> casbin.Enforcer:
        return enforcer

    monkeypatch.setattr(authz, "get_enforcer", _enforcer)
    await seed_curriculum(db)
    pins = {"ng-jss1-math-lesson-plans": {"revision": "abc123", "provenance_sha256": "f" * 64}}
    record = StudyImport(investigation_id=INVESTIGATION_ID, release=pins, importer="e" * 64)
    await import_study(db, ReleasedStudy(write_release(tmp_path)), record=record)
    caller = [_actor(RESEARCHER, "research_manager")]

    async def _db():  # type: ignore[no-untyped-def]
        yield db

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_actor] = lambda: caller[0]
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client, caller
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_a_researcher_reads_an_imported_lessons_record(http) -> None:  # type: ignore[no-untyped-def]
    client, _ = http

    provenance = (await client.get(f"{LESSON}/provenance")).json()
    schedule = (await client.get(f"{LESSON}/rater-schedule")).json()
    results = (await client.get(f"{LESSON}/study-results")).json()

    assert provenance["source"]["datasets"] == [
        {
            "repo": "tosinamuda/ng-jss1-math-lesson-plans",
            "revision": "abc123",
            "provenance_sha256": "f" * 64,
        }
    ]
    assert [(s["part"], s["condition"], s["draw"]) for s in schedule["sets"]] == [(1, "C2", 3)]
    assert [(m["condition"], m["n"]) for m in results["part_1"]] == [("C2", 1), ("C2", 1)]
    assert all(sum(m["score_counts"]) == m["n"] for m in results["part_1"])
    study = (
        await client.get(f"/experiments/investigations/{INVESTIGATION_ID}/study-results")
    ).json()
    assert [(o["lesson"], o["condition"], o["n"]) for o in study["objectives"]] == [
        ("study-t3-w05", "C2", 2)
    ]
    assert (
        study["objectives"][0]["objective_text"] == "identify properties of cylinders and spheres"
    )
    assert [(c["favoured"], c["count"]) for c in study["part_2"]] == [("P1", 1)]
    transcripts = (await client.get(f"{LESSON}/transcripts")).json()
    assert [t["kind"] for t in transcripts] == ["teacher_record", "teacher_cleaned", "cleaning_log"]
    design = (await client.get(f"/experiments/investigations/{INVESTIGATION_ID}/design")).json()
    t3_w05 = next(row for row in design["lessons"] if row["experiment_id"] == "EXP-STUDY-t3-w05")
    assert (t3_w05["objectives"], t3_w05["part_1_sets"], t3_w05["part_2_sets"]) == (2, 1, 0)
    assert design["conditions"] == ["C0", "C1", "C2", "C3"]
    assert (design["draws"], design["raters"]) == (3, 3)


@pytest.mark.asyncio
async def test_the_record_is_the_researchers_and_names_no_other_experiment(http) -> None:  # type: ignore[no-untyped-def]
    client, caller = http

    missing = await client.get("/experiments/EXP-none/rater-schedule")
    no_study = await client.get("/experiments/investigations/INV-none/study-results")
    caller[0] = _actor(TEACHER, "teacher")
    teacher = await client.get(f"{LESSON}/study-results")

    assert missing.status_code == 404
    assert no_study.status_code == 404
    assert teacher.status_code == 403
