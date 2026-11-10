"""A langchain chat model that makes the dspy arms' litellm call.

langgraph and deepagents drive a `BaseChatModel`, and nothing installed here speaks
OpenRouter: `langchain-openai` is absent, and `langchain-litellm` requires litellm >= 1.97
against the 1.82.6 every pack in this study was generated on. Adopting it would move the
transport under the dspy arms too — a change to the thing being held constant, and the
exact shape of the failure `harness.py` exists to catch.

So the model is the pinned litellm behind the interface langchain expects: messages in
OpenAI form, tools in OpenAI form, the reply back as an `AIMessage`.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from typing import Any

import litellm
from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    InvalidToolCall,
    ToolCall,
    convert_to_openai_messages,
)
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import Field

from experiments.h1_condition_eval.frameworks.provider import litellm_request


class LiteLLMChatModel(BaseChatModel):
    """The study's model, reached the way `build_dspy_lm` reaches it."""

    request: dict[str, Any] = Field(default_factory=litellm_request)

    @property
    def _llm_type(self) -> str:
        return "litellm"

    def bind_tools(
        self,
        tools: Sequence[dict[str, Any] | type | Callable[..., Any] | BaseTool],
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, AIMessage]:
        """Bind tools in OpenAI form, which is the form litellm forwards to the provider."""
        chosen = {"tool_choice": tool_choice} if tool_choice else {}
        return self.bind(tools=[convert_to_openai_tool(tool) for tool in tools], **chosen, **kwargs)

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        return _as_result(litellm.completion(**self._payload(messages, stop, kwargs)))

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        return _as_result(await litellm.acompletion(**self._payload(messages, stop, kwargs)))

    def _payload(
        self, messages: list[BaseMessage], stop: list[str] | None, bound: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            **self.request,
            **bound,
            "messages": convert_to_openai_messages(messages),
            **({"stop": stop} if stop else {}),
        }


def _as_result(response: Any) -> ChatResult:
    return ChatResult(generations=[ChatGeneration(message=_as_message(response))])


def _as_message(response: Any) -> AIMessage:
    """The provider's reply as langchain reads it, with unparseable calls kept as such.

    A malformed `arguments` string is handed back as an `InvalidToolCall` rather than
    raised: langgraph returns it to the model as a tool error and the loop recovers, where
    an exception would score the draw a dud on one bad JSON fragment.
    """
    reply = response.choices[0].message
    calls: list[ToolCall] = []
    invalid: list[InvalidToolCall] = []
    for call in reply.tool_calls or []:
        arguments = _parsed(call.function.arguments)
        if arguments is None:
            invalid.append(
                InvalidToolCall(
                    name=call.function.name,
                    args=call.function.arguments,
                    id=call.id,
                    error="arguments are not a JSON object",
                    type="invalid_tool_call",
                )
            )
        else:
            calls.append(
                ToolCall(name=call.function.name, args=arguments, id=call.id, type="tool_call")
            )
    return AIMessage(content=reply.content or "", tool_calls=calls, invalid_tool_calls=invalid)


def _parsed(arguments: str | None) -> dict[str, Any] | None:
    try:
        loaded = json.loads(arguments or "{}")
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, dict) else None
