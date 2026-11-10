"""An artefact plugin folder is read into a plugin, or into what is wrong with it."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import jsonschema
import pytest

from app.domains.content.plugins.__main__ import main
from app.domains.content.plugins.problems import Severity, errors_in
from tests.plugin_folder import (
    artefact_record,
    read_plugin,
    rewrite,
    rewrite_artefact,
    write_plugin,
)

SCHEMA = json.loads(
    Path("src/app/domains/content/plugins/artefact.schema.json").read_text(encoding="utf-8")
)


def test_a_valid_folder_is_read_into_a_plugin_with_its_skills_and_servers(tmp_path: Path) -> None:
    plugin, problems = read_plugin(write_plugin(tmp_path / "p"))

    assert problems == []
    assert plugin is not None
    assert (plugin.manifest.name, plugin.definition.slug, plugin.definition.kind) == (
        "worked-examples",
        "worked-examples",
        "worked_examples",
    )
    assert [skill.slug for skill in plugin.skills] == ["checking-worked-answers"]
    assert [ref.slug for ref in plugin.spec.skills] == ["checking-worked-answers"]
    assert [(s.name, s.tools, s.secret) for s in plugin.servers] == [
        ("maths", ("solve",), "MATHS_TOKEN")
    ]
    assert [s.name for s in plugin.spec.mcp] == ["maths"]


def _no_manifest(folder: Path) -> None:
    (folder / "plugin.json").unlink()


def _bad_schema(folder: Path) -> None:
    rewrite(folder / "plugin.json", lambda r: r.update({"$schema": "https://example.org/x"}))


def _unknown_manifest_field(folder: Path) -> None:
    rewrite(folder / "plugin.json", lambda r: r.update({"spec": {}}))


def _bad_name(folder: Path) -> None:
    rewrite(folder / "plugin.json", lambda r: r.update({"name": "Bad--Name"}))


def _no_artefact(folder: Path) -> None:
    (folder / "com.tosinamuda.lpcg" / "artefact.json").unlink()


def _no_extension(folder: Path) -> None:
    rewrite(folder / "plugin.json", lambda r: r["extensions"].clear())


def _artefact_path_that_climbs(folder: Path) -> None:
    def change(record: dict) -> None:
        record["extensions"]["com.tosinamuda.lpcg"]["artefacts"] = ["./../outside.json"]

    rewrite(folder / "plugin.json", change)


def _artefact_path_without_dot_slash(folder: Path) -> None:
    def change(record: dict) -> None:
        record["extensions"]["com.tosinamuda.lpcg"]["artefacts"] = [
            "com.tosinamuda.lpcg/artefact.json"
        ]

    rewrite(folder / "plugin.json", change)


def _unknown_artefact_key(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r.update({"hooks": []}))


def _missing_skill_file(folder: Path) -> None:
    (folder / "skills" / "checking-worked-answers" / "SKILL.md").unlink()


def _skill_without_front_matter(folder: Path) -> None:
    (folder / "skills" / "checking-worked-answers" / "SKILL.md").write_text("no front matter")


def _skill_named_unlike_its_folder(folder: Path) -> None:
    skill = folder / "skills" / "checking-worked-answers" / "SKILL.md"
    skill.write_text(
        skill.read_text().replace("name: checking-worked-answers", "name: Show the working")
    )


def _skill_with_a_long_description(folder: Path) -> None:
    skill = folder / "skills" / "checking-worked-answers" / "SKILL.md"
    skill.write_text(skill.read_text().replace("Use for any worked example.", "x" * 1025))


def _skill_folder_with_double_hyphen(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r.update({"skills": ["show--working"]}))


def _skill_folder_ending_in_a_hyphen(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r.update({"skills": ["show-"]}))


def _skill_folder_with_a_reserved_word(folder: Path) -> None:
    (folder / "skills" / "checking-worked-answers").rename(folder / "skills" / "claude-helper")
    rewrite_artefact(folder, lambda r: r.update({"skills": ["claude-helper"]}))
    skill = folder / "skills" / "claude-helper" / "SKILL.md"
    skill.write_text(skill.read_text().replace("checking-worked-answers", "claude-helper"))


def _skill_folder_that_climbs(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r.update({"skills": ["../x"]}))


def _stdio_server_that_is_listed(folder: Path) -> None:
    def change(record: dict) -> None:
        record["mcpServers"]["maths"] = {"type": "stdio", "command": "node"}

    rewrite(folder / "mcp.json", change)


def _mcp_without_schema(folder: Path) -> None:
    rewrite(folder / "mcp.json", lambda r: r.pop("$schema"))


def _literal_token(folder: Path) -> None:
    def change(record: dict) -> None:
        record["mcpServers"]["maths"]["headers"] = {"Authorization": "Bearer abc123"}

    rewrite(folder / "mcp.json", change)


def _other_header(folder: Path) -> None:
    def change(record: dict) -> None:
        record["mcpServers"]["maths"]["headers"] = {"X-Key": "${KEY}"}

    rewrite(folder / "mcp.json", change)


def _plain_http_server(folder: Path) -> None:
    def change(record: dict) -> None:
        record["mcpServers"]["maths"]["url"] = "http://tools.example.org/mcp"

    rewrite(folder / "mcp.json", change)


def _tools_not_listed(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r.update({"servers": {}}))


def _server_not_in_mcp_json(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r["servers"].update({"other": ["x"]}))


def _spec_without_parts(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r["spec"].pop("parts"))


def _learner_level_spec(folder: Path) -> None:
    rewrite_artefact(folder, lambda r: r["spec"].update({"levels": ["learner_level"]}))


@pytest.mark.parametrize(
    ("break_it", "file", "words"),
    [
        (_no_manifest, "plugin.json", "add plugin.json"),
        (_bad_schema, "plugin.json", "$schema"),
        (_unknown_manifest_field, "plugin.json", "Additional properties are not allowed"),
        (_bad_name, "plugin.json", "name: "),
        (_no_artefact, "com.tosinamuda.lpcg/artefact.json", "add the file"),
        (_no_extension, "plugin.json", "lists the artefact files"),
        (_artefact_path_that_climbs, "plugin.json", "stays inside the plugin"),
        (_artefact_path_without_dot_slash, "plugin.json", "lists the artefact files"),
        (_unknown_artefact_key, "com.tosinamuda.lpcg/artefact.json", "not a field"),
        (_missing_skill_file, "skills/checking-worked-answers/SKILL.md", "add SKILL.md"),
        (_skill_without_front_matter, "skills/checking-worked-answers/SKILL.md", "front matter"),
        (
            _skill_named_unlike_its_folder,
            "skills/checking-worked-answers/SKILL.md",
            "it is the folder name",
        ),
        (_skill_with_a_long_description, "skills/checking-worked-answers/SKILL.md", "at most 1024"),
        (
            _skill_folder_with_double_hyphen,
            "com.tosinamuda.lpcg/artefact.json",
            "folder of lowercase words",
        ),
        (
            _skill_folder_ending_in_a_hyphen,
            "com.tosinamuda.lpcg/artefact.json",
            "folder of lowercase words",
        ),
        (
            _skill_folder_with_a_reserved_word,
            "skills/claude-helper/SKILL.md",
            "holds none of anthropic, claude",
        ),
        (
            _skill_folder_that_climbs,
            "com.tosinamuda.lpcg/artefact.json",
            "folder of lowercase words",
        ),
        (_stdio_server_that_is_listed, "mcp.json", "streamable-http servers only"),
        (_mcp_without_schema, "mcp.json", "$schema"),
        (_literal_token, "mcp.json", "never written"),
        (_other_header, "mcp.json", "send only"),
        (_plain_http_server, "mcp.json", "https"),
        (
            _tools_not_listed,
            "mcp.json",
            "no artefact file lists the tools of maths",
        ),
        (_server_not_in_mcp_json, "com.tosinamuda.lpcg/artefact.json", "other"),
        (_spec_without_parts, "com.tosinamuda.lpcg/artefact.json", "spec:"),
        (_learner_level_spec, "com.tosinamuda.lpcg/artefact.json", "spec:"),
    ],
)
def test_each_fault_is_named_with_its_file_and_stops_the_plugin(
    tmp_path: Path, break_it: Callable[[Path], None], file: str, words: str
) -> None:
    folder = write_plugin(tmp_path / "p")
    break_it(folder)

    plugin, problems = read_plugin(folder)

    assert plugin is None
    assert any(p.file == file and words in p.message for p in errors_in(problems)), problems


def test_a_revision_in_skill_front_matter_is_warned_about_and_ignored(tmp_path: Path) -> None:
    folder = write_plugin(tmp_path / "p")
    skill = folder / "skills" / "checking-worked-answers" / "SKILL.md"
    skill.write_text(skill.read_text().replace("description:", "revision: 4\ndescription:", 1))

    plugin, problems = read_plugin(folder)

    assert plugin is not None and plugin.skills[0].revision == 1
    assert [(p.file, p.severity) for p in problems] == [
        ("skills/checking-worked-answers/SKILL.md", Severity.WARNING)
    ]


def test_the_plugin_keeps_its_files_as_text_and_leaves_out_hidden_ones(tmp_path: Path) -> None:
    folder = write_plugin(tmp_path / "p")
    (folder / ".DS_Store").write_bytes(b"\x00\xff")

    plugin, problems = read_plugin(folder)

    assert problems == [] and plugin is not None
    assert sorted(plugin.files) == [
        "com.tosinamuda.lpcg/artefact.json",
        "mcp.json",
        "plugin.json",
        "skills/checking-worked-answers/SKILL.md",
    ]
    skill = folder / "skills" / "checking-worked-answers" / "SKILL.md"
    assert plugin.files["skills/checking-worked-answers/SKILL.md"] == skill.read_text()


def test_a_file_that_is_not_text_is_refused_by_name(tmp_path: Path) -> None:
    folder = write_plugin(tmp_path / "p")
    (folder / "skills" / "checking-worked-answers" / "logo.png").write_bytes(b"\x89PNG\xff\xfe")

    plugin, problems = read_plugin(folder)

    assert plugin is None
    assert [(p.file, "not text" in p.message) for p in errors_in(problems)] == [
        ("skills/checking-worked-answers/logo.png", True)
    ]


def test_a_reference_file_the_instructions_never_name_is_a_warning(tmp_path: Path) -> None:
    folder = write_plugin(tmp_path / "p")
    references = folder / "skills" / "checking-worked-answers" / "references"
    references.mkdir()
    (references / "layout.md").write_text("Layout.")

    plugin, problems = read_plugin(folder)

    assert plugin is not None
    assert [(p.file, p.severity, "layout.md" in p.message) for p in problems] == [
        ("skills/checking-worked-answers/SKILL.md", Severity.WARNING, True)
    ]


def test_a_server_the_app_cannot_connect_to_is_skipped_with_a_warning_when_no_tool_is_listed(
    tmp_path: Path,
) -> None:
    """The standard has a client skip a transport it does not support and load the rest."""
    folder = write_plugin(tmp_path / "p")

    def add_stdio(record: dict) -> None:
        record["mcpServers"]["local"] = {"type": "stdio", "command": "./bin/server"}

    rewrite(folder / "mcp.json", add_stdio)

    plugin, problems = read_plugin(folder)

    assert plugin is not None
    assert [s.name for s in plugin.servers] == ["maths"]
    assert [(p.file, p.severity) for p in problems] == [("mcp.json", Severity.WARNING)]


def test_a_skill_no_spec_pins_is_a_warning_and_the_plugin_still_reads(tmp_path: Path) -> None:
    folder = write_plugin(tmp_path / "p")
    extra = folder / "skills" / "unused"
    extra.mkdir()
    (extra / "SKILL.md").write_text("---\nname: unused\ndescription: x\n---\nText.\n")

    plugin, problems = read_plugin(folder)

    assert plugin is not None
    assert [(p.file, p.severity) for p in problems] == [("skills/unused", Severity.WARNING)]


def test_a_skills_reference_files_come_with_it(tmp_path: Path) -> None:
    folder = write_plugin(tmp_path / "p")
    (folder / "skills" / "checking-worked-answers" / "references").mkdir()
    (folder / "skills" / "checking-worked-answers" / "references" / "layout.md").write_text(
        "Layout."
    )

    plugin, _ = read_plugin(folder)

    assert plugin is not None
    assert [f.path for f in plugin.skills[0].files] == ["references/layout.md"]


def test_the_validate_command_reports_and_exits_by_the_result(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    good = write_plugin(tmp_path / "good")
    bad = write_plugin(tmp_path / "bad")
    _bad_name(bad)

    assert main(["validate", str(good)]) == 0
    assert "valid (worked-examples, 1 skills)" in capsys.readouterr().out
    assert main(["validate", str(bad)]) == 1
    assert "error: plugin.json: name: " in capsys.readouterr().out


def test_the_published_schema_accepts_the_artefact_file_and_refuses_an_unknown_key() -> None:
    jsonschema.validate(artefact_record(), SCHEMA)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({**artefact_record(), "hooks": []}, SCHEMA)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({**artefact_record(), "audience": "everyone"}, SCHEMA)


def test_installing_a_folder_with_a_fault_exits_before_the_database_is_used(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    folder = write_plugin(tmp_path / "p")
    _bad_name(folder)

    assert main(["install", str(folder)]) == 1
    assert "error: plugin.json: name: " in capsys.readouterr().out
