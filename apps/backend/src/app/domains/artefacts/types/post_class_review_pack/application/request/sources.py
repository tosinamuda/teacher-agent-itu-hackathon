"""Lesson sources available to review-pack generation."""

from __future__ import annotations

from dataclasses import dataclass

from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources


@dataclass(frozen=True)
class LessonSource:
    """One lesson-plan citation paired with the content it makes available."""

    citation: str
    content: str
    record_id: str | None = None


@dataclass(frozen=True)
class LessonSources:
    """The ordered sources resolved for one frozen lesson plan, and which expert content is read."""

    items: tuple[LessonSource, ...] = ()
    expert: ExpertSources = ExpertSources.LESSON_NOTE

    @classmethod
    def unresolved(cls, citations: list[str]) -> LessonSources:
        """Represent citations whose external content could not be resolved."""
        return cls(
            items=tuple(
                LessonSource(citation=citation, content=citation)
                for citation in citations
                if citation
            )
        )
