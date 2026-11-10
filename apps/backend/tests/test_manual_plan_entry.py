"""FD-01: assembling + checking a hand-entered teacher lesson plan."""

from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.application.manual_entry import (
    assemble_manual_session_plan,
    curriculum_mapping_issues,
)
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext

_CURRICULUM = [
    {
        "curriculum_objective_id": "cur_obj01",
        "objective_text": "Read place value",
        "objective_order": 1,
    },
    {
        "curriculum_objective_id": "cur_obj02",
        "objective_text": "Write numbers",
        "objective_order": 2,
    },
]


def _session_context(**overrides: object) -> SessionContext:
    base: dict[str, object] = {
        "session_id": "sid-123",
        "subject": "Mathematics",
        "track": "General",
        "grade": "JSS1",
        "term": "Term 1",
        "week": 1,
        "day_index": 1,
        "topic": "Whole Numbers",
        "subtopic": "Place value",
        "duration_minutes": 45,
        "session_objectives": [],
        "general_objectives": [],
        "reference_materials": [],
    }
    base.update(overrides)
    return SessionContext(**base)  # type: ignore[arg-type]


def test_assemble_forces_identity_and_curriculum_over_teacher_input() -> None:
    # The teacher tries to send a different lesson identity; it must be ignored.
    content = {
        "plan_id": "HACK",
        "session_id": "OTHER",
        "subject": "English",
        "lesson_plan_objectives": [
            {"lesson_objective_id": "lop01", "curriculum_objective_id": "cur_obj01"}
        ],
        "steps": [],
    }
    session_plan = assemble_manual_session_plan(
        _session_context(theme="Number and Numeration"), _CURRICULUM, content
    )
    assert session_plan["plan_id"] == "manual-pending"
    assert session_plan["session_id"] == "sid-123"
    assert session_plan["subject"] == "Mathematics"
    assert session_plan["grade"] == "JSS1"
    assert session_plan["theme"] == "Number and Numeration"
    assert session_plan["curriculum_objectives"] == _CURRICULUM
    # Teacher content is preserved.
    assert session_plan["lesson_plan_objectives"][0]["lesson_objective_id"] == "lop01"


def test_assemble_omits_theme_when_absent() -> None:
    session_plan = assemble_manual_session_plan(_session_context(), _CURRICULUM, {"steps": []})
    assert "theme" not in session_plan


def test_mapping_issues_flags_unknown_and_missing_ids() -> None:
    session_plan = {
        "lesson_plan_objectives": [
            {"lesson_objective_id": "lop01", "curriculum_objective_id": "cur_obj01"},
            {"lesson_objective_id": "lop02", "curriculum_objective_id": "ghost"},
            {"lesson_objective_id": "lop03"},
        ]
    }
    issues = curriculum_mapping_issues(session_plan, _CURRICULUM)
    assert len(issues) == 2
    assert any("lop02" in issue and "ghost" in issue for issue in issues)
    assert any("lop03" in issue for issue in issues)


def test_mapping_issues_empty_when_all_mapped() -> None:
    session_plan = {
        "lesson_plan_objectives": [
            {"lesson_objective_id": "lop01", "curriculum_objective_id": "cur_obj01"},
            {"lesson_objective_id": "lop02", "curriculum_objective_id": "cur_obj02"},
        ]
    }
    assert curriculum_mapping_issues(session_plan, _CURRICULUM) == []
