"""Run a DSPy agent loop, and read why it stopped."""

import asyncio

import dspy


async def run_agent_loop(
    agent: dspy.Module,
    lm: dspy.BaseLM,
    inputs: dict,
) -> dspy.Prediction:
    """Await an agent loop, threading DSPy's synchronous-only implementations."""
    with dspy.settings.context(lm=lm):
        if hasattr(agent, "aforward"):
            return await agent.acall(**inputs)
        return await asyncio.to_thread(agent, **inputs)


# ReActV2 does NOT raise on a failed turn: it catches AdapterParseError, breaks, and
# returns a Prediction carrying only ``termination_reason``. The composing tools write
# into the draft as they go, so a truncated loop still yields a section — a silently
# short one. Anything but a submit means the loop gave up.
COMPLETED = ("submit", "forced_submit")


def termination_of(result: object) -> str:
    """Why the agent loop stopped. ``submit`` means it finished on purpose."""
    return getattr(result, "termination_reason", "") or "n/a"


def trajectory_of(result: object) -> object:
    """The loop's step record, whatever the engine calls it."""
    return getattr(result, "trajectory", None) or getattr(result, "history", None)
