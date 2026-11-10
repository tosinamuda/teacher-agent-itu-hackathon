"""Progress a running experiment reports to whoever is watching it."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass

from app.domains.experiments.domain.types import ConditionCode
from app.shared.json_types import JsonObject

ProgressSink = Callable[[JsonObject], None]


@dataclass
class GenerationProgress:
    """Call-scope counter that turns each finished condition into one live event."""

    sink: ProgressSink
    total: int
    done: int = 0

    def finished(self, message: str) -> None:
        self.done += 1
        self.sink(
            {
                "type": "progress",
                "phase": "generation",
                "done": self.done,
                "total": self.total,
                "message": message,
            }
        )


_ACTIVE_PROGRESS: ContextVar[GenerationProgress | None] = ContextVar(
    "study_pack_generation_progress",
    default=None,
)


@contextmanager
def watch_generation(sink: ProgressSink | None, *, total: int) -> Iterator[None]:
    """Turn conditions finished inside this block into live events for ``sink``."""
    watcher = None if sink is None else GenerationProgress(sink=sink, total=total)
    token = _ACTIVE_PROGRESS.set(watcher)
    try:
        yield
    finally:
        _ACTIVE_PROGRESS.reset(token)


def report_generated(condition: ConditionCode) -> None:
    """Report a generated pack only while someone is watching."""
    _report(f"Generated study pack {condition.value}")


def report_generation_failed(condition: ConditionCode) -> None:
    """Report a failed condition only while someone is watching."""
    _report(f"{condition.value} generation failed")


def report_learner_packs(focal_learner_id: str) -> None:
    """Report one learner's finished packs only while someone is watching."""
    _report(f"P0/P1 ready for {focal_learner_id}")


def report_learner_failed(focal_learner_id: str) -> None:
    """Report one learner's failed pair only while someone is watching."""
    _report(f"P0/P1 failed for {focal_learner_id}")


def _report(message: str) -> None:
    watcher = _ACTIVE_PROGRESS.get()
    if watcher is not None:
        watcher.finished(message)
