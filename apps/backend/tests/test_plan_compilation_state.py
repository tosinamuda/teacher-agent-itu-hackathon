import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.db.deps import get_db
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor

client = TestClient(app)


@pytest.fixture(autouse=True)
def _teacher_may_read_plans(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reading a plan needs a signed-in reader; the permission table is tested elsewhere."""

    async def _allow(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(authz, "enforce", _allow)
    teacher = Actor(role="teacher", auth_id="code|t1", teacher_id=uuid.uuid4())
    monkeypatch.setitem(app.dependency_overrides, get_actor, lambda: teacher)


class FakeScalars:
    def __init__(self, result):
        self._result = result

    def first(self):
        return self._result


class FakeResult:
    def __init__(self, result):
        self._result = result

    def scalars(self):
        return FakeScalars(self._result)

    def first(self):
        return self._result


class FakeSession:
    def __init__(self, plan_result=None, pack_result=None):
        self._plan_result = plan_result
        self._pack_result = pack_result

    async def execute(self, stmt):
        stmt_str = str(stmt)
        if "artefacts" in stmt_str:
            return FakeResult(self._pack_result)
        # plan_versions + lesson_plans join query returns a tuple row
        if "plan_versions" in stmt_str:
            return FakeResult(self._plan_result)
        # Any other table (the lesson's session, say) holds nothing here.
        return FakeResult(None)


def _session_plan_payload() -> dict:
    return {
        "plan_id": "LP-TEST-1",
        "session_id": "SESSION-1",
        "subject": "Math",
        "track": "General",
        "grade": "SS1",
        "term": "First Term",
        "week": 1,
        "topic": "Number Bases",
        "subtopic": "Binary Conversion",
        "curriculum_objectives": [
            {
                "curriculum_objective_id": "curr-1",
                "objective_text": "Convert binary numbers to base 10",
                "objective_order": 1,
            }
        ],
        "lesson_plan_objectives": [
            {
                "lesson_objective_id": "obj01",
                "objective_text": "Convert binary numbers to base 10",
                "objective_order": 1,
                "curriculum_objective_id": "curr-1",
                "curriculum_objective_text": "Convert binary numbers to base 10",
                "kc_type": "representation",
                "kc_focus": "Convert binary numbers to base 10",
                "source_form": "base 2",
                "target_form": "base 10",
            }
        ],
        "steps": [
            {
                "step_id": "step-core-01",
                "step_kind": "core",
                "instructional_type": "explain_only",
                "kc_type": "representation",
                "lesson_objective_id": "obj01",
                "title": "Practice",
                "content": "Convert 1010 to base 10.",
                "estimated_minutes": 10,
                "activities": [],
                "blocks": [
                    {
                        "id": "block-exp-01",
                        "type": "explanation",
                        "content": "Convert $1010_2$ to base 10.",
                    },
                    {
                        "id": "block-example-01",
                        "type": "worked_example",
                        "problem": "Convert 1010 in base 2 to base 10.",
                        "steps": [{"label": "Step 1", "content": "Expand using place values."}],
                        "final_answer": "10",
                    },
                    {
                        "id": "block-practice-01",
                        "type": "practice",
                        "question": "Convert 1100 in base 2 to base 10.",
                        "answer": "12",
                        "lesson_objective_id": "obj01",
                    },
                ],
            }
        ],
    }


def test_get_plan_includes_compiled_artefact_id():
    plan_id = "LP-TEST-1"
    version_id = "LPV-TEST-1"
    artefact_id = "ARTEFACT-TEST-1"

    mock_plan = SimpleNamespace(
        id="uuid-plan",
        plan_id=plan_id,
        lesson_period_id=uuid.uuid4(),
        subject="Math",
        track="General",
        grade="SS1",
    )

    mock_version = SimpleNamespace(
        id="uuid-version",
        version_id=version_id,
        plan_id=plan_id,
        status="approved",
        closed_reason=None,
        closed_at=None,
        session_plan=_session_plan_payload(),
        created_at=datetime.now(timezone.utc),
    )

    mock_pack = SimpleNamespace(
        artefact_id=artefact_id,
        plan_version_id=version_id,
        created_at=datetime.now(timezone.utc),
    )

    async def _fake_db():
        yield FakeSession(
            plan_result=(mock_version, mock_plan),
            pack_result=mock_pack,
        )

    app.dependency_overrides[get_db] = _fake_db

    response = client.get(f"/artefacts/lesson-plans/{plan_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["plan_id"] == plan_id
    assert data["version_id"] == version_id
    assert data["compiled_artefact_id"] == artefact_id
    # A single core step is not a lesson the spec accepts; the teacher is shown why.
    assert data["unmet_requirements"] == [
        "steps run ['core']: an introduction, then the core steps"
    ]


def test_get_plan_no_artefact_returns_null():
    plan_id = "LP-TEST-1"
    version_id = "LPV-TEST-1"

    mock_plan = SimpleNamespace(
        id="uuid-plan",
        plan_id=plan_id,
        lesson_period_id=uuid.uuid4(),
        subject="Math",
        track="General",
        grade="SS1",
    )

    mock_version = SimpleNamespace(
        id="uuid-version",
        version_id=version_id,
        plan_id=plan_id,
        status="approved",
        closed_reason=None,
        closed_at=None,
        session_plan=_session_plan_payload(),
        created_at=datetime.now(timezone.utc),
    )

    async def _fake_db():
        yield FakeSession(
            plan_result=(mock_version, mock_plan),
            pack_result=None,
        )

    app.dependency_overrides[get_db] = _fake_db

    response = client.get(f"/artefacts/lesson-plans/{plan_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["compiled_artefact_id"] is None


def test_get_plan_normalizes_saved_session_plan_content():
    plan_id = "LP-TEST-1"
    version_id = "LPV-TEST-1"

    mock_plan = SimpleNamespace(
        id="uuid-plan",
        plan_id=plan_id,
        lesson_period_id=uuid.uuid4(),
        subject="Math",
        track="General",
        grade="SS1",
    )

    session_plan = _session_plan_payload()
    session_plan["steps"][0]["content"] = r"Write \(1,000,000,000,000\)\nIn words."
    session_plan["steps"][0]["blocks"] = [
        {
            "id": "block-exp-01",
            "type": "explanation",
            "content": r"Write \(1,000,000,000,000\)\nIn words.",
        },
        {
            "id": "block-example-01",
            "type": "worked_example",
            "problem": "Read 1,000,000,000,000 aloud.",
            "steps": [{"label": "Step 1", "content": "Group digits into periods."}],
            "final_answer": "One trillion",
        },
        {
            "id": "block-pr-01",
            "type": "practice",
            "question": r"Write \(1,000,000,000,000\) in words.",
            "answer": r"Digits: \(1,000,000,000,000\)\nWords: one trillion",
            "hints": [r"Start with \(1,000,000,000,000\)."],
            "lesson_objective_id": "obj01",
        },
    ]

    mock_version = SimpleNamespace(
        id="uuid-version",
        version_id=version_id,
        plan_id=plan_id,
        status="approved",
        closed_reason=None,
        closed_at=None,
        session_plan=session_plan,
        created_at=datetime.now(timezone.utc),
    )

    async def _fake_db():
        yield FakeSession(
            plan_result=(mock_version, mock_plan),
            pack_result=None,
        )

    app.dependency_overrides[get_db] = _fake_db

    response = client.get(f"/artefacts/lesson-plans/{plan_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    step = data["session_plan"]["steps"][0]
    practice_block = next(block for block in step["blocks"] if block["type"] == "practice")
    assert step["content"] == "Write $1,000,000,000,000$\nIn words."
    assert practice_block["answer"] == "Digits: $1,000,000,000,000$\nWords: one trillion"
