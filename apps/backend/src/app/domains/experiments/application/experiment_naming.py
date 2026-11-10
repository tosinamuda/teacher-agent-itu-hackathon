"""Experiment naming + presentation labels — pure formatters, no DB.

The five helpers below own ``experiment_code`` generation (per-workspace prefix
+ term/grade/subject segments) and the two presentation labels the dashboard
reads. They are stateless and side-effect free, so they live as module-level
functions rather than service methods — one decision per function (Rule 3), no
``self`` plumbing.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Protocol

from app.domains.teaching.models import TeacherWorkspace


class PlanVersionLabelData(Protocol):
    """Plan-version fields required to render an experiment label."""

    version_id: str
    approved_at: datetime | None


def normalize_segment(value: str | None, fallback: str) -> str:
    """Uppercase + collapse non-alphanumerics to ``-``; return ``fallback`` if empty."""
    if value is None:
        return fallback
    cleaned = re.sub(r"[^A-Z0-9]+", "-", value.upper()).strip("-")
    return cleaned or fallback


def term_code(term: str | None) -> str:
    """Return ``T1``/``T2``/``T3`` for first/second/third term phrasing, else a slug."""
    normalized = (term or "").strip().lower()
    if "first" in normalized or "1st" in normalized or normalized.endswith("1"):
        return "T1"
    if "second" in normalized or "2nd" in normalized or normalized.endswith("2"):
        return "T2"
    if "third" in normalized or "3rd" in normalized or normalized.endswith("3"):
        return "T3"
    return normalize_segment(term, "TERM")


def workspace_name(workspace: TeacherWorkspace) -> str:
    """Compose the dashboard workspace label — school · class · subject · term · teacher."""
    school = (
        workspace.term_class_subject.classroom.school.name
        if workspace.term_class_subject
        and workspace.term_class_subject.classroom
        and workspace.term_class_subject.classroom.school
        else "School"
    )
    class_name = (
        workspace.term_class_subject.classroom.name
        if workspace.term_class_subject and workspace.term_class_subject.classroom
        else "Class"
    )
    subject = (
        workspace.term_class_subject.course.subject.name
        if workspace.term_class_subject and workspace.term_class_subject.course
        else "Subject"
    )
    term = workspace.term_class_subject.term if workspace.term_class_subject else "Term"
    teacher = workspace.teacher.full_name or "Teacher" if workspace.teacher else "Teacher"
    return " · ".join([school, class_name, subject, term, teacher])


def baseline_version_label(plan_version: PlanVersionLabelData) -> str:
    """Render a plan-version label ("vN · approved DD Mon YYYY" when approved)."""
    if plan_version.approved_at is not None:
        stamp = plan_version.approved_at.strftime("%d %b %Y")
        return f"{plan_version.version_id} · approved {stamp}"
    return plan_version.version_id


def experiment_code_prefix(workspace: TeacherWorkspace) -> str:
    """Build the per-workspace ``experiment_code`` prefix (EXP-SCH-GRADE-SUBJ-Tn)."""
    school_code = (
        workspace.term_class_subject.classroom.school.code
        if workspace.term_class_subject
        and workspace.term_class_subject.classroom
        and workspace.term_class_subject.classroom.school
        else None
    )
    grade_level = (
        workspace.term_class_subject.course.grade_level.name
        if workspace.term_class_subject and workspace.term_class_subject.course
        else None
    )
    subject_code = (
        workspace.term_class_subject.course.subject.code
        if workspace.term_class_subject and workspace.term_class_subject.course
        else None
    )
    term = workspace.term_class_subject.term if workspace.term_class_subject else None
    return "-".join(
        [
            "EXP",
            normalize_segment(school_code, "SCH"),
            normalize_segment(grade_level, "GRADE"),
            normalize_segment(subject_code, "SUBJ"),
            term_code(term),
        ]
    )
