"""Exporting a revision note adds where it was written, keeping what the note records."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

from app.domains.artefacts.core.application.service import ArtefactApplicationService


class _Store:
    def export_review_pack(self, artefact_id, manifest):
        return {"manifest_path": f"/exports/{artefact_id}.json"}


class _Session:
    async def commit(self) -> None: ...

    async def refresh(self, artefact) -> None: ...


def test_an_export_keeps_the_grounding_the_note_records() -> None:
    grounding = {"expert_sources": "lesson-note", "lesson_note": {"id": "AT-note", "version": 1}}
    artefact = SimpleNamespace(artefact_id="AT-pack", manifest={}, artefact_refs=dict(grounding))
    service = ArtefactApplicationService(None, _Store(), approvals=None)  # type: ignore[arg-type]

    exported = asyncio.run(service.export_review_pack(db=_Session(), artefact=artefact))  # type: ignore[arg-type]

    assert exported.artefact_refs == {**grounding, "manifest_path": "/exports/AT-pack.json"}
