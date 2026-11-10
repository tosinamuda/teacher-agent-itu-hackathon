"""Tests for the WeasyPrint source-grounding audit-pack renderer.

These exercise the *active* download path (``service.export_source_audit_pack``
now calls ``render_source_audit_pack_html_pdf``). WeasyPrint needs native libs
(pango/cairo/gdk-pixbuf/fontconfig/harfbuzz); each test skips cleanly if the
import fails. The reportlab path in ``audit_pack_pdf.py`` is kept as fallback.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

import pytest


def _audit_detail() -> dict[str, object]:
    return {
        "textbook_name": "JSS1 Mathematics Textbook",
        "items": [
            {
                "audit_item_id": "SG-ABC123",
                "condition_code": "C2",
                "lesson_objective_id": "obj-1",
                "objective_text": "Identify common multiples of two or more whole numbers",
                "generated_excerpt": (
                    "A **common multiple** is shared by two numbers; "
                    "for example *6 and 12* share the multiple 12. The LCM → smallest one."
                ),
                "source_ref": "ch01-b029",
                "source_record_id": "ch01-b029",
                "source_excerpt": (
                    "A multiple of a number is the product of that number and a whole number."
                ),
                # Cited record is a VisualBlock — pack pulls the cached PNG
                # from app/static/figures/ via _resolve_figure_src.
                "figure_url": ("https://electricbookworks.github.io/figures/ebw-jss1-01-001.png"),
                "figure_caption": "Common multiples laid out on a number line.",
                "scope_boundary": "JSS1 · Week 3 · LCM of whole numbers",
            },
            {
                "audit_item_id": "SG-DEF456",
                "condition_code": "C0",
                "lesson_objective_id": "obj-2",
                "objective_text": "Find the LCM of whole numbers",
                "generated_excerpt": "The least common multiple is the smallest shared one.",
                "source_ref": "ch02-b011",
                "source_record_id": "ch02-b011",
                "source_excerpt": None,  # exercises the snippet fallback
                # Text-only cited source — no figure should render in the PDF.
                "figure_url": None,
                "figure_caption": None,
                "scope_boundary": "JSS1 · Week 3",
            },
        ],
    }


def _render(detail: dict[str, object]) -> bytes:
    try:
        from app.domains.evaluation.application.worksheet_html.audit_renderer import (
            render_source_audit_pack_html_pdf,
        )

        return render_source_audit_pack_html_pdf(detail)
    except (ImportError, OSError) as exc:  # WeasyPrint or its native deps missing
        pytest.skip(f"WeasyPrint unavailable: {exc}")


def test_audit_pack_html_contains_expected_text() -> None:
    pdf_bytes = _render(_audit_detail())

    assert pdf_bytes.startswith(b"%PDF")
    text = _extract_pdf_text(pdf_bytes).replace("\n", " ")
    assert "Source-Grounding Audit Pack" in text
    # Eyebrow is uppercased by CSS.
    assert "EXPERT SOURCE-AUDIT WORKSHEET" in text
    # Instructions + the 0/1/2 legend.
    assert "JSS1 Mathematics Textbook" in text
    assert "criterion not met" in text
    assert "clearly met" in text
    # Per-item structure.
    assert "Audit item 1" in text
    assert "Audit item 2" in text
    assert "SG-ABC123" in text
    assert "Topic/scope boundary" in text
    # The snippet fallback for the item with no source_excerpt.
    assert "consult the textbook" in text


def test_audit_pack_html_renders_the_four_criteria() -> None:
    text = _extract_pdf_text(_render(_audit_detail()))
    assert "Source relevance" in text
    assert "Support sufficiency" in text
    assert "Faithfulness" in text
    assert "Scope correctness" in text
    assert "Comment" in text


def test_audit_pack_html_renders_markdown_emphasis_not_literal_markers() -> None:
    text = _extract_pdf_text(_render(_audit_detail()))
    assert "common multiple" in text
    assert "6 and 12" in text
    assert "**common multiple**" not in text
    assert "*6 and 12*" not in text


def test_audit_pack_html_has_no_missing_glyph_boxes() -> None:
    detail = _audit_detail()
    items = cast(list[dict[str, object]], detail["items"])
    items[0]["generated_excerpt"] = "A billion equals 10⁹ (million → billion)."
    text = _extract_pdf_text(_render(detail))
    assert "■" not in text  # ■ missing-glyph box


def test_audit_pack_html_renders_cited_figure_when_present() -> None:
    """Item 1 cites a VisualBlock — caption surfaces in the PDF; item 2 stays text-only.

    Also asserts the rendered HTML carries an ``<img>`` tag for item 1 only:
    the figure renders alongside the snippet (not in place of it), while
    text-only items keep the existing one-cell layout with no broken image.
    """
    detail = _audit_detail()
    text = _extract_pdf_text(_render(detail))
    # Item 1 figure caption is surfaced as <figcaption> text in the rendered PDF.
    assert "Common multiples laid out on a number line" in text

    # And the HTML carries exactly one <img> tag (item 1 only). Item 2 is
    # text-only — no <figure>/<img> should be emitted, even an empty one.
    from app.domains.evaluation.application.worksheet_html.audit_renderer import (
        render_source_audit_pack_html,
    )

    html = render_source_audit_pack_html(detail)
    assert html.count("<img ") == 1
    assert "Common multiples laid out on a number line" in html


def test_audit_pack_html_handles_empty_items() -> None:
    pdf_bytes = _render({"textbook_name": "JSS1 Mathematics Textbook", "items": []})
    assert pdf_bytes.startswith(b"%PDF")
    text = _extract_pdf_text(pdf_bytes)
    assert "No audit items have been built" in text


def _extract_pdf_text(pdf_bytes: bytes) -> str:
    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext is not available")
    with TemporaryDirectory() as tmpdir:
        pdf_path = Path(tmpdir) / "audit.pdf"
        text_path = Path(tmpdir) / "audit.txt"
        pdf_path.write_bytes(pdf_bytes)
        subprocess.run(
            ["pdftotext", str(pdf_path), str(text_path)],
            check=True,
            capture_output=True,
        )
        return text_path.read_text(encoding="utf-8")
