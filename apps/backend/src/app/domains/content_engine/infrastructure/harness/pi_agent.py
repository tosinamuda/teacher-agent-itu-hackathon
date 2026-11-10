"""pi for one run: its RPC agent, configured for that run alone.

``pi --mode rpc`` is started in a workspace of the run's own, with a home of the run's own,
so nothing set up for pi elsewhere reaches the model. The generator is its only model, the
prompt is the whole system prompt, and its tools are the run's MCP tools, which pi connects
from an ``mcp.json`` the run writes, and ``read`` when the run gives it skills. Skills are
``SKILL.md`` files in the workspace; pi lists them in its prompt and the model loads one by
reading it.

pi speaks JSON lines: a command per line to it, and the agent's events per line back.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import tempfile
from collections.abc import AsyncIterator, Callable, Sequence
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass, field
from pathlib import Path

from app.domains.content_engine.infrastructure.harness.workspace import (
    SKILLS_DIR,
    WorkspaceSkill,
    write_skills,
)
from app.shared.json_types import JsonObject

#: The release the adapter was traced on: ``npm i -g @earendil-works/pi-coding-agent@0.99.1``.
PI_VERSION = "0.99.1"
_EXTENSION = Path(__file__).with_name("pi_extension.ts")
_PROVIDER = "generator"
_KEY_ENV = "ENGINE_MODEL_KEY"
#: Event lines carry whole messages and tool results.
_LINE_LIMIT = 16 * 1024 * 1024
#: How much of pi's error output an error quotes.
_ERROR_TAIL = 2000
_CONTEXT_WINDOW = 131_072
_MAX_TOKENS = 32_768


class PiUnavailableError(RuntimeError):
    """pi is missing, or is not the release the adapter was traced on."""


class PiError(RuntimeError):
    """pi ended, or refused a command."""


@dataclass(frozen=True)
class PiModel:
    """The generator on its OpenAI-compatible endpoint."""

    id: str
    base_url: str
    key: str


@dataclass(frozen=True)
class McpServer:
    """An MCP server over HTTP whose tools the run offers, as ``mcp__<name>__<tool>``."""

    name: str
    url: str
    headers: dict[str, str]
    tools: tuple[str, ...]
    #: Whether a call of its tools is the run's last: the agent stops once one is answered.
    final: bool = False

    def tool_names(self) -> list[str]:
        return [f"mcp__{self.name}__{tool}" for tool in self.tools]

    def variable(self, header: str) -> str:
        """The environment variable that holds the value of one of its headers."""
        name = re.sub(r"[^A-Z0-9]", "_", f"{self.name}_{header}".upper())
        return f"ENGINE_MCP_{name}"


@dataclass
class Turn:
    """What one prompt came to: why it stopped, what the model said, and each model call."""

    stop_reason: str = ""
    messages: list[JsonObject] = field(default_factory=list)
    cancelled: bool = False

    @property
    def model_calls(self) -> int:
        return len(self.messages)

    @property
    def text(self) -> str:
        """What the model said in its last message."""
        content = self.messages[-1].get("content") if self.messages else None
        blocks = content if isinstance(content, list) else []
        said = [b["text"] for b in blocks if isinstance(b, dict) and b.get("type") == "text"]
        return "".join(str(part) for part in said).strip()


def _made_a_call(message: JsonObject) -> bool:
    """Whether an assistant message is a model call's, not what an abort before one leaves."""
    usage = message.get("usage")
    used = [usage.get("input"), usage.get("output")] if isinstance(usage, dict) else []
    unused = not any(isinstance(count, int) and count > 0 for count in used)
    aborted = message.get("stopReason") == "aborted" or "aborted" in str(
        message.get("errorMessage")
    )
    return not (unused and aborted)


def _tool_calls(message: JsonObject) -> int:
    content = message.get("content")
    blocks = content if isinstance(content, list) else []
    return sum(isinstance(b, dict) and b.get("type") == "toolCall" for b in blocks)


class PiAgent:
    """One pi process and its session."""

    def __init__(self, process: asyncio.subprocess.Process, errors: Path) -> None:
        self._process = process
        self._errors = errors

    def _failed(self, doing: str, error: object) -> PiError:
        said = self._errors.read_text(encoding="utf-8", errors="replace")[-_ERROR_TAIL:]
        return PiError(f"pi failed during {doing}: {error}; it said: {said}")

    async def _send(self, command: JsonObject) -> None:
        if self._process.stdin is None:
            raise PiError("pi has no input to write to")
        self._process.stdin.write(json.dumps(command).encode() + b"\n")
        await self._process.stdin.drain()

    async def _events(self) -> AsyncIterator[JsonObject]:
        if self._process.stdout is None:
            raise PiError("pi has no output to read")
        while line := await self._process.stdout.readline():
            event = json.loads(line)
            if isinstance(event, dict):
                yield event
        raise self._failed("its turn", f"it exited with {await self._process.wait()}")

    async def prompt(
        self,
        text: str,
        *,
        model_calls: int,
        done: Callable[[], bool] = lambda: False,
    ) -> Turn:
        """One prompt's turn, aborted after ``model_calls`` model calls or once ``done``.

        Only a call that made tool calls is stopped, once they have run: its answer may be one.
        """
        turn, running = Turn(), 0
        await self._send({"type": "prompt", "message": text})
        async for event in self._events():
            kind = event.get("type")
            message = event.get("message")
            if kind == "response" and event.get("success") is False:
                raise self._failed("prompt", event.get("error"))
            if kind == "message_end" and isinstance(message, dict):
                if message.get("role") == "assistant" and _made_a_call(message):
                    turn.messages.append(message)
                    running += _tool_calls(message)
            elif kind == "tool_execution_end":
                running -= 1
            elif kind == "agent_end":
                break
            over = turn.model_calls >= model_calls or done()
            if kind == "tool_execution_end" and over and running <= 0 and not turn.cancelled:
                turn.cancelled = True
                await self._send({"type": "abort"})
        last = turn.messages[-1].get("stopReason") if turn.messages else None
        stopped = turn.cancelled or last == "toolUse"
        turn.stop_reason = "aborted" if stopped else str(last)
        return turn


async def check_version() -> None:
    try:
        process = await asyncio.create_subprocess_exec(
            "pi", "--version", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )
    except FileNotFoundError as error:
        raise PiUnavailableError(
            f"install it: npm i -g @earendil-works/pi-coding-agent@{PI_VERSION}"
        ) from error
    version = (await process.communicate())[0].decode().strip()
    if version != PI_VERSION:
        raise PiUnavailableError(f"pi {version} found; the adapter needs {PI_VERSION}")


def models_file(model: PiModel) -> JsonObject:
    """The file ``models.json`` for pi: the generator as the one provider."""
    entry: JsonObject = {
        "id": model.id,
        "name": model.id,
        "reasoning": False,
        "input": ["text"],
        "contextWindow": _CONTEXT_WINDOW,
        "maxTokens": _MAX_TOKENS,
    }
    provider: JsonObject = {
        "baseUrl": model.base_url,
        "api": "openai-completions",
        "apiKey": f"${_KEY_ENV}",
        "models": [entry],
    }
    return {"providers": {_PROVIDER: provider}}


def mcp_file(servers: Sequence[McpServer]) -> JsonObject:
    """The file ``mcp.json`` for pi: each server, its tools declared to the model.

    A header's value is the name of an environment variable, so the file holds no secret.
    """
    listed: JsonObject = {}
    for server in servers:
        headers: JsonObject = {name: f"${{{server.variable(name)}}}" for name in server.headers}
        listed[server.name] = {"url": server.url, "headers": headers, "exposure": "direct"}
    return {"mcpServers": listed}


def arguments(
    model: PiModel, prompt: str, servers: Sequence[McpServer], *, skills: bool
) -> list[str]:
    """The command line of pi for one run: only its tools, prompt and skills.

    The workspace holds the run's own skills, so pi is told to trust it: a run has no one to ask.
    """
    allowed = [name for server in servers for name in server.tool_names()]
    argv = ["pi", "--mode", "rpc", "--no-session", "--offline", "--provider", _PROVIDER]
    argv += ["--model", model.id, "--system-prompt", prompt]
    argv += ["--no-extensions", "--extension", "builtin:mcp", "--extension", str(_EXTENSION)]
    argv += ["--no-context-files", "--no-prompt-templates", "--no-themes"]
    argv += ["--tools", ",".join([*allowed, *(["read"] if skills else [])])]
    return [*argv, "--approve"] if skills else [*argv, "--no-skills"]


def _environment(
    home: Path, workspace: Path, model: PiModel, servers: Sequence[McpServer], model_calls: int
) -> dict[str, str]:
    kept = {name: value for name, value in os.environ.items() if not name.startswith("PI_")}
    headers = {s.variable(name): value for s in servers for name, value in s.headers.items()}
    answers = [name for s in servers if s.final for name in s.tool_names()]
    return (
        kept
        | headers
        | {
            "ENGINE_MAX_MODEL_CALLS": str(model_calls),
            "HOME": str(home),
            "PI_CODING_AGENT_DIR": str(home / "agent"),
            "PI_OFFLINE": "1",
            "PI_SKIP_VERSION_CHECK": "1",
            _KEY_ENV: model.key,
            "ENGINE_ANSWER_TOOLS": ",".join(answers),
            "ENGINE_SKILLS_DIR": str(workspace / SKILLS_DIR),
        }
    )


@asynccontextmanager
async def pi_run(
    model: PiModel,
    prompt: str,
    servers: Sequence[McpServer],
    *,
    model_calls: int,
    skills: Sequence[WorkspaceSkill] | None = None,
) -> AsyncIterator[PiAgent]:
    """The pi agent for one run, stopped and its home removed when the block ends.

    The run may make ``model_calls`` model calls in all, however many prompts it is given. The
    extension stops the run before the next one; each prompt's own limit is a backstop.

    Given ``skills``, even none, the workspace holds them as files and pi loads them itself;
    otherwise pi has no skills.
    """
    await check_version()
    with tempfile.TemporaryDirectory(prefix="engine-pi-") as folder:
        home = Path(folder).resolve()
        (home / "agent").mkdir()
        for name, content in (("models.json", models_file(model)), ("mcp.json", mcp_file(servers))):
            (home / "agent" / name).write_text(json.dumps(content), encoding="utf-8")
        workspace = home / "workspace"
        workspace.mkdir()
        write_skills(workspace, skills or ())
        errors = home / "pi.stderr"
        argv = arguments(model, prompt, servers, skills=skills is not None)
        with errors.open("wb") as error_output:
            process = await asyncio.create_subprocess_exec(
                *argv,
                cwd=workspace,
                env=_environment(home, workspace, model, servers, model_calls),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=error_output,
                limit=_LINE_LIMIT,
            )
            try:
                yield PiAgent(process, errors)
            finally:
                with suppress(ProcessLookupError):
                    process.terminate()
                await process.wait()
