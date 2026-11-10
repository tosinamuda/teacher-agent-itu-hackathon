"""An agent spoken to over the Agent Client Protocol, through the protocol's Python SDK.

The SDK runs the connection. What is kept here is what this client decides: the agent has
no file system or terminal of the client's, it may run the tools it is given (they are the
engine's own), what it says is kept, and its turn is cancelled once it has made as many
model calls as the loop allows, or once the answer it was asked for has come.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable, Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from acp import PROTOCOL_VERSION, RequestError, spawn_agent_process, text_block
from acp.client.connection import ClientSideConnection
from acp.interfaces import Agent, Client
from acp.schema import (
    AgentMessageChunk,
    AllowedOutcome,
    ClientCapabilities,
    CreateElicitationResponse,
    CreateTerminalResponse,
    DeclineElicitationResponse,
    DeniedOutcome,
    ElicitationMode,
    EnvVariable,
    FileSystemCapabilities,
    HttpHeader,
    HttpMcpServer,
    KillTerminalResponse,
    PermissionOption,
    ReadTextFileResponse,
    ReleaseTerminalResponse,
    RequestPermissionResponse,
    TerminalOutputResponse,
    TextContentBlock,
    ToolCallProgress,
    ToolCallStart,
    ToolCallUpdate,
    UsageUpdate,
    WaitForTerminalExitResponse,
    WriteTextFileResponse,
)

#: ACP lines carry whole prompts and tool results.
_LINE_LIMIT = 16 * 1024 * 1024
#: How much of the agent's error output an error quotes.
_ERROR_TAIL = 2000


class AcpError(RuntimeError):
    """The agent ended, or answered a request with an error."""


def http_server(name: str, url: str, headers: Mapping[str, str]) -> HttpMcpServer:
    """An MCP server the agent reaches over streamable HTTP."""
    sent = [HttpHeader(name=key, value=value) for key, value in headers.items()]
    return HttpMcpServer(name=name, url=url, headers=sent, type="http")


@dataclass
class Turn:
    """What one prompt came to: why it stopped, what the agent said, and its model calls."""

    model_calls_allowed: int
    done: Callable[[], bool]
    stop_reason: str = ""
    said: list[str] = field(default_factory=list)
    model_calls: int = 0
    cancelled: bool = False
    #: The tool calls that have started and not ended.
    running: set[str] = field(default_factory=set)
    #: Whether a tool call has started since the last allowed model call was made.
    ran_at_the_limit: bool = False

    @property
    def text(self) -> str:
        return "".join(self.said).strip()

    def over(self) -> bool:
        """Whether the turn should be cancelled now.

        The agent reports a model call before it runs that call's tools, so the last allowed
        call's tools are let finish: its answer may be one.
        """
        spent = self.ran_at_the_limit and not self.running
        return spent or self.done()


class _Listener(Client):
    """Hears the agent's turn as it happens, and grants it its tools.

    It offers the agent no file system, terminal or questions for a person: those requests
    are refused, as the capabilities it declares say they will be.
    """

    def __init__(self) -> None:
        self.turn: Turn | None = None
        self.agent: Agent | None = None

    def on_connect(self, conn: Agent) -> None:
        self.agent = conn

    async def session_update(self, session_id: str, update: object, **kwargs: Any) -> None:
        turn = self.turn
        if turn is None:
            return
        if isinstance(update, AgentMessageChunk) and isinstance(update.content, TextContentBlock):
            turn.said.append(update.content.text)
        elif isinstance(update, ToolCallStart):
            turn.running.add(update.tool_call_id)
            turn.ran_at_the_limit |= turn.model_calls >= turn.model_calls_allowed
        elif isinstance(update, ToolCallProgress) and update.status in ("completed", "failed"):
            turn.running.discard(update.tool_call_id)
        elif isinstance(update, UsageUpdate):
            # The agent reports its context use once after each model call.
            turn.model_calls += 1
        if turn.over() and not turn.cancelled and self.agent is not None:
            turn.cancelled = True
            await self.agent.cancel(session_id=session_id)

    async def request_permission(
        self,
        session_id: str,
        tool_call: ToolCallUpdate,
        options: list[PermissionOption],
        **kwargs: Any,
    ) -> RequestPermissionResponse:
        for kind in ("allow_always", "allow_once"):
            chosen = next((option for option in options if option.kind == kind), None)
            if chosen is not None:
                allowed = AllowedOutcome(option_id=chosen.option_id, outcome="selected")
                return RequestPermissionResponse(outcome=allowed)
        return RequestPermissionResponse(outcome=DeniedOutcome(outcome="cancelled"))

    async def read_text_file(
        self,
        session_id: str,
        path: str,
        line: int | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> ReadTextFileResponse:
        raise RequestError.method_not_found("fs/read_text_file")

    async def write_text_file(
        self, session_id: str, path: str, content: str, **kwargs: Any
    ) -> WriteTextFileResponse | None:
        raise RequestError.method_not_found("fs/write_text_file")

    async def create_terminal(
        self,
        session_id: str,
        command: str,
        args: list[str] | None = None,
        env: list[EnvVariable] | None = None,
        cwd: str | None = None,
        output_byte_limit: int | None = None,
        **kwargs: Any,
    ) -> CreateTerminalResponse:
        raise RequestError.method_not_found("terminal/create")

    async def terminal_output(
        self, session_id: str, terminal_id: str, **kwargs: Any
    ) -> TerminalOutputResponse:
        raise RequestError.method_not_found("terminal/output")

    async def wait_for_terminal_exit(
        self, session_id: str, terminal_id: str, **kwargs: Any
    ) -> WaitForTerminalExitResponse:
        raise RequestError.method_not_found("terminal/wait_for_exit")

    async def kill_terminal(
        self, session_id: str, terminal_id: str, **kwargs: Any
    ) -> KillTerminalResponse | None:
        raise RequestError.method_not_found("terminal/kill")

    async def release_terminal(
        self, session_id: str, terminal_id: str, **kwargs: Any
    ) -> ReleaseTerminalResponse | None:
        raise RequestError.method_not_found("terminal/release")

    async def create_elicitation(
        self, message: str, mode: ElicitationMode, **kwargs: Any
    ) -> CreateElicitationResponse:
        return DeclineElicitationResponse(action="decline")

    async def complete_elicitation(self, elicitation_id: str, **kwargs: Any) -> None:
        return None

    async def ext_method(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        raise RequestError.method_not_found(method)

    async def ext_notification(self, method: str, params: dict[str, Any]) -> None:
        return None


class AcpAgent:
    """One agent process and its connection."""

    def __init__(self, connection: ClientSideConnection, listener: _Listener, errors: Path) -> None:
        self._connection = connection
        self._listener = listener
        self._errors = errors

    def failed(self, doing: str, error: Exception) -> AcpError:
        """An error naming what failed, with the tail of what the agent wrote to stderr."""
        said = self._errors.read_text(encoding="utf-8", errors="replace")[-_ERROR_TAIL:]
        return AcpError(f"the agent failed during {doing}: {error}; it said: {said}")

    async def new_session(self, cwd: Path, servers: tuple[HttpMcpServer, ...] = ()) -> str:
        try:
            opened = await self._connection.new_session(
                cwd=str(cwd.resolve()), mcp_servers=[*servers]
            )
        except Exception as error:
            raise self.failed("session/new", error) from error
        return opened.session_id

    async def prompt(
        self,
        session_id: str,
        text: str,
        *,
        model_calls: int,
        done: Callable[[], bool] = lambda: False,
    ) -> Turn:
        """One prompt's turn, cancelled after ``model_calls`` model calls or once ``done``.

        ``done`` is asked after every update the agent sends, such as a tool call's end.
        """
        turn = self._listener.turn = Turn(model_calls, done)
        try:
            answered = await self._connection.prompt(
                session_id=session_id, prompt=[text_block(text)]
            )
        except Exception as error:
            raise self.failed("session/prompt", error) from error
        finally:
            self._listener.turn = None
        turn.stop_reason = str(answered.stop_reason)
        return turn


@asynccontextmanager
async def launched(
    argv: tuple[str, ...], *, env: Mapping[str, str], cwd: Path
) -> AsyncIterator[AcpAgent]:
    """An initialised agent, its process shut down when the block ends.

    Its error output goes to a file in ``cwd``, so an error can quote it.
    """
    errors = cwd / "agent.stderr"
    listener = _Listener()
    capabilities = ClientCapabilities(
        fs=FileSystemCapabilities(read_text_file=False, write_text_file=False), terminal=False
    )
    with errors.open("wb") as error_output:
        transport = {"stderr": error_output.fileno(), "limit": _LINE_LIMIT}
        async with spawn_agent_process(
            listener, argv[0], *argv[1:], env=env, cwd=cwd, transport_kwargs=transport
        ) as (connection, _process):
            agent = AcpAgent(connection, listener, errors)
            try:
                await connection.initialize(
                    protocol_version=PROTOCOL_VERSION, client_capabilities=capabilities
                )
            except Exception as error:
                raise agent.failed("initialize", error) from error
            yield agent
