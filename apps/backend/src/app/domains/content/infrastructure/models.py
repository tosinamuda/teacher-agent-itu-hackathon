"""The registered content types, and the skills their content is written with."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID


class ContentTypeRecord(Base):
    """One registered content type. Rows are added, never edited."""

    __tablename__ = "content_types"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_content_types_slug"),
        UniqueConstraint("kind", name="uq_content_types_kind"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(64))
    kind: Mapped[str] = mapped_column(String(64))
    label: Mapped[str] = mapped_column(String(120))
    audience: Mapped[str] = mapped_column(String(16))
    engine: Mapped[str] = mapped_column(String(16))
    made_from_a_plan_version: Mapped[bool] = mapped_column(Boolean)
    position: Mapped[int] = mapped_column(Integer)
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )


class ContentSkillRecord(Base):
    """One revision of a skill. Revisions are added, never edited."""

    __tablename__ = "content_skills"
    __table_args__ = (UniqueConstraint("slug", "revision", name="uq_content_skills_revision"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(64), index=True)
    revision: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    instructions: Mapped[str] = mapped_column(Text)
    files: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )


class ContentPluginRecord(Base):
    """One install, update or removal of an artefact plugin. Rows are added, never edited."""

    __tablename__ = "content_plugins"
    __table_args__ = (UniqueConstraint("name", "revision", name="uq_content_plugins_revision"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(64), index=True)
    revision: Mapped[int] = mapped_column(Integer)
    version: Mapped[str] = mapped_column(String(64))
    digest: Mapped[str] = mapped_column(String(64))
    type_slug: Mapped[str] = mapped_column(String(64), index=True)
    spec_revision: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(16))
    installed_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    #: The plugin adds a generator to the type, which it did not add.
    implements: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("0"))
    #: The plugin folder's files as text by path; a removal has none.
    files: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )


class ContentTypeGeneratorRecord(Base):
    """One generator of a content type at one level. Seeded rows are never overwritten.

    ``default_key`` is the type and level while the row is the default, and NULL otherwise.
    MySQL allows repeated NULLs in a unique index, so this says "one default for each type and
    level" without a partial index.
    """

    __tablename__ = "content_type_generators"
    __table_args__ = (
        UniqueConstraint("type_slug", "level", "harness", "ref", name="uq_content_type_generators"),
        UniqueConstraint("default_key", name="uq_content_type_generators_default"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_slug: Mapped[str] = mapped_column(String(64), index=True)
    level: Mapped[str] = mapped_column(String(16))
    harness: Mapped[str] = mapped_column(String(32))
    schema_source: Mapped[str] = mapped_column(String(16))
    ref: Mapped[str] = mapped_column(String(128))
    spec_revision: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(16))
    default_key: Mapped[str | None] = mapped_column(String(96), nullable=True)
    changed_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )


class TeacherPreferenceRecord(Base):
    """What one teacher has switched: the optional materials they hide."""

    __tablename__ = "teacher_preferences"
    __table_args__ = (UniqueConstraint("auth_id", name="uq_teacher_preferences_auth_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id: Mapped[str] = mapped_column(String(128))
    #: Slugs of the optional content types this teacher does not use, in no order.
    hidden_types: Mapped[list] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=text("now()"),
    )
