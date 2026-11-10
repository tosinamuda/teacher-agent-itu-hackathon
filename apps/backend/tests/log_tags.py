"""The log tags a model call made at this point would be recorded under."""

from typing import Any

from app.domains.generation_log.application.recorder import current_tags


def active_log_tags() -> dict[str, Any]:
    return current_tags()
