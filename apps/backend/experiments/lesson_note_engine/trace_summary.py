"""A traced draft, to read: what each call sent and what came back, a stream reassembled."""

from __future__ import annotations

import json
import re

from app.shared.json_types import JsonObject, JsonValue
from experiments.lesson_note_engine.wire import Exchange

_SHOWN = 400
#: The part schemas in a message, as a harness sends them or as DSPy's adapter writes them.
_SCHEMAS = re.compile(
    r"(?:## part_schemas|\[\[ ## part_schemas ## \]\])\n(.*?)(?:\n\n(?:## |\[\[ )|\Z)", re.DOTALL
)
_TEXT_CALLS = "[[ ## tool_calls ## ]]"
#: How a refusal starts, as each loop words it: dsh puts "Error: " before the server's text.
_REFUSED = ("ERROR", "Error executing", "Error: Error executing")


def _cut(text: str, limit: int = _SHOWN) -> str:
    return text if len(text) <= limit else f"{text[:limit]}… ({len(text)} characters)"


def _objects(value: JsonValue | None) -> list[JsonObject]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _object(value: JsonValue | None) -> JsonObject:
    return value if isinstance(value, dict) else {}


def _streamed(raw: str) -> JsonObject:
    """A streamed reply put back together: its text, reasoning, tool calls and usage."""
    text, reasoning, usage = "", "", None
    calls: dict[int, JsonObject] = {}
    for line in raw.splitlines():
        data = line.removeprefix("data:").strip()
        if not line.startswith("data:") or data == "[DONE]":
            continue
        chunk = json.loads(data)
        usage = chunk.get("usage") or usage
        for choice in chunk.get("choices") or []:
            delta = choice.get("delta") or {}
            text += delta.get("content") or ""
            reasoning += delta.get("reasoning_content") or delta.get("reasoning") or ""
            for call in delta.get("tool_calls") or []:
                kept = calls.setdefault(call.get("index", 0), {"name": "", "arguments": ""})
                function = call.get("function") or {}
                kept["name"] = f"{kept['name']}{function.get('name') or ''}"
                kept["arguments"] = f"{kept['arguments']}{function.get('arguments') or ''}"
    return {
        "content": text,
        "reasoning": reasoning,
        "tool_calls": list(calls.values()),
        "usage": usage,
    }


def reply(raw: str) -> JsonObject:
    """What came back for one call, streamed or not."""
    if raw.lstrip().startswith("data:"):
        return _streamed(raw)
    body = json.loads(raw)
    message = (body.get("choices") or [{}])[0].get("message") or {}
    calls = [call.get("function") or {} for call in message.get("tool_calls") or []]
    reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    return {
        "content": message.get("content") or "",
        "reasoning": reasoning,
        "tool_calls": calls,
        "usage": body.get("usage"),
    }


def _sent(request: JsonObject) -> list[str]:
    messages = _objects(request.get("messages"))
    system = next((str(m.get("content")) for m in messages if m.get("role") == "system"), "")
    tools = [str(_object(t.get("function")).get("name")) for t in _objects(request.get("tools"))]
    params = {key: request[key] for key in request if key not in ("messages", "tools")}
    return [
        f"- system: {_cut(system.splitlines()[0] if system else '(none)', 120)}",
        f"- tools offered: {tools or 'none'}",
        f"- other parameters: {json.dumps(params)}",
    ]


def _call(call: JsonObject) -> str:
    """A native call, flagged when its arguments are not JSON and so cannot be run."""
    arguments = str(call.get("arguments"))
    try:
        json.loads(arguments)
        readable = ""
    except json.JSONDecodeError as error:
        readable = f" (NOT valid JSON: {error})"
    return f"`{call.get('name')}` {_cut(arguments, 300)}{readable}"


def _answered(exchange: Exchange) -> list[str]:
    if exchange.status != 200:
        return [f"- HTTP {exchange.status}: {_cut(exchange.response)}"]
    got = reply(exchange.response)
    written = _TEXT_CALLS in str(got["content"])
    calls = [_call(call) for call in _objects(got["tool_calls"])]
    return [
        f"- native tool calls: {calls or 'none'}",
        f"- tool calls written as text: {'yes' if written else 'no'}",
        f"- text: {_cut(str(got['content'])) or '(none)'}",
        f"- reasoning returned: {len(str(got['reasoning']))} characters",
        f"- usage: {json.dumps(got['usage'])}",
    ]


def _refusals(exchanges: list[Exchange]) -> list[str]:
    """Each tool result that refused a call, once, as the model was sent it."""
    seen: list[str] = []
    for exchange in exchanges:
        for message in _objects(exchange.request.get("messages")):
            content = str(message.get("content"))
            if (
                message.get("role") == "tool"
                and content.startswith(_REFUSED)
                and content not in seen
            ):
                seen.append(content)
    return [f"- {_cut(text, 1500)}" for text in seen] or ["- none"]


def _first_schemas(exchanges: list[Exchange]) -> str:
    for exchange in exchanges:
        for message in _objects(exchange.request.get("messages")):
            found = _SCHEMAS.search(str(message.get("content")))
            if message.get("role") == "user" and found:
                return found.group(1)
    return "(no part schema was sent)"


def _add_part(exchanges: list[Exchange]) -> str:
    for exchange in exchanges:
        for tool in _objects(exchange.request.get("tools")):
            function = _object(tool.get("function"))
            if str(function.get("name")).endswith("add_part"):
                return json.dumps(function, indent=1)
    return "(no native tools: DSPy's adapter describes the tools in the prompt instead)"


def summary(exchanges: list[Exchange]) -> str:
    lines = [f"# Trace: {len(exchanges)} calls", "", "## The part schema as sent", "", "```json"]
    lines += [_first_schemas(exchanges), "```", "", "## add_part as offered", "", "```json"]
    lines += [_add_part(exchanges), "```", "", "## Refusals sent back to the model", ""]
    lines += [*_refusals(exchanges), ""]
    for number, exchange in enumerate(exchanges, start=1):
        lines += [f"## Call {number}", "", *_sent(exchange.request), *_answered(exchange), ""]
    return "\n".join(lines)
