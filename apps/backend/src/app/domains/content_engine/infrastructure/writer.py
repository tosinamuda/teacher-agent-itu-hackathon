"""The app's own writer: a model that fills a draft through the same MCP tools anyone uses.

It writes and revises parts; it never submits. The engine checks the draft is complete and
submits it, so what reaches a teacher is put together by code, not by the model.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable

import dspy
from dspy.adapters.types.tool import convert_input_schema_to_tool_args
from mcp import Client
from mcp.types import TextContent, Tool

from app.infra.dspy_agent_loop import COMPLETED, run_agent_loop, termination_of
from app.shared.json_types import JsonObject

#: Tool calls the writer may make: a unit takes a write and, when a check sends it back, two
#: revisions; the rest is for reading the lesson and submitting.
_ITERATIONS_PER_UNIT, _ITERATIONS_BESIDES = 4, 8


class WriteContent(dspy.Signature):
    """Write every part of the draft with the tools: one part for each unit.

    Write for the audience in the brief and meet every requirement in it, and follow every
    skill the brief gives, each where its use_when says it applies. Each part must
    match the part schema for its unit exactly. With a source, write from the source only:
    keep its content in its own words and order, objectives included. Leave out an optional
    field the source says nothing about, and add only the least the schema and the
    requirements need where it leaves something out. Without one, write from the lesson only.
    Write one unit's part per turn: think about that unit alone, write its part in full,
    and read the tool's reply before you start the next. Call add_part once for each unit
    that has no part yet. When a tool reports an error or an issue, correct the part it names
    and send it again with revise_part. With feedback
    from the teacher, change the parts it concerns with revise_part. Finish when no unit is
    missing and no issue is left.
    """

    draft_id: str = dspy.InputField(desc="The draft every tool call names.")
    brief: dict[str, object] = dspy.InputField(
        desc="What to write, who it is for, and the requirements every part must meet."
    )
    part_schemas: dict[str, object] = dspy.InputField(
        desc="The JSON Schema a unit's part must match, by the kind of unit."
    )
    units: list[dict[str, object]] = dspy.InputField(
        desc="The units that each need one part, with the kind of each; has_part says which "
        "are written."
    )
    lesson: dict[str, object] = dspy.InputField(desc="What the lesson is and teaches.")
    source: str = dspy.InputField(
        desc="The teacher's document to write from; empty when writing from the lesson."
    )
    feedback: str = dspy.InputField(desc="The teacher's feedback to apply; empty for a new draft.")
    summary: str = dspy.OutputField(desc="One or two sentences on what you wrote or changed.")


class WriterStoppedError(RuntimeError):
    """The writer's loop ended without finishing."""


def text_of(result: object) -> str:
    content = getattr(result, "content", None) or []
    return "\n".join(block.text for block in content if isinstance(block, TextContent))


def _bridged(client: Client, tool: Tool, loop: asyncio.AbstractEventLoop) -> dspy.Tool:
    """An MCP tool the agent can call from its worker thread, on the client's own loop.

    A tool error comes back as text, so the model reads why a part was refused and fixes it.
    """
    args, arg_types, arg_desc = convert_input_schema_to_tool_args(tool.input_schema)

    def call(**arguments: object) -> str:
        future = asyncio.run_coroutine_threadsafe(client.call_tool(tool.name, arguments), loop)
        result = future.result()
        text = text_of(result)
        return f"ERROR: {text}" if result.is_error else text

    return dspy.Tool(
        call,
        name=tool.name,
        desc=tool.description or tool.name,
        args=args,
        arg_types=arg_types,
        arg_desc=arg_desc,
    )


async def run_tool_agent(
    client: Client,
    lm: dspy.BaseLM,
    signature: type[dspy.Signature],
    inputs: dict[str, object],
    *,
    max_iters: int,
    loop: Callable[..., dspy.Module] = dspy.ReActV2,
) -> dspy.Prediction:
    """Run ``signature`` as an agent over the tools ``client`` offers; refuse one that gave up."""
    listed = await client.list_tools()
    running = asyncio.get_running_loop()
    tools = [_bridged(client, tool, running) for tool in listed.tools]
    result = await run_agent_loop(loop(signature, tools=tools, max_iters=max_iters), lm, inputs)
    if termination_of(result) not in (*COMPLETED, "n/a"):
        raise WriterStoppedError(f"the writer stopped: {termination_of(result)}")
    return result


class EngineWriter:
    def __init__(self, lm: dspy.BaseLM, *, loop: Callable[..., dspy.Module] = dspy.ReActV2) -> None:
        self._lm = lm
        self._loop = loop

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        """Fill the draft through ``client``. Returns the writer's summary of what it did."""
        units = draft["units"]
        if not isinstance(units, list):
            raise WriterStoppedError("the draft names no units")
        result = await run_tool_agent(
            client,
            self._lm,
            WriteContent,
            {
                "draft_id": draft["draft_id"],
                "brief": draft["brief"],
                "part_schemas": draft["part_schemas"],
                "units": units,
                "lesson": lesson,
                "source": draft.get("source", ""),
                "feedback": feedback,
            },
            max_iters=_ITERATIONS_PER_UNIT * len(units) + _ITERATIONS_BESIDES,
            loop=self._loop,
        )
        return str(getattr(result, "summary", "") or "")
