"""P5.7 — synthetic research-fixture lesson_period for the 5 outlier lesson_plans.

The audit-flagged polymorphic ``lesson_plans.session_id`` column has two kinds
of values in live data: 14 of 19 rows hold a stringified UUID pointing at a
``lesson_periods.id`` (the canonical execution-side path), and 5 of 19 hold a
curriculum-side `class_sessions.session_id` from early dev/research runs that
were generated against the NERDC curriculum directly, before the
teacher-workspace + scheme_of_work flow existed end-to-end.

The user's chosen direction (recorded in
``docs/domain-architecture-baseline.md`` "Canonical Lesson Chain"): make
``lesson_period`` the canonical execution entity for `lesson_plan`. To do
that without dropping data, this function builds a clearly-labeled
``research_*`` execution context (school -> class -> teacher -> workspace
-> scheme_of_work -> lesson_period) so the 5 outliers can FK into a real
``lesson_periods.id`` like everything else.

Idempotent: every ``INSERT`` is gated on a lookup so re-running this against
a database that already has the fixture is a no-op. The 5 outlier rows are
repointed only when their ``session_id`` matches the curriculum-side literal;
rows already pointing at a UUID are left alone.

Invocation: see ``scripts/seed_research_lesson_period_fixture.py``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import sqlalchemy as sa

_RESEARCH_SCHOOL_CODE = "RES"
_RESEARCH_SCHOOL_NAME = "Research Fixture School"
_RESEARCH_CLASS_NAME = "Research Fixture Class"
_RESEARCH_TEACHER_AUTH_ID = "research-fixture-teacher"
_RESEARCH_TEACHER_EMAIL = "research-fixture@plan-to-tutor.local"
_RESEARCH_TEACHER_NAME = "Research Fixture Teacher"
_RESEARCH_TERM = "Research"
_RESEARCH_YEAR = "Research"
_RESEARCH_SCHEME_TITLE = "Research fixture week (P5.7 outlier home)"
_RESEARCH_PERIOD_TITLE = "Research fixture period (P5.7 outlier home)"

# The curriculum-side literal that the 5 outliers share. Anything else is
# either already a UUID-string for a real lesson_period or out of scope.
_OUTLIER_SESSION_ID = "session-jss1-math-whole-numbers-millions-and-billions"
_OUTLIER_SUBTOPIC_ID = "jss1-math-whole-numbers-millions-and-billions"
_RESEARCH_SUBJECT_NAME = "Mathematics"
_RESEARCH_GRADE_NAME = "JSS1"


@dataclass(frozen=True)
class _ResearchFixtureIds:
    """The UUIDs created (or rediscovered) by the fixture seed."""

    school_id: uuid.UUID
    class_id: uuid.UUID
    teacher_id: uuid.UUID
    course_id: uuid.UUID
    term_class_subject_id: uuid.UUID
    teacher_workspace_id: uuid.UUID
    scheme_of_work_id: uuid.UUID
    lesson_period_id: uuid.UUID
    outliers_repointed: int


def _existing_uuid(
    conn: sa.Connection, table: str, where_sql: str, params: dict[str, object]
) -> uuid.UUID | None:
    row = conn.execute(sa.text(f"SELECT id FROM {table} WHERE {where_sql} LIMIT 1"), params).first()
    return None if row is None else row[0]


def seed_research_lesson_period_fixture(conn: sa.Connection) -> _ResearchFixtureIds:
    """Build (or rediscover) the synthetic research execution context.

    Steps:
    1. Look up the existing `subjects` / `grade_levels` rows for "Mathematics"
       and "JSS1" (the curriculum that the 5 outlier plans belong to).
       These are not synthetic — they're seeded as part of the normal curriculum
       boot. Aborting if they're absent surfaces a real environment problem.
    2. Idempotently create the research school, class, teacher, course,
       term_class_subject, teacher_workspace, scheme_of_work, and lesson_period
       — each gated on a "does it exist by its distinguishing key" lookup.
    3. Re-point any ``lesson_plans.session_id`` row whose current value is the
       curriculum-side literal to the research lesson_period's UUID, as text.
    """
    subject_row = conn.execute(
        sa.text("SELECT id FROM subjects WHERE name = :name"),
        {"name": _RESEARCH_SUBJECT_NAME},
    ).first()
    if subject_row is None:
        raise RuntimeError(
            f"curriculum subject '{_RESEARCH_SUBJECT_NAME}' not found — seed the "
            "curriculum before applying the research fixture"
        )
    subject_id: uuid.UUID = subject_row[0]

    grade_row = conn.execute(
        sa.text("SELECT id FROM grade_levels WHERE name = :name"),
        {"name": _RESEARCH_GRADE_NAME},
    ).first()
    if grade_row is None:
        raise RuntimeError(
            f"curriculum grade_level '{_RESEARCH_GRADE_NAME}' not found — seed the "
            "curriculum before applying the research fixture"
        )
    grade_level_id: uuid.UUID = grade_row[0]

    school_id = _existing_uuid(
        conn, "schools", "code = :code", {"code": _RESEARCH_SCHOOL_CODE}
    ) or _insert_school(conn)
    class_id = _existing_uuid(
        conn,
        "classes",
        "school_id = :sid AND grade_level_id = :gid AND name = :name",
        {"sid": school_id, "gid": grade_level_id, "name": _RESEARCH_CLASS_NAME},
    ) or _insert_class(conn, school_id=school_id, grade_level_id=grade_level_id)
    teacher_id = _existing_uuid(
        conn, "teachers", "auth_id = :auth_id", {"auth_id": _RESEARCH_TEACHER_AUTH_ID}
    ) or _insert_teacher(conn)
    course_id = _existing_uuid(
        conn,
        "courses_curriculum",
        "subject_id = :sid AND grade_level_id = :gid",
        {"sid": subject_id, "gid": grade_level_id},
    ) or _insert_course(conn, subject_id=subject_id, grade_level_id=grade_level_id)
    term_class_subject_id = _existing_uuid(
        conn,
        "term_class_subjects",
        "course_id = :cid AND class_id = :clsid AND term = :term",
        {"cid": course_id, "clsid": class_id, "term": _RESEARCH_TERM},
    ) or _insert_term_class_subject(conn, course_id=course_id, class_id=class_id)
    teacher_workspace_id = _existing_uuid(
        conn,
        "teacher_workspaces",
        "teacher_id = :tid AND term_class_subject_id = :tcsid",
        {"tid": teacher_id, "tcsid": term_class_subject_id},
    ) or _insert_teacher_workspace(
        conn, teacher_id=teacher_id, term_class_subject_id=term_class_subject_id
    )
    scheme_of_work_id = _existing_uuid(
        conn,
        "scheme_of_work",
        "term_class_subject_id = :tcsid AND title = :title",
        {"tcsid": term_class_subject_id, "title": _RESEARCH_SCHEME_TITLE},
    ) or _insert_scheme_of_work(conn, term_class_subject_id=term_class_subject_id)
    lesson_period_id = _existing_uuid(
        conn,
        "lesson_periods",
        "scheme_of_work_id = :sid AND title = :title",
        {"sid": scheme_of_work_id, "title": _RESEARCH_PERIOD_TITLE},
    ) or _insert_lesson_period(conn, scheme_of_work_id=scheme_of_work_id)

    repoint_result = conn.execute(
        sa.text("UPDATE lesson_plans SET session_id = :new_id WHERE session_id = :old_id"),
        {"new_id": str(lesson_period_id), "old_id": _OUTLIER_SESSION_ID},
    )
    outliers_repointed = repoint_result.rowcount or 0

    return _ResearchFixtureIds(
        school_id=school_id,
        class_id=class_id,
        teacher_id=teacher_id,
        course_id=course_id,
        term_class_subject_id=term_class_subject_id,
        teacher_workspace_id=teacher_workspace_id,
        scheme_of_work_id=scheme_of_work_id,
        lesson_period_id=lesson_period_id,
        outliers_repointed=outliers_repointed,
    )


def _insert_school(conn: sa.Connection) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text("INSERT INTO schools (id, name, code) VALUES (:id, :name, :code)"),
        {"id": new_id, "name": _RESEARCH_SCHOOL_NAME, "code": _RESEARCH_SCHOOL_CODE},
    )
    return new_id


def _insert_class(
    conn: sa.Connection, *, school_id: uuid.UUID, grade_level_id: uuid.UUID
) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO classes (id, name, grade_level_id, school_id) "
            "VALUES (:id, :name, :gid, :sid)"
        ),
        {
            "id": new_id,
            "name": _RESEARCH_CLASS_NAME,
            "gid": grade_level_id,
            "sid": school_id,
        },
    )
    return new_id


def _insert_teacher(conn: sa.Connection) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO teachers (id, auth_id, email, full_name, role) "
            "VALUES (:id, :auth_id, :email, :name, 'teacher')"
        ),
        {
            "id": new_id,
            "auth_id": _RESEARCH_TEACHER_AUTH_ID,
            "email": _RESEARCH_TEACHER_EMAIL,
            "name": _RESEARCH_TEACHER_NAME,
        },
    )
    return new_id


def _insert_course(
    conn: sa.Connection, *, subject_id: uuid.UUID, grade_level_id: uuid.UUID
) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO courses_curriculum (id, name, subject_id, grade_level_id) "
            "VALUES (:id, :name, :sid, :gid)"
        ),
        {
            "id": new_id,
            "name": f"{_RESEARCH_SUBJECT_NAME} {_RESEARCH_GRADE_NAME} (research)",
            "sid": subject_id,
            "gid": grade_level_id,
        },
    )
    return new_id


def _insert_term_class_subject(
    conn: sa.Connection, *, course_id: uuid.UUID, class_id: uuid.UUID
) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO term_class_subjects (id, course_id, term, year, class_id) "
            "VALUES (:id, :cid, :term, :year, :clsid)"
        ),
        {
            "id": new_id,
            "cid": course_id,
            "term": _RESEARCH_TERM,
            "year": _RESEARCH_YEAR,
            "clsid": class_id,
        },
    )
    return new_id


def _insert_teacher_workspace(
    conn: sa.Connection, *, teacher_id: uuid.UUID, term_class_subject_id: uuid.UUID
) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO teacher_workspaces "
            "(id, teacher_id, term_class_subject_id, is_primary) "
            "VALUES (:id, :tid, :tcsid, false)"
        ),
        {"id": new_id, "tid": teacher_id, "tcsid": term_class_subject_id},
    )
    return new_id


def _insert_scheme_of_work(conn: sa.Connection, *, term_class_subject_id: uuid.UUID) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO scheme_of_work "
            "(id, term_class_subject_id, week_number, title) "
            "VALUES (:id, :tcsid, 1, :title)"
        ),
        {"id": new_id, "tcsid": term_class_subject_id, "title": _RESEARCH_SCHEME_TITLE},
    )
    return new_id


def _insert_lesson_period(conn: sa.Connection, *, scheme_of_work_id: uuid.UUID) -> uuid.UUID:
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO lesson_periods "
            "(id, scheme_of_work_id, period_number, subtopic_id, title) "
            "VALUES (:id, :sid, 1, :subtopic, :title)"
        ),
        {
            "id": new_id,
            "sid": scheme_of_work_id,
            "subtopic": _OUTLIER_SUBTOPIC_ID,
            "title": _RESEARCH_PERIOD_TITLE,
        },
    )
    return new_id
