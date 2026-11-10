"""The MSc study's classwork, kept as the study recorded it: questions, scripts and answers.

The study's classwork was constructed response, marked by the teacher and coded for
misconceptions by the researcher. It is the evidence each learner's state was read from,
and fits none of the app's multiple-choice records, so it is kept here unchanged.
"""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID


class StudyClassworkQuestion(Base):
    """One question of a lesson's classwork, with the answer the study took as right."""

    __tablename__ = "study_classwork_questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("plan_versions.version_id", name="fk_study_questions_plan_version_id"),
        index=True,
    )
    #: Where the questions came from, e.g. ``step-t2w09-02:b4``, with any note on how they
    #: diverge from the plan as sat.
    assessed_set: Mapped[str] = mapped_column(Text)
    question_n: Mapped[int] = mapped_column(Integer)
    lesson_objective_id: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(Text)
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    #: Where the answer came from: the teacher's correction, or derived by the researcher.
    answer_source: Mapped[str | None] = mapped_column(String(32), nullable=True)


class StudyClassworkScript(Base):
    """One learner's marked script for a lesson."""

    __tablename__ = "study_classwork_scripts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("plan_versions.version_id", name="fk_study_scripts_plan_version_id"),
        index=True,
    )
    student_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("student_profiles.student_id", name="fk_study_scripts_student_id")
    )
    #: The total the teacher wrote on the script, e.g. ``1/4``.
    teacher_total: Mapped[str] = mapped_column(String(16))
    capture_complete: Mapped[bool] = mapped_column(Boolean)


class StudyClassworkAnswer(Base):
    """A learner's answer to one question: their working, the teacher's mark, and its coding."""

    __tablename__ = "study_classwork_answers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    script_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("study_classwork_scripts.id", name="fk_study_answers_script_id"),
        index=True,
    )
    plan_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("plan_versions.version_id", name="fk_study_answers_plan_version_id"),
    )
    question_n: Mapped[int] = mapped_column(Integer)
    #: ``correct``, ``incorrect`` or ``unmarked``, as the teacher marked it.
    mark: Mapped[str] = mapped_column(String(16))
    #: The transcriber could not read the mark with certainty.
    uncertain: Mapped[bool] = mapped_column(Boolean)
    working: Mapped[str] = mapped_column(Text)
    misconception_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    misconception_why: Mapped[str | None] = mapped_column(Text, nullable=True)
