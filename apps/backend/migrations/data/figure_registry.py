"""Register every drawing already stored, and draw the ones not yet drawn.

Content written from now on registers its drawings as it is flushed; this covers what was
written before, and draws each pending drawing so no reader waits on TeX. Idempotent: a
drawing registered or drawn already is left as it is.
"""

from __future__ import annotations

from collections.abc import Callable

import sqlalchemy as sa

from app.domains.figures.infrastructure.models import Figure, FigureState
from app.shared.tikz_figures import drawings_in, figure_id
from app.shared.time import utc_now

_STORED = (
    sa.table("artefacts", sa.column("manifest", sa.JSON)).c.manifest,
    sa.table("plan_versions", sa.column("session_plan", sa.JSON)).c.session_plan,
)


def register_stored_drawings(conn: sa.Connection) -> int:
    """Register every drawing in stored content. Returns how many were new."""
    sources: dict[str, str] = {}
    for column in _STORED:
        for (value,) in conn.execute(sa.select(column)):
            for source in drawings_in(value):
                sources[figure_id(source)] = source
    known = set(conn.execute(sa.select(Figure.figure_id)).scalars())
    new = [
        {"figure_id": key, "source": source} for key, source in sources.items() if key not in known
    ]
    if new:
        conn.execute(sa.insert(Figure).prefix_with("IGNORE"), new)
    return len(new)


def draw_pending(conn: sa.Connection, draw: Callable[[str], str | None]) -> tuple[int, int]:
    """Draw every pending drawing. Returns how many drew and how many would not."""
    pending = conn.execute(
        sa.select(Figure.figure_id, Figure.source).where(Figure.state == FigureState.PENDING)
    ).all()
    drawn = 0
    for key, source in pending:
        svg = draw(source)
        conn.execute(
            sa.update(Figure)
            .where(Figure.figure_id == key)
            .values(
                svg=svg,
                state=FigureState.DRAWN if svg else FigureState.UNDRAWABLE,
                drawn_at=utc_now(),
            )
        )
        drawn += bool(svg)
    return drawn, len(pending) - drawn
