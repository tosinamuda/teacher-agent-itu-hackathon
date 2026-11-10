"""Check a part against its fields: the part as stored, or every place it misses them."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from app.domains.artefacts.core.domain import latex_text, maths_line
from app.domains.artefacts.core.domain.part_fields import (
    KIND_KEY,
    FieldType,
    PartField,
    PartInvalidError,
)
from app.shared.json_types import JsonObject, JsonValue

TIKZ_BEGIN = "\\begin{tikzpicture}"


def _at(where: str, name: str | int) -> str:
    return f"{where}.{name}" if where else str(name)


class _Check:
    """One pass over a part, recording every problem instead of stopping at the first."""

    def __init__(self, *, formulas: bool = True) -> None:
        self.problems: list[str] = []
        self._formulas = formulas

    def text(self, raw: object, field: PartField, where: str) -> str | None:
        if isinstance(raw, int | float) and not isinstance(raw, bool):
            self.problems.append(
                f'{where}: must be text, not a number: write it between quotes, such as "{raw}"'
            )
            return None
        if not isinstance(raw, str) or not raw.strip():
            self.problems.append(f"{where}: must be text that is not empty")
            return None
        if field.options and raw.strip() not in field.options:
            self.problems.append(f"{where}: must be one of: {', '.join(field.options)}")
        return raw.strip()

    def drawing(self, raw: object, field: PartField, where: str) -> str | None:
        source = self.text(raw, field, where)
        if source is not None and TIKZ_BEGIN not in source:
            self.problems.append(f"{where}: must be a tikzpicture environment")
        return source

    def markdown(self, raw: object, field: PartField, where: str) -> str | None:
        text = self.text(raw, field, where)
        if text is not None:
            self.problems.extend(f"{where}: {problem}" for problem in latex_text.problems(text))
        return text

    def maths(self, raw: object, field: PartField, where: str) -> str | None:
        line = self.markdown(raw, field, where)
        wrong = maths_line.problem(line, formulas=self._formulas) if line is not None else None
        if wrong:
            self.problems.append(f"{where}: {wrong}")
        return line

    def whole_number(self, raw: object, field: PartField, where: str) -> int | None:
        if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
            self.problems.append(f"{where}: must be a whole number")
            return None
        return raw

    def yes_no(self, raw: object, field: PartField, where: str) -> bool | None:
        if not isinstance(raw, bool):
            self.problems.append(f"{where}: must be true or false")
            return None
        return raw

    def entries(self, raw: object, field: PartField, where: str) -> list[object]:
        if isinstance(raw, str):
            self.problems.append(
                f'{where}: must be a list, not text: write each item in square brackets, ["a", "b"]'
            )
            return []
        if not isinstance(raw, list) or len(raw) < field.min_items:
            self.problems.append(f"{where}: must be a list{_at_least(field.min_items)}")
            return []
        return list(raw)

    def field(self, raw: object, field: PartField, where: str) -> JsonValue:
        scalar = _SCALARS.get(field.type)
        if scalar is not None:
            return scalar(self, raw, field, where)
        if field.type is FieldType.GROUP:
            return self.record(raw, field.fields, where)
        entries = self.entries(raw, field, where)
        if field.type is FieldType.LIST:
            return [
                self.text(entry, field, _at(where, index)) for index, entry in enumerate(entries)
            ]
        return [self.item(entry, field, _at(where, index)) for index, entry in enumerate(entries)]

    def item(self, raw: object, field: PartField, where: str) -> JsonObject:
        if not field.kinds:
            return self.record(raw, field.fields, where)
        if not isinstance(raw, dict):
            self.problems.append(f"{where}: must be an object")
            return {}
        given = {str(key): value for key, value in raw.items()}
        kind = next((kind for kind in field.kinds if kind.name == given.get(KIND_KEY)), None)
        if kind is None:
            names = ", ".join(kind.name for kind in field.kinds)
            self.problems.append(f"{_at(where, KIND_KEY)}: must be one of: {names}")
            return {}
        rest = {key: value for key, value in given.items() if key != KIND_KEY}
        return {KIND_KEY: kind.name, **self.record(rest, kind.fields, where)}

    def record(self, raw: object, fields: Sequence[PartField], where: str) -> JsonObject:
        """``raw`` as stored, recording every way it misses ``fields``."""
        if not isinstance(raw, dict):
            self.problems.append(f"{where or 'the part'}: must be an object")
            return {}
        given = _named_as_fields({str(key): value for key, value in raw.items()}, fields)
        stored: JsonObject = {}
        for field in fields:
            value = given.get(field.name)
            if value is None or (not field.required and value in ("", [])):
                if field.required:
                    self.problems.append(f"{_at(where, field.name)}: is required")
                continue
            stored[field.name] = self.field(value, field, _at(where, field.name))
        known = {field.name for field in fields}
        self.problems.extend(
            f"{_at(where, name)}: is not a field of this part"
            for name, value in given.items()
            # A key the part has no field for says nothing when it is empty, so it is let go.
            if name not in known and value not in _NOTHING
        )
        return stored


_NOTHING: tuple[JsonValue, ...] = ("", [], {}, None)


def _named_as_fields(
    given: dict[str, JsonValue], fields: Sequence[PartField]
) -> dict[str, JsonValue]:
    """The part's keys, with one written in capitals taken for the field of that name.

    Field names are lowercase, and a writer who keys options "A" to "D" means the fields a to d.
    A key whose lowercase form is a field and which the part does not also give in lowercase is
    renamed; every other key is left to be refused.
    """
    names = {field.name for field in fields}
    return {
        (
            key.lower()
            if key not in names and key.lower() in names and key.lower() not in given
            else key
        ): value
        for key, value in given.items()
    }


_SCALARS: dict[FieldType, Callable[[_Check, object, PartField, str], JsonValue]] = {
    FieldType.TEXT: _Check.text,
    FieldType.MARKDOWN: _Check.markdown,
    FieldType.TIKZ: _Check.drawing,
    FieldType.MATHS: _Check.maths,
    FieldType.WHOLE_NUMBER: _Check.whole_number,
    FieldType.YES_NO: _Check.yes_no,
}


def _at_least(count: int) -> str:
    if count == 0:
        return ""
    return " with at least one item" if count == 1 else f" with at least {count} items"


def checked_part(part: object, fields: Sequence[PartField], *, formulas: bool = True) -> JsonObject:
    """``part`` as stored, with text stripped and unset optional fields dropped."""
    check = _Check(formulas=formulas)
    stored = check.record(part, fields, "")
    if check.problems:
        raise PartInvalidError(check.problems)
    return stored
