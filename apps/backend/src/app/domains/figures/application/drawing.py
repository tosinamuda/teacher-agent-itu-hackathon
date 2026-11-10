"""A registered drawing as SVG: drawn the first time it is asked for, then kept.

Drawing is a TeX run, so it happens once per drawing across every server: the first request
draws it holding the drawing's row, and the rest wait and read what it stored. Each process
runs only a few TeX runs at a time.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable

from anyio import to_thread
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.figures.infrastructure.models import Figure, FigureState
from app.shared.tikz_svg import tikz_available, tikz_to_svg
from app.shared.time import utc_now

_DRAWING_AT_ONCE = asyncio.Semaphore(2)

Draw = Callable[[str], str | None]


async def figure_svg(
    db: AsyncSession, figure_id: str, *, draw: Draw = tikz_to_svg, can_draw: bool | None = None
) -> str | None:
    """The drawing's SVG, drawing it now if it has not been; none if it cannot be drawn."""
    stored = await db.scalar(select(Figure).where(Figure.figure_id == figure_id))
    if stored is None or stored.state == FigureState.UNDRAWABLE:
        return None
    if stored.state == FigureState.DRAWN:
        return stored.svg
    if not (tikz_available() if can_draw is None else can_draw):
        return None
    figure = await db.scalar(
        select(Figure)
        .where(Figure.figure_id == figure_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if figure is None or figure.state != FigureState.PENDING:
        await db.commit()
        return figure.svg if figure is not None else None
    async with _DRAWING_AT_ONCE:
        svg = await to_thread.run_sync(draw, figure.source)
    figure.svg = svg
    figure.state = FigureState.DRAWN if svg else FigureState.UNDRAWABLE
    figure.drawn_at = utc_now()
    await db.commit()
    return svg
