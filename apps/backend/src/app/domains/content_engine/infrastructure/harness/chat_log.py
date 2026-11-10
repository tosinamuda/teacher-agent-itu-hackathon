"""Every LangChain chat-model call a harness makes, written to the generation log."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any
from uuid import UUID

from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.messages import BaseMessage, messages_to_dict
from langchain_core.outputs import ChatGeneration, LLMResult

from app.domains.generation_log.application.recorder import Generation, GenerationLog, current_tags


@dataclass
class _Started:
    request: dict[str, Any]
    tags: dict[str, Any]
    started_at: float = field(default_factory=perf_counter)

    def elapsed_ms(self) -> float:
        return round((perf_counter() - self.started_at) * 1000, 1)


def _reply(result: LLMResult) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """The reply, and the tokens the provider says it cost."""
    generation = result.generations[0][0] if result.generations else None
    if not isinstance(generation, ChatGeneration):
        return {}, None
    message = generation.message
    usage = message.response_metadata.get("token_usage") or getattr(message, "usage_metadata", None)
    reported = {name: count for name, count in dict(usage or {}).items() if count is not None}
    return {"completions": messages_to_dict([message])}, reported or None


class ChatModelLog(AsyncCallbackHandler, GenerationLog):
    """Records each chat-model call under the log tags active when it started."""

    def __init__(self, model: str) -> None:
        self._model = model
        self._calls: dict[UUID, _Started] = {}

    async def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        request = {"messages": [messages_to_dict(batch) for batch in messages]}
        self._calls[run_id] = _Started(request, current_tags())

    async def on_llm_end(self, response: LLMResult, *, run_id: UUID, **kwargs: Any) -> None:
        started = self._calls.pop(run_id, None)
        if started is not None:
            reply, usage = _reply(response)
            self._record(started, reply, usage)

    async def on_llm_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> None:
        started = self._calls.pop(run_id, None)
        if started is not None:
            self._record(started, {"error": str(error)}, None)

    def _record(
        self, started: _Started, response: dict[str, Any], usage: dict[str, Any] | None
    ) -> None:
        self.record(
            Generation(
                self._model, started.tags, started.request, response, started.elapsed_ms(), usage
            )
        )
