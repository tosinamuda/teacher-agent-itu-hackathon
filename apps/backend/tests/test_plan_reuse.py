"""Reusing a lesson plan that already exists: its old field names, and its curriculum mapping.

The fixture is the study's own plan for Week 9, as the study stored it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domains.artefacts.types.lesson_plan.application.errors import PlanValidationError
from app.domains.artefacts.types.lesson_plan.application.plan_reuse import (
    canonical_content,
    map_curriculum,
)
from app.shared.json_types import JsonObject

STUDY_PLAN: JsonObject = json.loads(
    (Path(__file__).parent / "fixtures" / "study_t2_w09_plan.json").read_text()
)
STUDY_CURRICULUM_ID = STUDY_PLAN["lesson_plan_objectives"][0]["curriculum_objective_id"]


def _curriculum(*ids: str) -> list[JsonObject]:
    return [
        {"curriculum_objective_id": found, "objective_text": f"text of {found}"} for found in ids
    ]


def test_a_plan_written_with_the_old_field_names_is_read_with_the_current_ones() -> None:
    content = canonical_content(STUDY_PLAN)

    assert [step["step_kind"] for step in content["steps"]] == [
        "intro",
        "core",
        "core",
        "core",
        "evaluation",
    ]
    assert all("step_role" not in step for step in content["steps"])
    first = content["lesson_plan_objectives"][0]
    assert first["kc_type"] == "procedure"
    assert first["kc_focus"]
    assert "knowledge_focus" not in first


def test_a_plan_that_cannot_be_read_is_refused_with_what_is_wrong() -> None:
    with pytest.raises(PlanValidationError):
        canonical_content({"steps": "not a list"})


def test_an_objective_keeps_the_curriculum_objective_the_lesson_has() -> None:
    mapped = map_curriculum(STUDY_PLAN, _curriculum(STUDY_CURRICULUM_ID, "other"), {})

    first = mapped.content["lesson_plan_objectives"][0]
    assert first["curriculum_objective_id"] == STUDY_CURRICULUM_ID
    assert first["curriculum_objective_text"] == f"text of {STUDY_CURRICULUM_ID}"
    assert [found["lesson_objective_id"] for found in mapped.unmapped] == [
        "lo-t2w09-02",
        "lo-t2w09-03",
    ]


def test_the_only_curriculum_objective_of_a_lesson_takes_every_objective() -> None:
    mapped = map_curriculum(STUDY_PLAN, _curriculum("only"), {})

    assert mapped.unmapped == []
    assert {
        found["curriculum_objective_id"] for found in mapped.content["lesson_plan_objectives"]
    } == {"only"}


def test_a_chosen_curriculum_objective_wins_over_the_one_a_plan_names() -> None:
    chosen = {"lo-t2w09-01": "b", "lo-t2w09-02": "a", "lo-t2w09-03": "a"}

    mapped = map_curriculum(STUDY_PLAN, _curriculum("a", "b"), chosen)

    assert mapped.unmapped == []
    assert [
        found["curriculum_objective_id"] for found in mapped.content["lesson_plan_objectives"]
    ] == ["b", "a", "a"]


def test_a_choice_that_is_not_a_curriculum_objective_of_the_lesson_leaves_it_unmapped() -> None:
    mapped = map_curriculum(STUDY_PLAN, _curriculum("a", "b"), {"lo-t2w09-01": "elsewhere"})

    assert "lo-t2w09-01" in [found["lesson_objective_id"] for found in mapped.unmapped]


def test_mapping_leaves_the_rest_of_the_plan_as_it_was() -> None:
    mapped = map_curriculum(STUDY_PLAN, _curriculum("only"), {})

    assert mapped.content["steps"] == STUDY_PLAN["steps"]
    assert (
        mapped.content["lesson_plan_objectives"][0]["objective_text"]
        == (STUDY_PLAN["lesson_plan_objectives"][0]["objective_text"])
    )
