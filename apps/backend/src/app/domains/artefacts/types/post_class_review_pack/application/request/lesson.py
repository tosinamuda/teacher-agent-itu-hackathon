"""Project condition-allowed lesson-level context into a generation request."""

from dataclasses import dataclass

from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.shared.session_plan_view import SessionPlanView

from .schemas import LessonContextForGeneration


@dataclass(frozen=True)
class _GlobalLessonContext:
    """The lesson-wide fields exposed by one experimental condition."""

    subject: str
    grade_level: str
    topic: str
    subtopic: str | None
    term: str | None
    week: int | None
    curriculum_scope: str | None


def _project_global_context(
    plan: SessionPlanView,
    *,
    included: bool,
) -> _GlobalLessonContext:
    if not included:
        return _GlobalLessonContext("", "", "", None, None, None, None)
    return _GlobalLessonContext(
        subject=plan.subject or "",
        grade_level=plan.grade or "",
        topic=plan.topic or "",
        subtopic=plan.subtopic,
        term=plan.term,
        week=plan.week,
        curriculum_scope=plan.theme,
    )


def _project_objectives(plan: SessionPlanView, *, included: bool) -> list[str]:
    if not included:
        return []
    return [
        objective.objective_text
        for objective in plan.lesson_plan_objectives
        if objective.objective_text
    ]


def _project_text_items(items: list[str], *, included: bool) -> list[str]:
    if not included:
        return []
    return [item for item in items if item]


def project_lesson_context(
    plan: SessionPlanView,
    policy: ReviewPackGenerationPolicy,
) -> LessonContextForGeneration:
    """Return only the lesson-level fields allowed by the condition policy."""
    context = policy.context
    global_context = _project_global_context(
        plan,
        included=context.include_global_lesson_context,
    )
    return LessonContextForGeneration(
        subject=global_context.subject,
        grade_level=global_context.grade_level,
        topic=global_context.topic,
        subtopic=global_context.subtopic,
        term=global_context.term,
        week=global_context.week,
        curriculum_scope=global_context.curriculum_scope,
        lesson_objectives=_project_objectives(
            plan,
            included=context.include_lesson_objectives,
        ),
        entry_behaviour=_project_text_items(
            plan.entry_behaviour,
            included=context.include_entry_behaviour,
        ),
        instructional_materials=_project_text_items(
            plan.instructional_materials,
            included=context.include_materials,
        ),
    )
