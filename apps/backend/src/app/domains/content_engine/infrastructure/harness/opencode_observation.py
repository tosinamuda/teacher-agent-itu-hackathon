"""What a tool call found, in one line a person reads: its result, compressed."""

from __future__ import annotations

import json
import re

from app.shared.json_types import JsonObject, JsonValue

#: The longest an observation is, in characters.
_LONGEST = 220
_REFUSED = re.compile(r"^Error executing tool \w+:\s*")
_OBJECTIVE_PART = re.compile(r"the [\w-]+-po(\d+) part, at ")
_OBJECTIVE_UNIT = re.compile(r"-po(\d+)$")
_NUMBERED = re.compile(r"^\d+: ", re.MULTILINE)


def _short(text: str) -> str:
    line = _OBJECTIVE_PART.sub(lambda found: f"objective {int(found[1])}, ", " ".join(text.split()))
    return line if len(line) <= _LONGEST else line[: _LONGEST - 1].rstrip() + "…"


def _object_of(output: object) -> JsonObject:
    try:
        found = json.loads(output) if isinstance(output, str) else None
    except ValueError:
        return {}
    return {str(key): value for key, value in found.items()} if isinstance(found, dict) else {}


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _draft_state(result: JsonObject, *, opening: bool) -> str | None:
    """Where a draft stands after a call: what the checks found, or what is still to write."""
    issues = result.get("issues")
    if isinstance(issues, list) and issues:
        more = f" (and {len(issues) - 1} more)" if len(issues) > 1 else ""
        return _short(f"The checks found: {issues[0]}{more}")
    missing = result.get("missing")
    if not isinstance(missing, list):
        return None
    if missing:
        return f"{_plural(len(missing), 'part')} {'to write' if opening else 'still to write'}"
    return "Every part is written and the checks pass"


def _where(matches: JsonValue) -> str:
    """Where the first match of a text search is, said as a person would."""
    first = matches[0] if isinstance(matches, list) and matches else None
    if not isinstance(first, dict):
        return ""
    unit = str(first.get("unit_id", ""))
    objective = _OBJECTIVE_UNIT.search(unit)
    name = f"objective {int(objective[1])}" if objective else unit
    return f"{name} \u00b7 {first.get('path', '')}"


def _found(result: JsonObject) -> str:
    count = result.get("count")
    if not isinstance(count, int):
        return ""
    if count == 0:
        return "Not in any part of the draft"
    place = _where(result.get("matches"))
    return f"Found in {place}" if count == 1 else f"Found in {count} places, first {place}"


def observation(name: str, state: JsonObject) -> str | None:
    """The one line a finished call says to a person, or none when it has nothing to add."""
    if state.get("status") == "error":
        refused = _REFUSED.sub("", str(state.get("error") or "")).strip()
        return _short(refused) if refused else None
    output = state.get("output")
    if name in ("add_part", "revise_part", "read_draft", "start_draft"):
        return _draft_state(_object_of(output), opening=name == "start_draft")
    if name == "locate_text":
        return _short(_found(_object_of(output))) or None
    if name == "submit_draft":
        return "Saved for the teacher to review" if _object_of(output).get("saved_as") else None
    if name == "read" and isinstance(output, str):
        lines = len(_NUMBERED.findall(output))
        return _plural(lines, "line") if lines else None
    return None
