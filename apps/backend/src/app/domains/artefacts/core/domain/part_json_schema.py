"""The JSON Schema a writer is shown for a part, built from the fields the check reads."""

from __future__ import annotations

from collections.abc import Sequence

from app.domains.artefacts.core.domain.part_fields import (
    KIND_KEY,
    FieldType,
    PartField,
    PartKind,
)
from app.shared.json_types import JsonObject

_TEXT: JsonObject = {"type": "string", "minLength": 1}
_SCALARS: dict[FieldType, JsonObject] = {
    FieldType.TEXT: _TEXT,
    FieldType.MARKDOWN: _TEXT,
    FieldType.TIKZ: {**_TEXT, "pattern": r"\\begin\{tikzpicture\}"},
    FieldType.MATHS: {**_TEXT, "pattern": r"\$"},
    FieldType.WHOLE_NUMBER: {"type": "integer", "minimum": 0},
    FieldType.YES_NO: {"type": "boolean"},
}


def _kind_schema(kind: PartKind) -> JsonObject:
    return {
        "description": kind.description,
        **object_schema(kind.fields, first={KIND_KEY: {"const": kind.name}}),
    }


def _item_schema(field: PartField) -> JsonObject:
    if field.kinds:
        return {"oneOf": [_kind_schema(kind) for kind in field.kinds]}
    return object_schema(field.fields)


def _field_schema(field: PartField) -> JsonObject:
    described: JsonObject = {"description": field.description}
    if field.type is FieldType.TEXT and field.options:
        return {**described, "type": "string", "enum": list(field.options)}
    if field.type in _SCALARS:
        return {**described, **_SCALARS[field.type]}
    if field.type is FieldType.GROUP:
        return {**described, **object_schema(field.fields)}
    items = _TEXT if field.type is FieldType.LIST else _item_schema(field)
    return {**described, "type": "array", "minItems": field.min_items, "items": items}


def object_schema(fields: Sequence[PartField], *, first: JsonObject | None = None) -> JsonObject:
    """An object with ``fields``, after any ``first`` properties, each of which is required."""
    leading = first or {}
    properties: JsonObject = {**leading, **{field.name: _field_schema(field) for field in fields}}
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": [*leading, *(field.name for field in fields if field.required)],
    }
