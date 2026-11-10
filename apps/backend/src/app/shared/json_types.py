"""JSON type aliases — a FROZEN public contract.

Fan-in ~83 (≈⅓ of the backend imports from here), so this is the single
highest change-blast-radius module: any edit to ``JsonValue``/``JsonObject``
recompiles a third of the tree and can ripple type errors everywhere. Treat the
aliases below as a stable contract — add new aliases freely, but change the
meaning of an existing one only with a coordinated sweep.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

JsonPrimitive: TypeAlias = str | int | float | bool | None

# Recursive JSON value, for *genuinely arbitrary* JSON only (raw LLM output,
# free-form notes, opaque snapshots). Structured payloads should be Pydantic
# models, not JsonObject — so this stays invariant list/dict on purpose: a
# list[str] / list[SomeDict] that won't fit is the type system telling you to
# model that payload.
#   mypy rejects the typing_extensions.TypeAliasType spelling as "cyclic" (then
#   treats it as Any, masking errors), while Pydantic needs that runtime
#   TypeAliasType to build schemas for models with JsonObject fields — so the
#   checkers get a string forward-reference alias and the runtime keeps it.
if TYPE_CHECKING:
    JsonValue: TypeAlias = (
        "str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]"
    )
else:
    from typing_extensions import TypeAliasType

    JsonValue = TypeAliasType(
        "JsonValue",
        JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"],
    )

JsonObject: TypeAlias = dict[str, JsonValue]
