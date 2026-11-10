"""Cross-cutting capture of every LLM call into the generation log.

``GenerationLogRecorder`` is a DSPy callback registered globally in
``app.dspy_setup``; it persists each LM call to ``generation_events`` using the sync
session (so it works from both async request handlers and jobs' processes).
``log_context(...)`` is the seam app code uses to tag the calls it makes with
meaningful context (which lesson plan, student, objective, experiment condition),
so the recorded events can be grouped and labelled.
"""

from __future__ import annotations

import contextlib
import contextvars
import logging
from collections.abc import Iterator
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

import dspy
from dspy.utils.callback import BaseCallback
from dspy.utils.usage_tracker import UsageTracker

from app.db.session import SessionLocal
from app.domains.generation_log.application.spend import count
from app.domains.generation_log.models.generation_event import GenerationEvent

logger = logging.getLogger(__name__)

# Tags applied to every LM call made within an active log_context() block.
_log_context: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar(
    "log_context", default=None
)

_MAX_DEPTH = 6


@contextlib.contextmanager
def log_context(**tags: Any) -> Iterator[None]:
    """Tag the LM calls made inside this block for the generation log.

    Recognised tags: ``kind`` (lesson_plan | diagnostic | personalise_section |
    experiment_condition), ``correlation_id`` (groups one run), plus
    any free-form context (``plan_version_id``, ``student_id``,
    ``lesson_objective_id``, ``condition_code``, ...). ``None`` values are dropped;
    nested blocks merge with the enclosing tags.
    """
    merged = {**(_log_context.get() or {}), **{k: v for k, v in tags.items() if v is not None}}
    token = _log_context.set(merged)
    try:
        yield
    finally:
        _log_context.reset(token)


def _jsonable(value: Any, depth: int = 0) -> Any:
    """Coerce arbitrary LM inputs/outputs into a JSON-serialisable structure."""
    if depth > _MAX_DEPTH:
        return str(value)
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _jsonable(item, depth + 1) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item, depth + 1) for item in value]
    return str(value)


def _extract_request(inputs: dict[str, Any] | None) -> dict[str, Any]:
    inputs = inputs or {}
    request: dict[str, Any] = {}
    if inputs.get("messages") is not None:
        request["messages"] = _jsonable(inputs["messages"])
    if inputs.get("prompt") is not None:
        request["prompt"] = _jsonable(inputs["prompt"])
    params = {
        key: _jsonable(value) for key, value in inputs.items() if key not in {"messages", "prompt"}
    }
    if params:
        request["params"] = params
    return request


def _extract_response(outputs: Any) -> dict[str, Any]:
    if outputs is None:
        return {}
    return {"completions": _jsonable(outputs)}


class CallUsage(UsageTracker):
    """The tokens of one LM call, passed on to any tracker counting the calls around it.

    DSPy hands a callback the call's outputs, which carry no usage; it reports usage only
    to the tracker in its settings. So each call is given a tracker of its own.
    """

    def __init__(self, outer: UsageTracker | None) -> None:
        super().__init__()
        self._outer = outer

    def add_usage(self, lm: str, usage_entry: dict[str, Any]) -> None:
        super().add_usage(lm, usage_entry)
        if self._outer is not None:
            self._outer.add_usage(lm, usage_entry)

    def tokens(self) -> dict[str, Any] | None:
        """The call's usage as the provider reported it; ``None`` for a cached answer."""
        totals = list(self.get_total_tokens().values())
        return _jsonable(totals[0]) if totals else None


@dataclass
class _Call:
    request: dict[str, Any]
    model: str
    tags: dict[str, Any]
    usage: CallUsage
    scope: AbstractContextManager[None]
    started_at: float = field(default_factory=perf_counter)

    def close(self) -> None:
        """Hand the settings back as they were before the call."""
        try:
            self.scope.__exit__(None, None, None)
        except ValueError:
            # The call ended in another context than it began in, which leaves the
            # settings in that context untouched; the usage is still this call's.
            pass


@dataclass(frozen=True)
class Generation:
    """One model call as the generation log keeps it."""

    model: str
    tags: dict[str, Any]
    request: dict[str, Any]
    response: dict[str, Any]
    duration_ms: float | None
    token_usage: dict[str, Any] | None


def current_tags() -> dict[str, Any]:
    """The log tags a model call made now is recorded under."""
    return dict(_log_context.get() or {})


class GenerationLog:
    """Writes model calls to ``generation_events``, grouped by their log tags.

    Failures here are swallowed and logged — generation logging must never break generation.
    """

    def record(self, generation: Generation) -> None:
        count(generation.token_usage)
        tags = dict(generation.tags)
        kind = str(tags.pop("kind", "lm_call"))
        correlation_id = (
            tags.pop("correlation_id", None)
            or tags.get("plan_version_id")
            or tags.get("artefact_plan_id")
        )
        self._persist(
            kind=kind,
            model=generation.model,
            correlation_id=str(correlation_id) if correlation_id is not None else None,
            context=_jsonable(tags),
            request=generation.request,
            response=generation.response,
            duration_ms=generation.duration_ms,
            token_usage=generation.token_usage,
        )

    def _persist(self, **fields: Any) -> None:
        try:
            with SessionLocal() as session:
                session.add(GenerationEvent(**fields))
                session.commit()
        except Exception:  # noqa: BLE001 - generation logging must never break generation
            logger.warning("generation log: failed to persist generation event", exc_info=True)


class GenerationLogRecorder(BaseCallback, GenerationLog):
    """Records each DSPy LM call, with its token usage; ``log_context`` tags the rows."""

    def __init__(self) -> None:
        self._calls: dict[str, _Call] = {}

    def on_lm_start(self, call_id: str, instance: object, inputs: dict[str, object]) -> None:
        model = str(getattr(instance, "model", None) or instance.__class__.__name__)
        usage = CallUsage(dspy.settings.get("usage_tracker"))
        scope = dspy.context(usage_tracker=usage)
        scope.__enter__()
        self._calls[call_id] = _Call(_extract_request(inputs), model, current_tags(), usage, scope)

    def on_lm_end(
        self, call_id: str, outputs: object | None, exception: Exception | None = None
    ) -> None:
        call = self._calls.pop(call_id, None)
        if call is None:
            return
        call.close()
        response = (
            {"error": str(exception)} if exception is not None else _extract_response(outputs)
        )
        self.record(
            Generation(
                model=call.model,
                tags=call.tags,
                request=call.request,
                response=response,
                duration_ms=round((perf_counter() - call.started_at) * 1000, 1),
                token_usage=call.usage.tokens(),
            )
        )
