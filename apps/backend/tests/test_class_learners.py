"""A teacher's class: each learner with the band and score of their latest class test.

The class is the workspace's class, the test is the latest submission for that workspace's
subject only, and a teacher reads only a workspace they teach.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import datetime

import casbin
import pytest
import pytest_asyncio
from casbin.persist.adapters.string_adapter import StringAdapter
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.db.deps import get_db
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
    PlanVersionObjective,
)
from app.domains.assessments.models.exit_ticket import ExitTicketSubmission
from app.domains.learners.models.learner import LearnerProfile
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.domain.class_test_outcome import outcome_of
from app.domains.teaching.models import TeacherWorkspace
from app.domains.teaching.models.syllabus import LessonPeriod, SchemeOfWork
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from migrations.data.casbin_policy_seed import _CAPABILITY_POLICIES

TEACHER = uuid.UUID(int=901)
OTHER_TEACHER = uuid.UUID(int=902)
CLASS_ID = uuid.uuid4()
MATHS_OFFERING = uuid.uuid4()
SCIENCE_OFFERING = uuid.uuid4()
WORKSPACE = uuid.uuid4()
PERIOD_OF: dict[str, uuid.UUID] = {}


def _objective(objective_id: str, correct: int, total: int) -> dict[str, object]:
    return {"lesson_objective_id": objective_id, "score": correct, "max_score": total}


def _lesson(offering: uuid.UUID, name: str) -> list[object]:
    scheme, period = uuid.uuid4(), uuid.uuid4()
    PERIOD_OF[name] = period
    return [
        SchemeOfWork(id=scheme, term_class_subject_id=offering, week_number=1, title=name),
        LessonPeriod(id=period, scheme_of_work_id=scheme, period_number=1),
        LessonPlan(
            plan_id=f"P-{name}",
            lesson_period_id=period,
            title=name,
            subject=name,
            track="General",
            grade="JSS1",
        ),
        PlanVersion(
            version_id=f"LPV-{name}",
            plan_id=f"P-{name}",
            source_type="manual",
            session_plan={"lesson_plan_objectives": []},
            status=PlanVersionStatus.APPROVED,
        ),
    ]


def _submission(
    student: str, version: str, day: int, objectives: list[object]
) -> ExitTicketSubmission:
    return ExitTicketSubmission(
        diagnostic_id=f"D-{student}-{version}",
        student_id=student,
        plan_version_id=version,
        results={"objectives": objectives},
        created_at=datetime(2026, 11, day),
    )


def _learner(student_id: str, name: str, class_id: uuid.UUID | None = CLASS_ID) -> LearnerProfile:
    return LearnerProfile(
        student_id=student_id, full_name=name, grade="JSS1", track="General", class_id=class_id
    )


@pytest_asyncio.fixture
async def client(db, monkeypatch) -> AsyncIterator[tuple[AsyncClient, dict[str, Actor]]]:  # type: ignore[no-untyped-def]
    policy = "\n".join(
        [f"p, {role}, {obj}, {act}, allow" for role, obj, act in _CAPABILITY_POLICIES]
        + [f"g, {TEACHER}, teacher", f"g, {OTHER_TEACHER}, teacher"]
    )
    enforcer = casbin.Enforcer(authz.MODEL_PATH, StringAdapter(policy))

    async def _enforcer() -> casbin.Enforcer:
        return enforcer

    monkeypatch.setattr(authz, "get_enforcer", _enforcer)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            TermClassSubject(
                id=MATHS_OFFERING, course_id=uuid.uuid4(), class_id=CLASS_ID, term="T1", year="2026"
            ),
            TermClassSubject(
                id=SCIENCE_OFFERING,
                course_id=uuid.uuid4(),
                class_id=CLASS_ID,
                term="T1",
                year="2026",
            ),
            TeacherWorkspace(
                id=WORKSPACE, teacher_id=TEACHER, term_class_subject_id=MATHS_OFFERING
            ),
            *_lesson(MATHS_OFFERING, "Fractions"),
            *_lesson(MATHS_OFFERING, "Decimals"),
            *_lesson(SCIENCE_OFFERING, "Cells"),
            PlanVersionObjective(
                plan_version_id="LPV-Fractions",
                lesson_objective_id="a",
                objective_text="Add fractions",
                objective_order=1,
            ),
            PlanVersionObjective(
                plan_version_id="LPV-Fractions",
                lesson_objective_id="b",
                objective_text="Compare fractions",
                objective_order=2,
            ),
            _learner("S-ADA", "Adaeze O."),
            _learner("S-IBR", "Ibrahim S."),
            _learner("S-NEW", "Kelechi N."),
            _learner("S-ELSEWHERE", "Someone Else", class_id=uuid.uuid4()),
        ]
    )
    await db.flush()
    db.add_all(
        [
            _submission(
                "S-ADA", "LPV-Fractions", 3, [_objective("a", 1, 2), _objective("b", 1, 3)]
            ),
            _submission("S-ADA", "LPV-Decimals", 5, [_objective("a", 2, 2), _objective("b", 3, 3)]),
            _submission(
                "S-IBR", "LPV-Fractions", 4, [_objective("a", 2, 2), _objective("b", 2, 3)]
            ),
            _submission("S-IBR", "LPV-Cells", 6, [_objective("a", 0, 2)]),
        ]
    )
    await db.flush()
    caller = {"actor": Actor(role="teacher", auth_id="code|t", teacher_id=TEACHER)}

    async def _db() -> AsyncIterator:
        yield db

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_actor] = lambda: caller["actor"]
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
            yield http, caller
    finally:
        app.dependency_overrides.clear()


def _by_id(body: dict[str, list[dict[str, object]]]) -> dict[str, dict[str, object]]:
    return {row["student_id"]: row for row in body["learners"]}  # type: ignore[misc]


@pytest.mark.asyncio
async def test_each_learner_shows_their_latest_test_for_this_subject(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client

    response = await http.get(f"/teaching/workspaces/{WORKSPACE}/learners")

    assert response.status_code == 200, response.text
    rows = _by_id(response.json())
    assert set(rows) == {"S-ADA", "S-IBR", "S-NEW"}
    assert rows["S-ADA"]["last_test"] == {
        "lesson_title": "Decimals",
        "band": "extend",
        "correct": 5,
        "out_of": 5,
        "taken_at": rows["S-ADA"]["last_test"]["taken_at"],  # type: ignore[index]
    }
    # Ibrahim's Cells test is another subject, so his Fractions test is the latest here.
    assert rows["S-IBR"]["last_test"]["lesson_title"] == "Fractions"  # type: ignore[index]
    assert rows["S-NEW"]["last_test"] is None


@pytest.mark.asyncio
async def test_a_teacher_cannot_read_another_teachers_class(client) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    caller["actor"] = Actor(role="teacher", auth_id="code|o", teacher_id=OTHER_TEACHER)

    response = await http.get(f"/teaching/workspaces/{WORKSPACE}/learners")

    assert response.status_code == 403


def test_a_learner_is_placed_by_their_weakest_objective() -> None:
    outcome = outcome_of("S-1", {"objectives": [_objective("a", 2, 2), _objective("b", 0, 2)]})

    assert outcome is not None
    assert (outcome.band, outcome.correct, outcome.out_of) == ("remediate", 2, 4)


def test_a_test_without_objectives_places_nobody() -> None:
    assert outcome_of("S-1", {"objectives": []}) is None


def test_a_test_without_counts_still_has_a_band_but_no_score() -> None:
    outcome = outcome_of(
        "S-1", {"objectives": [{"lesson_objective_id": "a", "score": None, "max_score": None}]}
    )

    assert outcome is not None
    assert (outcome.correct, outcome.out_of) == (None, None)


@pytest.mark.asyncio
async def test_a_learner_page_lists_their_tests_newest_first_and_objectives_weakest_first(
    client,
) -> None:  # type: ignore[no-untyped-def]
    http, _ = client

    response = await http.get(f"/teaching/workspaces/{WORKSPACE}/learners/S-ADA/results")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["full_name"] == "Adaeze O."
    assert [test["lesson_title"] for test in body["tests"]] == ["Decimals", "Fractions"]
    assert [
        (row["objective_text"], row["band"], row["correct"], row["out_of"])
        for row in body["objectives"]
    ][:2] == [("Compare fractions", "remediate", 1, 3), ("Add fractions", "reinforce", 1, 2)]


@pytest.mark.asyncio
async def test_a_learner_outside_the_class_has_no_page(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client

    response = await http.get(f"/teaching/workspaces/{WORKSPACE}/learners/S-ELSEWHERE/results")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_another_teacher_cannot_read_a_learner_page(client) -> None:  # type: ignore[no-untyped-def]
    http, caller = client
    caller["actor"] = Actor(role="teacher", auth_id="code|o", teacher_id=OTHER_TEACHER)

    response = await http.get(f"/teaching/workspaces/{WORKSPACE}/learners/S-ADA/results")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_lesson_evidence_is_each_learners_test_for_that_lesson(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client
    lesson = PERIOD_OF["Fractions"]

    response = await http.get(f"/teaching/workspaces/{WORKSPACE}/lessons/{lesson}/evidence")

    assert response.status_code == 200, response.text
    rows = _by_id(response.json())
    assert rows["S-ADA"]["last_test"]["lesson_title"] == "Fractions"  # type: ignore[index]
    assert rows["S-ADA"]["last_test"]["correct"] == 2  # type: ignore[index]
    assert rows["S-NEW"]["last_test"] is None


@pytest.mark.asyncio
async def test_a_lesson_of_another_subject_has_no_evidence_here(client) -> None:  # type: ignore[no-untyped-def]
    http, _ = client
    lesson = PERIOD_OF["Cells"]

    response = await http.get(f"/teaching/workspaces/{WORKSPACE}/lessons/{lesson}/evidence")

    assert response.status_code == 404
