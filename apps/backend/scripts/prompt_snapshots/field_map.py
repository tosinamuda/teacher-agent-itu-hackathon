"""Which conditions receive which field, read off the rendered prompts.

Derived rather than declared. The profile definitions say what a condition MAY carry; only
the render says what it does, and the two have disagreed before. Under the shared contract
production binds, all four H1 arms send the same five signature fields, so the manipulation
lives one level down — in the keys inside `lesson_context` and `unit_context`, and in
whether evidence has anything in it.
"""

from __future__ import annotations

from scripts.prompt_snapshots.arms import Arm
from scripts.prompt_snapshots.evidence import rendered_evidence
from scripts.prompt_snapshots.rendered import field_blocks, json_value

CONTEXT_FIELDS = ("lesson_context", "unit_context", "learner_state", "session_signals")
EVIDENCE_KEY = "source_evidence[]"
"""Stands for 'evidence arrived with something in it', which is the evidence step itself
rather than a key inside a dict."""


def sent_keys(arm: Arm) -> set[str]:
    """Every dotted field key this arm's rendered prompt carries, evidence included."""
    if arm.call is None:
        return set()
    blocks = field_blocks(arm.call)
    keys = {
        f"{field}.{key}"
        for field in CONTEXT_FIELDS
        if field in blocks
        for key in _keys(json_value(blocks[field]))
    }
    return keys | ({EVIDENCE_KEY} if rendered_evidence(arm.call) else set())


def receiving_conditions(arms: list[Arm]) -> dict[str, frozenset[str]]:
    """Field key -> the conditions whose rendered prompt carries it."""
    everything = sorted({key for arm in arms for key in sent_keys(arm)})
    return {
        key: frozenset(arm.condition.value for arm in arms if key in sent_keys(arm))
        for key in everything
    }


def _keys(value: object) -> list[str]:
    return sorted(value) if isinstance(value, dict) else []
