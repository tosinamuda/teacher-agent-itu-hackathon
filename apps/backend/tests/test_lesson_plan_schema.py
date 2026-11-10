"""One lesson plan schema for the study's plans and the app's, drafted or entered."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.domains.artefacts.types.lesson_plan.domain.schema import schema_issues
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import StepActivity
from app.domains.artefacts.types.lesson_plan.drafting.validation import validate_session_plan
from app.shared.json_types import JsonObject

EVAL_SET = Path("experiments/h1_condition_eval/eval_set.json")
#: A step's lesson note: the teacher's content for teaching it, a record of its own. The
#: study's frozen plans carry it inline because that is how the generator read it.
LESSON_NOTE_FIELDS = ("note", "note_file")


def _study_lesson_plans() -> dict[str, JsonObject]:
    plans = {}
    for case in json.loads(EVAL_SET.read_text(encoding="utf-8"))["cases"]:
        plan = case["plan"]
        steps = [
            {key: value for key, value in step.items() if key not in LESSON_NOTE_FIELDS}
            for step in plan["steps"]
        ]
        plans[case["lesson"]] = {**plan, "steps": steps}
    return plans


@pytest.mark.parametrize("lesson", sorted(_study_lesson_plans()))
def test_each_study_lesson_plan_has_the_lesson_plan_shape(lesson: str) -> None:
    assert schema_issues(_study_lesson_plans()[lesson]) == []


def test_the_study_plans_declare_which_student_activities_set_work() -> None:
    declared = [
        activity["sets_work"]
        for plan in _study_lesson_plans().values()
        for step in plan["steps"]
        for activity in step.get("activities", [])
        if "sets_work" in activity
    ]

    assert len(declared) == 19


def test_a_teachers_plan_is_not_held_to_the_rules_a_draft_meets() -> None:
    """t3-w06 teaches five objectives; a drafted plan may carry four."""
    plan = _study_lesson_plans()["t3-w06"]

    assert schema_issues(plan) == []
    assert "lesson plan may define at most 4 core lesson objectives" in {
        issue["message"] for issue in validate_session_plan(plan)
    }


def test_only_a_student_activity_says_whether_it_sets_work() -> None:
    assert StepActivity(who="student", what="solve the questions", sets_work=True).sets_work
    assert StepActivity(who="teacher", what="explains the rule").sets_work is None
    with pytest.raises(ValidationError):
        StepActivity(who="teacher", what="sets questions", sets_work=True)


def test_an_undeclared_activity_is_stored_without_the_key() -> None:
    """The schema takes a boolean; a teacher's line, or an undeclared one, has no key at all."""
    assert StepActivity(who="teacher", what="explains the rule").model_dump() == {
        "who": "teacher",
        "what": "explains the rule",
    }


def test_a_stored_plan_is_read_as_kept_though_a_new_one_must_carry_every_block() -> None:
    """The teacher's perimeter step works examples and sets no practice block of its own."""
    import json

    import pytest
    from pydantic import ValidationError

    from app.domains.artefacts.types.lesson_plan.application.service import (
        normalize_session_plan_payload,
    )
    from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
        READING_A_STORED_PLAN,
        SessionPlan,
    )
    from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
    from experiments.study_import.dataset import LESSON_NOTE_FIELDS

    [plan] = [
        case["plan"]
        for case in json.loads(EVAL_SET_PATH.read_text())["cases"]
        if case["lesson"] == "t3-w02"
    ]
    steps = [
        {k: v for k, v in step.items() if k not in LESSON_NOTE_FIELDS} for step in plan["steps"]
    ]
    stored = normalize_session_plan_payload({**plan, "steps": steps})

    read = SessionPlan.model_validate(stored, context=READING_A_STORED_PLAN)

    assert len(read.steps) == len(plan["steps"])
    with pytest.raises(ValidationError, match="procedure core steps require blocks: practice"):
        SessionPlan.model_validate(stored)
