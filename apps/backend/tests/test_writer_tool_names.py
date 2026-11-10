from app.domains.content_engine.infrastructure.harness.brief import (
    WRITER_PROMPT,
    as_named_by,
    follow_up_message,
)
from app.domains.content_engine.infrastructure.harness.opencode_feed import TOOL_PREFIX


def test_the_writer_is_told_each_tool_by_the_name_opencode_gives_it() -> None:
    named = as_named_by(WRITER_PROMPT, TOOL_PREFIX)

    for tool in ("add_part", "revise_part"):
        assert f"{TOOL_PREFIX}{tool}" in named
        assert f" {tool}" not in named


def test_a_tool_already_named_with_the_prefix_is_not_named_twice() -> None:
    once = as_named_by("Call revise_part, or engine_add_part.", TOOL_PREFIX)

    assert once == "Call engine_revise_part, or engine_add_part."
    assert as_named_by(once, TOOL_PREFIX) == once


def test_the_message_to_a_writer_that_has_its_brief_names_the_tools_the_same_way() -> None:
    message = as_named_by(follow_up_message({"draft_id": "D-1"}, "Shorter."), TOOL_PREFIX)

    assert "engine_revise_part" in message
    assert "engine_add_part" in message
