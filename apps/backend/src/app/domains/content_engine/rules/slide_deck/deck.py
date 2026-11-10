"""The slides written so far, one part for each step of the lesson, in the lesson's order."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from app.shared.json_types import JsonObject


def _object(value: object) -> JsonObject:
    return {str(k): v for k, v in value.items()} if isinstance(value, dict) else {}


@dataclass(frozen=True)
class Unit:
    unit_id: str


@dataclass(frozen=True)
class Deck:
    sections: tuple[tuple[Unit, JsonObject], ...]

    @classmethod
    def of(cls, sections: list[Mapping[str, object]]) -> Deck:
        """A deck from the sections of a draft: each has a ``unit_id`` and a ``part``."""
        return cls(
            tuple(
                (Unit(str(section["unit_id"])), _object(section.get("part")))
                for section in sections
            )
        )

    def written(self) -> list[tuple[Unit, JsonObject]]:
        return list(self.sections)
