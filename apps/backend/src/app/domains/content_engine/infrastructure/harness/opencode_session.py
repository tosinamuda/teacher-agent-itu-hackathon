"""One OpenCode session: a prompt run to the end, and every model step it took on the way.

The steps are read from the server's event stream, as OpenCode's own ``run`` command reads
them. Listing a session's messages afterwards fails in 1.18.32 once a prompt asked for
structured output: the stored format does not encode.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from pathlib import Path

import httpx

from app.domains.content_engine.infrastructure.harness.opencode_feed import Feed
from app.domains.content_engine.infrastructure.harness.opencode_home import (
    remember_session,
    remembered_session,
)
from app.domains.content_engine.infrastructure.tap import current_tap
from app.infra.llm_models import recorded
from app.shared.json_types import JsonObject

_LOG = logging.getLogger(__name__)

#: A run is bounded by its step limit and each model call's own timeout, not by this.
RUN_TIMEOUT_SECONDS = 3600.0
#: How long the events of a finished run may trail its reply.
_TRAILING_SECONDS = 30.0


@dataclass(frozen=True)
class Model:
    """The generator on its OpenAI-compatible endpoint, as OpenCode's provider sees it."""

    id: str
    base_url: str
    key: str

    def provider(self) -> JsonObject:
        options: JsonObject = {"baseURL": self.base_url, "apiKey": "{env:ENGINE_MODEL_KEY}"}
        known = recorded(f"openai/{self.id}")
        model: JsonObject = {"name": self.id, "tool_call": True}
        if known and known.opencode_options:
            model["options"] = known.opencode_options
        return {
            "npm": "@ai-sdk/openai-compatible",
            "name": "Engine generator",
            "options": options,
            "models": {self.id: model},
        }


@dataclass
class Steps:
    """Each assistant message of one session as last updated, with its parts."""

    session_id: str
    messages: dict[str, JsonObject] = field(default_factory=dict)
    parts: dict[str, dict[str, JsonObject]] = field(default_factory=dict)

    def take(self, event: JsonObject) -> bool:
        """Keep what ``event`` says about the session; true once the session is idle."""
        kind, properties = event.get("type"), event.get("properties")
        if not isinstance(properties, dict) or properties.get("sessionID") != self.session_id:
            return False
        info, part = properties.get("info"), properties.get("part")
        if kind == "message.updated" and isinstance(info, dict) and info.get("role") == "assistant":
            self.messages[str(info.get("id"))] = info
        if kind == "message.part.updated" and isinstance(part, dict):
            self.parts.setdefault(str(part.get("messageID")), {})[str(part.get("id"))] = part
        status = properties.get("status")
        return (
            kind == "session.status" and isinstance(status, dict) and status.get("type") == "idle"
        )

    def each(self) -> list[JsonObject]:
        """Every step in order, as ``{"info", "parts"}``."""
        return [
            {"info": info, "parts": list(self.parts.get(message_id, {}).values())}
            for message_id, info in sorted(self.messages.items())
        ]


async def _events(lines: AsyncIterator[str]) -> AsyncIterator[JsonObject]:
    async for line in lines:
        if line.startswith("data:"):
            event = json.loads(line.removeprefix("data:"))
            if isinstance(event, dict):
                yield event


@dataclass(frozen=True)
class Session:
    http: httpx.AsyncClient
    id: str
    model: Model
    #: Whether the session is one an earlier server opened, with its history.
    resumed: bool = False

    @classmethod
    async def open(
        cls, http: httpx.AsyncClient, model: Model, *, kept: Path | None = None
    ) -> Session:
        """A session on the server: the one ``kept`` holds if the server has it, else a new one."""
        if kept is not None and (earlier := remembered_session(kept)) is not None:
            found = await http.get(f"/session/{earlier}")
            if found.status_code == httpx.codes.OK:
                remember_session(kept, earlier)
                return cls(http, earlier, model, resumed=True)
        # A session opened with a title of its own is not given one by another model call.
        opened = await http.post("/session", json={"title": "engine run"})
        opened.raise_for_status()
        session_id = str(opened.json()["id"])
        if kept is not None:
            remember_session(kept, session_id)
        return cls(http, session_id, model)

    async def run(
        self, text: str, *, format: JsonObject | None = None, report: bool = False
    ) -> tuple[JsonObject, Steps]:
        """Run the agent on ``text`` to the end: its last message, and every step it took.

        With ``report``, what the agent writes and does is reported to the chat of the message
        being answered, as it happens.
        """
        steps = Steps(self.id)
        tap = current_tap() if report else None
        feed = Feed(self.id, tap) if tap is not None else None
        async with self.http.stream("GET", "/event") as stream:
            events = _events(stream.aiter_lines())
            await anext(events)
            collecting = asyncio.ensure_future(_until_idle(events, steps, feed))
            reply = await self._prompt(text, format)
            await asyncio.wait_for(collecting, timeout=_TRAILING_SECONDS)
        return reply, steps

    async def abort(self) -> None:
        """Ask the server to stop the agent's run, which makes the running prompt return."""
        stopped = await self.http.post(f"/session/{self.id}/abort")
        stopped.raise_for_status()

    async def _prompt(self, text: str, format: JsonObject | None) -> JsonObject:
        body: JsonObject = {
            "agent": "engine",
            "model": {"providerID": "engine", "modelID": self.model.id},
            "parts": [{"type": "text", "text": text}],
        }
        if format is not None:
            body["format"] = format
        answered = await self.http.post(f"/session/{self.id}/message", json=body)
        answered.raise_for_status()
        reply = answered.json()
        return reply if isinstance(reply, dict) else {}


async def _until_idle(
    events: AsyncIterator[JsonObject], steps: Steps, feed: Feed | None = None
) -> None:
    async for event in events:
        if feed is not None:
            try:
                await feed.take(event)
            except Exception:  # noqa: BLE001  (a chat that cannot be told never stops the agent)
                _LOG.warning("a chat could not be told of the agent's work", exc_info=True)
                feed = None
        if steps.take(event):
            return
