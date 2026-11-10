"""Register every drawing a flush writes into stored content, so it can be drawn and served.

Content is written by generation, revision, teachers and imports alike; registering at the
flush catches all of them without any of them knowing. A drawing already registered is left
as it is, so two writers never conflict over one.
"""

from __future__ import annotations

from itertools import chain

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.figures.infrastructure.models import Figure, FigureState
from app.shared.tikz_figures import drawings_in, figure_id


def _stored_content(row: object) -> object:
    if isinstance(row, Artefact):
        return row.manifest
    if isinstance(row, PlanVersion):
        return row.session_plan
    return None


def register_drawings(session: Session) -> None:
    sources = {
        figure_id(source): source
        for row in chain(session.new, session.dirty)
        for source in drawings_in(_stored_content(row))
    }
    if not sources:
        return
    with session.no_autoflush:
        session.execute(
            insert(Figure)
            .prefix_with("IGNORE")
            .values(
                [
                    {"figure_id": key, "source": source, "state": FigureState.PENDING}
                    for key, source in sources.items()
                ]
            )
        )
