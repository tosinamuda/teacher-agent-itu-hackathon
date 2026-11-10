"""OpenCode's events, as what a chat shows: the agent's text as it is written, and its tools.

OpenCode reports each part of a message as it changes. A text part grows by deltas and is
done when it has an end time; a tool part goes from pending to completed or failed. The
user's own message arrives as events too, and is left out. The model's reasoning is a part of
its own: its deltas arrive as text, but it is kept apart from the agent's reply as ``thinking``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domains.content_engine.infrastructure import tap as taps
from app.domains.content_engine.infrastructure.harness.opencode_observation import observation
from app.domains.content_engine.infrastructure.tap import Tap
from app.shared.json_types import JsonObject

#: The tools of the engine's own server arrive named ``engine_<tool>``.
TOOL_PREFIX = "engine_"
#: What of a tool's input a chat shows: where in the content it worked, not the part it wrote.
_SHOWN = ("unit_id", "draft_id", "content_id")


#: Where the files a run is given sit in its workspace.
_SKILL_FILES = ".agents/skills/"


def _detail(name: str, given: JsonObject) -> JsonObject:
    """The one thing a tool names that a person understands: the skill, or the file it read."""
    if name == "skill" and isinstance(given.get("name"), str):
        return {"detail": given["name"]}
    path = given.get("filePath") or given.get("path")
    if name == "read" and isinstance(path, str):
        return {"detail": path.partition(_SKILL_FILES)[2] or path.rsplit("/", 1)[-1]}
    return {}


def _object(value: object) -> JsonObject:
    return {str(key): item for key, item in value.items()} if isinstance(value, dict) else {}


def _called(part: JsonObject) -> tuple[str, JsonObject, JsonObject]:
    """A tool part's name, its state, and what of its input a chat shows."""
    state = _object(part.get("state"))
    name = str(part.get("tool")).removeprefix(TOOL_PREFIX)
    given = _object(state.get("input"))
    shown = {key: given[key] for key in _SHOWN if isinstance(given.get(key), str)}
    return name, state, shown | _detail(name, given)


def working_on(part: JsonObject) -> JsonObject:
    """What a chat shows of a tool that has started."""
    name, _, shown = _called(part)
    return {"tool": name, **shown}


def finished_tool(part: JsonObject) -> JsonObject | None:
    """What a chat shows of a tool that has completed or failed; none while it is still running."""
    name, state, shown = _called(part)
    status = str(state.get("status"))
    if status not in ("completed", "error"):
        return None
    found = observation(name, state)
    return {"tool": name, "status": status, **shown, **({"observed": found} if found else {})}


@dataclass
class Feed:
    """The events of one session, turned into chat events for the tap of the running message."""

    session_id: str
    tap: Tap
    _roles: dict[str, str] = field(default_factory=dict)
    _texts: dict[str, str] = field(default_factory=dict)
    _message_of: dict[str, str] = field(default_factory=dict)
    _said: set[str] = field(default_factory=set)
    _reasoning: set[str] = field(default_factory=set)
    _thoughts: dict[str, str] = field(default_factory=dict)
    _tools: set[str] = field(default_factory=set)

    async def take(self, event: JsonObject) -> None:
        properties = _object(event.get("properties"))
        if properties.get("sessionID") != self.session_id:
            return
        kind = event.get("type")
        if kind == "message.updated":
            info = _object(properties.get("info"))
            self._roles[str(info.get("id"))] = str(info.get("role"))
        elif kind == "message.part.updated":
            await self._part(_object(properties.get("part")))
        elif kind == "message.part.delta":
            await self._delta(properties)
        elif kind == "session.status":
            status = _object(properties.get("status")).get("type")
            await self._send("status", {"working": status == "busy"})
            if status == "idle":
                await self._flush()

    async def _send(self, kind: str, data: JsonObject) -> None:
        await self.tap.emit(taps.AgentChatEvent(kind, data))

    async def _part(self, part: JsonObject) -> None:
        part_id, message_id = str(part.get("id")), str(part.get("messageID"))
        if self._roles.get(message_id) == "user":
            return
        kind = part.get("type")
        if kind == "text":
            self._message_of[part_id] = message_id
            text = str(part.get("text") or self._texts.get(part_id, ""))
            self._texts[part_id] = text
            if _object(part.get("time")).get("end") is not None:
                await self._say(part_id)
            elif text:
                await self._send("partial", {"part_id": part_id, "text": text})
        elif kind == "reasoning":
            self._reasoning.add(part_id)
            self._texts.pop(part_id, None)
            if part_id not in self._said:
                self._thoughts[part_id] = str(part.get("text") or self._thoughts.get(part_id, ""))
            if _object(part.get("time")).get("end") is not None:
                await self._think(part_id)
        elif kind == "tool":
            await self._tool(part, part_id)
        elif kind == "step-finish":
            await self._flush(message_id)

    async def _delta(self, properties: JsonObject) -> None:
        part_id, message_id = str(properties.get("partID")), str(properties.get("messageID"))
        if self._roles.get(message_id) == "user" or properties.get("field") != "text":
            return
        if part_id in self._reasoning:
            self._thoughts[part_id] = self._thoughts.get(part_id, "") + str(
                properties.get("delta") or ""
            )
            return
        if part_id in self._said:
            return
        self._message_of.setdefault(part_id, message_id)
        text = self._texts.get(part_id, "") + str(properties.get("delta") or "")
        self._texts[part_id] = text
        await self._send("partial", {"part_id": part_id, "text": text})

    async def _tool(self, part: JsonObject, part_id: str) -> None:
        if str(_object(part.get("state")).get("status")) in ("pending", "running"):
            await self._send("working_on", working_on(part))
            return
        data = finished_tool(part)
        if data is not None and part_id not in self._tools:
            self._tools.add(part_id)
            await self._send("tool", data)

    async def _say(self, part_id: str) -> None:
        text = self._texts.get(part_id, "").strip()
        if part_id in self._said or not text:
            return
        self._said.add(part_id)
        await self._send("agent_text", {"part_id": part_id, "text": text})

    async def _think(self, part_id: str) -> None:
        text = self._thoughts.pop(part_id, "").strip()
        if text and part_id not in self._said:
            self._said.add(part_id)
            await self._send("thinking", {"part_id": part_id, "text": text})

    async def _flush(self, message_id: str | None = None) -> None:
        for part_id in list(self._texts):
            if message_id is None or self._message_of.get(part_id) == message_id:
                await self._say(part_id)
        for part_id in list(self._thoughts):
            await self._think(part_id)
