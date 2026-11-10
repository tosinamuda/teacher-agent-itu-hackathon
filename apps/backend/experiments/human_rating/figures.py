"""The diagrams the packs carry, drawn rather than described.

A pack's ``visual`` block holds the teacher's own TikZ. The worksheet renderer has always
drawn it; these documents printed the caption instead, so a rater judging representations
read a sentence about a picture. Every figure in the corpus is one of 38 drawings, so they
are rendered once each into a content-addressed cache and referenced from the markdown.

Needs a TeX installation and cairo, both developer tools. Where a drawing cannot be made
the caption still stands on its own, so a document is never worse than it was.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Any

from app.shared.native_libs import ensure_native_lib_path
from app.shared.tikz_svg import tikz_to_svg

CACHE = Path(__file__).resolve().parent / ".figures"
WIDTH = 1100  #: pixels rendered, for a drawing that stays sharp when printed
#: Millimetres on the page. A drawing is given the narrower of a comfortable column width
#: and whatever keeps a tall figure from filling the sheet on its own.
MAX_WIDTH_MM = 120
MAX_HEIGHT_MM = 95


def _set_print_size(path: Path) -> None:
    """Write the print size into the file itself.

    pandoc ignores a width given in markdown or in the HTML it passes through, and takes
    the size from the image's own resolution, so that is where the size has to go. A tall
    drawing is narrowed rather than allowed to fill the sheet.
    """
    from PIL import Image

    with Image.open(path) as image:
        aspect = image.height / image.width if image.width else 1
        width_mm = min(MAX_WIDTH_MM, MAX_HEIGHT_MM / aspect) if aspect else MAX_WIDTH_MM
        dpi = image.width / (width_mm / 25.4)
        image.save(path, dpi=(dpi, dpi))


def png_for(block: dict[str, Any]) -> Path | None:
    """A drawing of this block's TikZ, or None if it carries none or will not draw."""
    source = (block.get("source_tikz") or "").strip()
    if not source:
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{hashlib.sha256(source.encode()).hexdigest()[:16]}.png"
    if path.exists():
        return path
    svg = tikz_to_svg(source)
    if not svg:
        return None
    if not _rasterise(svg, path):
        return None
    _set_print_size(path)
    return path


def _rasterise(svg: str, path: Path) -> bool:
    """cairo in this process, falling back to rsvg-convert if it is not installed."""
    ensure_native_lib_path()
    try:
        import cairosvg

        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(path), output_width=WIDTH)
        return path.exists()
    except (ImportError, OSError):
        pass
    scratch = path.with_suffix(".svg")
    scratch.write_text(svg)
    try:
        subprocess.run(
            ["rsvg-convert", "-w", str(WIDTH), "-o", str(path), str(scratch)],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return False
    finally:
        scratch.unlink(missing_ok=True)
    return path.exists()
