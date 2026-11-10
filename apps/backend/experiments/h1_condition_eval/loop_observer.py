"""Count the agent-loop failures that never reach the caller.

Two of them are invisible without this:

* ``ChatAdapter`` catches its own ``AdapterParseError`` and retries through
  ``JSONAdapter``. A recovered parse failure costs a whole extra LM call and is
  the first sign a model is drifting off-format, but nothing is raised.
* ``ReActV2`` catches ``AdapterParseError`` mid-loop, breaks, and returns a
  ``Prediction`` carrying only ``termination_reason``. Because the composing
  tools write into the draft as they go, a loop that gave up still yields a
  section — a silently short one.

A run whose sections are quietly truncated scores as data rather than as a
failure, which is how a broken arm looks merely mediocre. dspy's callback
mechanism sees both, so the counts come from the library rather than from
wrapping its methods.
"""

from __future__ import annotations

import logging
from collections import Counter
from typing import Any

from dspy.utils.callback import BaseCallback

from app.infra.dspy_agent_loop import COMPLETED


class LoopObserver(BaseCallback):
    """Tallies parse failures, tool errors and non-submit loop terminations."""

    #: How many failure messages to keep. A count says a model drifted off format;
    #: it never says HOW, so a count alone cannot be acted on. Keeping the first few
    #: is the difference between "DeepSeek had 13 parse failures" and knowing which
    #: field it malformed.
    KEEP = 5

    def __init__(self) -> None:
        self.parse_failures: Counter[str] = Counter()
        self.abandonments: list[str] = []
        self.tool_errors: Counter[str] = Counter()
        self.terminations: Counter[str] = Counter()
        self.samples: list[str] = []

    def on_adapter_parse_end(
        self,
        call_id: str,
        outputs: dict[str, Any] | None,
        exception: Exception | None = None,
    ) -> None:
        if exception is not None:
            self.parse_failures[type(exception).__name__] += 1
            if len(self.samples) < self.KEEP:
                self.samples.append(f"{type(exception).__name__}: {exception}")

    def on_tool_end(
        self,
        call_id: str,
        outputs: dict[str, Any] | None,
        exception: Exception | None = None,
    ) -> None:
        if exception is not None:
            self.tool_errors[type(exception).__name__] += 1

    def on_module_end(
        self,
        call_id: str,
        outputs: Any,  # noqa: ANN401 — dspy hands back a Prediction or None
        exception: Exception | None = None,
    ) -> None:
        reason = getattr(outputs, "termination_reason", None)
        if reason:
            self.terminations[reason] += 1

    @property
    def abandoned_loops(self) -> int:
        """Loops that stopped without submitting — the silently short sections."""
        return sum(n for reason, n in self.terminations.items() if reason not in COMPLETED)

    def watch_the_loop(self) -> None:
        """Capture WHY a loop gave up, which only dspy's logger is told.

        ``ReActV2`` catches its own failure, logs it, and returns a Prediction carrying
        `termination_reason` and nothing else — so the count says a loop was abandoned
        and never says what abandoned it. Diagnosing one meant finding a traceback in a
        run log by hand. It also catches ValueError alongside AdapterParseError and
        calls both "parse_error", so the reason cannot even be inferred from the name.
        """
        observer = self

        class _Capture(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                if len(observer.abandonments) < observer.KEEP:
                    observer.abandonments.append(record.getMessage().strip())

        handler = _Capture(level=logging.WARNING)
        logging.getLogger("dspy.predict.react_v2").addHandler(handler)

    def summary(self) -> str:
        completed = sum(n for r, n in self.terminations.items() if r in COMPLETED)
        parts = [f"{completed} loops submitted"]
        if self.abandoned_loops:
            gave_up = {r: n for r, n in self.terminations.items() if r not in COMPLETED}
            parts.append(f"{self.abandoned_loops} ABANDONED {gave_up}")
        if self.parse_failures:
            parts.append(f"parse failures (incl. recovered) {dict(self.parse_failures)}")
        if self.tool_errors:
            parts.append(f"tool errors {dict(self.tool_errors)}")
        return " | ".join(parts)

    def detail(self) -> str:
        """The kept failure messages, one per line, for a run that had any."""
        parts: list[str] = []
        if self.samples:
            parts += [
                f"first {len(self.samples)} parse failure(s), verbatim:",
                *(f"  - {text}" for text in self.samples),
            ]
        if self.abandonments:
            parts += [
                f"first {len(self.abandonments)} abandonment(s), verbatim:",
                *(f"  - {text[:1200]}" for text in self.abandonments),
            ]
        return "\n".join(parts)
