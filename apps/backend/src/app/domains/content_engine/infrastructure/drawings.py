"""Drawings checked by drawing them with TeX, off the event loop."""

from __future__ import annotations

from anyio import to_thread

from app.shared.tikz_svg import tikz_problem


class TexDrawings:
    async def problem(self, source: str) -> str | None:
        return await to_thread.run_sync(tikz_problem, source)
