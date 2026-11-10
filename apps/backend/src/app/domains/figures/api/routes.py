"""GET a drawing from stored content as SVG, by the SHA-256 of its source.

Public, because an ``<img>`` cannot carry the header the API authenticates with. It serves
only drawings found in content the app already stores, never source a client sends, and an
id cannot be guessed. An SVG may carry script, so it is served sandboxed: opened on its own,
nothing in it runs.
"""

from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.figures.application.drawing import figure_svg

router = APIRouter(prefix="/figures", tags=["figures"])

_FIGURE_ID = re.compile(r"^[0-9a-f]{64}$")
#: A drawing never changes under its id, so anything may keep it for good.
_SERVED = {
    "Cache-Control": "public, max-age=31536000, immutable",
    "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox",
    "X-Content-Type-Options": "nosniff",
}


@router.get("/{figure_id}.svg", response_class=Response)
async def figure(figure_id: str, db: AsyncSession = Depends(get_db)) -> Response:
    """The drawing as SVG; 404 if no stored content carries it or it will not draw."""
    svg = await figure_svg(db, figure_id) if _FIGURE_ID.match(figure_id) else None
    if svg is None:
        raise HTTPException(status_code=404, headers={"Cache-Control": "no-store"})
    return Response(svg, media_type="image/svg+xml", headers=_SERVED)
