"""How a turn of an agent can end other than by finishing."""

from __future__ import annotations


class TurnStoppedError(Exception):
    """The teacher stopped the turn: nothing it did was saved, and the content is as it was."""
