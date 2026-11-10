"""Rendering a worksheet and reading it back as a reader gets it.

The list markers, the sub-step letters and the page order are the stylesheet's work,
not the markup's, so an assertion about what a learner reads has to be made against the
rendered page rather than the HTML. Both halves skip rather than fail where the tools
are missing: WeasyPrint needs pango/cairo, and the text extraction needs poppler.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


def render_worksheet_pdf(detail: dict[str, object]) -> bytes:
    """Render via WeasyPrint, skipping if the native libs are unavailable."""
    try:
        from app.domains.evaluation.application.worksheet_html.renderer import (
            render_h1_worksheet_html_pdf,
        )

        return render_h1_worksheet_html_pdf(detail)
    except (ImportError, OSError) as exc:  # WeasyPrint or its native deps missing
        pytest.skip(f"WeasyPrint unavailable: {exc}")


def extract_pdf_text(pdf_bytes: bytes) -> str:
    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext is not available")
    with TemporaryDirectory() as tmpdir:
        pdf_path = Path(tmpdir) / "worksheet.pdf"
        text_path = Path(tmpdir) / "worksheet.txt"
        pdf_path.write_bytes(pdf_bytes)
        subprocess.run(
            ["pdftotext", str(pdf_path), str(text_path)],
            check=True,
            capture_output=True,
        )
        return text_path.read_text(encoding="utf-8")


def worksheet_text(detail: dict[str, object]) -> str:
    """The rendered worksheet as one whitespace-flattened string."""
    return " ".join(extract_pdf_text(render_worksheet_pdf(detail)).split())
