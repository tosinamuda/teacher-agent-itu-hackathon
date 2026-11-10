"""Render an editor highlight for a revision reviser prompt.

Each artefact reviser (lesson plan, study pack, diagnostic) feeds the teacher's
selected highlight to the LLM as a short anchor + quoted-text string. The format is
identical across artefact types; only the set of anchor keys differs, so it is
passed in.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.shared.json_types import JsonObject


def format_highlight(highlight: JsonObject | None, anchor_keys: Sequence[str]) -> str:
    """Format a highlight as ``anchor: k=v, ... | selected text: "..."`` (empty if none)."""
    if not highlight:
        return ""
    anchors = [f"{key}={highlight[key]}" for key in anchor_keys if highlight.get(key)]
    selected = str(highlight.get("selected_text") or "").strip()
    parts: list[str] = []
    if anchors:
        parts.append("anchor: " + ", ".join(anchors))
    if selected:
        parts.append(f'selected text: "{selected}"')
    return " | ".join(parts)
