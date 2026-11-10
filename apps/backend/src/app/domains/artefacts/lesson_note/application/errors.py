"""What can go wrong in writing or revising a lesson note."""

from __future__ import annotations


class UnreadableReplyError(Exception):
    """The model's reply did not come in the shape asked for, even after asking again."""
