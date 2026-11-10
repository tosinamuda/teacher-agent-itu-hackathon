"""Register every drawing already stored, and draw each one not yet drawn.

Invocation::

    uv run python -m scripts.seed_figures

Idempotent. Where TeX is not installed the drawings are registered and left pending, to be
drawn when they are first asked for on a host that has it.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from app.shared.tikz_svg import tikz_available, tikz_to_svg
from migrations.data.figure_registry import draw_pending, register_stored_drawings


def main() -> int:
    with sync_engine.begin() as conn:
        registered = register_stored_drawings(conn)
    if not tikz_available():
        print(f"figures: registered {registered}; not drawn, as TeX is not installed")
        return 0
    with sync_engine.begin() as conn:
        drawn, undrawable = draw_pending(conn, tikz_to_svg)
    print(f"figures: registered {registered}, drew {drawn}, {undrawable} would not draw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
