"""Compile a ``tikzpicture`` to SVG, so a drawing that IS the method reaches the page.

The teacher's note carries its diagrams as TikZ source, and on a construction lesson the
drawing is not decoration: "slide the set square along the ruler" is unfollowable from its
caption alone. The evidence conditions carry those figures into the pack, and the worksheet
printed the caption and nothing else — fourteen of them on ``t3-w06``.

A miss is not an error. Where no TeX is installed, or a picture will not compile, this
returns ``None`` and the caller falls back to the caption it already prints.
"""

from __future__ import annotations

import logging
import os

# This renderer invokes only the fixed command tuples below and never enables a shell.
import re
import shutil
import subprocess  # nosec B404
import tempfile
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

# dvisvgm reads a DVI, so `latex` rather than `pdflatex`. `standalone` crops the page to
# the picture, which is what an inline figure needs.
# The drawing is its own file, so TeX reports an error's line within the drawing itself.
_DOCUMENT = r"""\documentclass[dvisvgm,tikz,border=2pt]{standalone}
\usepackage{tikz}
\begin{document}
\input{drawing.tex}
\end{document}
"""
_FILE_ERROR = re.compile(r"^(?:\./)?drawing\.tex:(?P<number>\d+): (?P<message>.*)")
_READING = re.compile(r"^l\.\d+ ?(?P<text>.*)")
# Long enough for a page of arcs, short enough that a picture waiting on a missing
# package cannot hold a render open. TeX prompts on error; -interaction stops that.
_TIMEOUT_SECONDS = 30
_LATEX = (
    "latex",
    "-interaction=nonstopmode",
    "-halt-on-error",
    "-file-line-error",
    # The source is the teacher's own note rather than anything a user submits, and a
    # figure still has no business starting a subprocess.
    "-no-shell-escape",
    "figure.tex",
)
# --no-fonts draws glyphs as paths, so the SVG carries its own labels and needs no font
# on the reading machine; the exact box crops to the ink rather than to TeX's metrics.
_DVISVGM = ("dvisvgm", "--no-fonts", "--exact-bbox", "-o", "figure.svg", "figure.dvi")


#: TeX may read and write only inside the figure's own working folder: no absolute paths, no
#: ``..``, no hidden files. The source is stored content, some of it a teacher's own writing.
_PARANOID = {
    **os.environ,
    "openin_any": "p",
    "openout_any": "p",
    # A long error stays on one line, so it is read whole.
    "max_print_line": "10000",
}


def _write_figure(directory: Path, source: str) -> None:
    (directory / "drawing.tex").write_text(source, encoding="utf-8")
    (directory / "figure.tex").write_text(_DOCUMENT, encoding="utf-8")


def tikz_available() -> bool:
    """Whether both halves of the toolchain are installed."""
    return bool(shutil.which("latex") and shutil.which("dvisvgm"))


@lru_cache(maxsize=512)
def tikz_to_svg(source: str) -> str | None:
    """The picture as SVG markup, or ``None`` if it cannot be drawn here.

    Cached on the source: one run renders seventy-two packets from the same handful
    of drawings, and each compilation is a TeX process.
    """
    if not source.strip() or not tikz_available():
        return None
    with tempfile.TemporaryDirectory(prefix="tikz-") as workspace:
        directory = Path(workspace)
        _write_figure(directory, source)
        for command in (_LATEX, _DVISVGM):
            if not _run(command, directory, source):
                return None
        return (directory / "figure.svg").read_text(encoding="utf-8")


def _run(command: tuple[str, ...], directory: Path, source: str) -> bool:
    try:
        result = subprocess.run(  # noqa: S603  # nosec B603
            command,
            cwd=directory,
            capture_output=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
            env=_PARANOID,
        )
    except (OSError, subprocess.TimeoutExpired):
        logger.warning("%s failed on a figure; falling back to its caption", command[0])
        return False
    if result.returncode:
        logger.warning(
            "%s rejected a figure (%s); falling back to its caption: %.120s",
            command[0],
            result.returncode,
            source.strip().replace("\n", " "),
        )
    return not result.returncode


@lru_cache(maxsize=512)
def tikz_problem(source: str) -> str | None:
    """Why the picture will not draw, in TeX's words; ``None`` when it draws or TeX is absent.

    A writer that can read the reason can mend its drawing, so the first error TeX reports
    is returned rather than a bare refusal.
    """
    if "\\\\begin{" in source:
        return (
            "the drawing has two backslashes before a command: write one, as in \\begin and \\draw"
        )
    if not tikz_available():
        return None
    if "\\begin{tikzpicture}" not in source:
        return "a drawing is one tikzpicture environment"
    with tempfile.TemporaryDirectory(prefix="tikz-") as workspace:
        directory = Path(workspace)
        _write_figure(directory, source)
        try:
            result = subprocess.run(  # noqa: S603  # nosec B603
                _LATEX,
                cwd=directory,
                capture_output=True,
                timeout=_TIMEOUT_SECONDS,
                check=False,
                env=_PARANOID,
            )
        except (OSError, subprocess.TimeoutExpired):
            return "TeX could not finish drawing it"
    if not result.returncode:
        return None
    return first_error(result.stdout.decode("utf-8", errors="replace").splitlines())


def first_error(log: list[str]) -> str:
    """TeX's first error in the drawing, with its line there and the text TeX was reading.

    ``-file-line-error`` makes TeX report ``drawing.tex:<line>: <message>``, and it prints
    the text it was reading on the ``l.<n>`` line after. An error outside the drawing, such
    as one in the wrapper, is given by its message alone.
    """
    for index, line in enumerate(log):
        found = _FILE_ERROR.match(line)
        if found is None:
            continue
        reading = next(
            (
                read["text"].strip()
                for later in log[index + 1 : index + 12]
                if (read := _READING.match(later))
            ),
            "",
        )
        where = f"line {found['number']} of the drawing" + (f": {reading}" if reading else "")
        return f"{found['message'].strip()} ({where})"
    return next((line[2:].strip() for line in log if line.startswith("! ")), "TeX refused it")
