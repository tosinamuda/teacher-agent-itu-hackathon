"""Artefact plugins over HTTP, with the production permission table."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient

from app.shared.auth import Actor
from tests.plugin_folder import write_plugin
from tests.test_content_engine_http import TEACHER, _actor, http  # noqa: F401

pytestmark = pytest.mark.asyncio


@pytest.fixture
def session(http: tuple[AsyncClient, list[Actor]]) -> tuple[AsyncClient, list[Actor]]:  # noqa: F811
    """The client and the signed-in actor of the content HTTP tests: a researcher to begin with."""
    return http


TYPE = "plugin-examples"


def _files(folder: Path) -> dict[str, str]:
    return {
        p.relative_to(folder).as_posix(): p.read_text() for p in folder.rglob("*") if p.is_file()
    }


async def test_a_researcher_installs_updates_and_removes_a_plugin(
    session: tuple[AsyncClient, list[Actor]],
    tmp_path: Path,
) -> None:
    client, _ = session
    folder = write_plugin(tmp_path / "p", "lesson-tools", TYPE)

    installed = await client.post("/content/plugins", json={"files": _files(folder)})
    listed = await client.get("/content/plugins")
    types = await client.get("/content/types")
    again = await client.post("/content/plugins", json={"files": _files(folder)})
    skill = folder / "skills" / "checking-worked-answers" / "SKILL.md"
    skill.write_text(skill.read_text() + "More.\n")
    updated = await client.put("/content/plugins/lesson-tools", json={"files": _files(folder)})
    removed = await client.delete("/content/plugins/lesson-tools")

    assert installed.status_code == 201, installed.text
    assert installed.json()[0]["type"] == TYPE
    assert [p["name"] for p in listed.json()] == ["lesson-tools"]
    assert [p["plugin"] for p in listed.json()] == ["lesson-tools"]
    assert TYPE in [t["type"] for t in types.json()]
    assert again.status_code == 409
    assert (updated.json()[0]["revision"], updated.json()[0]["spec_revision"]) == (2, 2)
    assert removed.json()["status"] == "removed"
    retired = {t["type"]: t["retired"] for t in (await client.get("/content/types")).json()}
    assert retired[TYPE] is True and retired["lesson-note"] is False


async def test_a_plugin_with_faults_is_refused_with_every_problem(
    session: tuple[AsyncClient, list[Actor]],
    tmp_path: Path,
) -> None:
    client, _ = session
    files = _files(write_plugin(tmp_path / "p", "lesson-tools", TYPE))
    files["mcp.json"] = files["mcp.json"].replace("${MATHS_TOKEN}", "abc123")
    files["skills/checking-worked-answers/SKILL.md"] = "no front matter"

    refused = await client.post("/content/plugins", json={"files": files})

    assert refused.status_code == 422
    assert any("never written" in line for line in refused.json()["detail"])
    assert any("front matter" in line for line in refused.json()["detail"])


@pytest.mark.parametrize("path", ["../escape.json", "/etc/plugin.json", "a//b.json"])
async def test_a_path_that_leaves_the_plugin_folder_is_refused(
    session: tuple[AsyncClient, list[Actor]],
    tmp_path: Path,
    path: str,
) -> None:
    client, _ = session
    files = _files(write_plugin(tmp_path / "p", "lesson-tools", TYPE))
    files[path] = "{}"

    refused = await client.post("/content/plugins", json={"files": files})

    assert refused.status_code == 422
    assert any(path in line for line in refused.json()["detail"])


async def test_a_teacher_may_not_install_a_plugin(
    session: tuple[AsyncClient, list[Actor]],
    tmp_path: Path,
) -> None:
    client, caller = session
    caller[0] = _actor(TEACHER, "teacher")
    folder = write_plugin(tmp_path / "p", "lesson-tools", TYPE)

    denied = await client.post("/content/plugins", json={"files": _files(folder)})

    assert denied.status_code == 403


@pytest.fixture
def shipped(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A folder of shipped plugins holding one named ``lesson-tools``."""
    shipped_dir = tmp_path / "shipped"
    write_plugin(shipped_dir / "lesson-tools", "lesson-tools", TYPE)
    monkeypatch.setattr("app.domains.content.plugins.shipped.SHIPPED_DIR", shipped_dir)
    return shipped_dir


async def test_a_plugin_that_ships_with_the_app_is_listed_as_system_and_the_api_leaves_it_alone(
    session: tuple[AsyncClient, list[Actor]], shipped: Path, tmp_path: Path
) -> None:
    client, _ = session
    files = _files(write_plugin(tmp_path / "p", "lesson-tools", TYPE))
    other = _files(write_plugin(tmp_path / "q", "other-tools", "other-examples"))

    refused_install = await client.post("/content/plugins", json={"files": files})
    refused_update = await client.put("/content/plugins/lesson-tools", json={"files": files})
    refused_removal = await client.delete("/content/plugins/lesson-tools")
    installed = await client.post("/content/plugins", json={"files": other})
    listed = await client.get("/content/plugins")

    for refused in (refused_install, refused_update, refused_removal):
        assert refused.status_code == 409
        assert "plugin_ships_with_the_app" in refused.text
    assert installed.status_code == 201 and installed.json()[0]["system"] is False
    assert {p["name"]: p["system"] for p in listed.json()} == {"other-tools": False}
