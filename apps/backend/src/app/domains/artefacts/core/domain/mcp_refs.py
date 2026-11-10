"""A spec's reference to an external MCP server its type is written with."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlsplit

from app.shared.json_types import JsonObject

_NAME = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
_TOOL = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
_SECRET = re.compile(r"^[A-Z][A-Z0-9_]*$")
#: What a name may not be: the servers of the engine itself.
RESERVED = frozenset({"engine", "answer"})
_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
_NAME_LIMIT = 32
#: A link that is a path, such as ``/mcp``, is the app's own MCP server, which it reaches itself.
_OWN_PATH = re.compile(r"^/[A-Za-z0-9/_-]*$")


class McpServerRefError(ValueError):
    """A reference to an external server that a run could not safely use."""


@dataclass(frozen=True)
class McpServerRef:
    """One server a spec's content is written with, checked by, or finished by.

    Only the tools it lists are offered to a writer, each as ``<name>__<tool>``. The app calls
    the others itself, with a draft's ID, and the writer never sees them: ``checks`` find a
    draft's faults, ``adds`` answer fields that are added to the content when it is saved, and
    ``files`` make a file of saved content.
    The token the server needs is read from the environment variable ``secret`` names, never
    stored here. A link that is a path (``/mcp``) is the app's own server, which lists checks,
    adds and files only.
    """

    name: str
    url: str
    tools: tuple[str, ...]
    secret: str | None = None
    checks: tuple[str, ...] = ()
    adds: tuple[str, ...] = ()
    files: tuple[str, ...] = ()

    @property
    def own(self) -> bool:
        """The link names the app's own server, which the app reaches without a network."""
        return self.url.startswith("/")

    def __post_init__(self) -> None:
        """Refuse a server that is not named, not reached over a safe link, or lists no tools."""
        if not _NAME.match(self.name) or len(self.name) > _NAME_LIMIT or self.name in RESERVED:
            raise McpServerRefError(f"a server has a lowercase name of its own: {self.name!r}")
        self._refuse_unsafe_link()
        listed = (*self.tools, *self.checks, *self.adds, *self.files)
        if not listed or len(set(listed)) != len(listed):
            raise McpServerRefError(f"{self.name}: list each tool it may use, once")
        if not all(_TOOL.match(tool) for tool in listed):
            raise McpServerRefError(f"{self.name}: a tool is named by its own name")
        if self.secret is not None and not _SECRET.match(self.secret):
            raise McpServerRefError(f"{self.name}: a secret names an environment variable")

    def _refuse_unsafe_link(self) -> None:
        if self.own:
            if not _OWN_PATH.match(self.url) or self.tools or self.secret is not None:
                raise McpServerRefError(
                    f"{self.name}: the app's own server is a path and lists "
                    f"checks, adds and files only: {self.url!r}"
                )
            return
        parts = urlsplit(self.url)
        local = parts.hostname in _LOCAL_HOSTS
        if (
            not parts.hostname
            or parts.scheme not in ("https", "http")
            or (parts.scheme == "http" and not local)
        ):
            raise McpServerRefError(f"{self.name}: a server is reached over https: {self.url!r}")
        if parts.username or parts.password:
            raise McpServerRefError(f"{self.name}: a URL carries no credentials")

    @classmethod
    def from_record(cls, record: object) -> McpServerRef:
        if not isinstance(record, dict):
            raise McpServerRefError("a server reference is an object with server, url and tools")
        fields = {str(key): value for key, value in record.items()}
        unknown = set(fields) - {"server", "url", "tools", "secret", "checks", "adds", "files"}
        tools = fields.get("tools") or []
        checks = fields.get("checks") or []
        adds = fields.get("adds") or []
        files = fields.get("files") or []
        secret = fields.get("secret")
        if (
            unknown
            or not isinstance(tools, list | tuple)
            or not isinstance(checks, list | tuple)
            or not isinstance(adds, list | tuple)
            or not isinstance(files, list | tuple)
        ):
            raise McpServerRefError(
                f"a server reference has server, url, tools, checks, adds, files, secret: {fields}"
            )
        return cls(
            name=str(fields.get("server")),
            url=str(fields.get("url")),
            tools=tuple(str(tool) for tool in tools),
            secret=str(secret) if secret is not None else None,
            checks=tuple(str(check) for check in checks),
            adds=tuple(str(add) for add in adds),
            files=tuple(str(file) for file in files),
        )

    def public(self) -> JsonObject:
        """What a reader of the type sees: the server and its tools, not how it is reached."""
        return {"server": self.name, "tools": list(self.tools)}

    def to_record(self) -> JsonObject:
        record: JsonObject = {"server": self.name, "url": self.url, "tools": list(self.tools)}
        if self.secret is not None:
            record["secret"] = self.secret
        if self.checks:
            record["checks"] = list(self.checks)
        if self.adds:
            record["adds"] = list(self.adds)
        if self.files:
            record["files"] = list(self.files)
        return record
