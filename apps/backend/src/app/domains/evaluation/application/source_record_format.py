"""Friendly labels for textbook source-record identifiers.

The expert-content domain stores citable textbook positions as stable opaque
ids like ``ch02-b031`` (chapter 2, block 31) or ``ch01-b041-i01`` (item 1 of
block 41 in chapter 1). Those identifiers are correct for analysis paths but
read awkwardly to a rater scanning a worksheet — the rater wants to see
"Chapter 2 — Block 31" so they can locate the cited passage in the printed
textbook quickly.

This module is a pure presentation helper: the raw id stays on the wire for
research; the friendly label is rendered into the rater-facing surfaces
(audit pack PDF + online audit item view).
"""

from __future__ import annotations

import re

# ``chXX-bYY`` is the canonical block id; the optional trailing
# ``-something`` (most commonly ``-iNN`` for inline images / sub-items) is
# preserved verbatim in parentheses so we never silently drop information.
_RECORD_ID_RE = re.compile(r"^ch(\d+)-b(\d+)(?:-(.+))?$", re.IGNORECASE)


def friendly_source_record_id(record_id: str | None) -> str | None:
    """Render a textbook block id as a rater-friendly label.

    ``ch02-b031`` → ``"Chapter 2 — Block 31"``; ``ch01-b041-i01`` →
    ``"Chapter 1 — Block 41 (i01)"``. Returns the original string unchanged
    if it does not look like a canonical block id, and ``None`` for ``None``
    input — so callers can render either the friendly form or fall back to
    the raw id without branching.
    """
    if record_id is None:
        return None
    text = record_id.strip()
    if not text:
        return None
    match = _RECORD_ID_RE.match(text)
    if match is None:
        return text
    chapter = int(match.group(1))
    block = int(match.group(2))
    extra = match.group(3)
    base = f"Chapter {chapter} — Block {block}"
    return f"{base} ({extra})" if extra else base
