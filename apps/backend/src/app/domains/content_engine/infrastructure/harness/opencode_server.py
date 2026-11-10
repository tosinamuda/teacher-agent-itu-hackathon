"""One OpenCode server for one run of one agent, and the session it runs in.

Each run gets a server of its own, configured for it alone: the generator as its only model,
the relay as its only MCP server, and one agent whose prompt is the whole system prompt.
Its config and data live in a directory of its own, so nothing a developer has set up for
OpenCode (skills, instructions, other servers) reaches the model. The directory is removed with
the server, unless the run is kept: then it stays, and the next server started on it continues
the session.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import tempfile
from collections.abc import AsyncIterator, Iterator, Sequence
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from pathlib import Path

import httpx

from app.config import BACKEND_DIR
from app.domains.content_engine.infrastructure.harness.opencode_session import (
    RUN_TIMEOUT_SECONDS,
    Model,
    Session,
)
from app.domains.content_engine.infrastructure.harness.workspace import (
    SKILLS_DIR,
    WorkspaceSkill,
    write_skills,
)
from app.shared.json_types import JsonObject

#: The OpenCode release the adapter was traced on: ``npm i -g opencode-ai@1.18.32``.
OPENCODE_VERSION = "1.18.32"
#: What OpenCode installs on first use (the provider package, the prompt plugin's
#: dependencies) is kept here between runs. It is the adapter's own folder inside the app's
#: data folder, not the developer's OpenCode config or a home the API's user cannot write in,
#: and the run's config reaches OpenCode in its environment.
_CACHE = BACKEND_DIR / "var" / "opencode-cache"
_PLUGIN = Path(__file__).with_name("opencode_prompt.js")
#: The skill OpenCode ships with, which is not one the run's type pins.
_BUILT_IN_SKILL = "customize-opencode"
_LISTENING = re.compile(rb"listening on (http://127\.0\.0\.1:\d+)")


class OpenCodeUnavailableError(RuntimeError):
    """OpenCode is missing, or is not the release the adapter was traced on."""


@dataclass(frozen=True)
class Agent:
    """The one agent a server runs: its prompt, step limit, and the tools it may call."""

    prompt: str
    steps: int
    allowed: tuple[str, ...]
    temperature: float | None = None

    def config(self) -> JsonObject:
        """The agent's settings; ``read``, when allowed, reaches only skill files.

        The home of the run holds no skills of its own, so the workspace's are the only ones.
        """
        permission: JsonObject = {"*": "deny", **dict.fromkeys(self.allowed, "allow")}
        if "skill" in self.allowed:
            permission["skill"] = {"*": "allow", _BUILT_IN_SKILL: "deny"}
        if "read" in self.allowed:
            permission["read"] = {"*": "deny", f"*/{SKILLS_DIR.as_posix()}/*": "allow"}
        agent: JsonObject = {"mode": "primary", "prompt": self.prompt, "steps": self.steps}
        agent["permission"] = permission
        if self.temperature is not None:
            agent["temperature"] = self.temperature
        return agent


def config(model: Model, agent: Agent, mcp: JsonObject | None) -> JsonObject:
    """The whole configuration of a server for one run."""
    return {
        "$schema": "https://opencode.ai/config.json",
        "autoupdate": False,
        "share": "disabled",
        "snapshot": False,
        "plugin": [_PLUGIN.as_uri()],
        "model": f"engine/{model.id}",
        "provider": {"engine": model.provider()},
        "mcp": {"engine": mcp} if mcp else {},
        "agent": {"engine": agent.config()},
    }


def _environment(home: Path, settings: JsonObject, model: Model, agent: Agent) -> dict[str, str]:
    kept = {name: value for name, value in os.environ.items() if not name.startswith("OPENCODE")}
    return kept | {
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(_CACHE / "config"),
        "XDG_DATA_HOME": str(home / "data"),
        "XDG_STATE_HOME": str(home / "state"),
        "XDG_CACHE_HOME": str(_CACHE / "cache"),
        "npm_config_cache": str(_CACHE / "npm"),
        "OPENCODE_CONFIG_CONTENT": json.dumps(settings),
        "OPENCODE_DISABLE_CLAUDE_CODE": "1",
        "ENGINE_MODEL_KEY": model.key,
        "ENGINE_SYSTEM_PROMPT": agent.prompt,
    }


async def _address(process: asyncio.subprocess.Process) -> str:
    """The URL the server reports it listens on."""
    if process.stdout is None:
        raise OpenCodeUnavailableError("opencode serve has no output to read")
    while line := await process.stdout.readline():
        if found := _LISTENING.search(line):
            return found.group(1).decode()
    raise OpenCodeUnavailableError(f"opencode serve exited with {await process.wait()}")


def _kept_in_cache() -> dict[str, str]:
    """Where OpenCode keeps its data when it only reports its version.

    It writes under the user's home even then, and the API's user has a home it cannot write
    in, so every folder it uses is in the adapter's cache.
    """
    return {
        "XDG_CONFIG_HOME": str(_CACHE / "config"),
        "XDG_DATA_HOME": str(_CACHE / "data"),
        "XDG_STATE_HOME": str(_CACHE / "state"),
        "XDG_CACHE_HOME": str(_CACHE / "cache"),
    }


async def check_version() -> None:
    try:
        process = await asyncio.create_subprocess_exec(
            "opencode",
            "--version",
            stdout=asyncio.subprocess.PIPE,
            env=os.environ | _kept_in_cache(),
        )
    except FileNotFoundError as error:
        raise OpenCodeUnavailableError(
            f"install it: npm i -g opencode-ai@{OPENCODE_VERSION}"
        ) from error
    version = (await process.communicate())[0].decode().strip()
    if version != OPENCODE_VERSION:
        raise OpenCodeUnavailableError(
            f"opencode {version} found; the adapter needs {OPENCODE_VERSION}"
        )


@contextmanager
def _folder(kept: Path | None) -> Iterator[Path]:
    """The run's directory: ``kept`` if the run is kept, else one removed when the run ends."""
    if kept is None:
        with tempfile.TemporaryDirectory(prefix="engine-opencode-") as folder:
            yield Path(folder)
    else:
        kept.mkdir(parents=True, exist_ok=True)
        yield kept


@asynccontextmanager
async def served(
    model: Model,
    agent: Agent,
    *,
    mcp: JsonObject | None = None,
    env: dict[str, str] | None = None,
    skills: Sequence[WorkspaceSkill] = (),
    kept: Path | None = None,
) -> AsyncIterator[Session]:
    """A session on a server of its own, started in a workspace holding ``skills``.

    The server stops when the block ends, and its workspace and home are removed with it. With
    ``kept``, they stay in that folder, and a later call with the same folder continues the
    session it holds.
    """
    await check_version()
    with _folder(kept) as home:
        workspace = home / "workspace"
        workspace.mkdir(exist_ok=True)
        write_skills(workspace, skills)
        environment = _environment(home, config(model, agent, mcp), model, agent) | (env or {})
        process = await asyncio.create_subprocess_exec(
            *("opencode", "serve", "--port", "0", "--hostname", "127.0.0.1"),
            cwd=workspace,
            env=environment,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        try:
            base_url = await asyncio.wait_for(_address(process), timeout=120)
            async with httpx.AsyncClient(base_url=base_url, timeout=RUN_TIMEOUT_SECONDS) as http:
                yield await Session.open(http, model, kept=kept)
        finally:
            process.terminate()
            await process.wait()
