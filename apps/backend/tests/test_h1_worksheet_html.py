"""Tests for the WeasyPrint H1 reading-note review worksheet renderer.

These exercise the *active* download path (``service.export_h1_packet_worksheet``
now calls ``render_h1_worksheet_html_pdf``). WeasyPrint needs native libs
(pango/cairo/gdk-pixbuf/fontconfig/harfbuzz); each test skips cleanly if the
import fails so the suite stays green on a box without them. The reportlab tests
in ``test_h1_packet_worksheet_pdf.py`` are left untouched as fallback coverage.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import pytest

from app.domains.evaluation.application.constants import H1_RUBRIC, rubric_for_display
from app.shared.llm_markup import count_bare_math
from tests.test_h1_packet_worksheet_pdf import _sample_detail
from tests.worksheet_pdf_support import extract_pdf_text, render_worksheet_pdf


def test_normalize_text_glyphs_maps_keycap_emoji_to_plain_numbers() -> None:
    # Emoji keycap digits (1️⃣ 2️⃣ …) are absent from Computer Modern and would
    # render as missing-glyph boxes; they must normalise to plain "1." text. No
    # WeasyPrint needed — pure function, so this test never skips.
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _normalize_text_glyphs,
    )

    out = _normalize_text_glyphs("1️⃣ one\n2️⃣ two\n10️⃣ ten")
    assert out == "1. one\n2. two\n10. ten"
    assert "⃣" not in out and "️" not in out


def _h1_detail() -> dict[str, object]:
    """The shared sample detail, but with the real H1 rubric (carries display_label)."""
    detail = _sample_detail()
    detail["rubric"] = rubric_for_display(H1_RUBRIC)
    return detail


def _set_first_block_content(detail: dict[str, object], content: str) -> None:
    """Overwrite the first reading-note block's prose (typed nav avoids ty noise)."""
    candidate_pack = cast(dict[str, object], detail["candidate_pack"])
    manifest = cast(dict[str, object], candidate_pack["manifest"])
    steps = cast(list[dict[str, object]], manifest["steps"])
    blocks = cast(list[dict[str, object]], steps[0]["blocks"])
    blocks[0]["content"] = content


def test_h1_html_worksheet_contains_expected_text() -> None:
    pdf_bytes = render_worksheet_pdf(_h1_detail())

    assert pdf_bytes.startswith(b"%PDF")
    text = extract_pdf_text(pdf_bytes).replace("\n", " ")
    # Single-line title; no "Expert rater" eyebrow / "Welcome" heading.
    assert "Revision-Note Review Worksheet for Expert Rater" in text
    assert "Welcome, expert rater" not in text
    # Verbatim welcome wording.
    assert "prepared by a teacher" in text
    assert "is clear and useful for the students" in text
    # Section structure. The "Student revision note" tag is uppercased by CSS, so
    # the extracted text reads "STUDENT REVISION NOTE"; match case-insensitively.
    assert "student revision note" in text.lower()
    assert "Rating sheet" in text
    assert "Flag any problems" in text
    # The major-issue flag plain labels.
    assert "Misses a required objective" in text
    assert "Goes beyond this lesson" in text
    # Institution band — blinded study title (no framework/AI hint for raters).
    assert "UNIVERSITY OF LAGOS" in text
    assert "research study of revision-note quality" in text
    assert "Lesson-Plan-Driven" not in text


def test_h1_html_worksheet_uses_teacher_friendly_rubric_labels() -> None:
    text = " ".join(extract_pdf_text(render_worksheet_pdf(_h1_detail())).split())
    # Teacher-friendly display labels lead each rubric row...
    assert "Covers the right topics" in text
    assert "Clear and useful for students" in text
    # ...and the technical research term is NOT shown to raters (data only).
    assert "Objective and curriculum alignment" not in text


def test_h1_html_worksheet_renders_markdown_emphasis_not_literal_markers() -> None:
    detail = _h1_detail()
    _set_first_block_content(
        detail,
        "The millions digit(s) - *million*; the thousands digit(s) - *thousand*. "
        "Use **clear examples** when teaching.",
    )
    text = extract_pdf_text(render_worksheet_pdf(detail))
    assert "million" in text
    assert "thousand" in text
    assert "clear examples" in text
    # Emphasis must render as bold/italic, never leak as literal markers.
    assert "*million*" not in text
    assert "*thousand*" not in text
    assert "**clear examples**" not in text


def test_h1_html_worksheet_has_no_missing_glyph_boxes() -> None:
    detail = _h1_detail()
    # Exotic glyphs that would be ■ boxes under reportlab's CP1252 fonts; WeasyPrint
    # renders the Computer Modern TTFs with full Unicode, so they survive.
    _set_first_block_content(detail, "A billion equals 10⁹ (million → ten million → billion).")
    text = extract_pdf_text(render_worksheet_pdf(detail))
    assert "■" not in text  # ■ missing-glyph box


def test_render_markdown_inline_math_emits_svg() -> None:
    # ``$inline$`` math becomes an inline ``<svg>`` of glyph outlines (via
    # math_svg + matplotlib mathtext) so WeasyPrint — which has no MathML support
    # and no JS engine (so neither a ``<math>`` element nor the frontend's KaTeX
    # works) — renders real math. Pure helper, no WeasyPrint required.
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _render_markdown,
    )

    html = str(_render_markdown("Scientific notation: $10^{6}$ in text."))
    assert "<svg " in html
    assert "math-svg--inline" in html
    # The raw dollar-bracketed LaTeX must not leak through to the rendered HTML.
    assert "$10^{6}$" not in html
    # The arithmatex sentinel must be replaced; if conversion failed we'd still
    # see the marker span.
    assert "arithmatex" not in html


def test_render_markdown_fraction_emits_svg_with_fraction_bar() -> None:
    # The bug this fixes: ``\frac{3}{4}`` was collapsing to "34" in the PDF
    # because WeasyPrint renders a ``<math>`` element as bare text. The SVG path
    # carries the fraction bar (a filled rect baked into the glyph path), so the
    # output is a real fraction. We assert an SVG with path data is emitted and no
    # MathML/raw-LaTeX leaks through.
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _render_markdown,
    )

    html = str(_render_markdown(r"Three quarters is $\frac{3}{4}$."))
    assert "<svg " in html
    assert "<path " in html
    assert "<math" not in html
    assert r"\frac" not in html
    assert "arithmatex" not in html


def test_render_markdown_display_math_emits_block_svg() -> None:
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _render_markdown,
    )

    # ``$$display$$`` on its own paragraph becomes a block-level SVG.
    html = str(_render_markdown("Lead in.\n\n$$10^{6}$$\n\nFollow up."))
    assert "<svg " in html
    assert "math-svg--block" in html
    assert "$$10^{6}$$" not in html
    assert "arithmatex" not in html


def test_render_markdown_passes_through_currency_dollars() -> None:
    # Non-math dollars (``$5 USD`` is currency, not LaTeX) must stay as text — no
    # ``<svg>`` math, no arithmatex sentinel. arithmatex's heuristic is ``$``
    # immediately followed by non-space content and a closing ``$``; ``$5 USD``
    # has no closing ``$`` so it is correctly left alone.
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _render_markdown,
    )

    html = str(_render_markdown("He paid $5 USD for the textbook."))
    assert "<svg" not in html
    assert "arithmatex" not in html
    assert "$5 USD" in html


def test_render_markdown_math_with_inequality_survives_html_pre_escape() -> None:
    # The renderer ``html.escape``s its input *before* markdown runs, so a math
    # snippet with ``<`` arrives at the math converter as ``&lt;``. The unescape
    # pass in ``_convert_arithmatex_to_svg`` must reverse that so mathtext parses a
    # real less-than operator (and the rendered SVG contains no stray entity).
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _render_markdown,
    )

    html = str(_render_markdown("Inequality: $x < 5$"))
    assert "<svg " in html
    # The escaped entity must not have leaked into the math (it would mean the
    # unescape pass was skipped and mathtext saw the literal ``&lt;`` text).
    assert "&lt;" not in html.split("<svg", 1)[1].split("</svg>", 1)[0]
    assert "math-svg--inline" in html


def test_h1_html_worksheet_embeds_math_svg_not_raw_dollars() -> None:
    # End-to-end: the active download path renders math to inline SVG and never
    # leaks the raw ``$…$`` source. The math glyphs are vector *outlines* (not
    # selectable text), so we assert structure on the HTML the renderer feeds
    # WeasyPrint — the SVG/path is present and the raw markers are gone.
    from app.domains.evaluation.application.worksheet_html.renderer import (
        render_h1_worksheet_html,
    )

    detail = _h1_detail()
    _set_first_block_content(
        detail,
        "One million is written as 1,000,000. In scientific notation it is "
        "$10^{6}$. Multiplication: $5 \\times 6 = 30$. He paid $5 USD for the textbook.",
    )
    html = render_h1_worksheet_html(detail)
    # Both inline expressions rendered to SVG glyph outlines.
    assert "math-svg--inline" in html
    assert "<path " in html
    # Raw math source markers do not leak through.
    assert "$10^{6}$" not in html
    assert "\\times" not in html
    # Currency dollars (not LaTeX) survive as plain text.
    assert "$5 USD" in html


def test_h1_pdf_renders_math_without_raw_dollars() -> None:
    # End-to-end PDF: the math SVGs render (no crash) and the raw ``$…$`` source
    # never reaches the page. pdftotext cannot extract the SVG glyph outlines, so
    # we only assert on the plain text — currency survives, markers do not.
    detail = _h1_detail()
    _set_first_block_content(
        detail,
        "One million is written as 1,000,000. In scientific notation it is "
        "$10^{6}$. Multiplication: $5 \\times 6 = 30$. He paid $5 USD for the textbook.",
    )
    text = extract_pdf_text(render_worksheet_pdf(detail))
    flat = " ".join(text.split())
    # Currency dollars survive as text.
    assert "$5 USD" in flat
    # Math source markers do not.
    assert "$10^{6}$" not in flat
    assert "\\times" not in flat
    # No missing-glyph boxes.
    assert "■" not in flat


def test_a_command_the_model_left_undelimited_is_typeset_not_printed() -> None:
    r"""The model writes maths in prose without marking it as maths.

    ``Perimeter = 4 \times side`` reached the page with the backslash showing, and
    only in C0 and C1 — the two arms the registered endpoint compares — because the
    note-carrying arms copy notation she delimits properly. The renderer supplies the
    delimiter so it goes through the same SVG path as maths the model marked itself.
    """
    from app.domains.evaluation.application.worksheet_html.renderer import (
        render_h1_worksheet_html,
    )

    detail = _h1_detail()
    _set_first_block_content(
        detail,
        "A square has four equal sides. Perimeter = 4 \\times side. "
        "For a circle, use \\pi = \\frac{22}{7}.",
    )
    html = render_h1_worksheet_html(detail)
    assert "\\times" not in html
    assert "\\pi" not in html
    assert "\\frac" not in html
    assert "math-svg--inline" in html
    # The words either side stay prose: delimiting the whole run would typeset
    # "Perimeter" as nine italic letters.
    assert "Perimeter = 4 " in html
    assert " side." in html


def test_no_pack_renders_a_bare_latex_command_to_the_page() -> None:
    r"""The blanket guard: whatever the model writes, no backslash-command survives.

    Both defects this covers were silent — the PDF was produced, nothing warned, and
    only reading the output showed it. One assertion over the whole rendered page
    catches the class rather than the two members of it we have met.
    """
    from app.domains.evaluation.application.worksheet_html.renderer import (
        render_h1_worksheet_html,
    )

    detail = _h1_detail()
    _set_first_block_content(
        detail,
        # Every shape seen in the run: undelimited command, unclosed run, and a
        # field that carried its own JSON punctuation in.
        "Perimeter = 2 \\times (length + breadth).\n\n"
        "Therefore \\(EF = 7\\text{ cm} + 7\\text{ cm} = 14\\text{ cm}.\n\n"
        'The answer is 4xy",',
    )
    html = render_h1_worksheet_html(detail)
    body = html[html.index("<body") if "<body" in html else 0 :]
    assert count_bare_math(body) == 0
    assert '4xy"' not in body


def test_strip_source_citations_removes_lines_and_inline_markers() -> None:
    # No WeasyPrint needed — this exercises the pure-text helper directly.
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _strip_source_citations,
    )

    raw = (
        "A common multiple is shared by two numbers (REF-1). The LCM is the smallest "
        "shared one [REF-2], as ⟦REF-3⟧ and 【REF-4】 explain; see also REF-5.\n"
        "Sources: REF-1, REF-2, REF-3\n"
        "_Sources: REF-4, REF-5_"
    )
    out = _strip_source_citations(raw)
    # Inline markers in all bracketings are gone.
    assert "REF-1" not in out
    assert "REF-2" not in out
    assert "REF-3" not in out
    assert "REF-4" not in out
    assert "REF-5" not in out
    assert "⟦" not in out
    assert "【" not in out
    # Whole "Sources:" lines (with and without leading/trailing _) are dropped.
    assert "Sources" not in out
    # Surrounding prose survives, with no double spaces or space-before-punctuation.
    assert "A common multiple is shared by two numbers." in out
    assert "The LCM is the smallest shared one," in out
    assert "  " not in out
    assert " ." not in out
    assert " ," not in out


def test_render_markdown_removes_contentless_source_markers() -> None:
    # The contentless "(Source:)" forms are dropped by _EDITORIAL_SOURCES_RE in the
    # full render path (mirrored by the frontend EDITORIAL_SOURCES_RE).
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _render_markdown,
    )

    out = str(
        _render_markdown(
            "Water boils at 100 degrees (Source:). The freezing point is 0 (Source: ). "
            "Plants need sunlight (Sources:) to photosynthesise."
        )
    )
    assert "Source" not in out
    assert "Water boils at 100 degrees." in out
    assert "The freezing point is 0." in out
    assert "Plants need sunlight to photosynthesise." in out


def test_render_markdown_removes_every_parenthesised_source_annotation() -> None:
    # Full parity with the frontend: editorial meta-commentary AND real-looking
    # "(Source: <text>)" citations are both cut, and stripping the inner REF-N
    # never leaves a mangled "(Source: for X)" fragment.
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _render_markdown,
    )

    out = str(
        _render_markdown(
            "This is the prime-factor method (Source: REF-1 for definition; REF-2 for the method). "
            "ATP is the energy currency (Sources: Khan Academy)."
        )
    )
    assert "Source" not in out
    assert "REF-" not in out
    assert "(" not in out
    assert "This is the prime-factor method." in out
    assert "ATP is the energy currency." in out


def test_strip_source_citations_is_a_noop_without_citations() -> None:
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _strip_source_citations,
    )

    # Plain prose + markdown structure must pass through untouched (incl. list indent).
    raw = "### Worked example\nStep 1: list multiples.\n- two\n- three"
    assert _strip_source_citations(raw) == raw


def test_h1_html_worksheet_strips_source_citations() -> None:
    detail = _h1_detail()
    _set_first_block_content(
        detail,
        "Common multiples are shared by two numbers (REF-1). See ⟦REF-2⟧ too.\n"
        "Sources: REF-1, REF-2",
    )
    text = " ".join(extract_pdf_text(render_worksheet_pdf(detail)).split())
    # The revision note shows the prose but not the citations (those are the audit's job).
    assert "Common multiples are shared by two numbers" in text
    assert "REF-1" not in text
    assert "REF-2" not in text
    assert "Sources" not in text


def test_h1_html_worksheet_drops_explanation_label() -> None:
    # The explanation block carries its own heading, so no generic "Explanation".
    detail = _h1_detail()
    _set_first_block_content(detail, "### Worked example\nWork through a sample LCM.")
    text = " ".join(extract_pdf_text(render_worksheet_pdf(detail)).split())
    assert "Worked example" in text  # the content's own heading survives
    assert "Explanation" not in text  # the redundant block label is gone


def test_h1_html_worksheet_renders_to_at_least_three_pages() -> None:
    page_texts = _extract_pdf_page_texts(render_worksheet_pdf(_h1_detail()))
    assert len(page_texts) >= 3
    assert all(page.strip() for page in page_texts)
    # Objectives on page 1; rating sheet at the tail.
    assert "Identify common multiples" in page_texts[0]
    tail = "\n".join(page_texts[-2:])
    assert "Rating sheet" in tail
    assert "Flag any problems" in tail


# --- pdftotext helpers (mirror test_h1_packet_worksheet_pdf) -----------------


def test_h1_html_worksheet_module_skips_without_weasyprint(monkeypatch: Any) -> None:
    # Sanity-check the skip guard itself: simulate a missing native dep.
    import app.domains.evaluation.application.worksheet_html.renderer as renderer_mod

    def _boom(*_args: object, **_kwargs: object) -> bytes:
        raise OSError("cannot load library 'libgobject-2.0-0'")

    monkeypatch.setattr(renderer_mod, "render_h1_worksheet_html_pdf", _boom)
    with pytest.raises(pytest.skip.Exception):
        render_worksheet_pdf(_h1_detail())


def _extract_pdf_page_texts(pdf_bytes: bytes) -> list[str]:
    if shutil.which("pdftotext") is None or shutil.which("pdfinfo") is None:
        pytest.skip("pdftotext/pdfinfo is not available")
    with TemporaryDirectory() as tmpdir:
        pdf_path = Path(tmpdir) / "worksheet.pdf"
        pdf_path.write_bytes(pdf_bytes)
        info = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        page_count = 0
        for line in info.stdout.splitlines():
            if line.startswith("Pages:"):
                page_count = int(line.split(":", maxsplit=1)[1].strip())
                break
        assert page_count > 0
        page_texts: list[str] = []
        for page_number in range(1, page_count + 1):
            text_path = Path(tmpdir) / f"page-{page_number}.txt"
            subprocess.run(
                [
                    "pdftotext",
                    "-f",
                    str(page_number),
                    "-l",
                    str(page_number),
                    str(pdf_path),
                    str(text_path),
                ],
                check=True,
                capture_output=True,
            )
            page_texts.append(text_path.read_text(encoding="utf-8"))
        return page_texts


def test_strip_source_citations_survives_unicode_dashes() -> None:
    """The model writes ``REF‑1`` with U+2011, not an ASCII hyphen.

    A pattern keyed on hyphen-minus stripped 0 of 25 markers from a real C2 pack, so
    every one reached the rater — and since C0/C1 carry no markers at all, one survivor
    identifies the condition on sight and the blinding is gone.
    """
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _strip_source_citations,
    )

    expected = "The perimeter is 30 cm and so on."
    for marker in ("REF-1", "REF‑1", "(REF‑2)", "[REF–3]", "REF4", "⟦REF-5⟧"):
        raw = f"The perimeter is 30 cm {marker} and so on."
        stripped = _strip_source_citations(raw)
        assert "REF" not in stripped.upper(), marker
        # The words either side must not be welded together by the cut.
        assert stripped == expected, (marker, stripped)


def test_source_ref_pattern_strips_ids_that_are_not_ref_shaped() -> None:
    """Scoped note evidence issues step ids, which match no ``REF-\\d+`` pattern."""
    from app.domains.evaluation.application.worksheet_html.renderer import (
        _source_ref_pattern,
    )

    pattern = _source_ref_pattern(["step-t3w02-04", "s1"])
    assert pattern is not None
    assert pattern.sub("", "Grounded in step-t3w02-04 here.") == "Grounded in here."
    assert pattern.sub("", "Grounded in (step‑t3w02‑04) here.") == "Grounded in here."
    assert _source_ref_pattern([]) is None
    assert _source_ref_pattern(["  "]) is None


def test_a_unit_typed_with_a_narrow_space_typesets_without_a_dummy_glyph() -> None:
    r"""The model writes "5 cm" — U+202F, which Computer Modern has no glyph for.

    mathtext substitutes a dummy symbol and the learner reads "5□cm" in an answer.
    ``\,`` is the same space in notation the font does have. 46 of the run's 72 cells
    carried one, across every arm.
    """
    from app.domains.evaluation.application.worksheet_html.math_svg import (
        _typesettable,
        render_latex_svg,
    )

    for space in (" ", " "):
        assert _typesettable(f"5{space}\\text{{cm}}") == r"5\,\text{cm}"
        assert "<svg " in render_latex_svg(f"5{space}\\text{{cm}}", display=False)


def test_a_degree_sign_inside_maths_is_not_drawn_as_a_gamma() -> None:
    r"""The silent one: nothing was missing, the wrong glyph was drawn.

    Computer Modern maps U+00B0 to the same outline as ``\gamma``, so
    ``\((n-2)\times180°\)`` reached the page as "180γ" — and because the glyph is
    present rather than missing, the fallback watcher never fired and no test, log
    or eye caught it. 13 fields across the judged run, C1 worst at 7.
    """
    from app.domains.evaluation.application.worksheet_html.math_svg import (
        _outline,
        _typesettable,
    )

    assert _typesettable(r"(n-2)\times180°") == r"(n-2)\times180^\circ"

    def extents(expr: str) -> list[float]:
        return list(_outline(expr, "cm", quiet=True)[0].get_extents().extents)

    degree = extents(_typesettable("180°"))
    assert degree != extents(r"180\gamma")
    assert degree == extents(r"180^\circ")


def test_latex_mathtext_does_not_implement_is_rewritten_not_refused() -> None:
    r"""Valid LaTeX the typesetter has no support for, so the source reaches the page.

    mathtext is a subset of LaTeX. ``\displaystyle``, ``\boxed{…}``, the ``\big``
    family and ``\tfrac`` all raise, and the caller then falls back to the raw
    expression — 18 across the judged run, 13 of them on C3, so it was directional
    toward the grounded arm.
    """
    from app.domains.evaluation.application.worksheet_html.math_svg import (
        _typesettable,
        render_latex_svg,
    )

    for written in (
        r"\displaystyle a + (b + c) = a + b + c",
        r"\boxed{2x + 40}",
        r"2\big((w + 3) + w\big) = 46",
        r"\bigl(a\bigr)",
        r"\tfrac{1}{2}",
        r"\dfrac{1}{2}",
    ):
        assert "<svg " in render_latex_svg(written, display=False)

    # Dropped, not mapped to \left…\right: those must pair, so an unpaired \big(
    # would trade a fallback for a parse error.
    assert _typesettable(r"2\big((w + 3) + w\big) = 46") == r"2((w + 3) + w) = 46"
    assert _typesettable(r"\boxed{2x + 40}") == r"{2x + 40}"


def test_missing_glyph_warnings_are_what_that_normalisation_silences(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Judged on the warning matplotlib emits, since the tofu itself is path data."""
    from app.domains.evaluation.application.worksheet_html.renderer import _render_markdown

    with caplog.at_level(logging.WARNING):
        html = str(_render_markdown("The perimeter is $22 \\text{cm}$ altogether."))
    assert "<svg " in html
    assert not [r for r in caplog.records if "does not have a glyph" in r.getMessage()]


def test_a_price_in_naira_is_not_drawn_as_a_box(caplog: pytest.LogCaptureFixture) -> None:
    """Computer Modern has no U+20A6, and mathtext substitutes rather than refusing.

    Her money problems are written in the currency the class uses, so a JSS1 learner
    read "▯250" where a price was — nine times in one arm of the run, and silently:
    the render succeeds, the glyph is just wrong.
    """
    from app.domains.evaluation.application.worksheet_html.math_svg import render_latex_svg

    with caplog.at_level(logging.WARNING):
        plain = render_latex_svg(r"3 \times 250 = 750", display=False)
        priced = render_latex_svg(r"3 \times ₦250 = ₦750", display=False)
    assert "<svg " in priced
    assert not [r for r in caplog.records if "does not have a glyph" in r.getMessage()]
    # Same expression plus two glyphs Computer Modern lacks: it cannot be the same
    # outline data, or the fallback did not happen.
    assert priced != plain


def test_computer_modern_still_sets_everything_it_can_draw() -> None:
    """The fallback is per-expression, and swapping the typeface is the cost of it.

    Judged against mathtext's own answer rather than a codepoint list, because it
    resolves literal × and − to Computer Modern glyphs their codepoints are not in
    the font's cmap for — a list would swap the typeface on expressions that set
    perfectly well.
    """
    from app.domains.evaluation.application.worksheet_html.math_svg import _outline

    for expr in (r"\frac{22}{7}", r"3 \times 4 = 12", "3 × 4", "5 − 2", "60°", r"\pi r^2"):
        _, missed = _outline(expr, "cm", quiet=True)
        assert not missed, f"{expr} would needlessly fall back off Computer Modern"
