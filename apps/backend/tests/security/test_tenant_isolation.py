"""Characterization tests for cross-tenant isolation on the experiments API.

Threat model
============

Teachers are tenants. Each ``teacher`` owns a set of ``teacher_workspaces``.
A teacher MUST NOT be able to read another teacher's experiments through any
``/experiments/{...}`` route.

The ``research_manager`` role is intentionally cross-tenant (the researcher
who oversees the study sees every workspace). It is NOT the threat surface.

The gap these tests pinned (found ``2026-06-07``, CLOSED ``2026-06-11``)
========================================================================

The per-id getters in ``app/domains/experiments/api/routes.py`` originally
took no ``Actor`` dependency at all — any caller, including anonymous, could
pass any ``experiment_id`` and read the row.

Fixed 2026-06-11: every researcher-surface route now carries
``requires(obj="experiment:*", act="read")`` (and siblings: ``study:*``,
``rating:*``, ``workspace:*``), and the teacher role no longer holds any
``experiment:*`` verb in the Casbin matrix — experiment detail / story /
statistics / export are researcher surfaces. Teachers as a ROLE are denied,
which subsumes the original per-workspace concern for these routes.

The tests are read-only (no DB writes) so they are safe to run against the
dev DB without test-DB isolation.

Operational notes
=================

Requires the backend running at ``PTT_TEST_BACKEND_URL`` (defaults to
``http://localhost:8010``) with the seeded personas + experiments. The
research-manager (``researcher``) is used only to *discover* an experiment
id to attack — every actual assertion is run from the teacher's perspective.
"""

from __future__ import annotations

import os

import httpx
import pytest

BASE_URL: str = os.environ.get("PTT_TEST_BACKEND_URL", "http://localhost:8010")
TIMEOUT_S: float = 10.0

# Minimal personas seeded by ``scripts/seed_minimal_users.py`` (2026-06-11).
# ``teacher-1`` is the sole teacher and owns every workspace — the role-wide
# denial of ``experiment:*`` makes owner-vs-non-owner moot for these routes.
RESEARCH_MANAGER_CODE: str = "researcher"
TEACHER_CODE: str = "teacher-1"


def _hdr(code: str | None) -> dict[str, str]:
    return {"x-teacher-code": code} if code else {}


def _discover_experiment_id() -> str:
    """Use the research-manager (cross-tenant by design) to find ONE experiment id.

    This is the *attack target* — never the actor performing the assertion.
    """
    try:
        resp = httpx.get(
            f"{BASE_URL}/experiments",
            headers=_hdr(RESEARCH_MANAGER_CODE),
            timeout=TIMEOUT_S,
        )
    except httpx.RequestError as exc:
        # No live backend at PTT_TEST_BACKEND_URL — this is an integration check that
        # needs the running stack (see module docstring). Skip cleanly when the server
        # is absent rather than erroring the whole suite for everyone running unit tests.
        pytest.skip(f"backend not reachable at {BASE_URL} ({exc!r}); start the stack to run this")
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        pytest.skip("dev DB has no experiments seeded; cannot exercise the isolation gap")
    return str(rows[0]["experiment_id"])


@pytest.fixture(scope="module")
def target_experiment_id() -> str:
    return _discover_experiment_id()


def test_experiment_byid_rejects_anonymous(target_experiment_id: str) -> None:
    """GET /experiments/{id} with no auth header must NOT return data."""
    resp = httpx.get(
        f"{BASE_URL}/experiments/{target_experiment_id}",
        timeout=TIMEOUT_S,
    )
    assert resp.status_code in (401, 403, 404), (
        f"GET /experiments/{{id}} is wide open to anonymous callers — got "
        f"{resp.status_code}. The route has no Actor dependency."
    )


def test_experiment_byid_rejects_non_owner_teacher(target_experiment_id: str) -> None:
    """A teacher must not read experiment detail — it is a researcher surface.

    Stronger than the original owner-vs-non-owner framing: since 2026-06-11
    the teacher role holds no ``experiment:*`` verb at all, so even the
    workspace owner is denied here (their flows ride workspace:* / pack:*).
    """
    resp = httpx.get(
        f"{BASE_URL}/experiments/{target_experiment_id}",
        headers=_hdr(TEACHER_CODE),
        timeout=TIMEOUT_S,
    )
    assert resp.status_code in (403, 404), (
        f"GET /experiments/{{id}} returned {resp.status_code} to a teacher. "
        f"Experiment detail is a researcher surface."
    )


def test_experiment_summary_allows_owner_teacher(target_experiment_id: str) -> None:
    """GET /experiments/{id}/summary IS the teacher's experiment-plan read.

    The teacher-accessible counterpart to the (denied) detail route: it rides the
    ``lesson_plan:* author_plan`` gate, so the owning teacher gets 200. This is the
    route the lesson-prep page now calls instead of the researcher detail endpoint.
    """
    resp = httpx.get(
        f"{BASE_URL}/experiments/{target_experiment_id}/summary",
        headers=_hdr(TEACHER_CODE),
        timeout=TIMEOUT_S,
    )
    assert resp.status_code == 200, (
        f"GET /experiments/{{id}}/summary returned {resp.status_code} to the owning "
        f"teacher — the teacher experiment-plan page can't load its lesson."
    )
    body = resp.json()
    assert body["experiment_id"] == target_experiment_id
    # Header only — none of the researcher-surface detail keys leak through here.
    for researcher_key in ("executions", "focal_learner_candidates", "latest_summary"):
        assert researcher_key not in body, (
            f"/summary leaked researcher-only key {researcher_key!r} to a teacher."
        )


def test_experiment_summary_rejects_anonymous(target_experiment_id: str) -> None:
    """The teacher read still requires auth — anonymous callers get nothing."""
    resp = httpx.get(
        f"{BASE_URL}/experiments/{target_experiment_id}/summary",
        timeout=TIMEOUT_S,
    )
    assert resp.status_code in (401, 403, 404), (
        f"GET /experiments/{{id}}/summary is open to anonymous callers — got {resp.status_code}."
    )


def test_experiment_story_rejects_anonymous(target_experiment_id: str) -> None:
    """Sibling per-id route: /story has the same gap and must close together."""
    resp = httpx.get(
        f"{BASE_URL}/experiments/{target_experiment_id}/story",
        timeout=TIMEOUT_S,
    )
    assert resp.status_code in (401, 403, 404), (
        f"GET /experiments/{{id}}/story is wide open to anonymous callers — got {resp.status_code}."
    )


def test_experiment_story_rejects_non_owner_teacher(target_experiment_id: str) -> None:
    resp = httpx.get(
        f"{BASE_URL}/experiments/{target_experiment_id}/story",
        headers=_hdr(TEACHER_CODE),
        timeout=TIMEOUT_S,
    )
    assert resp.status_code in (403, 404), (
        f"GET /experiments/{{id}}/story returned {resp.status_code} to a teacher. "
        f"The story view is a researcher surface."
    )


def test_research_manager_can_still_read_byid(target_experiment_id: str) -> None:
    """Cross-tenant access remains LEGITIMATE for the research-manager role.

    The fix must not over-correct: research-manager sees everything by design.
    """
    resp = httpx.get(
        f"{BASE_URL}/experiments/{target_experiment_id}",
        headers=_hdr(RESEARCH_MANAGER_CODE),
        timeout=TIMEOUT_S,
    )
    assert resp.status_code == 200, (
        f"research-manager must retain cross-tenant read; got {resp.status_code}"
    )
