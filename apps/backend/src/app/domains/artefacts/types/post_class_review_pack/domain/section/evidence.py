"""Pure evidence projection for generated and personalised sections."""

from __future__ import annotations

import re

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)

from .schemas import ReviewPackSection

_REF_MENTION = re.compile(r"REF[-‑]\d+")


def section_cited_refs(section: ReviewPackSection) -> set[str]:
    """Return source refs carried structurally or cited inline by a section."""
    refs = set(section.source_refs)
    for block in section.blocks:
        refs.update(block.source_refs)
        if block.text:
            refs.update(match.replace("‑", "-") for match in _REF_MENTION.findall(block.text))
    return {ref for ref in refs if ref}


def scope_unit_evidence(
    unit: SectionGenerationUnit,
    base_section: ReviewPackSection,
) -> SectionGenerationUnit:
    """Restrict personalisation evidence to sources cited by the approved base."""
    cited = section_cited_refs(base_section)
    scoped = [item for item in unit.source_evidence if item.source_ref in cited]
    if not scoped:
        return unit
    return unit.model_copy(update={"source_evidence": scoped})


def unit_for_personalisation_repair(
    unit: SectionGenerationUnit,
    base_section: ReviewPackSection,
) -> SectionGenerationUnit:
    """Restrict a repair unit to the context available during personalisation."""
    return clear_unit_fields(
        scope_unit_evidence(unit, base_section),
        {
            "source_step_id": None,
            "step_title": None,
            "step_content": None,
            "instructional_type": None,
            "estimated_minutes": None,
            "current_step": None,
            "instructional_events": [],
            "student_tasks": [],
            "activities": [],
            "assessment_points": [],
        },
    )


def clear_unit_fields(
    unit: SectionGenerationUnit,
    cleared_fields: dict[str, object],
) -> SectionGenerationUnit:
    """Clear known unit fields and reject stale field names deterministically."""
    unknown = set(cleared_fields) - set(type(unit).model_fields)
    if unknown:
        raise AttributeError(f"cannot clear fields that do not exist: {sorted(unknown)}")
    return unit.model_copy(update=cleared_fields)
