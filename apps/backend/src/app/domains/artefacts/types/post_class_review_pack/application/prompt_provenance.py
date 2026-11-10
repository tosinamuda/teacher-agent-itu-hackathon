"""Deterministic prompt fingerprints captured at the actual model-call boundary."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field

from app.domains.artefacts.types.post_class_review_pack.domain.prompt_provenance import (
    PromptProvenance,
)


@dataclass
class PromptTrace:
    """Mutable call-scope recorder whose snapshot is immutable and persistable."""

    components: dict[str, str] = field(default_factory=dict)

    def record(self, component: str, fingerprint: str) -> None:
        existing = self.components.get(component)
        if existing is not None and existing != fingerprint:
            raise ValueError(
                f"prompt component {component!r} used multiple signatures in one result"
            )
        self.components[component] = fingerprint

    def snapshot(self) -> PromptProvenance:
        return PromptProvenance(components=dict(self.components))


_ACTIVE_TRACE: ContextVar[PromptTrace | None] = ContextVar("review_pack_prompt_trace", default=None)


@contextmanager
def capture_prompt_provenance() -> Iterator[PromptTrace]:
    """Capture prompt signatures used by model calls inside one generated result."""
    trace = PromptTrace()
    token = _ACTIVE_TRACE.set(trace)
    try:
        yield trace
    finally:
        _ACTIVE_TRACE.reset(token)


def record_prompt_fingerprint(component: str, fingerprint: str) -> None:
    """Record a model-implementation fingerprint during an active generation."""
    trace = _ACTIVE_TRACE.get()
    if trace is not None:
        trace.record(component, fingerprint)
