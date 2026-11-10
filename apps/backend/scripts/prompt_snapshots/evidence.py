"""Read the evidence a call sends, out of the rendered prompt rather than the request.

The grounded conditions exist to teach from what the teacher actually wrote. Packs built
before 2026-06-11 were grounded in citation LABELS instead — the model was handed the name
of a source and asked to teach from it — and the request object looked correct throughout,
because a label and an excerpt are both a populated string in the same field.

So the check reads the rendered message, not the request: whatever survives serialisation
is what the model was taught from.
"""

from __future__ import annotations

from typing import Any

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prepared_call import (
    PreparedCall,
)
from scripts.prompt_snapshots.rendered import field_blocks, json_value

EVIDENCE_FIELDS = ("source_evidence", "lesson_content")
"""Every input field that carries teaching evidence: the shared contract's, and the
grounded per-level contract's."""


def rendered_evidence(call: PreparedCall) -> list[dict[str, Any]]:
    """Every evidence item in the call's rendered user message, whichever field carries it."""
    blocks = field_blocks(call)
    return [
        item
        for field in EVIDENCE_FIELDS
        if field in blocks
        for item in _items(json_value(blocks[field]))
    ]


def label_leaks(items: list[dict[str, Any]], *, citations: list[str]) -> list[str]:
    """The items whose excerpt is a label rather than the content it stands for.

    Three ways a label reaches the model, all of which leave a populated ``excerpt``:
    the citation copied in as its own content, which is what an unresolved source does;
    the item's own title; and the reference id it is filed under.
    """
    leaks = []
    for item in items:
        excerpt = (item.get("excerpt") or "").strip()
        if not excerpt:
            leaks.append(f"{item.get('source_ref')!r} carries no excerpt at all")
            continue
        for name, label in (
            ("its citation", _matching(excerpt, citations)),
            ("its title", item.get("title")),
            ("its source_ref", item.get("source_ref")),
        ):
            if label and excerpt == str(label).strip():
                leaks.append(f"{excerpt[:60]!r} is {name}, not an excerpt of it")
                break
    return leaks


def _matching(excerpt: str, citations: list[str]) -> str | None:
    return next((c for c in citations if excerpt == c.strip()), None)


def _items(value: object) -> list[dict[str, Any]]:
    """The evidence items in a rendered field: a JSON list of them, or a lone one.

    A field that rendered as something other than an object is not an evidence item and
    carries nothing to check, so it is dropped rather than read for an ``excerpt``.
    """
    candidates = value if isinstance(value, list) else [value]
    return [item for item in candidates if isinstance(item, dict)]
