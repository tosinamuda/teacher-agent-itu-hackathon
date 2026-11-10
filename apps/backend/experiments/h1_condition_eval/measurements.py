"""Derive reproducible measurements from one generated H1 study pack."""

import hashlib
import re
from typing import Any

from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    WRITTEN_PRACTICE_FIELDS,
)
from app.shared.llm_html import count_html_tags
from app.shared.llm_markup import count_bare_math

_INLINE_REF = re.compile(r"REF[-‐-―−\s]*\d+", re.IGNORECASE)
_EATEN_COMMAND = re.compile(r"[\t\b\f][a-zA-Z]")


def evidence_record(units: list[Any]) -> list[dict[str, Any]]:
    """Record the identity and digest of every evidence item given to a unit."""
    return [
        {
            "unit_id": unit.unit_id,
            "source_ref": item.source_ref,
            "chars": len(item.excerpt),
            "sha256": hashlib.sha256(item.excerpt.encode()).hexdigest()[:12],
        }
        for unit in units
        for item in (unit.source_evidence or [])
    ]


def reader_facing_text(sections: list[Any]) -> str:
    """Every string a learner reads in these sections, one field per line.

    Block text, figure captions, and each written practice field. A leak in a
    practice answer is a leak, and the practice is where most of the maths sits.
    """
    parts: list[str] = []
    for section in sections:
        for block in section.blocks:
            parts += [block.text or "", block.caption or ""]
        for item in section.practice:
            parts += [getattr(item, field) or "" for field in WRITTEN_PRACTICE_FIELDS]
    return "\n".join(part for part in parts if part)


def pack_metrics(sections: list[Any]) -> dict[str, int]:
    """Measure section shape and the markup that would reach a reader as source."""
    blocks = [block for section in sections for block in section.blocks]
    text = reader_facing_text(sections)
    return {
        "sections": len(sections),
        "blocks": len(blocks),
        "chars": len("\n".join(block.text or "" for block in blocks)),
        "blocks_with_source_refs": sum(1 for block in blocks if block.source_refs),
        "inline_ref_markers": len(_INLINE_REF.findall(text)),
        # Commands that reach the reader as a backslash, NOT every command in the
        # pack: this counted `\times` and `\text{` whether or not they were
        # delimited, so a correctly typeset pack scored as badly as a broken one.
        # Counted over every reader-facing field, not block text alone, so a run
        # measured under either earlier definition is not comparable.
        "raw_latex_markers": count_bare_math(text),
        # Tags a reader would see as literal angle brackets: every surface escapes
        # before it converts markdown, so `<strong>` is never rendered, only shown.
        "html_markers": count_html_tags(text),
    }


def validation_metrics(result: GeneratedReviewPack) -> dict[str, Any]:
    """Measure what validation caught before repair and across later rounds."""
    validation = result.validation_before_repair
    if validation is None:
        return {
            "validated": False,
            "passed": "",
            "repaired": "",
            "findings": 0,
            "findings_text": [],
        }
    failed = [check for check in validation.checks if not check.passed]
    findings = [item for check in failed for item in (check.details or {}).get("findings", [])]
    per_round = [
        [
            item
            for check in round_result.checks
            if not check.passed
            for item in (check.details or {}).get("findings", [])
        ]
        for round_result in result.validation_rounds
    ]
    return {
        "validated": True,
        "passed": result.validation.passed if result.validation else "",
        "repaired": result.repaired,
        "findings": len(findings),
        "findings_text": findings,
        "failed_checks": ", ".join(check.check for check in failed),
        "repair_rounds": max(len(per_round) - 1, 0),
        "findings_per_round": [len(items) for items in per_round],
        "later_round_findings": [item for items in per_round[1:] for item in items],
    }


def eaten_latex_commands(rows: list[dict]) -> list[str]:
    r"""Return cells whose prose contains a control character from malformed LaTeX."""
    return [
        f"{row['lesson']}/{row['condition']}"
        for row in rows
        for section in row.get("sections_json") or []
        for block in section.get("blocks") or []
        if _EATEN_COMMAND.search(block.get("text") or "")
    ]
