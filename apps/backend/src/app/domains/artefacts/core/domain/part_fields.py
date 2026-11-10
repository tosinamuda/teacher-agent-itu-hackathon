"""The fields a part schema is made of: their types, and the shapes of the objects they hold."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum

from app.shared.json_types import JsonObject

_FIELD_NAME = re.compile(r"^[a-z][a-z0-9_]{0,39}$")

#: The key that names which kind an item of a mixed list is.
KIND_KEY = "kind"


class FieldType(str, Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    #: A drawing: one ``tikzpicture`` environment, drawn to check it before it is saved.
    TIKZ = "tikz"
    #: One line of mathematics in LaTeX, such as a line of a worked solution.
    MATHS = "maths"
    WHOLE_NUMBER = "whole_number"
    YES_NO = "yes_no"
    LIST = "list"
    GROUP = "group"
    ITEMS = "items"


_NESTING = (FieldType.GROUP, FieldType.ITEMS)
_COUNTED = (FieldType.LIST, FieldType.ITEMS)


class PartSchemaError(ValueError):
    """A part schema that cannot be used."""


class PartInvalidError(ValueError):
    """A part that does not match its schema; ``problems`` says where and why."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("; ".join(problems))
        self.problems = problems


def _record_of(raw: object, what: str) -> dict[str, object]:
    if not isinstance(raw, Mapping):
        raise PartSchemaError(f"{what} is an object")
    return {str(key): value for key, value in raw.items()}


def records_of(raw: object, what: str) -> list[dict[str, object]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise PartSchemaError(f"{what} are a list")
    return [_record_of(entry, what) for entry in raw]


def unique_names(names: Sequence[str], *, where: str) -> None:
    repeated = sorted({name for name in names if names.count(name) > 1})
    if repeated:
        raise PartSchemaError(f"{where} repeats names: {', '.join(repeated)}")


def _refuse_bad_name(name: str, description: str) -> None:
    if not _FIELD_NAME.match(name):
        raise PartSchemaError(f"a name must be snake_case: {name!r}")
    if not description.strip():
        raise PartSchemaError(f"{name!r} needs a description")


@dataclass(frozen=True)
class PartKind:
    """One shape an item of a mixed list may take, named by the item's ``kind``."""

    name: str
    description: str
    fields: tuple[PartField, ...]

    def __post_init__(self) -> None:
        """Refuse a kind a writer could not be told how to fill."""
        _refuse_bad_name(self.name, self.description)
        if not self.fields:
            raise PartSchemaError(f"kind {self.name!r} needs fields of its own")
        if any(field.name == KIND_KEY for field in self.fields):
            raise PartSchemaError(f"kind {self.name!r} cannot have a field named {KIND_KEY}")
        unique_names([field.name for field in self.fields], where=f"kind {self.name!r}")

    @classmethod
    def from_record(cls, record: Mapping[str, object]) -> PartKind:
        return cls(
            name=str(record.get("name", "")),
            description=str(record.get("description", "")),
            fields=tuple(
                PartField.from_record(f) for f in records_of(record.get("fields"), "fields")
            ),
        )

    def to_record(self) -> JsonObject:
        return {
            "name": self.name,
            "description": self.description,
            "fields": [field.to_record() for field in self.fields],
        }


@dataclass(frozen=True)
class PartField:
    """One named field of a part.

    A group holds one object with ``fields`` of its own. A list of items holds objects with
    ``fields``, or with the fields of one of its ``kinds`` each. Text may be limited to
    ``options``. A list or list of items holds at least ``min_items`` entries.
    """

    name: str
    description: str
    type: FieldType
    required: bool = True
    fields: tuple[PartField, ...] = ()
    kinds: tuple[PartKind, ...] = ()
    options: tuple[str, ...] = ()
    min_items: int = 1

    def __post_init__(self) -> None:
        """Refuse a field a writer could not be told how to fill."""
        _refuse_bad_name(self.name, self.description)
        self._refuse_misplaced_shape()
        if self.options:
            if self.type is not FieldType.TEXT:
                raise PartSchemaError(f"only a text field has options: {self.name!r}")
            unique_names(list(self.options), where=f"the options of {self.name!r}")
        if self.min_items != 1 and self.type not in _COUNTED:
            raise PartSchemaError(f"only a list says how many items it holds: {self.name!r}")
        if self.min_items < 0:
            raise PartSchemaError(f"{self.name!r} cannot hold fewer than no items")
        unique_names([field.name for field in self.fields], where=f"field {self.name!r}")
        unique_names([kind.name for kind in self.kinds], where=f"the kinds of {self.name!r}")

    def _refuse_misplaced_shape(self) -> None:
        if self.type is FieldType.ITEMS and bool(self.fields) == bool(self.kinds):
            raise PartSchemaError(f"items field {self.name!r} needs fields of its own or kinds")
        if self.type is FieldType.GROUP and (not self.fields or self.kinds):
            raise PartSchemaError(f"group {self.name!r} needs fields of its own")
        if self.type not in _NESTING and (self.fields or self.kinds):
            raise PartSchemaError(f"only a group or items field has fields: {self.name!r}")

    def depth(self) -> int:
        """How many levels of objects the field holds: none for text, one for a group."""
        inner = [*self.fields, *(field for kind in self.kinds for field in kind.fields)]
        return 1 + max((field.depth() for field in inner), default=0) if inner else 0

    @classmethod
    def from_record(cls, record: Mapping[str, object]) -> PartField:
        try:
            return cls(
                name=str(record["name"]),
                description=str(record["description"]),
                type=FieldType(record["type"]),
                required=bool(record.get("required", True)),
                fields=tuple(
                    cls.from_record(f) for f in records_of(record.get("fields"), "fields")
                ),
                kinds=tuple(
                    PartKind.from_record(k) for k in records_of(record.get("kinds"), "kinds")
                ),
                options=tuple(_options(record.get("options"))),
                min_items=_whole(record.get("min_items", 1)),
            )
        except KeyError as error:
            raise PartSchemaError(f"field is missing {error}") from error
        except ValueError as error:
            if isinstance(error, PartSchemaError):
                raise
            raise PartSchemaError(str(error)) from error

    def to_record(self) -> JsonObject:
        record: JsonObject = {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "required": self.required,
        }
        if self.fields:
            record["fields"] = [field.to_record() for field in self.fields]
        if self.kinds:
            record["kinds"] = [kind.to_record() for kind in self.kinds]
        if self.options:
            record["options"] = list(self.options)
        if self.min_items != 1:
            record["min_items"] = self.min_items
        return record


def _options(raw: object) -> list[str]:
    if raw is None:
        return []
    if not isinstance(raw, list) or not all(isinstance(option, str) for option in raw):
        raise PartSchemaError("options are a list of text")
    return [str(option) for option in raw]


def _whole(raw: object) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise PartSchemaError("min_items is a whole number")
    return raw
