"""A stored revision note as a reader is shown it.

A note is stored as it was generated. Notes written before generation made the model's text
reader-ready still carry its HTML and bare LaTeX, which a page shows as tags and backslashes;
the study's raters read those notes rendered, not as source. Reading a note makes its text
reader-ready, which leaves text that already is unchanged.
"""

from __future__ import annotations

from app.shared.json_types import JsonObject, JsonValue
from app.shared.llm_markup import reader_ready

#: The fields of a block that hold what the model wrote.
_MODEL_TEXT = ("content", "question", "answer")


def _block(block: JsonValue) -> JsonValue:
    if not isinstance(block, dict):
        return block
    return {
        key: reader_ready(value) if key in _MODEL_TEXT and isinstance(value, str) else value
        for key, value in block.items()
    }


def _step(step: JsonValue) -> JsonValue:
    blocks = step.get("blocks") if isinstance(step, dict) else None
    if not isinstance(step, dict) or not isinstance(blocks, list):
        return step
    return {**step, "blocks": [_block(block) for block in blocks]}


def for_reading(manifest: JsonObject) -> JsonObject:
    steps = manifest.get("steps")
    if not isinstance(steps, list):
        return manifest
    return {**manifest, "steps": [_step(step) for step in steps]}
