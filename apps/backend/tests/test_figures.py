"""Every drawing in stored content is registered as it is written, drawn once, and served safely."""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.figures.application.drawing import figure_svg
from app.domains.figures.infrastructure.models import Figure, FigureState
from app.shared.tikz_figures import drawings_in, figure_id
from migrations.data.figure_registry import register_stored_drawings

#: Shared with the browser's test (apps/frontend/src/shared/utils/figures.test.ts): both must
#: name this drawing by the same id.
DRAWING = "\\begin{tikzpicture}\n  \\draw (0,0) -- (1,1);\n\\end{tikzpicture}"
DRAWING_ID = "b428001695a60547dffb293ba008d6c97d5f0c15d47993429e87da33d8b08ce6"
NOTE = f"Two lines meet at a right angle.\n\n\\begin{{center}}\n{DRAWING}\n\\end{{center}}\n\nSo."
SVG = '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>'


def _note(artefact_id: str, body: str) -> Artefact:
    return Artefact(
        artefact_id=artefact_id,
        artefact_type="lesson_note",
        scope="class_level",
        plan_version_id="LPV-FIG",
        manifest={"sections": [{"step_id": "s1", "body": body}]},
        review_status=ArtefactReviewStatus.PENDING,
    )


def _pack(artefact_id: str) -> Artefact:
    block = {
        "type": "visual",
        "variant": "diagram_tikz",
        "caption": "A line",
        "source_tikz": DRAWING,
    }
    return Artefact(
        artefact_id=artefact_id,
        artefact_type="post_class_review_pack",
        scope="class_level",
        plan_version_id="LPV-FIG",
        manifest={"steps": [{"step_id": "s1", "blocks": [block]}]},
        review_status=ArtefactReviewStatus.PENDING,
    )


async def _figures(db: AsyncSession) -> list[Figure]:
    return list((await db.execute(select(Figure))).scalars())


def test_a_drawing_has_one_id_wherever_it_is_written() -> None:
    in_prose = list(drawings_in({"body": NOTE}))
    in_a_block = list(drawings_in({"source_tikz": f"  {DRAWING}\n"}))

    assert [figure_id(source) for source in in_prose + in_a_block] == [DRAWING_ID, DRAWING_ID]


@pytest.mark.asyncio
async def test_writing_content_registers_its_drawings_once(db: AsyncSession) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all([_note("AT-FIG-1", NOTE), _pack("AT-FIG-2")])
    await db.flush()
    db.add(_note("AT-FIG-3", "No drawing here."))
    await db.flush()

    [figure] = await _figures(db)
    assert (figure.figure_id, figure.state, figure.source) == (
        DRAWING_ID,
        FigureState.PENDING,
        DRAWING,
    )


@pytest.mark.asyncio
async def test_a_drawing_is_drawn_once_and_then_read(db: AsyncSession) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_note("AT-FIG-1", NOTE))
    await db.commit()
    runs: list[str] = []

    def draw(source: str) -> str:
        runs.append(source)
        return SVG

    first = await figure_svg(db, DRAWING_ID, draw=draw, can_draw=True)
    second = await figure_svg(db, DRAWING_ID, draw=draw, can_draw=True)

    assert (first, second, runs) == (SVG, SVG, [DRAWING])


@pytest.mark.asyncio
async def test_a_drawing_waits_for_tex_and_one_that_will_not_compile_is_left_to_its_caption(
    db: AsyncSession,
) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_note("AT-FIG-1", NOTE))
    await db.commit()

    assert await figure_svg(db, DRAWING_ID, draw=lambda _: SVG, can_draw=False) is None
    assert (await _figures(db))[0].state == FigureState.PENDING
    assert await figure_svg(db, DRAWING_ID, draw=lambda _: None, can_draw=True) is None
    assert await figure_svg(db, DRAWING_ID, draw=lambda _: SVG, can_draw=True) is None
    assert (await _figures(db))[0].state == FigureState.UNDRAWABLE


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncIterator[AsyncClient]:
    from app.main import app

    app.dependency_overrides[get_db] = lambda: db
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
            yield http
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.mark.asyncio
async def test_a_drawn_figure_is_served_cached_for_good_and_sandboxed(
    db: AsyncSession, client: AsyncClient
) -> None:
    db.add(Figure(figure_id=DRAWING_ID, source=DRAWING, svg=SVG, state=FigureState.DRAWN))
    await db.commit()

    served = await client.get(f"/figures/{DRAWING_ID}.svg")
    unknown = await client.get(f"/figures/{'0' * 64}.svg")
    malformed = await client.get("/figures/not-an-id.svg")

    assert (served.status_code, served.text) == (200, SVG)
    assert served.headers["content-type"].startswith("image/svg+xml")
    assert "immutable" in served.headers["cache-control"]
    assert "sandbox" in served.headers["content-security-policy"]
    assert (unknown.status_code, malformed.status_code) == (404, 404)
    assert unknown.headers["cache-control"] == "no-store"


@pytest.mark.asyncio
async def test_drawings_stored_before_registration_are_registered_by_the_data_step(
    db: AsyncSession,
) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_note("AT-OLD", NOTE))
    await db.flush()
    await db.execute(delete(Figure))

    new = await db.run_sync(lambda session: register_stored_drawings(session.connection()))
    again = await db.run_sync(lambda session: register_stored_drawings(session.connection()))

    assert (new, again) == (1, 0)
    assert [figure.figure_id for figure in await _figures(db)] == [DRAWING_ID]
