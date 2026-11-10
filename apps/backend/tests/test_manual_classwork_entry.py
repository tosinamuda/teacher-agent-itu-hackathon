"""FD-02: assembling + checking hand-entered classwork MCQ items (pure helpers)."""

from __future__ import annotations

import uuid

from app.domains.assessments.application.manual_entry import (
    build_classwork_item_payloads,
    classwork_item_issues,
)
from app.domains.assessments.classwork_schemas import ManualClassworkItem
from app.domains.curriculum.models.exit_tickets import ExitTicketItem


def _item(**overrides: object) -> ManualClassworkItem:
    base: dict[str, object] = {
        "lesson_objective_id": "lop01",
        "stem": "What is 2 + 2?",
        "options": {"A": "3", "B": "4"},
        "correct_option": "B",
    }
    base.update(overrides)
    return ManualClassworkItem(**base)  # type: ignore[arg-type]


def test_payload_matches_exit_ticket_item_columns() -> None:
    # The misconception map is filtered to wrong options that exist (the correct
    # option and unknown keys drop out), mirroring the LLM diagnostic path.
    payloads = build_classwork_item_payloads(
        [
            _item(
                difficulty="easy",
                option_misconceptions={"A": "off_by_one", "B": "correct_drop", "Z": "ghost"},
            )
        ],
        subtopic_id="sub-1",
        plan_version_id="LPV-1",
    )
    assert len(payloads) == 1
    payload = payloads[0]
    assert payload["subtopic_id"] == "sub-1"
    assert payload["plan_version_id"] == "LPV-1"
    assert payload["lesson_objective_id"] == "lop01"
    assert payload["correct_option"] == "B"
    assert payload["option_misconceptions"] == {"A": "off_by_one"}
    assert payload["knowledge_component_id"] is None
    # Pipeline-compatible by construction: the payload is exactly an ExitTicketItem's
    # columns, so the scoring/diagnostic pipeline reads manual items like generated ones.
    item = ExitTicketItem(**payload)
    assert item.correct_option == "B"
    assert item.options == {"A": "3", "B": "4"}


def test_payload_empty_misconceptions_becomes_none() -> None:
    payload = build_classwork_item_payloads([_item()], subtopic_id="s", plan_version_id="v")[0]
    assert payload["option_misconceptions"] is None


def test_payload_converts_kc_id_to_uuid() -> None:
    kc_id = str(uuid.uuid4())
    payload = build_classwork_item_payloads(
        [_item(knowledge_component_id=kc_id)], subtopic_id="s", plan_version_id="v"
    )[0]
    assert payload["knowledge_component_id"] == uuid.UUID(kc_id)


def test_issues_flags_objective_not_in_plan() -> None:
    issues = classwork_item_issues(
        [_item(lesson_objective_id="ghost")], valid_objective_ids={"lop01"}
    )
    assert any("objective" in issue.lower() for issue in issues)


def test_issues_flags_correct_option_not_among_options() -> None:
    issues = classwork_item_issues([_item(correct_option="Z")], valid_objective_ids={"lop01"})
    assert any("correct" in issue.lower() for issue in issues)


def test_issues_flags_blank_option_text_and_stem() -> None:
    issues = classwork_item_issues(
        [_item(stem="   ", options={"A": "", "B": "4"}, correct_option="B")],
        valid_objective_ids={"lop01"},
    )
    assert any("option needs text" in issue for issue in issues)
    assert any("question" in issue.lower() for issue in issues)


def test_issues_empty_when_every_item_is_valid() -> None:
    assert classwork_item_issues([_item(), _item()], valid_objective_ids={"lop01"}) == []
