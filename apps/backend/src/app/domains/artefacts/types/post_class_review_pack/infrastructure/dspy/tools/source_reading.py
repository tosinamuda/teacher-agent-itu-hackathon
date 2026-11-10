"""Read-only tools that expose approved source material to an LLM.

A ``Toolset`` maps one condition-filtered request and generation unit to the
approved reading capabilities exposed for that model call.
"""

from __future__ import annotations

from collections.abc import Callable

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)

Toolset = Callable[[ReviewPackRequest, SectionGenerationUnit], list]


def numbered(lines: list[str], start_line: int, end_line: int | None) -> str:
    """Lines as the tools show them: 1-indexed, inclusive, each prefixed by its number."""
    start = max(start_line, 1)
    end = len(lines) if end_line is None else min(end_line, len(lines))
    return "\n".join(
        f"{index}: {line}" for index, line in enumerate(lines[start - 1 : end], start=start)
    )


def reading_tools(unit: SectionGenerationUnit) -> list:
    """File-style tools over one unit's evidence documents.

    A document's declared regions are offered as documents in their own right, so a
    reader can ask for "the properties of a cylinder" by name. That address survives
    editing; a line number does not, because it moves the moment anyone changes a word
    above it. Plans that declare no regions are unaffected and still read by line.
    """
    documents: dict[str, tuple[str, str]] = {}
    for item in unit.source_evidence:
        documents[item.source_ref] = (item.title or "", item.excerpt)
        for region in item.regions:
            documents[region.region_id] = (region.title, region.excerpt)

    def list_documents() -> list[dict]:
        """List the source documents available to read: name, title, and total lines."""
        return [
            {"document": ref, "title": title, "lines": len(excerpt.splitlines())}
            for ref, (title, excerpt) in documents.items()
        ]

    def read_document(document: str, start_line: int = 1, end_line: int | None = None) -> str:
        """Read a source document (1-indexed, inclusive). Omit end_line to read to the end."""
        found = documents.get(document)
        if found is None:
            return f"No document named {document!r}. Available: {sorted(documents)}"
        lines = found[1].splitlines()
        if max(start_line, 1) > len(lines):
            return f"{document} has only {len(lines)} lines."
        return numbered(lines, start_line, end_line)

    return [list_documents, read_document]


def evidence_toolset() -> Toolset:
    """Sources arrive on the unit."""
    return lambda request, unit: reading_tools(unit)
