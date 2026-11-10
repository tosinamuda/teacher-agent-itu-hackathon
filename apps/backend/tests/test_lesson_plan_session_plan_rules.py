"""Safety-net checks for the strict post-generation objective-count cap.

The refine loop self-corrects on the cap (see test_semantic_score and
test_lesson_plan_no_linkage), but the deterministic validator must remain the
final backstop so a plan that slips through still fails closed rather than
persisting more than the allowed number of objectives.
"""

from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.drafting.validation.session_plan_rules import (
    MAX_LESSON_OBJECTIVES,
    validate_lesson_objective_step_alignment,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.types import ValidationIssue
from app.shared.json_types import JsonObject


def _plan_with_objectives(count: int) -> JsonObject:
    return {
        "curriculum_objectives": [{"curriculum_objective_id": "co-1"}],
        "lesson_plan_objectives": [
            {
                "lesson_objective_id": f"lop{index:02d}",
                "curriculum_objective_id": "co-1",
                "kc_type": "concept",
                "kc_focus": f"distinct focus {index}",
            }
            for index in range(1, count + 1)
        ],
        "steps": [],
    }


def _has_cap_issue(issues: list[ValidationIssue]) -> bool:
    return any(
        "at most" in issue["message"] and "core lesson objectives" in issue["message"]
        for issue in issues
    )


def test_safety_net_flags_more_than_max_objectives() -> None:
    issues = validate_lesson_objective_step_alignment(
        _plan_with_objectives(MAX_LESSON_OBJECTIVES + 1)
    )
    assert _has_cap_issue(issues)


def test_safety_net_allows_exactly_max_objectives() -> None:
    issues = validate_lesson_objective_step_alignment(_plan_with_objectives(MAX_LESSON_OBJECTIVES))
    assert not _has_cap_issue(issues)
