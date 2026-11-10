"""Compose a section with the deepagents harness.

`create_deep_agent` is the framework's headline entry point and it brings a harness with
it: a todo list, a virtual filesystem (`ls`, `read_file`, `write_file`, `edit_file`,
`glob`, `grep`), an `execute` tool that refuses on the default state backend, and a `task`
tool for subagents. None of that is trimmed. The harness IS the framework's contribution,
and an arm that stripped it back to a bare tool loop would be measuring langgraph twice.
"""

from __future__ import annotations

from deepagents import create_deep_agent
from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError

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


class DeepAgentsComposeSection(FrameworkComposer):
    """`compose-v2` with deepagents' harness driving the composition tools."""

    framework = "deepagents"

    async def compose(self, *, draft: SectionDraft, instructions: str, inputs: str) -> str:
        agent = create_deep_agent(
            model=LiteLLMChatModel(),
            tools=composition_tools(draft),
            system_prompt=instructions,
        )
        try:
            await agent.ainvoke(
                {"messages": [HumanMessage(content=inputs)]},
                config=superstep_budget(self.max_iterations),
            )
        except GraphRecursionError:
            return ITERATION_LIMIT
        return SUBMITTED
