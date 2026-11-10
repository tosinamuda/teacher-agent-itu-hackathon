"""Attachment service: store + fetch provenance images, with validation."""

from __future__ import annotations

import hashlib

import pytest

from app.domains.attachments.application.service import AttachmentError, AttachmentService

pytestmark = pytest.mark.asyncio

_PNG = b"\x89PNG\r\n\x1a\n" + b"fake-image-bytes"


async def test_save_writes_file_and_records_handle(db, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("UPLOADS_DIR", str(tmp_path))
    service = AttachmentService()
    attachment = await service.save(
        db,
        data=_PNG,
        content_type="image/png",
        kind="student_answer_sheet",
        uploaded_by="Teacher One",
        caption="page 1",
    )
    assert attachment.byte_size == len(_PNG)
    assert attachment.sha256 == hashlib.sha256(_PNG).hexdigest()
    assert attachment.content_type == "image/png"
    assert service.absolute_path(attachment).exists()

    fetched = await service.get(db, str(attachment.id))
    assert fetched is not None and fetched.id == attachment.id


async def test_rejects_non_image(db, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("UPLOADS_DIR", str(tmp_path))
    with pytest.raises(AttachmentError) as exc:
        await AttachmentService().save(
            db, data=b"hello", content_type="text/plain", kind="x", uploaded_by=None
        )
    assert exc.value.status_code == 415


async def test_rejects_too_large(db, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("UPLOADS_DIR", str(tmp_path))
    oversized = b"x" * (10 * 1024 * 1024 + 1)
    with pytest.raises(AttachmentError) as exc:
        await AttachmentService().save(
            db, data=oversized, content_type="image/png", kind="x", uploaded_by=None
        )
    assert exc.value.status_code == 413


async def test_rejects_empty(db, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("UPLOADS_DIR", str(tmp_path))
    with pytest.raises(AttachmentError) as exc:
        await AttachmentService().save(
            db, data=b"", content_type="image/png", kind="x", uploaded_by=None
        )
    assert exc.value.status_code == 422


async def test_get_unknown_id_returns_none(db, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("UPLOADS_DIR", str(tmp_path))
    service = AttachmentService()
    assert await service.get(db, "not-a-uuid") is None
