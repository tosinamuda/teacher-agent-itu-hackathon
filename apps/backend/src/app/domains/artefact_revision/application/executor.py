"""The shared role contract for a per-artefact-type revision executor.

The revision service holds one executor per ``artefact_type`` and dispatches
turns + current-artefact reads through this contract — so adding a new artefact
type means adding a new executor and registering it, not editing every
``if artefact_type == ...`` branch (the OCP fix for P3.7).

Each executor owns:
- ``artefact_type`` — the registry key
- ``revise(...)`` — apply one revision turn, persist the result, return the
  outcome the service records
- ``current_artefact(...)`` — read the current (version_id, manifest/payload)
  pair for the subject id, so the service can render the thread view without
  knowing the per-type repository or assembly logic
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class RevisionExecutionOutcome:
    """What an executor produced for one turn (persisted by the service)."""

    base_version_id: str
    result_version_id: str
    session_plan: JsonObject
    change_summary: str
    validation_passed: bool


class RevisionExecutor(Protocol):
    """The minimal role shape every artefact-type revision executor implements."""

    artefact_type: str

    async def revise(
        self,
        *,
        db: AsyncSession,
        subject_id: str,
        thread_id: str,
        instruction: str,
        highlight: JsonObject | None,
        conversation_summary: str,
    ) -> RevisionExecutionOutcome:
        """Apply one revision turn to ``subject_id`` and persist the result."""

    async def current_artefact(
        self,
        *,
        db: AsyncSession,
        subject_id: str,
    ) -> tuple[str | None, JsonObject | None]:
        """Return the current ``(version_id, payload)`` for the subject id.

        Returns ``(None, None)`` when the subject id does not resolve to an artefact.
        """
