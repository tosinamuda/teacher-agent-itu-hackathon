"""An OpenAI-compatible chat endpoint on localhost, answering from a script.

The harnesses reach a model over HTTP, whether in this process or in a subprocess, so the
stand-in is a real server. It keeps every request, which is what a harness actually sent.
"""

from __future__ import annotations

import json
import socket
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.routing import Route

Reply = Callable[[dict[str, Any]], dict[str, Any]]
USAGE = {"prompt_tokens": 120, "completion_tokens": 30, "total_tokens": 150}


def tool_call(
    name: str, arguments: dict[str, Any] | str, call_id: str = "call-1"
) -> dict[str, Any]:
    """An assistant turn that calls one tool; arguments given as text are sent as they are."""
    text = arguments if isinstance(arguments, str) else json.dumps(arguments)
    function = {"name": name, "arguments": text}
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [{"id": call_id, "type": "function", "function": function}],
    }


def answer(text: str) -> dict[str, Any]:
    return {"role": "assistant", "content": text}


def _completion(body: dict[str, Any], message: dict[str, Any]) -> dict[str, Any]:
    finish = "tool_calls" if message.get("tool_calls") else "stop"
    choice = {"index": 0, "message": message, "finish_reason": finish}
    return {
        "id": "stub",
        "object": "chat.completion",
        "created": 0,
        "model": body["model"],
        "choices": [choice],
        "usage": USAGE,
    }


def _chunks(completion: dict[str, Any]) -> Iterator[str]:
    """The completion as a stream: one delta with all of it, then the usage."""
    message = dict(completion["choices"][0]["message"])
    for index, call in enumerate(message.get("tool_calls") or []):
        call["index"] = index
    base = {key: completion[key] for key in ("id", "created", "model")} | {
        "object": "chat.completion.chunk"
    }
    choice = {
        "index": 0,
        "delta": message,
        "finish_reason": completion["choices"][0]["finish_reason"],
    }
    yield f"data: {json.dumps(base | {'choices': [choice]})}\n\n"
    yield f"data: {json.dumps(base | {'choices': [], 'usage': USAGE})}\n\n"
    yield "data: [DONE]\n\n"


class StubModel:
    def __init__(self, reply: Reply) -> None:
        self.requests: list[dict[str, Any]] = []
        self._reply = reply

    async def chat(self, request: Request) -> Response:
        body = await request.json()
        self.requests.append(body)
        completion = _completion(body, self._reply(body))
        if body.get("stream"):
            return StreamingResponse(_chunks(completion), media_type="text/event-stream")
        return JSONResponse(completion)


@contextmanager
def stub_model(reply: Reply) -> Iterator[tuple[StubModel, str]]:
    """The stub, and its base URL, served for the length of the block."""
    model = StubModel(reply)
    app = Starlette(routes=[Route("/v1/chat/completions", model.chat, methods=["POST"])])
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    server = uvicorn.Server(uvicorn.Config(app, log_level="error"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.01)
    try:
        yield model, f"http://127.0.0.1:{sock.getsockname()[1]}/v1"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
