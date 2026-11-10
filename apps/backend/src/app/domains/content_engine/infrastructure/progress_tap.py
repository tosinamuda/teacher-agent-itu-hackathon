"""What the agent says and does, as chat events a page can show while the work has no chat yet.

A lesson plan's chat exists once the plan does. Until then the page follows the work through a
progress channel, which the job's process writes and the API reads, as other jobs' progress is.
The events are the ones the chat keeps, so the page draws them as the chat does.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from app.domains.content_engine.infrastructure.tap import AgentChatEvent
from app.infra import progress
from app.shared.json_types import JsonObject

#: The events the chat page draws: what the agent says and thinks, and the tools it uses.
SHOWN = frozenset({"agent_text", "thinking", "tool"})


@dataclass(frozen=True)
class ProgressTap:
    channel: str

    async def emit(self, event: AgentChatEvent) -> None:
        if event.kind in SHOWN:
            await self._publish({"kind": event.kind, "data": event.data})

    async def start(self) -> None:
        await self._publish({"kind": "start", "data": {}})

    async def _publish(self, payload: JsonObject) -> None:
        await asyncio.to_thread(progress.publish, self.channel, payload)
