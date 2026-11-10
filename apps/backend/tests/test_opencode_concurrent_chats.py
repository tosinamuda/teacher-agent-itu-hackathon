"""Several chats at once: each keeps an agent, a session and a folder of its own."""

from __future__ import annotations

import asyncio
import re
import shutil
from collections import defaultdict
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import pytest
from mcp import Client
from mcp.server import MCPServer

from app.domains.content_engine.infrastructure.harness import opencode
from app.domains.content_engine.infrastructure.harness.opencode import OpenCodeWriter
from app.domains.content_engine.infrastructure.harness.opencode_home import (
    home_of,
    remembered_session,
)
from app.domains.content_engine.infrastructure.harness.opencode_server import Model
from app.shared.json_types import JsonObject
from tests.harness_script import message_text
from tests.openai_stub import answer, stub_model, tool_call

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32"),
]

CHATS = 3
MESSAGES = 2


def _server(calls: dict[str, list[str]]) -> MCPServer:
    server = MCPServer("fake-draft-tools")

    @server.tool(name="revise_part")
    def revise_part(draft_id: str, unit_id: str, part: dict[str, str]) -> str:
        calls[draft_id].append(part["note"])
        return "revised"

    return server


def _script(body: dict[str, Any]) -> dict[str, Any]:
    """Revise the part of the draft the latest message names, noting its turn, then answer."""
    messages = body["messages"]
    users = [message_text(m) for m in messages if m["role"] == "user"]
    draft = re.findall(r"## draft_id\s+(\S+)", " ".join(users))[-1]
    last_user = max(i for i, m in enumerate(messages) if m["role"] == "user")
    if any(m["role"] == "tool" for m in messages[last_user:]):
        return answer(f"done {draft}")
    note = f"{draft} message {len(users)}"
    return tool_call(
        "engine_revise_part", {"draft_id": draft, "unit_id": "s1", "part": {"note": note}}
    )


async def test_chats_running_together_do_not_share_an_agent_a_session_or_a_history(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: dict[str, list[str]] = defaultdict(list)
    running, peak = 0, 0
    real = opencode.served

    @asynccontextmanager
    async def counting(*arguments: Any, **keywords: Any) -> AsyncIterator[Any]:
        nonlocal running, peak
        async with real(*arguments, **keywords) as session:
            running += 1
            peak = max(peak, running)
            try:
                yield session
            finally:
                running -= 1

    monkeypatch.setattr(opencode, "served", counting)

    async def chat(client: Client, writer: OpenCodeWriter, number: int) -> tuple[str, list[str]]:
        draft_id = f"D-{number}"
        draft: JsonObject = {"draft_id": draft_id, "brief": {}, "part_schemas": {}, "units": [{}]}
        summaries = []
        async with writer.keep(client, draft, {}, key=f"T-{number}") as kept:
            for message in range(1, MESSAGES + 1):
                summaries.append(await kept.write(client, draft, {}, feedback=f"change {message}"))
                await asyncio.sleep(0)
        return draft_id, summaries

    with stub_model(_script) as (stub, base_url):
        writer = OpenCodeWriter(Model("stub-model", base_url, "k"))
        async with Client(_server(calls)) as client:
            answered = await asyncio.gather(*(chat(client, writer, n) for n in range(CHATS)))

    assert peak == CHATS
    for draft_id, summaries in answered:
        assert summaries == [f"done {draft_id}"] * MESSAGES
        assert calls[draft_id] == [f"{draft_id} message {m}" for m in range(1, MESSAGES + 1)]
    sessions = {remembered_session(home_of(f"T-{n}")) for n in range(CHATS)}
    assert len(sessions) == CHATS and None not in sessions
    for request in stub.requests:
        users = [message_text(m) for m in request["messages"] if m["role"] == "user"]
        assert len({d for d in re.findall(r"## draft_id\s+(\S+)", " ".join(users))}) == 1
