"""Read + validate a Pydantic model from an arbitrary LLM payload.

Tiny shared module: the LLM may return a ``BaseModel``, a JSON string, or a
``dict`` depending on the DSPy adapter, and the pipeline always wants a typed
Pydantic instance. ``read_validated_model`` does both steps in one call.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import TypeVar, cast

from pydantic import BaseModel

from app.shared.json_types import JsonObject

ModelT = TypeVar("ModelT", bound=BaseModel)


def to_record_object(record: Mapping[str, object]) -> JsonObject:
    """Coerce a generic mapping to ``JsonObject`` (a fresh dict, no aliasing)."""
    return cast(JsonObject, dict(record))


def read_model_object(value: object, *, label: str) -> JsonObject:
    """Coerce an LLM payload (BaseModel | JSON string | dict) to a plain ``JsonObject``."""
    if isinstance(value, BaseModel):
        value = value.model_dump()
    elif isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise ValueError(f"{label} is not an object")
    return cast(JsonObject, value)


def read_validated_model(
    value: object,
    *,
    label: str,
    model_type: type[ModelT],
) -> ModelT:
    """Parse an LLM payload as a concrete Pydantic model."""
    return model_type.model_validate(read_model_object(value, label=label))
