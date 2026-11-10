"""The catalogues a researcher picks from when setting an experiment up.

Workspaces, their lessons, and the approved plan versions of one lesson —
rendered as the option DTOs the setup forms bind to.
"""

from __future__ import annotations

import uuid

from app.domains.experiments.api.schemas import (
    ExperimentApprovedVersionResponse,
    ExperimentLessonOptionResponse,
    ExperimentWorkspaceOptionResponse,
)
from app.domains.experiments.application import experiment_naming
from app.domains.experiments.application.experiment_context_service import (
    ExperimentWorkspaceCatalogueReader,
    ExperimentWorkspaceCatalogueService,
)


async def list_workspace_options(
    experiments: ExperimentWorkspaceCatalogueReader,
    *,
    school_id: uuid.UUID | None,
    teacher_id: uuid.UUID | None = None,
) -> list[ExperimentWorkspaceOptionResponse]:
    """Render the workspace catalog as option DTOs (drops incomplete workspaces).

    When ``teacher_id`` is provided, only workspaces taught by that user are
    returned — the actor-derived scope filter for non-researcher callers.
    """
    context = ExperimentWorkspaceCatalogueService(experiments)
    workspaces = await context.list_workspace_options(school_id=school_id)
    responses: list[ExperimentWorkspaceOptionResponse] = []
    for workspace in workspaces:
        if workspace.term_class_subject is None or workspace.term_class_subject.course is None:
            continue
        classroom = workspace.term_class_subject.classroom
        school = classroom.school if classroom is not None else None
        course = workspace.term_class_subject.course
        subject = course.subject
        grade_level = course.grade_level
        teacher = workspace.teacher
        if (
            classroom is None
            or school is None
            or subject is None
            or grade_level is None
            or teacher is None
        ):
            continue
        if teacher_id is not None and teacher.id != teacher_id:
            continue
        responses.append(
            ExperimentWorkspaceOptionResponse(
                teacher_workspace_id=workspace.id,
                term_class_subject_id=workspace.term_class_subject.id,
                school_id=school.id,
                school_name=school.name,
                school_code=school.code,
                class_id=classroom.id,
                class_name=classroom.name,
                subject_name=subject.name,
                subject_code=subject.code,
                grade_level=grade_level.name,
                term=workspace.term_class_subject.term,
                academic_year=workspace.term_class_subject.year,
                teacher_id=teacher.id,
                teacher_name=teacher.full_name,
                workspace_name=experiment_naming.workspace_name(workspace),
                is_primary=workspace.is_primary,
            )
        )
    return responses


async def list_workspace_lesson_options(
    experiments: ExperimentWorkspaceCatalogueReader,
    *,
    workspace_id: uuid.UUID,
) -> list[ExperimentLessonOptionResponse]:
    """Lessons for a workspace + the under-research flag, rendered as option DTOs."""
    context = ExperimentWorkspaceCatalogueService(experiments)
    lessons = await context.list_workspace_lessons(workspace_id=workspace_id)
    under_study = await experiments.list_lesson_period_ids_with_experiments(
        teacher_workspace_id=workspace_id
    )
    return [
        ExperimentLessonOptionResponse(
            lesson_period_id=candidate.lesson_period.id,
            week_number=candidate.lesson_period.scheme_of_work.week_number,
            period_number=candidate.lesson_period.period_number,
            lesson_title=(
                candidate.lesson_period.title
                or (
                    candidate.lesson_period.subtopic.title
                    if candidate.lesson_period.subtopic
                    else "Lesson"
                )
            ),
            lesson_subtitle=(
                candidate.lesson_period.subtopic.title if candidate.lesson_period.subtopic else None
            ),
            approved_version_count=len(candidate.approved_versions),
            latest_approved_version_id=(
                candidate.approved_versions[0][0].version_id
                if candidate.approved_versions
                else None
            ),
            latest_approved_version_label=(
                experiment_naming.baseline_version_label(candidate.approved_versions[0][0])
                if candidate.approved_versions
                else None
            ),
            under_research_study=candidate.lesson_period.id in under_study,
        )
        for candidate in lessons
    ]


async def list_workspace_lesson_approved_versions(
    experiments: ExperimentWorkspaceCatalogueReader,
    *,
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
) -> list[ExperimentApprovedVersionResponse]:
    """Approved versions for a workspace+lesson, rendered as the API response DTO."""
    context = ExperimentWorkspaceCatalogueService(experiments)
    versions = await context.list_approved_versions_for_workspace_lesson(
        workspace_id=workspace_id,
        lesson_period_id=lesson_period_id,
    )
    return [
        ExperimentApprovedVersionResponse(
            plan_id=lesson_plan.plan_id,
            plan_version_id=plan_version.version_id,
            lesson_period_id=lesson_period.id,
            lesson_title=lesson_period.title
            or (lesson_period.subtopic.title if lesson_period.subtopic else lesson_plan.title),
            lesson_subtitle=lesson_period.subtopic.title if lesson_period.subtopic else None,
            version_label=experiment_naming.baseline_version_label(plan_version),
            approved_at=plan_version.approved_at,
            approved_by=plan_version.approved_by,
        )
        for plan_version, lesson_plan, lesson_period in versions
    ]
