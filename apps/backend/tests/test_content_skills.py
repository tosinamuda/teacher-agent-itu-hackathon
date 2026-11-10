"""Skills as data: written as SKILL.md, stored by revision, pinned by specs, given to writers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from mcp import Client
from mcp.types import TextResourceContents
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.skill_refs import SkillRef, SkillRefError
from app.domains.content.application.errors import ContentError
from app.domains.content.domain.skills import Skill, SkillError, SkillFile
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.skill_seed import read_skills, seed_skills
from app.domains.content_engine.infrastructure.writer import text_of
from app.domains.content_engine.mcp.caller import as_the_app
from tests.content_engine_support import PLAN, SPEC, TYPE, seed_lesson, server_over

SKILL_MD = """---
name: Show the working
description: Use when an answer needs its working.
revision: 2
---
Write each line of working in LaTeX.
"""


def test_a_skill_is_read_from_its_skill_md() -> None:
    skill = Skill.from_markdown("show-the-working", SKILL_MD)

    assert (skill.slug, skill.revision, skill.name) == ("show-the-working", 2, "Show the working")
    assert skill.instructions == "Write each line of working in LaTeX."
    assert skill.for_writer()["use_when"] == "Use when an answer needs its working."


@pytest.mark.parametrize(
    ("slug", "text", "problem"),
    [
        ("working", "Write the working.", "front matter"),
        ("Working", SKILL_MD, "lowercase words"),
        ("working", SKILL_MD.replace("name: Show the working\n", ""), "has a name"),
        ("working", SKILL_MD.replace("Write each line of working in LaTeX.", ""), "instructions"),
    ],
)
def test_a_skill_a_writer_could_not_use_is_refused(slug: str, text: str, problem: str) -> None:
    with pytest.raises(SkillError, match=problem):
        Skill.from_markdown(slug, text)


def test_every_shipped_skill_reads() -> None:
    shipped = [(skill.slug, skill.revision) for skill in seed_skills()]

    assert ("state-the-content", 1) in shipped and ("show-the-working", 1) in shipped
    assert len(shipped) == len(set(shipped))


def _write(path: Path, revision: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SKILL_MD.replace("revision: 2", f"revision: {revision}"), encoding="utf-8")


def test_a_skill_ships_its_earlier_revisions_beside_the_current_one(tmp_path: Path) -> None:
    _write(tmp_path / "working" / "SKILL.md", 3)
    _write(tmp_path / "working" / "revisions" / "1.md", 1)
    _write(tmp_path / "working" / "revisions" / "2.md", 2)

    assert [skill.revision for skill in read_skills(tmp_path)] == [1, 2, 3]


@pytest.mark.parametrize(
    ("revision_file", "revision", "problem"),
    [("2.md", 1, "2.md holds revision 1"), ("3.md", 3, "SKILL.md is the latest revision")],
)
def test_a_revision_history_that_contradicts_itself_is_refused(
    tmp_path: Path, revision_file: str, revision: int, problem: str
) -> None:
    _write(tmp_path / "working" / "SKILL.md", 3)
    _write(tmp_path / "working" / "revisions" / revision_file, revision)

    with pytest.raises(SkillError, match=problem):
        read_skills(tmp_path)


def test_a_skill_ships_the_markdown_under_its_references_folder(tmp_path: Path) -> None:
    _write(tmp_path / "working" / "SKILL.md", 1)
    (tmp_path / "working" / "references" / "steps").mkdir(parents=True)
    (tmp_path / "working" / "references" / "layout.md").write_text("Layout.", encoding="utf-8")
    (tmp_path / "working" / "references" / "steps" / "one.md").write_text("One.", "utf-8")
    (tmp_path / "working" / "references" / "notes.txt").write_text("Skipped.", "utf-8")

    (skill,) = read_skills(tmp_path)

    assert [(f.path, f.text) for f in skill.files] == [
        ("references/layout.md", "Layout."),
        ("references/steps/one.md", "One."),
    ]


def test_a_reference_names_a_skill_and_the_revision_it_pins() -> None:
    assert SkillRef.from_record({"skill": "show-the-working", "revision": 1}).revision == 1
    with pytest.raises(SkillRefError, match="revision"):
        SkillRef.from_record({"skill": "show-the-working"})


def _with_skills(*refs: tuple[str, int]) -> dict[str, object]:
    return {**SPEC, "skills": [{"skill": slug, "revision": rev} for slug, rev in refs]}


@pytest.mark.asyncio
async def test_a_spec_may_pin_only_skills_the_library_holds(db: AsyncSession) -> None:
    await seed_lesson(db)
    catalogue = build_content_catalogue()

    spec = await catalogue.add(db, TYPE, _with_skills(("show-the-working", 1)), "Researcher")

    assert [ref.slug for ref in spec.skills] == ["show-the-working"]
    with pytest.raises(ContentError, match="unknown_skill_revision:show-the-working@9"):
        await catalogue.add(db, TYPE, _with_skills(("show-the-working", 9)), "Researcher")


@pytest.mark.asyncio
async def test_a_new_revision_is_added_and_the_pinned_one_stays_readable(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    library = build_content_catalogue().skills
    first = await library.skill(db, "show-the-working")

    added = await library.add(db, Skill("show-the-working", 1, "Working", "When.", "New."), "R")

    assert added.revision == first.revision + 1
    assert (await library.skill(db, "show-the-working")).instructions == "New."
    pinned = await library.pinned(db, [first.ref()])
    assert pinned[0].instructions == first.instructions


@pytest.mark.asyncio
async def test_a_draft_s_brief_carries_the_skills_its_spec_pins(db: AsyncSession) -> None:
    await seed_lesson(db)
    await build_content_catalogue().add(
        db, TYPE, _with_skills(("state-the-content", 1), ("show-the-working", 1)), "Researcher"
    )

    with as_the_app():
        async with Client(server_over(db)) as client:
            started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            listed = await client.read_resource("skills://?search=working")
            one = await client.read_resource("skill://show-the-working")

    brief = json.loads(text_of(started))["brief"]
    assert [skill["name"] for skill in brief["skills"]] == ["State the content", "Show the working"]
    assert "LaTeX" in brief["skills"][1]["instructions"]
    listing, found = listed.contents[0], one.contents[0]
    assert isinstance(listing, TextResourceContents) and isinstance(found, TextResourceContents)
    assert [s["skill"] for s in json.loads(listing.text)] == ["show-the-working"]
    assert "instructions" in json.loads(found.text)


@pytest.mark.asyncio
async def test_a_skill_is_served_at_its_revision_with_its_reference_files(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    library = build_content_catalogue().skills
    files = (SkillFile("references/rules.md", "Rule one."),)
    with_files = Skill("show-the-working", 1, "Working", "When.", "With rules.", files)
    added = await library.add(db, with_files, "R")

    with as_the_app():
        async with Client(server_over(db)) as client:
            old = await client.read_resource("skill://show-the-working?revision=1")
            new = await client.read_resource(f"skill://show-the-working?revision={added.revision}")

    first, second = old.contents[0], new.contents[0]
    assert isinstance(first, TextResourceContents) and isinstance(second, TextResourceContents)
    assert json.loads(first.text)["files"] == []
    assert json.loads(second.text)["files"] == [
        {"path": "references/rules.md", "text": "Rule one."}
    ]


def test_the_skills_routes_come_before_the_content_item_route() -> None:
    from fastapi.routing import APIRoute

    from app.main import app

    paths = [route.path for route in app.routes if isinstance(route, APIRoute)]

    assert paths.index("/content/skills") < paths.index("/content/{content_id}")
