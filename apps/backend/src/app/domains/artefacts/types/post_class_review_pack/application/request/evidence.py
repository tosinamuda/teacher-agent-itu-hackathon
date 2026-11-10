"""Project lesson-plan sources and figures into condition-scoped evidence."""

from typing import Literal

from app.domains.artefacts.types.lesson_plan.drafting.domain.note_figures import figures_in_text
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanStepView

from .schemas import SourceEvidenceItem, SourceFigure, SourceRegion
from .source_content import (
    block_text,
    drawings_as_references,
    without_review_markup,
)
from .sources import LessonSources

EVIDENCE_LABEL = "the lesson note"

FigureSource = Literal["reference", "source"]
"""Whether a drawing reaches the model as a reference label or as its own source."""


def declared_regions(
    regions: list[JsonObject],
    step_id: str,
    figures: FigureSource,
) -> list[SourceRegion]:
    """The note's declared parts, each treated the way the whole note is treated.

    A region's text goes through the same figure policy as the note it came from, so a
    reader cannot reach drawing source through a part that the whole withheld. Empty for
    a plan that declares no regions, which is every plan the app drafts today.
    """
    declared = []
    for region in regions:
        body = str(region.get("body") or "").strip()
        if not body:
            continue
        readable = without_review_markup(body)
        declared.append(
            SourceRegion(
                region_id=str(region.get("id") or ""),
                title=str(region.get("title") or ""),
                excerpt=(
                    readable if figures == "source" else drawings_as_references(readable, step_id)
                ),
            )
        )
    return declared


def reads_lesson_note(policy: ReviewPackGenerationPolicy) -> bool:
    """Whether a condition's generation reads each step's lesson note.

    ``for_step`` states the same test inline: its source is part of the evaluated pipeline's
    fingerprint, so it is not rewritten to call this. A test holds the two to one answer.
    """
    return policy.retrieval.enabled and policy.retrieval.evidence_scope in {
        "objective",
        "step",
        "unit",
    }


class SourceEvidenceProjector:
    """Build source evidence and attached figures under the retrieval policy."""

    def __init__(self, *, figures: FigureSource = "reference") -> None:
        self._figures = figures

    def for_step(
        self,
        step: SessionPlanStepView,
        policy: ReviewPackGenerationPolicy,
    ) -> list[SourceEvidenceItem]:
        """Build the step's own lesson-note evidence when its condition allows it."""
        if not policy.retrieval.enabled or policy.retrieval.evidence_scope not in {
            "objective",
            "step",
            "unit",
        }:
            return []
        note = (step.note or "").strip() or "\n\n".join(
            filter(None, (block_text(block) for block in step.blocks))
        )
        if not note:
            return []
        readable = without_review_markup(note)
        excerpt = (
            readable
            if self._figures == "source"
            else drawings_as_references(readable, step.step_id)
        )
        return [
            SourceEvidenceItem(
                source_ref=EVIDENCE_LABEL,
                excerpt=excerpt,
                regions=declared_regions(step.regions, step.step_id, self._figures),
            )
        ]

    @staticmethod
    def for_plan(
        sources: LessonSources,
        policy: ReviewPackGenerationPolicy,
    ) -> list[SourceEvidenceItem]:
        """Build plan-source evidence within the policy's item cap."""
        if not policy.retrieval.provides_evidence:
            return []
        limit = policy.retrieval.max_evidence_items_per_unit
        return [
            SourceEvidenceItem(
                source_ref=f"REF-{index}",
                excerpt=source.content,
                title=source.citation if source.content != source.citation else None,
            )
            for index, source in enumerate(sources.items[:limit], start=1)
        ]

    @staticmethod
    def figures_for_step(
        step: SessionPlanStepView,
        policy: ReviewPackGenerationPolicy,
        objective_id: str,
    ) -> list[SourceFigure]:
        """Carry source-derived figures only into evidence-enabled conditions."""
        if not policy.retrieval.provides_evidence:
            return []
        figures: list[SourceFigure] = [
            SourceFigure(
                figure_id=str(figure["id"]),
                variant="diagram_tikz",
                figure_ref=figure.get("figure_ref"),
                caption=figure.get("caption"),
                source_tikz=str(figure["source_tikz"]),
            )
            for figure in figures_in_text(step.note or "", step.step_id)
        ]
        seen: set[str] = set()
        for index, block in enumerate(step.blocks):
            if not isinstance(block, dict) or str(block.get("type") or "").strip() != "visual":
                continue
            url = str(block.get("url") or "").strip()
            record_id = str(block.get("source_record_id") or "").strip()
            if not url or not record_id or url in seen:
                continue
            seen.add(url)
            figures.append(
                SourceFigure(
                    figure_id=str(block.get("id") or f"{step.step_id}:fig{index}"),
                    variant="image",
                    url=url,
                    caption=(str(block.get("caption") or "").strip() or None),
                    source_record_id=record_id,
                )
            )
        return figures
