"""F as data: what one part of drafted content holds, and which lesson unit it covers.

A spec's part schema is the contract every part is checked against before it is stored.
The JSON Schema a writer is shown is built from the same fields the check reads, so what a
writer is told and what the app accepts cannot drift apart.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from app.domains.artefacts.core.domain.part_check import checked_part
from app.domains.artefacts.core.domain.part_fields import (
    KIND_KEY,
    FieldType,
    PartField,
    PartSchemaError,
    records_of,
    unique_names,
)
from app.domains.artefacts.core.domain.part_json_schema import object_schema
from app.shared.json_types import JsonObject, JsonValue

#: How deep groups and lists of items may nest inside one part.
MAX_DEPTH = 4


class Unit(str, Enum):
    """What one part covers: the whole lesson, one of its objectives, or one plan step.

    A curriculum objective is known before the lesson has a plan, so content made from the
    lesson itself, such as its plan, is written one curriculum objective at a time.
    """

    LESSON = "lesson"
    CURRICULUM_OBJECTIVE = "curriculum_objective"
    LESSON_OBJECTIVE = "lesson_objective"
    PLAN_STEP = "plan_step"


@dataclass(frozen=True)
class PartSchema:
    """The fields of one part, in the order a reader meets them."""

    fields: tuple[PartField, ...]

    def __post_init__(self) -> None:
        """Refuse a part with nothing a writer must fill, or one nested too deep to follow."""
        if not self.fields:
            raise PartSchemaError("a part has at least one field")
        unique_names([field.name for field in self.fields], where="the part")
        if not any(field.required for field in self.fields):
            raise PartSchemaError("a part has at least one required field")
        if max(field.depth() for field in self.fields) > MAX_DEPTH:
            raise PartSchemaError(f"a part nests groups and items at most {MAX_DEPTH} deep")

    @classmethod
    def from_record(cls, record: object) -> PartSchema:
        if record is None:
            raise PartSchemaError("parts is a list of fields")
        return cls(tuple(PartField.from_record(field) for field in records_of(record, "parts")))

    def to_record(self) -> list[JsonObject]:
        return [field.to_record() for field in self.fields]

    def json_schema(self) -> JsonObject:
        """What a writer is shown, from the same fields ``validate`` checks."""
        return object_schema(self.fields)

    def validate(self, part: object, *, formulas: bool = True) -> JsonObject:
        """The part as stored, with text stripped and unset optional fields dropped."""
        return checked_part(part, self.fields, formulas=formulas)

    def drawings(self, part: JsonObject) -> list[tuple[str, str]]:
        """Every drawing in a stored part, with the path to it."""
        found: list[tuple[str, str]] = []
        _collect(part, self.fields, "", found)
        return found

    def summary(self) -> tuple[str, ...]:
        """F in words, one line per field, for the places that list a spec's structure."""
        return tuple(_line(field) for field in self.fields)


def _collect(
    value: JsonValue, fields: Sequence[PartField], where: str, found: list[tuple[str, str]]
) -> None:
    if not isinstance(value, dict):
        return
    for field in fields:
        inner, at = value.get(field.name), f"{where}.{field.name}" if where else field.name
        if field.type is FieldType.TIKZ and isinstance(inner, str):
            found.append((at, inner))
        elif field.type is FieldType.GROUP:
            _collect(inner, field.fields, at, found)
        elif field.type is FieldType.ITEMS and isinstance(inner, list):
            for index, item in enumerate(inner):
                shape = _kind_fields(field, item)
                _collect(item, shape, f"{at}.{index}", found)


def _kind_fields(field: PartField, item: JsonValue) -> Sequence[PartField]:
    if not field.kinds:
        return field.fields
    named = item.get(KIND_KEY) if isinstance(item, dict) else None
    return next((kind.fields for kind in field.kinds if kind.name == named), ())


def _line(field: PartField) -> str:
    line = f"{field.name}: {field.description}"
    if field.kinds:
        line += " (each one of: " + ", ".join(kind.name for kind in field.kinds) + ")"
    elif field.fields:
        each = "each with" if field.type is FieldType.ITEMS else "with"
        line += f" ({each} " + ", ".join(sub.name for sub in field.fields) + ")"
    elif field.options:
        line += " (one of: " + ", ".join(field.options) + ")"
    return line if field.required else f"{line} (optional)"
