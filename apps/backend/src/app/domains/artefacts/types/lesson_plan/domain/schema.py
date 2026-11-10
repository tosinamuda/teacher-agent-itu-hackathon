"""The shape every lesson plan has, however it was made: drafted, entered or imported.

Structure only. What a drafted plan must also satisfy (an evaluation step covering every
objective, a worked example in a procedure step) is a drafting rule, and a teacher's own
plan is not held to it.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import cast

from jsonschema import Draft7Validator

from app.shared.json_types import JsonObject

_SCHEMA = Path(__file__).with_name("session_plan.schema.json")


@cache
def _validator() -> Draft7Validator:
    return Draft7Validator(cast(JsonObject, json.loads(_SCHEMA.read_text(encoding="utf-8"))))


def schema_issues(session_plan: JsonObject) -> list[tuple[list[str | int], str]]:
    """Where the plan departs from the lesson plan schema; empty when it has the shape."""
    return [(list(error.path), error.message) for error in _validator().iter_errors(session_plan)]
