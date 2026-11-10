"""Resolve the sources named by a frozen lesson plan."""

from app.domains.expert_content.application.excerpt_resolver import reference_record_id
from app.domains.expert_content.application.excerpts_port import ExcerptsPort
from app.shared.session_plan_view import SessionPlanView

from .sources import LessonSource, LessonSources


async def resolve_lesson_sources(excerpts: ExcerptsPort, plan: SessionPlanView) -> LessonSources:
    """Pair each lesson-plan citation with its resolved or literal content."""
    citations = tuple(reference for reference in plan.references if reference)
    resolved_content = await excerpts.excerpts_for(citations)
    sources: list[LessonSource] = []
    for citation in citations:
        record_id = reference_record_id(citation)
        sources.append(
            LessonSource(
                citation=citation,
                record_id=record_id,
                content=resolved_content.get(record_id, citation) if record_id else citation,
            )
        )
    return LessonSources(items=tuple(sources))
