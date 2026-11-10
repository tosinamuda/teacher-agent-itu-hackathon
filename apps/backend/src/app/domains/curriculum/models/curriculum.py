"""Curriculum and session models."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now


# Audit §2.3 (P5.7 finish): the 4 curriculum-identity reference catalogs the
# curriculum tables FK into. These hold what the NERDC-published curriculum
# carries (curriculum identity, not joined to the school-side `subjects` /
# `grade_levels` / `terms` tables which encode a school's offering).
class CurriculumSubject(Base):
    __tablename__ = "curriculum_subjects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class CurriculumTrack(Base):
    __tablename__ = "curriculum_tracks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class CurriculumGrade(Base):
    __tablename__ = "curriculum_grades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class CurriculumTerm(Base):
    __tablename__ = "curriculum_terms"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class CurriculumTopic(Base):
    __tablename__ = "curriculum_topics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    subject: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("curriculum_subjects.name", name="fk_curriculum_topics_subject"),
        index=True,
    )
    track: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("curriculum_tracks.name", name="fk_curriculum_topics_track"),
        index=True,
    )
    grade: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("curriculum_grades.name", name="fk_curriculum_topics_grade"),
        index=True,
    )
    term: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("curriculum_terms.name", name="fk_curriculum_topics_term"),
        index=True,
    )
    week: Mapped[int] = mapped_column(Integer, index=True)
    topic: Mapped[str] = mapped_column(String(256))
    general_objectives: Mapped[list] = mapped_column(JSON)
    theme_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("curriculum_themes.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )

    subtopics: Mapped[list[CurriculumSubtopic]] = relationship(
        "CurriculumSubtopic", back_populates="topic", cascade="all, delete-orphan"
    )
    sessions: Mapped[list[ClassSession]] = relationship(
        "ClassSession", back_populates="topic", cascade="all, delete-orphan"
    )


class CurriculumSubtopic(Base):
    __tablename__ = "curriculum_subtopics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subtopic_id: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    topic_key: Mapped[str] = mapped_column(
        String(128), ForeignKey("curriculum_topics.topic_key"), index=True
    )
    title: Mapped[str] = mapped_column(String(256))
    performance_objectives: Mapped[list] = mapped_column(JSON)
    teacher_activities: Mapped[list | None] = mapped_column(JSON, nullable=True)
    student_activities: Mapped[list | None] = mapped_column(JSON, nullable=True)
    teaching_learning_materials: Mapped[list | None] = mapped_column(JSON, nullable=True)
    evaluation_guide: Mapped[list | None] = mapped_column(JSON, nullable=True)

    topic: Mapped[CurriculumTopic] = relationship("CurriculumTopic", back_populates="subtopics")


class CurriculumPerformanceObjective(Base):
    """One curriculum-published performance objective (NERDC po-id) under a subtopic.

    P5.6 Phase 2: promotes the curriculum-side performance objectives into a real
    table so ``plan_version_objectives.curriculum_objective_id`` has a proper FK
    target. The expert-content ``ao_textbook_objective_links`` table already
    carried each ``curriculum_objective_id`` at the atomic-objective grain (with
    duplicates per AO decomposition); this new table is at the canonical
    one-row-per-objective grain so ``curriculum_objective_id`` can be UNIQUE
    and FK-targetable.

    The curriculum domain owns this table. The expert_content
    ``ao_textbook_objective_links`` table remains the place where each curriculum
    objective is decomposed into atomic objectives + linked to textbook
    evidence — a separate concern at a finer grain. The backfill that lands
    this table is sourced from the existing rows in
    ``ao_textbook_objective_links`` (the only place the structured po-id +
    text data lives today; the legacy ``CurriculumSubtopic.performance_objectives``
    JSON is a plain string array and isn't the source of truth for ids).
    """

    __tablename__ = "curriculum_performance_objectives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subtopic_id: Mapped[str] = mapped_column(
        String(200),
        ForeignKey(
            "curriculum_subtopics.subtopic_id",
            name="fk_curriculum_performance_objectives_subtopic_id",
            ondelete="RESTRICT",
        ),
        index=True,
    )
    # Globally unique business key (e.g. ``jss1-math-...-po01``). The string
    # carries the subtopic identifier inside it, so it's unique cross-subtopic;
    # the UNIQUE constraint here makes it FK-targetable from elsewhere.
    curriculum_objective_id: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    curriculum_objective_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class ClassSession(Base):
    __tablename__ = "class_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    topic_key: Mapped[str] = mapped_column(
        String(128), ForeignKey("curriculum_topics.topic_key"), index=True
    )
    subtopic_id: Mapped[str] = mapped_column(
        String(200), ForeignKey("curriculum_subtopics.subtopic_id"), index=True
    )
    subject: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("curriculum_subjects.name", name="fk_class_sessions_subject"),
        index=True,
    )
    track: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("curriculum_tracks.name", name="fk_class_sessions_track"),
        index=True,
    )
    grade: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("curriculum_grades.name", name="fk_class_sessions_grade"),
        index=True,
    )
    term: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("curriculum_terms.name", name="fk_class_sessions_term"),
        index=True,
    )
    week: Mapped[int] = mapped_column(Integer, index=True)
    day_index: Mapped[int] = mapped_column(Integer)
    sequence_in_topic: Mapped[int] = mapped_column(Integer)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    session_objectives: Mapped[list] = mapped_column(JSON)

    topic: Mapped[CurriculumTopic] = relationship("CurriculumTopic", back_populates="sessions")


class ReferenceMaterial(Base):
    __tablename__ = "reference_materials"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    type: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(256))
    subject: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("curriculum_subjects.name", name="fk_reference_materials_subject"),
        index=True,
    )
    track: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("curriculum_tracks.name", name="fk_reference_materials_track"),
        index=True,
    )
    grade: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("curriculum_grades.name", name="fk_reference_materials_grade"),
        index=True,
    )
    license: Mapped[str] = mapped_column(String(64))
    topics: Mapped[list] = mapped_column(JSON)
    chunk_refs: Mapped[list] = mapped_column(JSON)
