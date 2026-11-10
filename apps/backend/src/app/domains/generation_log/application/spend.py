"""What the model calls made in a block cost, in tokens, whichever harness made them.

Providers and harnesses count alike but name the counts differently. OpenCode leaves
cached input out of ``input`` and reasoning out of ``output``; the chat completions API
counts both in. So a count is read into prompt and completion tokens as the API bills them.
"""

from __future__ import annotations

import contextlib
import contextvars
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass


@dataclass
class Spend:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    def add(self, usage: Mapping[str, object] | None) -> None:
        self.calls += 1
        prompt, completion = billed(usage or {})
        self.prompt_tokens += prompt
        self.completion_tokens += completion


def _whole(counts: Iterable[object]) -> int:
    return sum(count for count in counts if isinstance(count, int))


def billed(usage: Mapping[str, object]) -> tuple[int, int]:
    """Prompt and completion tokens, from any of the ways a call's usage is reported."""
    if "prompt_tokens" in usage or "input_tokens" in usage:
        return _whole(usage.get(n) for n in ("prompt_tokens", "input_tokens")), _whole(
            usage.get(n) for n in ("completion_tokens", "output_tokens")
        )
    cache = usage.get("cache")
    cached = (
        _whole(count for kind, count in cache.items() if kind in ("read", "write"))
        if isinstance(cache, Mapping)
        else 0
    )
    return _whole([usage.get("input")]) + cached, _whole(
        usage.get(n) for n in ("output", "reasoning")
    )


_meter: contextvars.ContextVar[Spend | None] = contextvars.ContextVar("spend", default=None)


@contextlib.contextmanager
def metered() -> Iterator[Spend]:
    """The spend of every model call recorded inside the block."""
    spend = Spend()
    token = _meter.set(spend)
    try:
        yield spend
    finally:
        _meter.reset(token)


def count(usage: Mapping[str, object] | None) -> None:
    """Add one recorded call to the block it was made in, if one is metered."""
    spend = _meter.get()
    if spend is not None:
        spend.add(usage)
