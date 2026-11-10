"""Compose a section with a langgraph state graph.

The loop is written out rather than taken from `langgraph.prebuilt.create_react_agent`,
which is deprecated in langgraph 1.0 and now lives in `langchain.agents`. Calling it would
record a langgraph run that langchain actually drove, and a harness that misnames what
produced it is the failure this package exists to prevent. `ToolNode` and `tools_condition`
are langgraph's own and are used as they are.
"""

from __future__ import annotations

from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.section_draft import (  # noqa: E501
    SectionDraft,
    composition_tools,
)
from experiments.h1_condition_eval.frameworks.chat_model import LiteLLMChatModel
from experiments.h1_condition_eval.frameworks.composer import (
    ITERATION_LIMIT,
    SUBMITTED,
    FrameworkComposer,
    superstep_budget,
)


class LangGraphComposeSection(FrameworkComposer):
    """`compose-v2` with a langgraph model/tools cycle in place of dspy's ReActV2."""

    framework = "langgraph"

    async def compose(self, *, draft: SectionDraft, instructions: str, inputs: str) -> str:
        graph = _cycle(composition_tools(draft))
        opening: list[BaseMessage] = [
            SystemMessage(content=instructions),
            HumanMessage(content=inputs),
        ]
        try:
            await graph.ainvoke({"messages": opening}, config=superstep_budget(self.max_iterations))
        except GraphRecursionError:
            # dspy stops at max_iters and returns what the tools wrote; a raise here would
            # score a long composition as a dud rather than as a truncated one.
            return ITERATION_LIMIT
        return SUBMITTED


def _cycle(tools: list[Any]) -> CompiledStateGraph:
    """Model, then tools, then the model again until it calls none."""
    model = LiteLLMChatModel().bind_tools(tools)

    async def call_model(state: MessagesState) -> dict[str, list[BaseMessage]]:
        return {"messages": [await model.ainvoke(state["messages"])]}

    builder = StateGraph(MessagesState)
    builder.add_node("model", call_model)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "model")
    builder.add_conditional_edges("model", tools_condition, {"tools": "tools", END: END})
    builder.add_edge("tools", "model")
    return builder.compile()
