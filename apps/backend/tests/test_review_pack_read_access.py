"""Who may read a revision note: a teacher of its class, researchers and admins, and a learner
only for their own note once it stands approved at the class note's current version."""

from __future__ import annotations

import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import app.domains.artefacts.types.post_class_review_pack.api.pack_access as access
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.content_engine.infrastructure.engine import Request
from app.shared.auth import Actor
from tests.content_engine_support import PLAN, ScriptedWriter, engine_over
from tests.test_learner_revision_note import (
    NOTE,
    STUDENT,
    _class_note_approved,
    _learner,
    _part,
    _with_the_learner_writer_as_default,
)

TEACHER = Actor(role="teacher", auth_id="code|t", teacher_id=uuid.UUID(int=1))
RESEARCHER = Actor(role="research_manager", auth_id="code|r", teacher_id=uuid.UUID(int=2))
ANONYMOUS = Actor(role="anonymous", auth_id="anonymous")
LEARNER = Actor(role="student", auth_id="code|s", teacher_id=uuid.UUID(int=3))


def _is_learner(monkeypatch: pytest.MonkeyPatch, student_id: str) -> None:
    async def resolved(*_args: object, **_kwargs: object) -> str:
        return student_id

    monkeypatch.setattr(access, "student_id_of", resolved)


def _teaches(monkeypatch: pytest.MonkeyPatch, owns: bool) -> None:
    async def owned(*_args: object, **_kwargs: object) -> bool:
        return owns

    monkeypatch.setattr(access, "teacher_owns_plan_version", owned)


async def _learner_note(db: AsyncSession) -> Artefact:
    await _class_note_approved(db)
    await _learner(db, misconception="ADD_DENOMINATORS")
    await _with_the_learner_writer_as_default(db)
    built = await engine_over(db, ScriptedWriter({"lop01": [_part()]})).build(
        Request(type=NOTE, plan_version_id=PLAN, student_id=STUDENT)
    )
    note = await db.scalar(select(Artefact).where(Artefact.artefact_id == built.saved_as))
    assert note is not None
    return note


async def _approve(db: AsyncSession, note: Artefact) -> None:
    await db.execute(
        update(Artefact)
        .where(Artefact.artefact_id == note.artefact_id)
        .values(review_status="approved")
    )
    await db.commit()
    await db.refresh(note)


@pytest.mark.asyncio
async def test_an_anonymous_caller_reads_nothing(db: AsyncSession) -> None:
    note = await _learner_note(db)
    with pytest.raises(HTTPException) as refused:
        await access.require_readable(ANONYMOUS, db, note)
    assert refused.value.status_code == 403


@pytest.mark.asyncio
async def test_a_teacher_reads_the_notes_of_a_class_they_teach_and_no_other(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    note = await _learner_note(db)
    _teaches(monkeypatch, True)
    await access.require_readable(TEACHER, db, note)
    _teaches(monkeypatch, False)
    with pytest.raises(HTTPException) as refused:
        await access.require_readable(TEACHER, db, note)
    assert refused.value.status_code == 403


@pytest.mark.asyncio
async def test_a_researcher_reads_any_note(db: AsyncSession) -> None:
    await access.require_readable(RESEARCHER, db, await _learner_note(db))


@pytest.mark.asyncio
async def test_a_learner_reads_their_own_note_only_once_it_is_approved(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    note = await _learner_note(db)
    _is_learner(monkeypatch, STUDENT)
    with pytest.raises(HTTPException) as pending:
        await access.require_readable(LEARNER, db, note)
    assert pending.value.status_code == 404

    await _approve(db, note)
    await access.require_readable(LEARNER, db, note)


@pytest.mark.asyncio
async def test_a_learner_cannot_read_another_learners_note(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    note = await _learner_note(db)
    await _approve(db, note)
    _is_learner(monkeypatch, "ST-SOMEONE-ELSE")
    with pytest.raises(HTTPException) as refused:
        await access.require_readable(LEARNER, db, note)
    assert refused.value.status_code == 404


@pytest.mark.asyncio
async def test_a_learner_cannot_export_or_download(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    note = await _learner_note(db)
    await _approve(db, note)
    _is_learner(monkeypatch, STUDENT)
    with pytest.raises(HTTPException) as refused:
        await access.require_readable(LEARNER, db, note, learner_may=False)
    assert refused.value.status_code == 403
