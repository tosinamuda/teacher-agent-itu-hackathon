"""A run's workspace: the pinned skills written as files a harness finds where it starts."""

from __future__ import annotations

from pathlib import Path

import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.skills import Skill, SkillFile
from app.domains.content.domain.skills import SkillError as DomainSkillError
from app.domains.content_engine.infrastructure.harness.choice import (
    EngineLoop,
    SkillsMode,
    loop_for,
)
from app.domains.content_engine.infrastructure.harness.workspace import (
    SkillError,
    WorkspaceSkill,
    manifest,
    pinned_skills,
    without_skills,
    write_skills,
)
from app.domains.content_engine.mcp.caller import as_the_app
from app.shared.json_types import JsonObject
from tests.content_engine_support import PLAN, TYPE, seed_lesson, server_over

SKILL = WorkspaceSkill("show-the-working", "Use for any worked example.", "- Work each line.")


def _draft() -> JsonObject:
    pinned = {
        "name": "Show the working",
        "use_when": "Use for any worked example.",
        "instructions": "- Work each line.",
    }
    return {"draft_id": "d1", "brief": {"material": "notes", "skills": [pinned]}}


def test_the_document_is_front_matter_naming_the_skill_then_its_instructions() -> None:
    assert SKILL.document() == (
        '---\nname: "show-the-working"\ndescription: "Use for any worked example."\n---\n\n'
        "- Work each line.\n"
    )


def test_a_description_with_a_colon_and_quotes_stays_one_value() -> None:
    skill = WorkspaceSkill("a", 'Use when: the "step" is a test', "text")

    assert '"Use when: the \\"step\\" is a test"' in skill.document()


@pytest.mark.parametrize("description", ["", "   ", "x" * 1025])
def test_a_description_a_harness_would_not_read_is_refused(description: str) -> None:
    with pytest.raises(SkillError):
        WorkspaceSkill("a", description, "text").document()


def test_the_draft_without_its_skills_keeps_the_rest_of_its_brief() -> None:
    kept = without_skills(_draft())

    assert kept["brief"] == {"material": "notes"}
    assert kept["draft_id"] == "d1"


def test_each_skill_is_written_where_a_harness_looks_for_project_skills(tmp_path: Path) -> None:
    write_skills(tmp_path, [SKILL, WorkspaceSkill("other", "Use for others.", "Do it.")])

    written = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*.md"))
    assert written == [".agents/skills/other/SKILL.md", ".agents/skills/show-the-working/SKILL.md"]
    assert (tmp_path / ".agents/skills/show-the-working/SKILL.md").read_text() == SKILL.document()


def test_the_manifest_changes_with_any_skills_text_and_not_with_their_order() -> None:
    other = WorkspaceSkill("other", "Use for others.", "Do it.")
    changed = WorkspaceSkill("other", "Use for others.", "Do it twice.")

    assert manifest([SKILL, other]) == manifest([other, SKILL])
    assert manifest([SKILL, other])["sha256"] != manifest([SKILL, changed])["sha256"]
    assert manifest([SKILL, other]) != manifest([SKILL])


@pytest.mark.parametrize("harness", [EngineLoop.DSPY, EngineLoop.DEEP_AGENTS])
def test_a_loop_that_reads_no_workspace_is_refused_native_skills(harness: EngineLoop) -> None:
    with pytest.raises(ValueError, match="does not load skills from a workspace"):
        loop_for(harness, skills=SkillsMode.NATIVE)


@pytest.mark.parametrize("harness", [EngineLoop.OPENCODE, EngineLoop.DEEPSEEK, EngineLoop.PI])
def test_opencode_dsh_and_pi_take_native_skills(harness: EngineLoop) -> None:
    loop_for(harness, skills=SkillsMode.NATIVE)


@pytest.mark.asyncio
async def test_the_pinned_skills_are_read_at_their_revision_with_their_reference_files(
    db: AsyncSession,
) -> None:
    files = (SkillFile("references/rules.md", "Rule one."),)
    skill = Skill("check-rules", 1, "Check rules", "Use to check.", "Read the rules.", files)
    await seed_lesson(db, skills=("check-rules",), new_skills=(skill,))
    with as_the_app():
        async with Client(server_over(db)) as client:
            opened = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            assert opened.structured_content is not None
            skills = await pinned_skills(client, opened.structured_content)

    assert [(s.slug, s.description, s.files) for s in skills] == [
        ("check-rules", "Use to check.", files)
    ]


def test_a_skill_has_references_when_it_holds_files_beyond_its_instructions() -> None:
    bare = WorkspaceSkill("a", "Use it.", "Text.", copied={"SKILL.md": "---\n---\nText."})
    copied = WorkspaceSkill(
        "a", "Use it.", "Text.", copied={"SKILL.md": "x", "references/rules.md": "Rule."}
    )
    stored = WorkspaceSkill("a", "Use it.", "Text.", (SkillFile("references/r.md", "One."),))

    assert [s.has_references for s in (SKILL, bare, copied, stored)] == [False, False, True, True]


def test_a_skills_reference_files_are_written_beside_its_instructions(tmp_path: Path) -> None:
    files = (
        SkillFile("references/rules.md", "Rule one."),
        SkillFile("references/x/two.md", "Two."),
    )
    write_skills(tmp_path, [WorkspaceSkill("a", "Use it.", "Read the rules.", files)])

    root = tmp_path / ".agents/skills/a"
    assert (root / "references/rules.md").read_text() == "Rule one."
    assert (root / "references/x/two.md").read_text() == "Two."


def test_a_change_to_a_reference_file_changes_the_manifest() -> None:
    one = WorkspaceSkill("a", "Use it.", "Text.", (SkillFile("references/r.md", "One."),))
    two = WorkspaceSkill("a", "Use it.", "Text.", (SkillFile("references/r.md", "Two."),))

    assert manifest([one])["sha256"] != manifest([two])["sha256"]


@pytest.mark.parametrize(
    "path", ["rules.md", "/etc/x.md", "references/../x.md", "references/a.txt", "other/a.md"]
)
def test_a_reference_file_outside_references_or_not_markdown_is_refused(path: str) -> None:
    with pytest.raises(DomainSkillError):
        SkillFile(path, "text")
