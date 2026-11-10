"""Build source-grounding audit items from generated packs (Final Evaluation Protocol §5).

An audit item pairs one generated excerpt with the textbook source it cites, plus the
lesson objective and scope boundary, so an audit rater can check (0/1/2) whether the
source is relevant, sufficient, faithful, and in-scope. Audit applies to the
textbook-grounded conditions only (C2-C4); C0/C1 use no explicit source evidence.

This module is pure (no I/O): it parses manifests + reference lists into candidate
audit-item dicts and samples them deterministically. Persistence + source-snippet
fetching live in the evaluation service.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    ExplanationBlock,
    VisualBlock,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.shared.json_types import JsonObject

AUDIT_CONDITIONS = ("C2", "C3", "C4")
AUDIT_SAMPLE_CAP = 45

_REF_TOKEN = re.compile(r"REF-\d+")
# Trailing "(ch01-b029)" / "(ch01-b041-i01)" internal record id on a reference string.
_RECORD_ID_SUFFIX = re.compile(r"\(([^()]+)\)\s*$")
# A trailing italic "_Sources: REF-1, REF-2_" footer line appended to block content.
_SOURCES_FOOTER = re.compile(r"(?im)^[ \t]*_?\s*sources?:[^\n]*$")
_MAX_EXCERPT_CHARS = 700


def reference_record_map(references: Sequence[str]) -> dict[str, str]:
    """Map ``REF-1``..``REF-N`` to the textbook ``record_id`` parsed from each reference.

    Mirrors ``SourceEvidenceProjector.for_plan`` which assigns ``REF-{index}``
    to ``references[index-1]``;
    the record id is the parenthesised suffix, e.g. ``"Chapter 1 (ch01-b029)" -> "ch01-b029"``.
    """
    mapping: dict[str, str] = {}
    for index, reference in enumerate(references, start=1):
        match = _RECORD_ID_SUFFIX.search(str(reference).strip())
        if match:
            mapping[f"REF-{index}"] = match.group(1).strip()
    return mapping


def _excerpt(content: str) -> str:
    text = _SOURCES_FOOTER.sub("", content).strip()
    if len(text) > _MAX_EXCERPT_CHARS:
        text = text[:_MAX_EXCERPT_CHARS].rstrip() + "…"
    return text


def _cited_refs(block: ExplanationBlock) -> list[str]:
    """The refs this block is grounded in, deduplicated, in first-seen order.

    The structured field is authoritative. Scanning the prose is the fallback
    for packs stored before the field existed, when a "_Sources:" footer was the
    only channel — and it is a fallback rather than a supplement on purpose: an
    inline ``(REF-1)`` in a NEW pack is a policy violation (the text must read as
    prose to a student), not a citation to audit against.
    """
    tokens = block.source_refs or _REF_TOKEN.findall(block.content)
    seen: set[str] = set()
    ordered: list[str] = []
    for token in tokens:
        if token not in seen:
            seen.add(token)
            ordered.append(token)
    return ordered


def figures_by_record_id(pack: PostClassReviewPack) -> dict[str, dict[str, str | None]]:
    """Map each cited textbook ``record_id`` to the ``VisualBlock`` it points at.

    Walks the typed pack and returns ``{record_id: {"url": ..., "caption": ...}}``
    for every ``VisualBlock`` carrying both a ``source_record_id`` and a ``url``.
    Used by the audit pipeline to render the cited figure beside the source
    snippet when the cited record is a figure; text-only records yield no entry
    and the renderer falls back to text-only.

    The pack's discriminated-union ``ContentBlock`` makes ``isinstance(block,
    VisualBlock)`` safe — mirrors the same check ``candidate_audit_items`` uses
    for ``ExplanationBlock``. One ``VisualBlock`` per ``source_record_id`` is the
    typical case; on the off chance the same record is referenced twice in a
    single pack, last-write wins (URL/caption are stable per record).
    """
    figures: dict[str, dict[str, str | None]] = {}
    for step in pack.steps:
        for block in step.blocks:
            if not isinstance(block, VisualBlock):
                continue
            record_id = (block.source_record_id or "").strip()
            url = (block.url or "").strip()
            if not record_id or not url:
                continue
            figures[record_id] = {
                "url": url,
                "caption": (block.caption or None),
            }
    return figures


def candidate_audit_items(
    *,
    condition_code: str,
    condition_run_id: str,
    lesson_id: str | None,
    pack: PostClassReviewPack,
    objective_text_by_id: Mapping[str, str],
    scope_boundary: str | None,
) -> list[JsonObject]:
    """One candidate audit item per (explanation block, distinct cited ``REF-N``).

    Walks the typed ``PostClassReviewPack`` directly — the caller validates the
    JSON manifest once at the boundary, this function never does ``dict.get()``
    or isinstance-narrowing. Only ``ExplanationBlock`` instances carry textual
    content that cites sources; the other block variants
    (visual / worked_example / practice) are skipped by ``isinstance``-on-type,
    which the discriminated-union ``ContentBlock`` makes safe.
    """
    items: list[JsonObject] = []
    for step in pack.steps:
        objective_id = step.lesson_objective_id or None
        for block in step.blocks:
            if not isinstance(block, ExplanationBlock):
                continue
            content = block.content
            if not content.strip():
                continue
            excerpt = _excerpt(content)
            for ref in _cited_refs(block):
                items.append(
                    {
                        "condition_code": condition_code,
                        "condition_run_id": condition_run_id,
                        "lesson_id": lesson_id,
                        "lesson_objective_id": objective_id,
                        "objective_text": objective_text_by_id.get(objective_id or ""),
                        "generated_excerpt": excerpt,
                        "source_ref": ref,
                        "scope_boundary": scope_boundary,
                    }
                )
    return items


def sample_items(
    items: list[JsonObject], *, cap: int = AUDIT_SAMPLE_CAP
) -> tuple[list[JsonObject], int]:
    """Cap the audit sample, keeping a balanced spread across conditions.

    Deterministic (round-robin by condition over the input order). Returns
    ``(kept, dropped_count)`` so callers can log what was dropped — no silent truncation.
    """
    if len(items) <= cap:
        return items, 0
    by_condition: dict[str, list[JsonObject]] = {}
    for item in items:
        by_condition.setdefault(str(item["condition_code"]), []).append(item)
    queues = [iter(group) for group in by_condition.values()]
    kept: list[JsonObject] = []
    progressed = True
    while len(kept) < cap and progressed:
        progressed = False
        for queue in queues:
            nxt = next(queue, None)
            if nxt is not None:
                kept.append(nxt)
                progressed = True
                if len(kept) >= cap:
                    break
    return kept, len(items) - len(kept)
