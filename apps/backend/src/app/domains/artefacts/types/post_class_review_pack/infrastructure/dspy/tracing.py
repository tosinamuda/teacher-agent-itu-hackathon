"""Capture what agentic loops actually did so a run's behaviour is readable.

The blind rounds showed the reading agents skipping material (one of ten worked
examples kept on `t3-w02`) — but nothing recorded which lines they read, so the
failure could only be inferred from its output. A trace sink makes the loop
inspectable: each agent call records its trajectory (thoughts, tool calls,
observations), and persistence writes them beside the run they explain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_SINK: list[dict[str, Any]] | None = None
_STREAM: Path | None = None


def start_capture(stream_to: Path | None = None) -> None:
    """Open a capture window, writing each entry to *stream_to* as it arrives.

    Streaming rather than only accumulating: a run killed an hour in used to lose every
    trace it had taken, along with the rows they explain. One line per entry, appended
    from the harness's single event loop, so an interrupted run leaves a readable file
    of everything that had finished — and a resumed one adds to it rather than erasing it.
    """
    global _SINK, _STREAM  # noqa: PLW0603 — one harness process, one capture window
    _SINK, _STREAM = [], stream_to
    if stream_to is not None:
        stream_to.parent.mkdir(parents=True, exist_ok=True)
        stream_to.touch()


def drain() -> list[dict[str, Any]]:
    global _SINK, _STREAM  # noqa: PLW0603
    entries, _SINK, _STREAM = _SINK or [], None, None
    return entries


def record(entry: dict[str, Any]) -> None:
    """No-op unless a capture window is open (prod paths never open one)."""
    if _SINK is None:
        return
    captured = json.loads(json.dumps(entry, default=str))
    _SINK.append(captured)
    if _STREAM is not None:
        with _STREAM.open("a", encoding="utf-8") as sink:
            sink.write(json.dumps(captured, ensure_ascii=False) + "\n")
