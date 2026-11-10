"""The lesson-plan spec's requirements, as checks on a plan.

The spec asks what the study's own lesson plans did, which the grammar alone does not
enforce: each core-step student activity says whether it sets work, and the minutes add up
to the lesson. A plan the app writes is held to the same, so these are checked beside the
grammar.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

#: The step kinds of a lesson in the order the spec asks for them.
_ORDER = {"intro": 0, "core": 1, "evaluation": 2, "conclusion": 3}


def _steps(plan: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return list(plan.get("steps") or [])


def _undeclared_work(plan: Mapping[str, Any]) -> list[str]:
    return [
        f"{step.get('step_id')}: a student activity does not say whether it sets the "
        f"students work of their own ({str(activity.get('what') or '')[:60]!r})"
        for step in _steps(plan)
        if step.get("step_kind") == "core"
        for activity in step.get("activities") or []
        if activity.get("who") == "student" and activity.get("sets_work") is None
    ]


def _timing(plan: Mapping[str, Any], duration_minutes: int | None) -> list[str]:
    found = [
        f"{step.get('step_id')}: gives no minutes"
        for step in _steps(plan)
        if not isinstance(step.get("estimated_minutes"), int)
    ]
    total = sum(
        step["estimated_minutes"]
        for step in _steps(plan)
        if isinstance(step.get("estimated_minutes"), int)
    )
    if duration_minutes and total > duration_minutes:
        # Each step is written on its own, so each writer is shown every step's share.
        shares = ", ".join(
            f"{step.get('step_id')} {step['estimated_minutes']}"
            for step in _steps(plan)
            if isinstance(step.get("estimated_minutes"), int)
        )
        found.append(
            f"the steps take {total} minutes ({shares}); the lesson is {duration_minutes}, "
            f"so take {total - duration_minutes} minutes off"
        )
    return found


def _order(plan: Mapping[str, Any]) -> list[str]:
    kinds = [str(step.get("step_kind")) for step in _steps(plan)]
    ranks = [_ORDER.get(kind, -1) for kind in kinds]
    found = []
    if kinds[:1] != ["intro"] or "core" not in kinds:
        found.append(f"steps run {kinds}: an introduction, then the core steps")
    elif ranks != sorted(ranks):
        found.append(f"steps run {kinds}: out of teaching order")
    return found


def _untaught(plan: Mapping[str, Any]) -> list[str]:
    taught = {
        step.get("lesson_objective_id") for step in _steps(plan) if step.get("step_kind") == "core"
    }
    return [
        f"{objective.get('lesson_objective_id')}: no core step teaches it"
        for objective in plan.get("lesson_plan_objectives") or []
        if objective.get("lesson_objective_id") not in taught
    ]


def unmet(plan: Mapping[str, Any], *, duration_minutes: int | None) -> list[str]:
    """What the plan leaves of the spec's requirements; empty when it meets them all."""
    return [
        *_order(plan),
        *_untaught(plan),
        *_undeclared_work(plan),
        *_timing(plan, duration_minutes),
    ]
