"""Where the agent making content reports what it is doing."""

from __future__ import annotations


def generation_channel(plan_version_id: str, type: str) -> str:
    """The progress channel of the agent making a class's content of one type."""
    return f"content-draft:{plan_version_id.replace('-', '').lower()}:{type}"
