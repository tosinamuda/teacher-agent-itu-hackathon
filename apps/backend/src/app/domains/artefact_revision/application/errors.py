"""Artefact-revision application errors.

Kept in its own module so executors can raise ``ArtefactRevisionError`` without
importing ``service`` (which imports the executors — a cycle). ``service`` still
re-exports it for existing call sites.
"""

from __future__ import annotations

from dataclasses import dataclass


# Not frozen: Python sets __traceback__ on an exception as it passes through a context manager.
@dataclass(eq=False)
class ArtefactRevisionError(Exception):
    status_code: int
    detail: str
