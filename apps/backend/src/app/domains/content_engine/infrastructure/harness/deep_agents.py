"""The writer and checker on DeepAgents: LangGraph's agent loop with native tool calls.

DeepAgents gives every agent file-system tools and a subagent tool. They are taken out, so
the model is offered exactly the DSPy writer's tools and the loop is the only difference.
"""

from __future__ import annotations

import typing
from collections.abc import Sequence
from typing import Any

from deepagents import (
    FsToolName,
    GeneralPurposeSubagentProfile,
    HarnessProfile,
    create_deep_agent,
    register_harness_profile,
)
from langchain.agents.middleware import AgentMiddleware, ModelCallLimitMiddleware
from langchain.agents.middleware.model_call_limit import (
    ModelCallLimitExceededError,
    ModelCallLimitState,
)
from langchain.agents.middleware.types import InputAgentState
from langchain.agents.structured_output import ToolStrategy
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.errors import GraphRecursionError
from mcp import Client
from mcp.types import Tool

from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.harness.brief import (
    CHECKER_PROMPT,
    CHECKER_STEPS,
    WRITER_PROMPT,
    Verdict,
    answer_again,
    checker_message,
    refusal,
    turns_for,
    verdict_of,
    writer_message,
    written_answer,
)
from app.domains.content_engine.infrastructure.harness.unreadable_calls import RefuseUnreadableCalls
from app.domains.content_engine.infrastructure.writer import (
    WriterStoppedError,
    text_of,
)
from app.shared.json_types import JsonObject

#: DeepAgents' own tools, none of which the DSPy writer has.
BUILT_IN_TOOLS = frozenset({*typing.get_args(FsToolName), "task", "write_todos"})


def _only_our_tools(model: ChatOpenAI) -> None:
    register_harness_profile(
        f"openai:{model.model_name}",
        HarnessProfile(
            excluded_tools=BUILT_IN_TOOLS,
            general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False),
        ),
    )


def _bridged(client: Client, tool: Tool) -> StructuredTool:
    """An MCP tool as LangChain calls it; a refusal comes back as text the model can fix."""

    async def call(**arguments: object) -> str:
        result = await client.call_tool(tool.name, dict(arguments))
        text = text_of(result)
        return f"ERROR: {text}" if result.is_error else text

    return StructuredTool(
        name=tool.name,
        description=tool.description or tool.name,
        args_schema=tool.input_schema,
        coroutine=call,
    )


class DeepAgentsWriter:
    def __init__(self, model: ChatOpenAI, callbacks: Sequence[BaseCallbackHandler] = ()) -> None:
        """``callbacks`` see every model call, such as a log of its tokens."""
        _only_our_tools(model)
        self._model = model
        self._config: RunnableConfig = {"callbacks": list(callbacks)}

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        """Fill the draft through ``client``. Returns the writer's summary of what it did."""
        listed = await client.list_tools()
        tools: list[BaseTool] = [_bridged(client, t) for t in listed.tools]
        middleware: list[AgentMiddleware[ModelCallLimitState[None], None]] = [
            ModelCallLimitMiddleware(run_limit=turns_for(draft), exit_behavior="error"),
            RefuseUnreadableCalls[ModelCallLimitState[None]](),
        ]
        agent = create_deep_agent(
            self._model, tools, system_prompt=WRITER_PROMPT, middleware=middleware
        )
        message = HumanMessage(writer_message(draft, lesson, feedback))
        try:
            result = await agent.ainvoke({"messages": [message]}, self._config)
        except (ModelCallLimitExceededError, GraphRecursionError) as error:
            raise WriterStoppedError(f"the writer stopped: {error}") from error
        last = result["messages"][-1]
        return last.text if isinstance(last, AIMessage) else ""


class DeepAgentsChecker:
    def __init__(self, model: ChatOpenAI, callbacks: Sequence[BaseCallbackHandler] = ()) -> None:
        """``callbacks`` see every model call, such as a log of its tokens."""
        _only_our_tools(model)
        self._model = model
        self._config: RunnableConfig = {"callbacks": list(callbacks)}

    async def _answer(self, messages: list[AnyMessage], calls: int) -> dict[str, Any]:
        """One run of the checker's agent on ``messages``, with at most ``calls`` model calls."""
        limit = ModelCallLimitMiddleware(run_limit=calls, exit_behavior="error")
        agent = create_deep_agent(
            self._model,
            [],
            system_prompt=CHECKER_PROMPT,
            response_format=ToolStrategy(Verdict),
            middleware=(limit,),
        )
        try:
            state: InputAgentState = {"messages": [*messages]}
            result = await agent.ainvoke(state, self._config)
        except ModelCallLimitExceededError as error:
            raise CheckerStoppedError(f"the checker gave no valid answer: {error}") from error
        if not isinstance(result, dict):
            raise CheckerStoppedError(f"the checker's agent returned {type(result).__name__}")
        return result

    async def errors(
        self, brief: JsonObject, unit: dict[str, object], part: JsonObject
    ) -> list[str]:
        """The part's real errors; empty when it has none.

        gpt-oss can ignore the required answer tool and write its answer as text, which the
        tool never sees to send back; so an answer the schema refuses is sent back here.
        """
        result = await self._answer(
            [HumanMessage(checker_message(brief, unit, part))], CHECKER_STEPS
        )
        verdict = result.get("structured_response")
        if isinstance(verdict, Verdict):
            return verdict_of(verdict.model_dump())
        used = sum(isinstance(m, AIMessage) for m in result["messages"])
        reason = refusal(_written(result))
        if reason is not None and used < CHECKER_STEPS:
            asked = [*result["messages"], HumanMessage(answer_again(reason))]
            result = await self._answer(asked, CHECKER_STEPS - used)
            verdict = result.get("structured_response")
            if isinstance(verdict, Verdict):
                return verdict_of(verdict.model_dump())
        return verdict_of(_written(result))


def _written(result: dict[str, Any]) -> object:
    """The answer the model wrote as text in its last message."""
    messages = result.get("messages")
    last = messages[-1] if isinstance(messages, list) and messages else None
    return written_answer(last.text) if isinstance(last, AIMessage) else None
