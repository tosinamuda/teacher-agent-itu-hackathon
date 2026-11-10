"""What a lesson plan's draft acts on, and where it reports its progress, by lesson."""

from __future__ import annotations


def drafting_subject(session_id: str) -> str:
    """What one draft acts on: asking again for the same lesson follows the same job."""
    return f"lesson:{session_id}"


def drafting_channel(session_id: str) -> str:
    """Where a draft of the lesson's plan reports what the agent is doing."""
    return f"lesson-draft:{session_id.replace('-', '').lower()}"
