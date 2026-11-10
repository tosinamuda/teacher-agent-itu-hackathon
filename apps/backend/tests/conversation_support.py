"""Writers for conversation tests: one revises a unit at each message, one keeps its agent."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp import Client

from app.shared.json_types import JsonObject
from tests.content_engine_support import part


class Messages:
    """A writer that revises one unit to the next title in its list at each message."""

    def __init__(self, titles: list[tuple[str, str]]) -> None:
        self.titles = titles
        self.heard: list[str] = []

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        self.heard.append(feedback)
        unit, title = self.titles[len(self.heard) - 1]
        await client.call_tool(
            "revise_part", {"draft_id": draft["draft_id"], "unit_id": unit, "part": part(title)}
        )
        return f"Changed {unit}."


class Kept(Messages):
    """A writer that keeps its agent: it is opened once for the conversation and closed once.

    With ``resumed`` its agent is one an earlier conversation opened, already briefed.
    """

    def __init__(self, titles: list[tuple[str, str]], *, resumed: bool = False) -> None:
        super().__init__(titles)
        self.events: list[str] = []
        self.keys: list[str] = []
        self.briefed = resumed

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        summary = await super().write(client, draft, lesson, feedback=feedback)
        self.briefed = True
        return summary

    @asynccontextmanager
    async def keep(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, key: str
    ) -> AsyncIterator[Kept]:
        self.events.append("opened")
        self.keys.append(key)
        try:
            yield self
        finally:
            self.events.append("closed")
