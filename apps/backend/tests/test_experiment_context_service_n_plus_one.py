"""Regression guards: ``ExperimentContextApplicationService.list_workspace_lessons``
and ``.list_focal_learner_candidates`` must NOT call the repository in a loop.

Both previously did the textbook N+1 — query count grew linearly with the
collection size (lessons, learners). The fix lifts those into batched
repository methods. These tests pin the new contract: zero calls to the
per-element methods, exactly ONE call to each batched method, regardless of
collection size.

Mock-based — proves the call SHAPE without a live DB; the goal is to fail
loudly if anyone reintroduces a per-element loop.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, cast

import pytest

from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
    ExperimentContextReader,
    ExperimentWorkspaceCatalogueReader,
    ExperimentWorkspaceCatalogueService,
)
from app.domains.experiments.infrastructure.models import Experiment

# ----------------------------------------------------------------------------
# list_workspace_lessons — per-lesson list_approved_plan_versions_for_session N+1
# ----------------------------------------------------------------------------


@dataclass
class _FakeLessonsRepo:
    """Just enough for ``list_workspace_lessons`` to run end-to-end."""

    workspace: Any
    lessons: list[Any]
    calls: dict[str, int] = field(default_factory=dict)

    def _tick(self, name: str) -> None:
        self.calls[name] = self.calls.get(name, 0) + 1

    async def get_workspace(self, workspace_id: uuid.UUID) -> Any:
        self._tick("get_workspace")
        return self.workspace

    async def list_lessons_for_term_class_subject(
        self, *, term_class_subject_id: uuid.UUID
    ) -> list[Any]:
        self._tick("list_lessons_for_term_class_subject")
        return list(self.lessons)

    async def list_approved_plan_versions_for_lesson_periods(
        self, *, lesson_period_ids: Sequence[uuid.UUID]
    ) -> list[tuple[Any, Any]]:
        self._tick("list_approved_plan_versions_for_lesson_periods")
        return []

    async def list_approved_plan_versions_for_session(
        self, *, lesson_period_id: uuid.UUID
    ) -> list[tuple[Any, Any]]:
        # ANY call here is the N+1 we retired.
        self._tick("list_approved_plan_versions_for_session__NPLUSONE_REGRESSION")
        return []


@pytest.mark.parametrize("n_lessons", [1, 5, 30])
@pytest.mark.asyncio
async def test_list_workspace_lessons_is_constant_queries(n_lessons: int) -> None:
    """Repository call count must NOT grow with lesson count."""

    @dataclass
    class _FakeLesson:
        id: uuid.UUID

    @dataclass
    class _FakeWorkspace:
        term_class_subject: Any

    @dataclass
    class _FakeTCS:
        id: uuid.UUID

    workspace = _FakeWorkspace(term_class_subject=_FakeTCS(id=uuid.uuid4()))
    lessons = [_FakeLesson(id=uuid.uuid4()) for _ in range(n_lessons)]

    repo = _FakeLessonsRepo(workspace=workspace, lessons=lessons)
    service = ExperimentWorkspaceCatalogueService(
        repository=cast(ExperimentWorkspaceCatalogueReader, repo)
    )

    candidates = await service.list_workspace_lessons(workspace_id=uuid.uuid4())

    assert len(candidates) == n_lessons
    # Per-element method MUST NOT have been called.
    assert repo.calls.get("list_approved_plan_versions_for_session__NPLUSONE_REGRESSION", 0) == 0, (
        "list_approved_plan_versions_for_session() called per-lesson — the N+1 returned. "
        f"call counts: {repo.calls}"
    )
    # Batched method called exactly once.
    assert repo.calls.get("list_approved_plan_versions_for_lesson_periods") == 1


# ----------------------------------------------------------------------------
# list_focal_learner_candidates — per-learner latest_diagnostic_for_learner N+1
# ----------------------------------------------------------------------------


@dataclass
class _FakeFocalRepo:
    """Repo recording every method ``list_focal_learner_candidates`` touches.

    The service first calls ``get_experiment_context`` (not on this repo —
    that runs its own composition of repo calls) but we test the
    fast-path: a context fixture pre-built so the batched diagnostic
    lookup is what's measured.
    """

    workspace: Any
    learners: list[Any]
    calls: dict[str, int] = field(default_factory=dict)

    def _tick(self, name: str) -> None:
        self.calls[name] = self.calls.get(name, 0) + 1

    async def list_all_learners_for_class(self, *, class_id: uuid.UUID) -> list[Any]:
        self._tick("list_all_learners_for_class")
        return list(self.learners)

    async def latest_diagnostic_per_student(
        self, *, student_ids: Sequence[str], plan_version_id: str
    ) -> dict[str, Any]:
        self._tick("latest_diagnostic_per_student")
        return {}

    async def latest_diagnostic_for_learner(self, *, student_id: str, plan_version_id: str) -> Any:
        # ANY call here is the N+1.
        self._tick("latest_diagnostic_for_learner__NPLUSONE_REGRESSION")
        return None


@pytest.mark.parametrize("n_learners", [1, 8, 40])
@pytest.mark.asyncio
async def test_list_focal_learner_candidates_is_constant_queries(
    monkeypatch: pytest.MonkeyPatch, n_learners: int
) -> None:
    """One batched diagnostic lookup, regardless of learner count."""

    @dataclass
    class _FakeLearner:
        student_id: str

    @dataclass
    class _FakeWorkspace:
        term_class_subject: Any

    @dataclass
    class _FakeTCS:
        class_id: uuid.UUID

    @dataclass
    class _FakeContext:
        workspace: Any

    workspace = _FakeWorkspace(term_class_subject=_FakeTCS(class_id=uuid.uuid4()))
    learners = [_FakeLearner(student_id=f"S-{i}") for i in range(n_learners)]
    repo = _FakeFocalRepo(workspace=workspace, learners=learners)

    service = ExperimentContextApplicationService(repository=cast(ExperimentContextReader, repo))

    # Short-circuit get_experiment_context — its own query fan-out is a
    # separate concern. Inject the pre-built context.
    async def _fake_context(*, experiment: Any) -> _FakeContext:
        return _FakeContext(workspace=workspace)

    monkeypatch.setattr(service, "get_experiment_context", _fake_context)

    experiment = Experiment(
        id=uuid.uuid4(),
        experiment_id="EXP-test",
        experiment_code="EXP-TEST-001",
        teacher_workspace_id=uuid.uuid4(),
        plan_version_id="LPV-test",
        focal_learner_ids=[],
    )
    candidates = await service.list_focal_learner_candidates(experiment=experiment)

    assert len(candidates) == n_learners
    assert repo.calls.get("latest_diagnostic_for_learner__NPLUSONE_REGRESSION", 0) == 0, (
        "latest_diagnostic_for_learner() called per-learner — the N+1 returned. "
        f"call counts: {repo.calls}"
    )
    assert repo.calls.get("latest_diagnostic_per_student") == 1
