"""The id of a curriculum objective of a subtopic that has no textbook linkage."""

from __future__ import annotations


def performance_objective_id(subtopic_id: str, position: int) -> str:
    """The id the curriculum gives its ``position``-th performance objective, counting from 1.

    A subtopic linked to the textbook takes its ids from that linkage, which follows the same
    form (``…-po01``). One without it takes this id from the subtopic alone.
    """
    return f"{subtopic_id}-po{position:02d}"
