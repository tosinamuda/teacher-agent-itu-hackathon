"""The second reader enforces the brief's own requirements and skill rules, wording included."""

from __future__ import annotations

from app.domains.content_engine.infrastructure.harness.brief import CHECKER_PROMPT


def test_the_reader_is_told_to_check_each_requirement_and_skill_rule_of_the_brief() -> None:
    assert "each requirement of the brief and each rule of a skill" in CHECKER_PROMPT
    assert "wording and layout rules included" in CHECKER_PROMPT


def test_the_reader_judges_by_the_brief_and_not_by_its_own_preference() -> None:
    assert "never by a preference of your own" in CHECKER_PROMPT
    assert "Do not list matters of style" not in CHECKER_PROMPT
