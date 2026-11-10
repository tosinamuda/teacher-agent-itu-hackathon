from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path
from typing import cast

import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import get_sync_database_url
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import GeneratedLessonPlan
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import SessionPlan
from app.domains.artefacts.types.lesson_plan.infrastructure import repository
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.shared.json_types import JsonObject
from migrations.data.lesson_plan_payload_repairs import (
    PlanVersionPayloadSnapshot,
    apply_payload_repairs,
    build_audit_report,
    load_payload_repairs_jsonl,
)

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPAIR_JSONL_PATH = BACKEND_DIR / "migrations/data/records/lesson_plan_payload_repairs.jsonl"
AUDIT_JSON_PATH = BACKEND_DIR / "migrations/data/records/lesson_plan_payload_audit.json"
LEGACY_TOP_LEVEL_KEYS = {"objectives", "anticipated_misconceptions", "assignment"}
LEGACY_STEP_KEYS = {"type", "items"}


def _load_audit_payload() -> JsonObject:
    return json.loads(AUDIT_JSON_PATH.read_text(encoding="utf-8"))


def _json_rows(value: object) -> list[JsonObject]:
    if not isinstance(value, list):
        return []
    return cast(list[JsonObject], [row for row in value if isinstance(row, dict)])


def _load_live_snapshots() -> list[PlanVersionPayloadSnapshot]:
    engine = create_engine(get_sync_database_url())
    snapshots: list[PlanVersionPayloadSnapshot] = []
    with engine.begin() as connection:
        result = connection.execute(
            text(
                """
                SELECT version_id, plan_id, session_plan
                FROM plan_versions
                ORDER BY created_at, version_id
                """
            )
        )
        for row in result:
            session_plan = row.session_plan
            if isinstance(session_plan, str):
                session_plan = json.loads(session_plan)
            snapshots.append(
                PlanVersionPayloadSnapshot(
                    version_id=str(row.version_id),
                    plan_id=str(row.plan_id),
                    session_plan=session_plan or {},
                )
            )
    return snapshots


def _valid_session_plan() -> JsonObject:
    return {
        "plan_id": "LP-generated",
        "session_id": "SS1-GMATH-T1-W01-S01",
        "subject": "Mathematics (General)",
        "track": "General",
        "grade": "SS1",
        "term": "First Term",
        "week": 1,
        "topic": "Revision and number bases",
        "subtopic": "Place value and number systems",
        "curriculum_objectives": [
            {
                "curriculum_objective_id": "cur_obj01",
                "objective_text": "Convert numbers between common bases",
                "objective_order": 1,
            }
        ],
        "lesson_plan_objectives": [
            {
                "lesson_objective_id": "obj01",
                "objective_text": "Convert numbers between common bases",
                "objective_order": 1,
                "curriculum_objective_id": "cur_obj01",
                "curriculum_objective_text": "Convert numbers between common bases",
                "kc_type": "concept",
                "kc_focus": "convert numbers between common bases",
                "source_form": None,
                "target_form": None,
            }
        ],
        "misconceptions": [],
        "steps": [
            {
                "step_id": "step-intro",
                "step_kind": "intro",
                "instructional_type": None,
                "kc_type": None,
                "lesson_objective_id": None,
                "title": "Introduction",
                "content": "Review prior knowledge.",
                "estimated_minutes": 5,
                "activities": [],
                "blocks": [],
            },
            {
                "step_id": "step-core-01",
                "step_kind": "core",
                "instructional_type": "explain_only",
                "kc_type": "concept",
                "lesson_objective_id": "obj01",
                "title": "Place value",
                "content": "Explain place value.",
                "estimated_minutes": 20,
                "activities": [
                    {"who": "teacher", "what": "Model base conversion."},
                    {"who": "student", "what": "Answer guided questions."},
                ],
                "blocks": [
                    {
                        "id": "block-exp-01",
                        "type": "explanation",
                        "content": "Explain place value.",
                    }
                ],
            },
            {
                "step_id": "step-evaluation",
                "step_kind": "evaluation",
                "instructional_type": "check",
                "kc_type": None,
                "lesson_objective_id": None,
                "title": "Evaluation",
                "content": "Check understanding.",
                "estimated_minutes": 10,
                "activities": [],
                "blocks": [
                    {
                        "id": "block-eval-01",
                        "type": "practice",
                        "question": "Convert 1010 base 2 to base 10.",
                        "answer": "10",
                        "lesson_objective_id": "obj01",
                    }
                ],
            },
        ],
        "assessments": [],
        "entry_behaviour": [],
        "instructional_materials": [],
        "references": [],
    }


def _assert_no_legacy_payload_keys(session_plan: JsonObject) -> None:
    assert not (LEGACY_TOP_LEVEL_KEYS & set(session_plan))
    steps = session_plan.get("steps")
    assert isinstance(steps, list)
    for step in steps:
        assert isinstance(step, dict)
        assert not (LEGACY_STEP_KEYS & set(step))
        assert step["step_kind"] in {"intro", "core", "evaluation"}


def test_repair_jsonl_rows_validate_against_strict_session_plan() -> None:
    repair_records = load_payload_repairs_jsonl(REPAIR_JSONL_PATH)
    assert repair_records

    version_ids = [record.version_id for record in repair_records]
    assert len(version_ids) == len(set(version_ids))

    for record in repair_records:
        validated = SessionPlan.model_validate(record.repaired_session_plan)
        assert validated.plan_id == record.plan_id
        _assert_no_legacy_payload_keys(record.repaired_session_plan)


def test_repair_jsonl_matches_committed_audit_snapshot() -> None:
    audit_payload = _load_audit_payload()
    audit_invalid_ids = {
        str(row["version_id"]) for row in _json_rows(audit_payload.get("invalid_rows"))
    }
    repair_invalid_ids = {
        record.version_id for record in load_payload_repairs_jsonl(REPAIR_JSONL_PATH)
    }
    assert repair_invalid_ids == audit_invalid_ids


def test_live_db_audit_has_no_invalid_payloads() -> None:
    """The live DB carries no invalid lesson-plan payloads.

    Cleanliness holds two ways: the historical repair ran (``apply_payload_repairs``),
    and the persistence path now writes only strict payloads
    (``test_persist_plan_version_stores_strict_session_plan``). The committed audit
    snapshot remains as provenance of which rows were originally repaired.
    """
    try:
        audit_report = build_audit_report(_load_live_snapshots())
    except SQLAlchemyError as exc:
        pytest.skip(f"Live lesson-plan audit DB is unavailable: {exc}")

    live_invalid_ids = {
        str(row["version_id"]) for row in _json_rows(audit_report.get("invalid_rows"))
    }
    assert live_invalid_ids == set()


def _legacy_session_plan() -> JsonObject:
    """A pre-strict payload (legacy ``objectives`` / step ``type``+``items`` /
    ``assignment``) that the repair engine rewrites into a valid SessionPlan."""
    return {
        "session_id": "SS1-GMATH-T1-W01-S01",
        "subject": "Mathematics (General)",
        "track": "General",
        "grade": "SS1",
        "term": "First Term",
        "week": 1,
        "topic": "Revision and number bases",
        "subtopic": "Place value and number systems",
        "objectives": ["Convert numbers between common bases"],
        "anticipated_misconceptions": ["Place value does not matter"],
        "steps": [
            {
                "type": "intro",
                "title": "Introduction",
                "content": "Review prior knowledge.",
                "items": [],
            },
            {
                "type": "core",
                "title": "Place value",
                "content": "Explain place value.",
                "items": [
                    {"type": "explanation", "content": "Explain place value in number bases."},
                    {
                        "type": "worked_example",
                        "question": "Convert 1010 base 2 to base 10.",
                        "answer": "10",
                    },
                    {
                        "type": "practice",
                        "question": "Convert 11 base 2 to base 10.",
                        "answer": "3",
                    },
                ],
            },
            {
                "type": "evaluation",
                "title": "Evaluation",
                "content": "Check understanding.",
                "items": [
                    {
                        "type": "practice",
                        "question": "Convert 1010 base 2 to base 10.",
                        "answer": "10",
                    },
                ],
            },
        ],
        "assignment": "Practice converting 5 numbers between bases.",
    }


def _in_memory_plan_versions() -> tuple[sa.Engine, sa.Table]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    metadata = sa.MetaData()
    plan_versions = sa.Table(
        "plan_versions",
        metadata,
        sa.Column("version_id", sa.String(), primary_key=True),
        sa.Column("plan_id", sa.String(), nullable=True),
        sa.Column("session_plan", sa.JSON(), nullable=True),
    )
    metadata.create_all(engine)
    return engine, plan_versions


def test_apply_payload_repairs_repairs_invalid_and_is_idempotent() -> None:
    valid_plan = SessionPlan.model_validate(_valid_session_plan()).model_dump(
        mode="json",
        exclude_none=True,
    )
    engine, plan_versions = _in_memory_plan_versions()

    with engine.begin() as connection:
        connection.execute(
            plan_versions.insert(),
            [
                {
                    "version_id": "LPV-legacy",
                    "plan_id": "LP-legacy",
                    "session_plan": _legacy_session_plan(),
                },
                {
                    "version_id": "LPV-valid",
                    "plan_id": "LP-valid",
                    "session_plan": valid_plan,
                },
            ],
        )

        applied = apply_payload_repairs(connection)
        assert {record.version_id for record in applied} == {"LPV-legacy"}

        repaired_row = connection.execute(
            sa.select(plan_versions.c.session_plan).where(
                plan_versions.c.version_id == "LPV-legacy"
            )
        ).scalar_one()
        valid_row = connection.execute(
            sa.select(plan_versions.c.session_plan).where(plan_versions.c.version_id == "LPV-valid")
        ).scalar_one()

        # The legacy row is now a strict SessionPlan; the already-valid row is untouched.
        SessionPlan.model_validate(repaired_row)
        _assert_no_legacy_payload_keys(repaired_row)
        assert valid_row == valid_plan

        # Idempotent: a second pass audits clean and rewrites nothing.
        assert apply_payload_repairs(connection) == []


class _FakeScalars:
    def __init__(self, result: object) -> None:
        self._result = result

    def first(self) -> object:
        return self._result


class _FakeResult:
    def __init__(self, result: object) -> None:
        self._result = result

    def scalars(self) -> _FakeScalars:
        return _FakeScalars(self._result)


class _FakeAsyncSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.committed = False

    async def execute(self, _stmt, _params: object = None) -> _FakeResult:
        return _FakeResult(None)

    def add(self, instance: object) -> None:
        self.added.append(instance)

    async def flush(self) -> None:
        # persist_plan_version flushes the version row (for the objectives' FK) before
        # the single terminal commit; this unit test only inspects added/committed.
        return None

    async def commit(self) -> None:
        self.committed = True


def test_persist_plan_version_stores_strict_session_plan(monkeypatch: pytest.MonkeyPatch) -> None:
    generated_session_plan = _valid_session_plan()
    fake_db = _FakeAsyncSession()
    generated = GeneratedLessonPlan(
        session_plan=generated_session_plan,
        run_metadata={"model": "test"},
    )

    issued_ids = iter(["LP-persisted", "LPV-persisted"])
    monkeypatch.setattr(repository, "new_public_id", lambda _prefix: next(issued_ids))

    session_context = SessionContext(
        session_id="SS1-GMATH-T1-W01-S01",
        lesson_period_id=uuid.uuid4(),
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

    plan_version_info = asyncio.run(
        repository.persist_plan_version(
            cast(AsyncSession, fake_db),
            session_context=session_context,
            generation=generated,
            created_by="teacher-1",
        )
    )

    # persist_plan_version adds the PlanVersion plus the derived
    # PlanVersionObjective rows; pick the PlanVersion (the only added object
    # carrying a session_plan).
    stored_version = next(item for item in fake_db.added if isinstance(item, PlanVersion))
    expected_session_plan = SessionPlan.model_validate(_valid_session_plan()).model_dump(
        mode="json",
        exclude_none=True,
    )
    expected_session_plan["plan_id"] = "LP-persisted"

    assert fake_db.committed is True
    assert plan_version_info.plan_id == "LP-persisted"
    assert stored_version.session_plan == expected_session_plan
    assert "mode" not in stored_version.session_plan["steps"][0]
    assert generated_session_plan["plan_id"] == "LP-generated"
