"""A part as markdown, for content stored in the reading form of a type that has always had one.

A lesson note is read as markdown by teachers and by generation alike, so a part written to a
spec's fields is set down in that form: one headed block for each field, in the spec's order,
and nested fields as labelled blocks or, where an item is only short lines, as bullets.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domains.artefacts.core.domain.part_fields import KIND_KEY, FieldType, PartField
from app.shared.json_types import JsonObject, JsonValue

_TEXT = (FieldType.TEXT, FieldType.MARKDOWN, FieldType.MATHS, FieldType.TIKZ)


def title_of(name: str) -> str:
    """A field's name as a reader sees it: ``worked_examples`` reads "Worked examples"."""
    words = name.replace("_", " ")
    return words[:1].upper() + words[1:]


def part_as_markdown(part: JsonObject, fields: Sequence[PartField]) -> str:
    """The part's fields as headed markdown blocks, leaving out a field the part lacks."""
    blocks = [
        f"#### {title_of(field.name)}\n\n{body}"
        for field in fields
        if (body := _body(part.get(field.name), field, nested=False))
    ]
    return "\n\n".join(blocks)


def _body(value: JsonValue | None, field: PartField, *, nested: bool) -> str:
    if value is None:
        return ""
    if field.type in _TEXT:
        return str(value).strip()
    if field.type is FieldType.WHOLE_NUMBER:
        return str(value)
    if field.type is FieldType.YES_NO:
        return "Yes" if value else "No"
    if field.type is FieldType.LIST and isinstance(value, list):
        return "\n".join(f"- {str(point).strip()}" for point in value)
    if field.type is FieldType.GROUP and isinstance(value, dict):
        return _labelled(value, field.fields)
    if field.type is FieldType.ITEMS and isinstance(value, list):
        return _items(value, field, nested=nested)
    return ""


def _labelled(record: JsonObject, fields: Sequence[PartField]) -> str:
    blocks = [
        f"**{title_of(field.name)}.**\n\n{body}"
        for field in fields
        if (body := _body(record.get(field.name), field, nested=True))
    ]
    return "\n\n".join(blocks)


def _fields_of(item: JsonObject, field: PartField) -> tuple[str, Sequence[PartField]]:
    """What an item is called, if its kind names it, and the fields it holds."""
    if field.kinds:
        kind = next((k for k in field.kinds if k.name == item.get(KIND_KEY)), None)
        if kind is not None:
            return title_of(kind.name), kind.fields
    return "", field.fields


def _items(items: list[JsonValue], field: PartField, *, nested: bool) -> str:
    records = [item for item in items if isinstance(item, dict)]
    if nested and all(_one_line(record, _fields_of(record, field)[1]) for record in records):
        return "\n".join(
            "- " + " — ".join(str(record[f.name]).strip() for f in fields if f.name in record)
            for record in records
            for fields in [_fields_of(record, field)[1]]
        )
    blocks = []
    for number, record in enumerate(records, start=1):
        label, fields = _fields_of(record, field)
        name = f"{label} {number}" if label else str(number)
        blocks.append(f"**{name}.**\n\n{_labelled(record, fields)}")
    return "\n\n".join(blocks)


def _one_line(record: JsonObject, fields: Sequence[PartField]) -> bool:
    return all(
        field.type in _TEXT and "\n" not in str(record.get(field.name, "")).strip()
        for field in fields
        if field.name in record
    )
