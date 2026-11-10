"""The pinned skills as the plugin that made the type holds them, to copy into a workspace."""

from __future__ import annotations

from mcp import Client
from mcp.shared.exceptions import MCPError

from app.domains.content_engine.infrastructure.engine import resource_json
from app.shared.json_types import JsonObject

#: What the engine's server says when no plugin made the type.
_NO_PLUGIN = "no plugin made"


class PluginSkillError(ValueError):
    """A plugin's stored files do not hold a skill its type pins."""


def _text_of(files: object) -> dict[str, str]:
    if not isinstance(files, dict):
        raise PluginSkillError("the plugin's files are a mapping of paths to text")
    return {str(path): str(text) for path, text in files.items()}


def _names_of(pinned: object) -> list[str]:
    names: list[str] = []
    for ref in pinned if isinstance(pinned, list) else []:
        named = {str(key): value for key, value in ref.items()} if isinstance(ref, dict) else {}
        if "skill" in named:
            names.append(str(named["skill"]))
    return names


async def plugin_skill_files(client: Client, draft: JsonObject) -> dict[str, dict[str, str]] | None:
    """Each pinned skill's files by its name, then by path in its folder; none for a seed type.

    The text is what the plugin was installed with, so a copy is the plugin's own folder.
    """
    uri = f"plugin-skills://{draft['type']}?spec_revision={draft['spec_revision']}"
    try:
        found = await resource_json(client, uri)
    except MCPError as error:
        if _NO_PLUGIN in str(error):
            return None
        raise
    stored = _text_of(found.get("files"))
    skills: dict[str, dict[str, str]] = {}
    for name in _names_of(draft.get("pinned_skills")):
        prefix = f"skills/{name}/"
        files = {
            path[len(prefix) :]: text for path, text in stored.items() if path.startswith(prefix)
        }
        if "SKILL.md" not in files:
            raise PluginSkillError(f"the plugin holds no {prefix}SKILL.md for a pinned skill")
        skills[name] = files
    return skills
