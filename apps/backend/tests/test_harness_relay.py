"""The relay a harness in another process reaches the draft through."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content_engine.infrastructure.harness.relay import relayed
from app.domains.content_engine.mcp.caller import as_the_app
from tests.content_engine_support import PLAN, TYPE, seed_lesson, server_over, writer_client

pytestmark = pytest.mark.asyncio

_ACCEPT = {"Accept": "application/json, text/event-stream"}


async def _read_draft(db: AsyncSession, *, skills_hidden: bool) -> dict[str, Any]:
    """What ``read_draft`` returns through a relay, for a draft whose type pins a skill."""
    await seed_lesson(db, skills=("show-the-working",))
    with as_the_app():
        async with Client(server_over(db)) as base, writer_client(base) as client:
            opened = await base.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            assert opened.structured_content is not None
            draft_id = opened.structured_content["draft_id"]
            async with relayed(client, skills_hidden=skills_hidden) as r:
                call = {"name": "read_draft", "arguments": {"draft_id": draft_id}}
                request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": call}
                async with httpx.AsyncClient() as http:
                    reply = await http.post(r.url, json=request, headers=_ACCEPT | r.headers())
    result = reply.json()["result"]
    return {"text": json.loads(result["content"][0]["text"]), "data": result["structuredContent"]}


async def test_a_relay_can_leave_the_skills_out_of_a_drafts_brief(db: AsyncSession) -> None:
    read = await _read_draft(db, skills_hidden=True)

    for view in (read["text"], read["data"]):
        assert "skills" not in view["brief"]
        assert view["brief"]["audience"]


async def test_a_relay_gives_the_skills_in_a_drafts_brief_unless_told_not_to(
    db: AsyncSession,
) -> None:
    read = await _read_draft(db, skills_hidden=False)

    assert [s["name"] for s in read["text"]["brief"]["skills"]] == ["Show the working"]
