"""A tool call's result becomes the one line a chat shows under the step."""

from __future__ import annotations

import json

from app.domains.content_engine.infrastructure.harness.opencode_observation import observation


def _done(result: object) -> dict[str, object]:
    return {"status": "completed", "output": json.dumps(result)}


def test_a_refusal_says_why_without_the_tool_prefix() -> None:
    state = {
        "status": "error",
        "error": "Error executing tool revise_part: the part does not match its schema: "
        "entry_behaviour: must be a list, not text",
    }

    assert observation("revise_part", state) == (
        "the part does not match its schema: entry_behaviour: must be a list, not text"
    )


def test_a_part_written_says_what_the_checks_found_first() -> None:
    state = _done(
        {"missing": [], "issues": ["the x-lcm-po01 part, at core_step: no worked example", "other"]}
    )

    assert observation("add_part", state) == (
        "The checks found: objective 1, core_step: no worked example (and 1 more)"
    )


def test_a_part_written_says_how_many_are_still_to_write() -> None:
    assert observation("add_part", _done({"missing": ["a", "b"], "issues": []})) == (
        "2 parts still to write"
    )
    assert observation("add_part", _done({"missing": ["a"], "issues": []})) == (
        "1 part still to write"
    )


def test_a_draft_with_every_part_and_no_issue_says_so() -> None:
    assert observation("read_draft", _done({"missing": [], "issues": []})) == (
        "Every part is written and the checks pass"
    )


def test_opening_a_draft_says_how_many_parts_it_asks_for() -> None:
    assert observation("start_draft", _done({"missing": ["a", "b", "c"], "issues": []})) == (
        "3 parts to write"
    )


def test_submitting_says_it_went_to_the_teacher() -> None:
    assert observation("submit_draft", _done({"saved_as": "CNT-1"})) == (
        "Saved for the teacher to review"
    )


def test_a_file_read_says_its_length() -> None:
    state = {"status": "completed", "output": "<content>\n1: a\n2: b\n3: c\n</content>"}

    assert observation("read", state) == "3 lines"


def test_a_tool_with_nothing_to_add_gives_none() -> None:
    assert observation("skill", {"status": "completed", "output": "<skill_content>"}) is None
    assert observation("add_part", {"status": "completed", "output": "not json"}) is None


def test_a_long_observation_is_cut() -> None:
    state = {"status": "error", "error": "Error executing tool add_part: " + "x" * 500}

    assert len(observation("add_part", state) or "") <= 220


def test_a_text_search_says_where_it_found_the_text() -> None:
    one = _done(
        {
            "count": 1,
            "matches": [
                {
                    "unit_id": "jss1-lcm-po01",
                    "path": "lesson_objectives.0.core_step.blocks.1.question",
                }
            ],
        }
    )
    several = _done({"count": 3, "matches": [{"unit_id": "lesson", "path": "materials.1"}]})

    assert observation("locate_text", one) == (
        "Found in objective 1 \u00b7 lesson_objectives.0.core_step.blocks.1.question"
    )
    assert (
        observation("locate_text", several) == "Found in 3 places, first lesson \u00b7 materials.1"
    )
    assert observation("locate_text", _done({"count": 0, "matches": []})) == (
        "Not in any part of the draft"
    )
