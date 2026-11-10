"""A note field's name as a reader sees it."""

from __future__ import annotations


def title_of(name: str) -> str:
    """``worked_examples`` reads "Worked examples"."""
    words = name.replace("_", " ")
    return words[:1].upper() + words[1:]
