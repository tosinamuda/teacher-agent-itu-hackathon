"""A file made of a type's saved content, and what a builder of one answers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.shared.json_types import JsonObject


class FileRefusedError(ValueError):
    """The saved content cannot be made into a file; the message says why."""


@dataclass(frozen=True)
class BuiltFile:
    extension: str
    media_type: str
    data: bytes


#: Makes the file of one item of saved content, as stored: its manifest.
FileBuilder = Callable[[JsonObject], BuiltFile]
