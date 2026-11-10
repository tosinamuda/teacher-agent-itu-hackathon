"""``mcp.json``: the external MCP servers a plugin lists, and the tools the writer may use."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef, McpServerRefError
from app.domains.content.plugins.problems import Problem, Severity
from app.domains.content.plugins.standard import breaks_the_standard

MCP_FILE = "mcp.json"
_BEARER = re.compile(r"^Bearer \$\{([A-Z][A-Z0-9_]*)\}$")


def _secret(name: str, headers: object) -> tuple[str | None, list[Problem]]:
    """The variable a server's bearer token is read from; only that header is supported."""
    if headers is None:
        return None, []
    if not isinstance(headers, dict):
        return None, [Problem(MCP_FILE, f"{name}: headers is an object")]
    found: str | None = None
    problems: list[Problem] = []
    for header, value in headers.items():
        matched = _BEARER.match(value) if isinstance(value, str) else None
        if header != "Authorization" or matched is None:
            problems.append(
                Problem(
                    MCP_FILE,
                    f'{name}: send only "Authorization": "Bearer ${{VARIABLE}}"; '
                    "the token is never written in the file",
                )
            )
        else:
            found = matched.group(1)
    return found, problems


@dataclass(frozen=True)
class ListedTools:
    """The tools the artefact file lists for each server of ``mcp.json``, by what they are for."""

    #: The tools the writer may use.
    writer: dict[str, list[str]]
    #: The tools the app calls to check a draft.
    checks: dict[str, list[str]]
    #: The tools the app calls when it saves a draft.
    adds: dict[str, list[str]]
    #: The tools the app calls to make a file of saved content.
    files: dict[str, list[str]]

    def servers(self) -> set[str]:
        return {*self.writer, *self.checks, *self.adds, *self.files}


def _entry(
    name: str, entry: object, listed: ListedTools
) -> tuple[McpServerRef | None, list[Problem]]:
    """The server the artefact lists tools for; none, without a problem, for one it does not."""
    fields = {str(key): value for key, value in entry.items()} if isinstance(entry, dict) else {}
    if fields.get("type") != "streamable-http":
        is_listed = name in listed.servers()
        skipped = Problem(
            MCP_FILE,
            f"{name}: skipped, the app connects to streamable-http servers only",
            Severity.ERROR if is_listed else Severity.WARNING,
        )
        return None, [skipped]
    if name not in listed.servers():
        return None, []
    secret, problems = _secret(name, fields.get("headers"))
    if problems:
        return None, problems
    try:
        ref = McpServerRef(
            name,
            str(fields.get("url")),
            tuple(listed.writer.get(name, ())),
            secret,
            tuple(listed.checks.get(name, ())),
            tuple(listed.adds.get(name, ())),
            tuple(listed.files.get(name, ())),
        )
        return ref, []
    except McpServerRefError as error:
        return None, [Problem(MCP_FILE, str(error))]


def read_servers(
    folder: Path, listed_tools: ListedTools, artefact_file: str
) -> tuple[tuple[McpServerRef, ...], list[Problem]]:
    """The servers in ``folder``'s ``mcp.json``, each with the tools the artefact file lists."""
    path = folder / MCP_FILE
    if not path.is_file():
        unused = [
            Problem(
                artefact_file,
                f"servers lists {name}, which has no {MCP_FILE}",
            )
            for name in sorted(listed_tools.servers())
        ]
        return (), unused
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        return (), [Problem(MCP_FILE, f"is not valid JSON: {error}")]
    if broken := breaks_the_standard(MCP_FILE, "mcp", record):
        return (), broken
    listed = record["mcpServers"]
    servers: list[McpServerRef] = []
    problems: list[Problem] = []
    for name, entry in listed.items():
        ref, found = _entry(str(name), entry, listed_tools)
        problems += found
        if ref is not None:
            servers.append(ref)
    problems += [
        Problem(
            artefact_file,
            f"servers lists {name}, which {MCP_FILE} does not have",
        )
        for name in sorted(listed_tools.servers() - set(map(str, listed)))
    ]
    return tuple(servers), problems


def unused_servers(folder: Path, linked: set[str]) -> list[Problem]:
    """A problem for each server of ``mcp.json`` that no artefact of the plugin lists tools for."""
    path = folder / MCP_FILE
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        names = {
            str(name)
            for name, entry in record["mcpServers"].items()
            if isinstance(entry, dict) and entry.get("type") == "streamable-http"
        }
    except (OSError, ValueError, KeyError, TypeError):
        return []
    return [
        Problem(MCP_FILE, f"{name}: no artefact file lists the tools of {name}")
        for name in sorted(names - linked)
    ]
