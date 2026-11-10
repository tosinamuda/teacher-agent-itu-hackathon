"""What evaluation reads from peer domains, stated as evaluation's own contracts.

Separate from ``ports.py``, which is evaluation's own persistence. These are
narrow on purpose: the surface is what a rater packet needs to resolve — the
pack behind a condition run, and the names behind learner ids — not the peer
repository in full.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.domains.artefacts.core.infrastructure.models import Artefact, ArtefactPlan


class PackArtefactsPort(Protocol):
    """The generated packs a rater packet points at."""

    async def get_plan(self, artefact_plan_id: str) -> ArtefactPlan | None: ...

    async def current_artefact_for_condition_run(self, run_id: str) -> Artefact | None: ...


class LearnerNamesPort(Protocol):
    """The learner names an assignment lane displays."""

    async def list_names_by_student_ids(self, student_ids: set[str]) -> dict[str, str | None]: ...


class TextbookExcerptReader(Protocol):
    async def excerpt_for_record(self, *, record_id: str) -> str | None: ...


__all__ = ["LearnerNamesPort", "PackArtefactsPort", "TextbookExcerptReader"]
