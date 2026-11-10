"""A note made from another note's approved version, and whether that version is still current."""

from __future__ import annotations

from app.shared.json_types import JsonObject

MADE_FROM = "made_from"


def made_from(artefact_id: str, version: int) -> JsonObject:
    """What a note records of the version it was made from."""
    return {"artefact_id": artefact_id, "version": version}


def made_from_of(refs: JsonObject | None) -> tuple[str, int] | None:
    """The artefact and version a note says it was made from, when it says."""
    recorded = (refs or {}).get(MADE_FROM)
    if not isinstance(recorded, dict):
        return None
    artefact_id, version = recorded.get("artefact_id"), recorded.get("version")
    if isinstance(artefact_id, str) and isinstance(version, int):
        return artefact_id, version
    return None
