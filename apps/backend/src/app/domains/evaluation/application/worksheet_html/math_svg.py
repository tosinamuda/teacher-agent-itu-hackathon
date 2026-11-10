r"""LaTeX → inline SVG for the WeasyPrint rater/review PDFs.

WeasyPrint has **no MathML support and no JavaScript engine**: a ``<math>``
element renders as its bare text content, so ``\\frac{3}{4}`` collapses to the
two digits "34" (no fraction bar) and ``6/8`` to "68". The on-screen reader is
fine — it runs KaTeX — but every backend PDF (student review-note pack, H1 rater
worksheet, source-grounding audit pack) was broken.

WeasyPrint *does* render SVG, so we turn each LaTeX expression into a
self-contained inline ``<svg>`` of glyph outlines via **matplotlib's mathtext**
parser. mathtext is pure-Python (no system TeX install) and its bundled ``cm``
font set is Computer Modern — the same typeface family as the worksheet's
vendored ``CMU Serif`` body font — so the math blends into surrounding prose.

The SVG is sized in ``em`` (font-size independent) and baseline-aligned via
``vertical-align`` computed from the glyph depth, so inline math tucks into the
line and display math sits centred on its own line. ``fill="currentColor"`` lets
the math inherit the prose colour (verified to render in WeasyPrint).

Public entry point: :func:`render_latex_svg`. It raises on an empty or
unparseable expression so the caller (:func:`renderer._convert_arithmatex_to_svg`)
can fall back to the raw LaTeX marker — a bad expression must never crash a PDF.
"""

from __future__ import annotations

import logging
import re
import threading
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.path import Path as MplPath
    from matplotlib.transforms import Bbox

# matplotlib's mathtext parser is not guaranteed thread-safe (shared global parse
# state); serialise rendering so concurrent requests' threads cannot interleave.
_RENDER_LOCK = threading.Lock()

# Internal font size for the path geometry. The output is rescaled to ``em`` by
# dividing by this, so the absolute value only sets coordinate precision — 100
# gives two-decimal path data that is exact enough at any print size.
_EM = 100.0

# matplotlib path codes are stable integers, but import them by name for clarity.
# (Imported lazily inside the renderer to keep matplotlib off the import path of
# callers that never render math.)


def render_latex_svg(latex: str, *, display: bool) -> str:
    """Render a LaTeX math expression to a self-contained inline ``<svg>`` string.

    ``display`` selects block vs inline presentation: block math (``$$…$$``) gets
    ``class="math-svg math-svg--block"`` (centred on its own line via the print
    CSS); inline math (``$…$``) gets ``class="math-svg math-svg--inline"`` and a
    ``vertical-align`` offset so it sits on the text baseline.

    Raises ``ValueError`` if the expression is empty or matplotlib's mathtext
    parser rejects it — the caller keeps the raw marker as a graceful fallback.
    """
    expr = _typesettable(latex.strip())
    if not expr:
        raise ValueError("empty LaTeX expression")
    return _render_cached(expr, display)


# The model types a unit as "5<U+202F>cm" — a narrow no-break space, which is what it
# means and is not something Computer Modern has a glyph for. mathtext substitutes a
# dummy symbol and the learner reads "5□cm" in an answer. ``\,`` is the same space in
# the notation mathtext does have, and it parses in math mode and inside ``\text{}``.
# A degree sign inside maths is worse, because nothing reports it: Computer Modern
# maps U+00B0 to the same outline as ``\gamma``, so ``\((n-2)\times180°\)`` reaches
# the page as "180γ" and the missing-glyph watcher below never fires — the glyph is
# not missing, it is the wrong one. ``^\circ`` is how the teacher's own notes write
# it. Valid everywhere the corpus puts it; directly after a ``^`` it would be a double
# superscript, which mathtext rejects and the caller already falls back to raw LaTeX
# for, and which no field in any run on disk contains.
_MATH_SUBSTITUTIONS = str.maketrans({" ": r"\,", " ": r"\,", "\u00b0": r"^\circ"})


# Commands the model writes that mathtext does not implement at all. Each is valid
# LaTeX, so the model is not wrong; mathtext is a subset, and an expression carrying
# one of these raises and falls back to its own raw source on the page. Counted across
# every run on disk: `\displaystyle` 18, `\boxed` 13, the `\big` family 7, `\tfrac` 2 —
# and concentrated on C3, so leaving them is not neutral between the arms.
#
# `\boxed` and the sizing prefixes are dropped rather than translated. `\boxed{X}` left
# as `{X}` is a plain group, which mathtext renders as X. A sized delimiter could map to
# `\left(`/`\right)`, which mathtext does implement — but those MUST pair, so an
# unpaired `\big(` would trade a fallback for a parse error. Dropping always parses and
# costs only the sizing.
_UNSUPPORTED_COMMANDS = re.compile(
    r"\\displaystyle\s*"
    r"|\\boxed"
    r"|\\(?:bigg?|Bigg?)[lrm]?"
)
_NEAREST_SUPPORTED = re.compile(r"\\[td]frac")


def _supported(latex: str) -> str:
    return _NEAREST_SUPPORTED.sub(r"\\frac", _UNSUPPORTED_COMMANDS.sub("", latex))


def _typesettable(latex: str) -> str:
    return _supported(latex.translate(_MATH_SUBSTITUTIONS))


# Computer Modern's stand-in for a character it has no glyph for: the closest serif
# matplotlib ships, and it covers the currency this worksheet is written in.
_FALLBACK_FONTSET = "dejavuserif"
# mathtext does not raise on a character it cannot draw — it substitutes a dummy symbol
# and says so on this logger. That message is the only signal that the reader is about
# to get a box, so it is what the fallback is triggered by, rather than a guess at
# which codepoints the font set covers: mathtext resolves `×` and `−` to Computer
# Modern glyphs their codepoints are not in the cmap for, and second-guessing it there
# would swap the typeface on expressions that render perfectly well.
_MATHTEXT_LOGGER = "matplotlib.mathtext"
_MISSING_GLYPH = "does not have a glyph"


class _MissingGlyphWatcher(logging.Handler):
    """Records whether mathtext gave up on a character while drawing one expression."""

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.missed = False

    def emit(self, record: logging.LogRecord) -> None:
        self.missed = self.missed or _MISSING_GLYPH in record.getMessage()


@lru_cache(maxsize=256)
def _render_cached(expr: str, display: bool) -> str:
    with _RENDER_LOCK:
        # The Computer Modern attempt is a probe, so its complaint is muted: a miss
        # here is answered by the retry, not by the reader. A miss in the retry is
        # nobody's to answer and logs as usual.
        path, missed = _outline(expr, "cm", quiet=True)
        if missed:
            path, _ = _outline(expr, _FALLBACK_FONTSET, quiet=False)
    return _svg_from_path(path, path.get_extents(), display=display)


def _outline(expr: str, fontset: str, *, quiet: bool) -> tuple[MplPath, bool]:
    """The expression's glyph outlines in one font set, and whether any glyph was missing."""
    import matplotlib
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath

    watcher = _MissingGlyphWatcher()
    logger = logging.getLogger(_MATHTEXT_LOGGER)
    propagates = logger.propagate
    logger.addHandler(watcher)
    logger.propagate = propagates and not quiet
    try:
        # rc_context keeps the font set scoped to this call instead of mutating the
        # host process's global rcParams.
        with matplotlib.rc_context({"mathtext.fontset": fontset}):
            path = TextPath((0, 0), f"${expr}$", prop=FontProperties(size=_EM))
    except Exception as exc:  # noqa: BLE001 — mathtext raises ad-hoc parse exceptions (ValueError / ParseException / …) with no shared base; any of them means "unparseable", so normalise to ValueError for the caller's fallback.
        raise ValueError(f"unparseable LaTeX: {expr!r}") from exc
    finally:
        logger.propagate = propagates
        logger.removeHandler(watcher)
    return path, watcher.missed


def _svg_from_path(path: MplPath, extents: Bbox, *, display: bool) -> str:
    """Build the inline SVG from a matplotlib ``TextPath`` and its bounding box.

    matplotlib uses a y-up coordinate system with the text baseline at ``y = 0``;
    SVG is y-down, so every y is negated when emitting the path data and the
    viewBox. The box's height above the baseline is ``y1`` and the depth below is
    ``-y0``; sizing in ``em`` (dividing by ``_EM``) makes the glyphs scale with the
    surrounding ``font-size``, and a ``vertical-align`` of ``y0`` em drops the box
    by its depth so the math baseline meets the text baseline.
    """
    x0, y0, x1, y1 = extents.x0, extents.y0, extents.x1, extents.y1
    width = x1 - x0
    height = y1 - y0
    if width <= 0 or height <= 0:
        raise ValueError("LaTeX expression produced an empty glyph box")

    d = _path_to_svg_d(path)
    view_box = f"{x0:.2f} {-y1:.2f} {width:.2f} {height:.2f}"
    width_em = width / _EM
    height_em = height / _EM
    baseline_em = y0 / _EM  # negative: shifts the box down by its depth

    if display:
        css_class = "math-svg math-svg--block"
        style = f"height:{height_em:.3f}em;width:{width_em:.3f}em"
    else:
        css_class = "math-svg math-svg--inline"
        style = (
            f"height:{height_em:.3f}em;width:{width_em:.3f}em;vertical-align:{baseline_em:.3f}em"
        )

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'class="{css_class}" viewBox="{view_box}" style="{style}" '
        'preserveAspectRatio="xMidYMid meet" role="img" aria-hidden="true">'
        f'<path d="{d}" fill="currentColor"/></svg>'
    )


def _path_to_svg_d(path: MplPath) -> str:
    """Serialise a matplotlib ``Path`` to an SVG path ``d`` string (y negated).

    Handles the four segment kinds a glyph outline uses — MOVETO, LINETO,
    quadratic (CURVE3) and cubic (CURVE4) Béziers — plus CLOSEPOLY. The fraction
    bar and other rules are filled rectangles already baked into the same path by
    ``TextPath``, so a single ``<path>`` reproduces the whole expression.
    """
    import numpy as np
    from matplotlib.path import Path as MplPath

    if path.codes is None:
        raise ValueError("path has no segment codes")
    # Materialise the geometry as plain Python floats/ints up front: ``vertices``
    # is an ``(N, 2)`` ndarray and ``codes`` an ``(N,)`` ndarray, so indexing them
    # directly yields numpy scalars; ``.tolist()`` gives clean ``[x, y]`` pairs and
    # ints that serialise without per-element numpy coercion.
    verts: list[list[float]] = np.asarray(path.vertices, dtype=float).tolist()
    codes: list[int] = np.asarray(path.codes, dtype=int).tolist()

    parts: list[str] = []
    index = 0
    count = len(codes)
    while index < count:
        code = codes[index]
        if code == MplPath.MOVETO:
            x, y = verts[index]
            parts.append(f"M{x:.2f} {-y:.2f}")
            index += 1
        elif code == MplPath.LINETO:
            x, y = verts[index]
            parts.append(f"L{x:.2f} {-y:.2f}")
            index += 1
        elif code == MplPath.CURVE3:
            cx, cy = verts[index]
            ex, ey = verts[index + 1]
            parts.append(f"Q{cx:.2f} {-cy:.2f} {ex:.2f} {-ey:.2f}")
            index += 2
        elif code == MplPath.CURVE4:
            c1x, c1y = verts[index]
            c2x, c2y = verts[index + 1]
            ex, ey = verts[index + 2]
            parts.append(f"C{c1x:.2f} {-c1y:.2f} {c2x:.2f} {-c2y:.2f} {ex:.2f} {-ey:.2f}")
            index += 3
        elif code == MplPath.CLOSEPOLY:
            parts.append("Z")
            index += 1
        else:
            index += 1
    return "".join(parts)
