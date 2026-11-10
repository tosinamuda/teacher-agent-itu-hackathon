"""DeepSeek Harness (``dsh``) for one run: its ACP agent, configured for that run alone.

``dsh --profile acp`` is booted with a patch that makes the generator its only model, turns
off every tool of its own (shell, files, web, subagents, plans, goals, and skills unless the run
gives it some), its telemetry
and its session titles, and makes the run's prompt the whole system prompt. Its home is a directory
removed with the run, so nothing set up for dsh elsewhere reaches the model. The patch is
JSON, which YAML reads as is.
"""

from __future__ import annotations

import asyncio
import json
import os
import tempfile
from collections.abc import AsyncIterator, Iterator, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from app.domains.content_engine.infrastructure.harness.acp import AcpAgent, launched
from app.domains.content_engine.infrastructure.harness.workspace import (
    WorkspaceSkill,
    write_skills,
)
from app.shared.json_types import JsonObject

#: The release the adapter was traced on: ``npm i -g @deepseek-ai/dsh@0.1.5-rc.3``.
DSH_VERSION = "0.1.5-rc.3"
#: The rows that read skills from the workspace and offer them to the model as a tool.
SKILL_ROWS = ("skill", "skill-filesystem", "tool-skill")
#: The profile rows the run turns off: every tool the DSPy writer lacks, and what would send
#: the lesson elsewhere (telemetry) or spend on it (session titles).
OFF = (
    "session-telemetry-otel",
    "session-title-llm",
    "agent-instructions",
    "tool-bash",
    "tool-jobs",
    "tool-fs",
    "tool-fs-search",
    *SKILL_ROWS,
    "tool-subagent-control",
    "tool-subagent-list-agents",
    "tool-subagent",
    "tool-subagent-fork",
    "tool-workflow",
    "tool-todo",
    "tool-goal",
    "tool-ralph",
    "goal",
    "goal-round-driver",
    "command-goal",
    "plan-mode",
    "web",
    "web-search-deepseek",
    "web-fetch-http",
    "tool-web",
)
_PROVIDER = "generator"
_KEY_ENV = "ENGINE_MODEL_KEY"


class DshUnavailableError(RuntimeError):
    """dsh is missing, or is not the release the adapter was traced on."""


@dataclass(frozen=True)
class DshModel:
    """The generator on its OpenAI-compatible endpoint."""

    id: str
    base_url: str
    key: str


def patch(model: DshModel, prompt: str, home: Path, *, skills: bool = False) -> list[JsonObject]:
    """The overlay that configures the ACP profile for one run kept in ``home``.

    A row's ``config`` replaces the profile's whole config for that row. With ``skills`` the
    rows that load skills from the workspace stay on.
    """
    off = [row for row in OFF if not (skills and row in SKILL_ROWS)]
    rows: list[JsonObject] = [{"id": row, "disabled": True} for row in off]
    route: JsonObject = {
        "apiKeyEnv": _KEY_ENV,
        "api": "openai-completions",
        "baseURL": model.base_url,
        "models": [{"id": model.id, "name": model.id, "input": ["text"]}],
    }
    chosen: JsonObject = {"provider": _PROVIDER, "model": model.id}
    return [
        *rows,
        {"id": "llm-pi-ai", "config": {"providers": {_PROVIDER: route}}},
        {"id": "acp", "config": chosen},
        {"id": "agent-default-model", "config": chosen},
        {
            "id": "system-prompt",
            "config": {
                "includeHarnessIdentity": False,
                "includeRuntimeContext": False,
                "personaPrefix": prompt,
                "personaSuffix": "",
            },
        },
        {
            "id": "session-persistence-jsonl",
            "config": {"root": str(home / "sessions"), "compression": "none"},
        },
    ]


async def check_version() -> None:
    try:
        process = await asyncio.create_subprocess_exec(
            "dsh", "--version", stdout=asyncio.subprocess.PIPE
        )
    except FileNotFoundError as error:
        raise DshUnavailableError(f"install it: npm i -g @deepseek-ai/dsh@{DSH_VERSION}") from error
    version = (await process.communicate())[0].decode().strip()
    if version != DSH_VERSION:
        raise DshUnavailableError(f"dsh {version} found; the adapter needs {DSH_VERSION}")


def _environment(home: Path, model: DshModel) -> dict[str, str]:
    kept = {name: value for name, value in os.environ.items() if not name.startswith("DSH_")}
    return kept | {
        "DSH_HOME": str(home),
        "DSH_AGENTS_HOME": str(home / "agents"),
        "DSH_TELEMETRY_MODE": "OFF",
        _KEY_ENV: model.key,
    }


@dataclass(frozen=True)
class Run:
    """The agent of one run, the folder its sessions are kept in, and the workspace it works in."""

    agent: AcpAgent
    home: Path
    workspace: Path

    def model_calls(self) -> Iterator[JsonObject]:
        """Each model call of the run's sessions, as dsh logged it, with its token counts."""
        for log in sorted((self.home / "sessions").rglob("session.v*.jsonl")):
            for line in log.read_text(encoding="utf-8").splitlines():
                event = json.loads(line)
                if isinstance(event, dict) and event.get("type") == "assistant/message":
                    data = event.get("data")
                    if isinstance(data, dict):
                        yield data


@asynccontextmanager
async def dsh_run(
    model: DshModel, prompt: str, *, skills: Sequence[WorkspaceSkill] | None = None
) -> AsyncIterator[Run]:
    """Dsh's ACP agent for one run, stopped and its home removed when the block ends.

    Sessions are opened in ``Run.workspace``. Given ``skills``, even none, the workspace holds
    them as files and dsh loads them itself; otherwise dsh has no skills.
    """
    await check_version()
    with tempfile.TemporaryDirectory(prefix="engine-dsh-") as folder:
        home = Path(folder)
        workspace = home / "workspace"
        workspace.mkdir()
        write_skills(workspace, skills or ())
        overlay = home / "patch.yml"
        overlay.write_text(
            json.dumps(patch(model, prompt, home, skills=skills is not None)), encoding="utf-8"
        )
        argv = ("dsh", "--profile", "acp", "--patch", str(overlay))
        async with launched(argv, env=_environment(home, model), cwd=home) as agent:
            yield Run(agent, home, workspace)
