"""The id-selection rules behind the batched experiment-list loader.

Every function under test is pure: given the experiments (and, where the rule
needs a class, the workspace map), which ids should the batched read ask for?
That is where the real logic lives — the "awaiting its plan" exclusions, the
lesson-period union, the focal-selection preconditions — and none of it needs a
repository, a session or a protocol fake. The objects below are real ORM rows,
just never flushed.

Complementary to ``test_experiment_views_list_n_plus_one.py``, which pins the
call SHAPE (one batched read per layer, constant in N) and does need a
call-counting repository double to do it.
"""

from __future__ import annotations

import uuid

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.experiments.application.experiment_list_loader import (
    class_ids,
    class_of,
    class_plan_pairs,
    focal_class_ids,
    focal_students_by_plan,
    group_by,
    lesson_period_ids,
    plan_version_ids,
)
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models import TeacherWorkspace


def _workspace(class_id: uuid.UUID | None) -> TeacherWorkspace:
    """A workspace, optionally unassigned to any class (``class_id=None``)."""
    return TeacherWorkspace(
        id=uuid.uuid4(),
        term_class_subject=None if class_id is None else TermClassSubject(class_id=class_id),
    )


def _experiment(
    workspace: TeacherWorkspace,
    *,
    plan_version_id: str | None = None,
    lesson_period_id: uuid.UUID | None = None,
    focal_learner_ids: list[str] | None = None,
) -> Experiment:
    return Experiment(
        id=uuid.uuid4(),
        experiment_id=f"EXP-{uuid.uuid4().hex[:8]}",
        teacher_workspace_id=workspace.id,
        plan_version_id=plan_version_id,
        lesson_period_id=lesson_period_id,
        focal_learner_ids=focal_learner_ids,
    )


def _by_id(*workspaces: TeacherWorkspace) -> dict[uuid.UUID, TeacherWorkspace]:
    return {workspace.id: workspace for workspace in workspaces}


def _plan(version_id: str, lesson_period_id: uuid.UUID) -> tuple[PlanVersion, LessonPlan]:
    plan_id = f"LP-{version_id}"
    return (
        PlanVersion(version_id=version_id, plan_id=plan_id),
        LessonPlan(plan_id=plan_id, lesson_period_id=lesson_period_id),
    )


# ===== plan_version_ids =====


def test_plan_version_ids_skips_experiments_awaiting_their_plan() -> None:
    workspace = _workspace(uuid.uuid4())
    experiments = [
        _experiment(workspace, plan_version_id="LPV-1"),
        _experiment(workspace, plan_version_id=None),
    ]

    assert plan_version_ids(experiments) == {"LPV-1"}


def test_plan_version_ids_dedupes_experiments_sharing_a_plan() -> None:
    workspace = _workspace(uuid.uuid4())
    experiments = [_experiment(workspace, plan_version_id="LPV-1") for _ in range(3)]

    assert plan_version_ids(experiments) == {"LPV-1"}


# ===== lesson_period_ids =====


def test_lesson_period_ids_unions_plan_periods_with_plan_less_experiments() -> None:
    """A plan-less experiment still names its lesson, so its period must be loaded."""
    workspace = _workspace(uuid.uuid4())
    planned_period, unplanned_period = uuid.uuid4(), uuid.uuid4()
    plans = {"LPV-1": _plan("LPV-1", planned_period)}
    experiments = [
        _experiment(workspace, plan_version_id="LPV-1"),
        _experiment(workspace, lesson_period_id=unplanned_period),
    ]

    assert lesson_period_ids(experiments, plans) == {planned_period, unplanned_period}


def test_lesson_period_ids_is_empty_when_nothing_names_a_period() -> None:
    workspace = _workspace(uuid.uuid4())

    assert lesson_period_ids([_experiment(workspace)], {}) == set()


# ===== class_of =====


def test_class_of_resolves_through_the_workspace() -> None:
    class_id = uuid.uuid4()
    workspace = _workspace(class_id)

    assert class_of(_experiment(workspace), _by_id(workspace)) == class_id


def test_class_of_is_none_when_the_workspace_was_not_fetched() -> None:
    workspace = _workspace(uuid.uuid4())

    assert class_of(_experiment(workspace), {}) is None


def test_class_of_is_none_when_the_workspace_has_no_class_assigned() -> None:
    workspace = _workspace(None)

    assert class_of(_experiment(workspace), _by_id(workspace)) is None


# ===== class_ids / class_plan_pairs =====


def test_class_ids_counts_rosters_for_plan_less_experiments_too() -> None:
    """Roster size is shown before a plan exists, so a plan-less experiment still counts."""
    class_id = uuid.uuid4()
    workspace = _workspace(class_id)

    assert class_ids([_experiment(workspace)], _by_id(workspace)) == {class_id}


def test_class_ids_skips_experiments_whose_class_does_not_resolve() -> None:
    unassigned = _workspace(None)

    assert class_ids([_experiment(unassigned)], _by_id(unassigned)) == set()


def test_class_plan_pairs_excludes_experiments_awaiting_their_plan() -> None:
    class_id = uuid.uuid4()
    workspace = _workspace(class_id)
    experiments = [
        _experiment(workspace, plan_version_id="LPV-1"),
        _experiment(workspace, plan_version_id=None),
    ]

    assert class_plan_pairs(experiments, _by_id(workspace)) == {(class_id, "LPV-1")}


def test_class_plan_pairs_keeps_one_class_across_several_plans() -> None:
    class_id = uuid.uuid4()
    workspace = _workspace(class_id)
    experiments = [
        _experiment(workspace, plan_version_id="LPV-1"),
        _experiment(workspace, plan_version_id="LPV-2"),
    ]

    assert class_plan_pairs(experiments, _by_id(workspace)) == {
        (class_id, "LPV-1"),
        (class_id, "LPV-2"),
    }


# ===== focal_class_ids / focal_students_by_plan =====


def test_focal_class_ids_needs_a_selection_a_plan_and_a_class() -> None:
    class_id = uuid.uuid4()
    workspace = _workspace(class_id)
    unassigned = _workspace(None)
    experiments = [
        _experiment(workspace, plan_version_id="LPV-1", focal_learner_ids=["S1"]),
        _experiment(workspace, plan_version_id="LPV-1", focal_learner_ids=[]),
        _experiment(workspace, plan_version_id=None, focal_learner_ids=["S2"]),
        _experiment(unassigned, plan_version_id="LPV-1", focal_learner_ids=["S3"]),
    ]

    assert focal_class_ids(experiments, _by_id(workspace, unassigned)) == {class_id}


def test_focal_students_by_plan_merges_experiments_sharing_a_plan() -> None:
    """This merge is what bounds the diagnostic reads by plan count rather than by N."""
    workspace = _workspace(uuid.uuid4())
    experiments = [
        _experiment(workspace, plan_version_id="LPV-1", focal_learner_ids=["S1", "S2"]),
        _experiment(workspace, plan_version_id="LPV-1", focal_learner_ids=["S2", "S3"]),
        _experiment(workspace, plan_version_id="LPV-2", focal_learner_ids=["S4"]),
    ]

    assert focal_students_by_plan(experiments, _by_id(workspace)) == {
        "LPV-1": {"S1", "S2", "S3"},
        "LPV-2": {"S4"},
    }


def test_focal_students_by_plan_is_empty_without_selections() -> None:
    workspace = _workspace(uuid.uuid4())
    experiments = [_experiment(workspace, plan_version_id="LPV-1")]

    assert focal_students_by_plan(experiments, _by_id(workspace)) == {}


# ===== group_by =====


def test_group_by_keeps_arrival_order_within_each_bucket() -> None:
    rows = [("a", 1), ("b", 2), ("a", 3)]

    assert group_by(rows, lambda row: row[0]) == {"a": [("a", 1), ("a", 3)], "b": [("b", 2)]}


def test_group_by_returns_a_plain_dict_that_does_not_grow_on_lookup() -> None:
    """Callers do ``.get(key, [])``; a defaultdict leaking out would insert on read."""
    grouped = group_by([("a", 1)], lambda row: row[0])
    grouped.get("missing", [])

    assert "missing" not in grouped
