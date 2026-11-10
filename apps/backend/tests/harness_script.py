"""A model's replies to a harness writing the engine's draft, whatever the harness names tools.

The writer adds each part in turn, one refused by the part schema first, and then answers;
a checker, offered only its answer tool, finds no errors.
"""

from __future__ import annotations

import re
from typing import Any

from tests.content_engine_support import part
from tests.openai_stub import Reply, answer, tool_call

#: The unit and part each writer turn sends: the first part lacks its examples.
TURNS: list[tuple[str, dict[str, Any]]] = [
    ("s1", {"title": "No examples"}),
    ("s1", part("A")),
    ("s2", part("B")),
]
SUMMARY = "Wrote both steps."
#: The call id of a writer's load of a skill, which is not one of its writes.
SKILL_CALL = "call-skill"


def _tools(body: dict[str, Any]) -> list[str]:
    return [tool["function"]["name"] for tool in body.get("tools") or []]


def message_text(message: dict[str, Any]) -> str:
    """A message's text, whether its content is a string or a list of text parts."""
    content = message.get("content")
    if isinstance(content, list):
        return "".join(str(part.get("text", "")) for part in content if isinstance(part, dict))
    return str(content)


def _draft_id(body: dict[str, Any]) -> str:
    text = " ".join(message_text(message) for message in body["messages"])
    found = re.search(r"## draft_id\s+(\S+)", text)
    assert found, "the writer's message names no draft"
    return found.group(1)


def _write(body: dict[str, Any], add_part: str) -> dict[str, Any]:
    done = sum(
        message["role"] == "tool" and message.get("tool_call_id") != SKILL_CALL
        for message in body["messages"]
    )
    if done >= len(TURNS):
        return answer(SUMMARY)
    unit_id, attempt = TURNS[done]
    arguments = {"draft_id": _draft_id(body), "unit_id": unit_id, "part": attempt}
    return tool_call(add_part, arguments, call_id=f"call-{done}")


def engine_script() -> Reply:
    def reply(body: dict[str, Any]) -> dict[str, Any]:
        tools = _tools(body)
        add_part = next((name for name in tools if name.endswith("add_part")), None)
        if add_part is not None:
            return _write(body, add_part)
        return tool_call(tools[0], {"errors": []})

    return reply


def skill_first(skill: str) -> Reply:
    """The engine script for a writer that loads ``skill`` with its skill tool before writing."""
    script = engine_script()

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        tools = _tools(body)
        loaded = any(message.get("tool_call_id") == SKILL_CALL for message in body["messages"])
        skill_tool = next((name for name in tools if name == "skill"), None)
        if skill_tool is not None and not loaded:
            return tool_call(skill_tool, {"name": skill}, call_id=SKILL_CALL)
        return script(body)

    return reply


def reads_skill_first() -> Reply:
    """The engine script for a writer that reads the skill file its prompt lists, then writes."""
    script = engine_script()

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        loaded = any(message.get("tool_call_id") == SKILL_CALL for message in body["messages"])
        system = " ".join(message_text(m) for m in body["messages"] if m["role"] == "system")
        listed = re.search(r"<location>(.+?)</location>", system)
        if listed and "read" in _tools(body) and not loaded:
            return tool_call("read", {"path": listed.group(1)}, call_id=SKILL_CALL)
        return script(body)

    return reply


def reads_reference_first(reference: str) -> Reply:
    """The engine script for a writer that reads a skill's reference file, then writes.

    The file is found beside the skill file its prompt lists, with whatever name the harness
    gives the path argument of its ``read`` tool.
    """
    script = engine_script()

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        loaded = any(message.get("tool_call_id") == SKILL_CALL for message in body["messages"])
        system = " ".join(message_text(m) for m in body["messages"] if m["role"] == "system")
        listed = re.search(r"<location>(.+?)/SKILL\.md</location>", system)
        reader = next(
            (t["function"] for t in body.get("tools", []) if t["function"]["name"] == "read"), None
        )
        if listed and reader and not loaded:
            argument = "filePath" if "filePath" in reader["parameters"]["properties"] else "path"
            return tool_call(
                "read", {argument: f"{listed.group(1)}/{reference}"}, call_id=SKILL_CALL
            )
        return script(body)

    return reply


def calls_first(tool: str, arguments: dict[str, Any]) -> Reply:
    """The engine script for a writer that calls ``tool`` once, if it is offered, then writes."""
    script = engine_script()

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        called = any(message.get("tool_call_id") == SKILL_CALL for message in body["messages"])
        if tool in _tools(body) and not called:
            return tool_call(tool, arguments, call_id=SKILL_CALL)
        return script(body)

    return reply


def tool_replies(requests: list[dict[str, Any]]) -> list[str]:
    """Every tool result the harness sent back to the model, in order, once each."""
    seen: list[str] = []
    for body in requests:
        for message in body["messages"]:
            content = message.get("content")
            text = content if isinstance(content, str) else str(content)
            if message["role"] == "tool" and text not in seen:
                seen.append(text)
    return seen
