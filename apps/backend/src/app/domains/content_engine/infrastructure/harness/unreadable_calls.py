"""A tool call the model wrote with arguments that are not JSON, sent back to it as a refusal.

LangChain keeps such a call apart from the calls it can run, and its agent loop ends on a
turn with nothing to run: the writer stopped there, silently, with the revision it meant
to make unsent. The DSPy writer's model is told when a call fails, so this one is too.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain_core.messages import AIMessage, InvalidToolCall, ToolMessage
from langgraph.runtime import Runtime


def _refusal(call: InvalidToolCall) -> ToolMessage:
    name = call.get("name") or "the tool"
    return ToolMessage(
        content=f"ERROR: the arguments of {name} are not valid JSON: {call.get('error')}",
        tool_call_id=call.get("id") or "",
        name=name,
        status="error",
    )


State = TypeVar("State", bound=AgentState[Any])


class RefuseUnreadableCalls(AgentMiddleware[State, None], Generic[State]):
    """Works on any agent's state, so it stacks with middleware that extends the state."""

    @hook_config(can_jump_to=["model"])
    def after_model(self, state: State, runtime: Runtime[None]) -> dict[str, Any] | None:
        last = state["messages"][-1]
        if not isinstance(last, AIMessage) or not last.invalid_tool_calls:
            return None
        refusals = [_refusal(call) for call in last.invalid_tool_calls]
        # Calls it can run still go to the tools; with none, the model reads its refusals.
        return (
            {"messages": refusals}
            if last.tool_calls
            else {"messages": refusals, "jump_to": "model"}
        )
