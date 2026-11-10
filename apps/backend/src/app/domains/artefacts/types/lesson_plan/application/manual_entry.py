"""Assemble and check a hand-entered teacher lesson plan.

Pure helpers behind the manual-entry path (FD-01): a teacher supplies the lesson
*content*, while lesson identity and the curriculum-objective list are forced from
the lesson's ``SessionContext`` so a manual plan can only change content — never
which lesson (or which curriculum objectives) it is bound to. This mirrors the
manual-edit "force identity" rule, applied to a brand-new plan.
"""

from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.shared.json_types import JsonObject


def assemble_manual_session_plan(
    session_context: SessionContext,
    curriculum_objectives: list[JsonObject],
    content: JsonObject,
) -> JsonObject:
    """Merge teacher-supplied content with lesson identity + curriculum objectives.

    ``plan_id`` is a placeholder — ``persist_plan_version`` mints the real id.
    """
    session_plan = dict(content)
    session_plan["plan_id"] = "manual-pending"
    session_plan["session_id"] = session_context.session_id
    session_plan["subject"] = session_context.subject
    session_plan["track"] = session_context.track
    session_plan["grade"] = session_context.grade
    session_plan["term"] = session_context.term
    session_plan["week"] = session_context.week
    session_plan["topic"] = session_context.topic
    session_plan["subtopic"] = session_context.subtopic
    if session_context.theme:
        session_plan["theme"] = session_context.theme
    session_plan["curriculum_objectives"] = list(curriculum_objectives)
    return session_plan


def curriculum_mapping_issues(
    session_plan: JsonObject,
    curriculum_objectives: list[JsonObject],
) -> list[str]:
    """Lesson objectives whose ``curriculum_objective_id`` is missing or unknown.

    Returns one message per unmapped objective; an empty list means every lesson
    objective maps to one of the lesson's curriculum objectives.
    """
    valid_ids = {
        str(objective.get("curriculum_objective_id") or "").strip()
        for objective in curriculum_objectives
    }
    valid_ids.discard("")

    issues: list[str] = []
    objectives = session_plan.get("lesson_plan_objectives")
    if not isinstance(objectives, list):
        return issues
    for objective in objectives:
        if not isinstance(objective, dict):
            continue
        curriculum_objective_id = str(objective.get("curriculum_objective_id") or "").strip()
        label = str(objective.get("lesson_objective_id") or "").strip() or "(unnamed)"
        if not curriculum_objective_id:
            issues.append(f"{label}: no curriculum_objective_id")
        elif curriculum_objective_id not in valid_ids:
            issues.append(
                f"{label}: curriculum_objective_id '{curriculum_objective_id}' "
                "is not a curriculum objective of this lesson"
            )
    return issues
