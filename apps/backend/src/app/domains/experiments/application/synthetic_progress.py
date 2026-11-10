"""Publish an experiment's live progress to its channel, for the experiment's WebSocket.

The synthetic jobs and the generation jobs call ``publish_synthetic_progress`` as they work;
the experiments WS endpoint relays ``synthetic:{experiment_id}`` to the browser.
"""

from __future__ import annotations

from app.infra import progress
from app.shared.json_types import JsonObject


def synthetic_channel(experiment_id: str) -> str:
    """The progress channel of one experiment."""
    return f"synthetic:{experiment_id}"


def publish_synthetic_progress(experiment_id: str, event: JsonObject) -> None:
    """Report one progress event; best effort, as progress never fails the work."""
    progress.publish(synthetic_channel(experiment_id), event)
