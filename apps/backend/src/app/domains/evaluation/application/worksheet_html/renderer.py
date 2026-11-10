"""WeasyPrint renderer for the H1 reading-note review worksheet.

A parallel, additive alternative to ``h1_worksheet_pdf.py``. It builds the same
document — instruction cover, student revision note, rating sheet — from a Jinja2
HTML template + print CSS, and renders it to PDF with WeasyPrint.

Why this exists: the reportlab path hand-rolls markdown with regex (``_apply_
emphasis``) and maps non-CP1252 glyphs to ASCII to dodge missing-glyph boxes.
WeasyPrint renders real HTML with the full Unicode-capable Computer Modern TTFs,
so reading-note markdown (``**bold**``, ``*italic*``, lists, headings, tables)
renders natively via a proper markdown converter and exotic glyphs survive
unchanged. Selection markers are CSS shapes (circle = single-select score cells,
square = multi-select flags), not font glyphs.

Public entry point: :func:`render_h1_worksheet_html_pdf`.

Native libraries: WeasyPrint needs pango, cairo, gdk-pixbuf, fontconfig +
harfbuzz. On macOS (Homebrew) those dylibs live under ``$(brew --prefix)/lib``;
that directory is prepended to ``DYLD_FALLBACK_LIBRARY_PATH`` on import (only if
unset) so ``import weasyprint`` resolves them without the caller exporting it.
In the Docker image install the matching apt packages (see this module's README).
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from functools import lru_cache
from html import escape, unescape
from pathlib import Path
from typing import Any, cast

from markupsafe import Markup

from app.config import CONFIG

# Imported from its source-of-truth module (not ``service``) to avoid a circular
# import: ``service`` imports this renderer for the active download path.
from app.domains.evaluation.application.constants import H1_ALIGNMENT_GUIDANCE
from app.domains.evaluation.application.h1_worksheet_pdf import H1_MAJOR_ISSUE_FLAGS
from app.shared.item_numbering import under_supplied_number
from app.shared.llm_markup import reader_ready
from app.shared.native_libs import ensure_native_lib_path
from app.shared.tikz_svg import tikz_to_svg

_PACKAGE_DIR = Path(__file__).resolve().parent
# The Computer Modern TTFs are vendored next to the reportlab renderer.
_FONT_DIR = _PACKAGE_DIR.parent / "fonts"
_TEMPLATE_NAME = "worksheet.html.j2"
_STYLESHEET_NAME = "worksheet.css"

_SCALE_HEADERS: tuple[tuple[str, str], ...] = (
    ("1", "Poor"),
    ("2", "Weak"),
    ("3", "Adequate"),
    ("4", "Good"),
    ("5", "Excellent"),
)


@lru_cache(maxsize=1)
def _markdown_converter() -> Any:
    r"""Build a reusable python-markdown converter for trusted reading-note prose.

    ``extra`` gives fenced code, tables, and definition lists; ``sane_lists`` and
    ``nl2br`` make loose LLM markdown render predictably (single newlines become
    line breaks, mixed list markers do not merge). ``pymdownx.arithmatex`` with
    ``generic=True`` wraps ``$inline$`` / ``$$display$$`` math in
    ``<span class="arithmatex">\(…\)</span>`` / ``<div class="arithmatex">\[…\]</div>``
    sentinels — a later pass (:func:`_convert_arithmatex_to_svg`) swaps those for
    inline SVG so WeasyPrint can render the math without a MathML/JS engine.
    Input is XML-escaped *before* conversion (see :func:`_render_markdown`), so
    this only ever processes our own escaped text — no raw HTML injection path.
    """
    import markdown

    return markdown.Markdown(
        extensions=["extra", "sane_lists", "nl2br", "pymdownx.arithmatex"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}},
        output_format="html5",
    )


@lru_cache(maxsize=1)
def _jinja_environment() -> Any:
    """Autoescaping Jinja2 environment loaded from this package directory."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    return Environment(
        loader=FileSystemLoader(str(_PACKAGE_DIR)),
        autoescape=select_autoescape(default=True, enabled_extensions=("j2", "html")),
        trim_blocks=True,
        lstrip_blocks=True,
    )


@lru_cache(maxsize=4)
def _stylesheet(name: str = _STYLESHEET_NAME) -> str:
    """Return a print CSS with the {{ font_dir }} placeholder bound to a file:// URL.

    The fonts are referenced by absolute ``file://`` URL so WeasyPrint resolves
    them regardless of the process working directory. Packs that add rules of
    their own name a second sheet and concatenate; the shared one stays the base.
    """
    raw = (_PACKAGE_DIR / name).read_text(encoding="utf-8")
    font_url = _FONT_DIR.as_uri()
    return raw.replace("{{ font_dir }}", font_url)


def html_to_pdf(html: str) -> bytes:
    """Any HTML to PDF bytes, through the same native-library setup as the worksheet.

    The only place in the codebase that should import WeasyPrint: a caller that
    imports it directly works on a machine with the library path exported and
    fails on the next one with `cannot load library 'libgobject-2.0-0'`.
    """
    ensure_native_lib_path()
    from weasyprint import HTML  # imported lazily so the native-lib path is set first

    return cast(bytes, HTML(string=html, base_url=str(_PACKAGE_DIR)).write_pdf())


def render_h1_worksheet_html_pdf(detail: Mapping[str, object]) -> bytes:
    """Render the H1 reading-note review worksheet to PDF bytes via WeasyPrint.

    Accepts the same ``detail`` mapping as ``render_h1_packet_worksheet_pdf`` in
    the reportlab renderer (see ``_PacketDetailProjection._build_h1_packet_
    detail`` and ``tests.test_h1_packet_worksheet_pdf._sample_detail``). Returns a
    complete PDF document as bytes.
    """
    return html_to_pdf(_render_html(detail))


def render_h1_worksheet_html(detail: Mapping[str, object]) -> str:
    """Render the worksheet HTML only (no PDF) — useful for debugging/tests."""
    return _render_html(detail)


def _render_html(detail: Mapping[str, object]) -> str:
    reference_sheet = _as_mapping(detail.get("reference_sheet"))
    candidate_pack = _as_mapping(detail.get("candidate_pack"))
    manifest = _as_mapping(candidate_pack.get("manifest"))
    steps = [
        _step(cast(Mapping[str, object], step))
        for step in _sequence(manifest.get("steps"))
        if isinstance(step, Mapping)
    ]

    packet_code = _text_or_dash(detail.get("packet_code")) or "H1"
    candidate_label = _text_or_none(detail.get("candidate_label"))
    context = {
        "mode": "rater",
        "pack_label": None,
        # Blinded lesson-block position ("Candidate B") so an offline rater can
        # track which of the lesson's anonymous candidates this booklet is.
        "candidate_label": candidate_label,
        # The rater's footer-left keeps the packet code (their reference).
        "footer_note": packet_code,
        "institution_name": CONFIG.institution_name.upper(),
        "study_title": CONFIG.study_title,
        "packet_code": packet_code,
        "subtopic": _text_or_dash(reference_sheet.get("subtopic")),
        "grade": _text_or_dash(reference_sheet.get("grade")),
        "subject": _text_or_dash(reference_sheet.get("subject")),
        "week": _text_or_dash(reference_sheet.get("week")),
        "welcome_note": _welcome_note(reference_sheet),
        "reference_rows": _reference_rows(reference_sheet),
        "objectives": _objectives(detail.get("objectives")),
        "steps": steps,
        "answer_key": _answer_key(_sequence(manifest.get("steps"))),
        "rubric": _rubric(detail.get("rubric")),
        "rating_guidance": list(H1_ALIGNMENT_GUIDANCE),
        "scale_headers": [{"num": num, "word": word} for num, word in _SCALE_HEADERS],
        "major_issue_flags": _major_issue_flags(),
        "stylesheet": _stylesheet(),
    }
    template = _jinja_environment().get_template(_TEMPLATE_NAME)
    return cast(str, template.render(**context))


# --- Context builders -------------------------------------------------------


def _welcome_note(reference_sheet: Mapping[str, object]) -> str:
    grade = _text_or_dash(reference_sheet.get("grade"))
    subject = _text_or_dash(reference_sheet.get("subject"))
    subtopic = _text_or_dash(reference_sheet.get("subtopic"))
    return (
        "This booklet contains one student revision note to review. It is a "
        f"take-home revision note prepared by a teacher for a {grade} {subject} "
        f"class on {subtopic}. Judge how well it covers the intended objectives "
        "and curriculum, follows the teacher's lesson plan, stays on topic and is "
        "conceptually correct, and is clear and useful for the students."
    )


def _reference_rows(reference_sheet: Mapping[str, object]) -> list[dict[str, object]]:
    """Ordered key/value rows for the lesson-context table.

    Scalar rows carry ``value`` (``items`` = None); list rows carry ``items`` (a
    bulleted list) with ``value`` = None. Mirrors the reportlab reference table —
    textbook references are intentionally omitted (they belong to the separate
    source-grounding audit, not the H1 rater worksheet).
    """
    return [
        _scalar_row("Subject", reference_sheet.get("subject")),
        _scalar_row("Grade", reference_sheet.get("grade")),
        _scalar_row("Term", reference_sheet.get("term")),
        _scalar_row("Week", reference_sheet.get("week")),
        _scalar_row("Topic", reference_sheet.get("topic")),
        _scalar_row("Subtopic", reference_sheet.get("subtopic")),
        _scalar_row("Theme", reference_sheet.get("theme")),
        _list_row("Curriculum objectives", reference_sheet.get("curriculum_objectives")),
        _list_row("Previous knowledge", reference_sheet.get("entry_behaviour")),
        _list_row("Lesson sequence", reference_sheet.get("lesson_sequence")),
        _list_row("Instructional materials", reference_sheet.get("instructional_materials")),
        _list_row("Evaluation", reference_sheet.get("evaluation")),
    ]


def _scalar_row(label: str, value: object) -> dict[str, object]:
    return {"label": label, "value": _text_or_dash(value), "list_items": None}


def _list_row(label: str, value: object) -> dict[str, object]:
    """A list row, each item rendered as the pack's own text is.

    Her evaluation questions and the work she set carry maths the same way the
    pack does, and a rater comparing the two should meet it typeset in both
    places rather than as source on one side.
    """
    return {
        "label": label,
        "value": None,
        "list_items": [_render_markdown(item) for item in _string_list(value)],
    }


def _objectives(value: object) -> list[str]:
    texts: list[str] = []
    for entry in _sequence(value):
        if isinstance(entry, Mapping):
            entry_map = cast(Mapping[str, object], entry)
            text = _text_or_none(entry_map.get("objective_text"))
            texts.append(text or "—")
    return texts


def _rubric(value: object) -> list[dict[str, str]]:
    """Rubric rows for the rating sheet.

    Each row carries the teacher-friendly ``display_label`` (the bold lead, from
    ``CONFIG.rater_term_aliases`` via ``rubric_for_display``), the canonical
    technical ``label`` (shown small/gray in parens for the dataset/thesis link),
    and the ``description`` (the rater question). Mirrors the reportlab renderer.
    """
    rows: list[dict[str, str]] = []
    for entry in _sequence(value):
        if not isinstance(entry, Mapping):
            continue
        criterion = cast(Mapping[str, object], entry)
        label = _text_or_dash(criterion.get("label"))
        display_label = _text_or_none(criterion.get("display_label")) or label
        rows.append(
            {
                "display_label": display_label,
                "label": label,
                "description": _text_or_dash(criterion.get("description")),
            }
        )
    return rows


def _answer_key(steps: Sequence[object]) -> list[dict[str, object]]:
    """The answers, gathered out of the activities and into a closing section.

    The learner has no teacher to hand, so the worksheet has to be self-checkable —
    and it has to be attemptable first. An answer printed under its own question is
    neither, which is what three blinded judges marked packs down for (issue #163).
    Each practice item still carries its answer; only the placement is decided here.
    """
    groups: list[dict[str, object]] = []
    for entry in steps:
        if not isinstance(entry, Mapping):
            continue
        step = cast(Mapping[str, object], entry)
        answers = [
            {
                "question_html": rendered["question_html"],
                "answer_html": rendered["answer_html"],
                "hints_html": rendered["hints_html"],
            }
            for block in _sequence(step.get("blocks"))
            if isinstance(block, Mapping)
            for rendered in (_block(cast(Mapping[str, object], block), numbered=True),)
            if rendered is not None and rendered.get("type") == "practice"
        ]
        if answers:
            # Never fall back to step_id: the conditioned pipeline keys it to the
            # generation unit ("objective:…" for the baseline, "step:…" for every
            # lesson-plan condition), so printing it would tell a blinded rater
            # which condition they are scoring.
            title = _text_or_none(step.get("title")) or "Step"
            groups.append({"title": title, "answers": answers})
    return groups


def _step(step: Mapping[str, object]) -> dict[str, object]:
    """One objective's section: the instructional stream, then its practice as one set.

    Each practice item is its own manifest block, which rendered as its own "Practice /
    Question:" heading — five of them down a page for a five-question set. They are one
    activity to the learner, so they are numbered together and the numbering is what the
    answer page keys off.
    """
    # step_id is condition-correlated; see _answer_key.
    title = _text_or_none(step.get("title")) or "Step"
    rendered_blocks = [
        rendered
        for block in _sequence(step.get("blocks"))
        if isinstance(block, Mapping)
        for rendered in (_block(cast(Mapping[str, object], block), numbered=True),)
        if rendered is not None
    ]
    instruction = [block for block in rendered_blocks if block.get("type") != "practice"]
    practice = [
        block["question_html"] for block in rendered_blocks if block.get("type") == "practice"
    ]
    if practice:
        instruction.append({"type": "practice_set", "questions_html": practice})
    return {"title": title, "blocks": instruction}


def _explanation(block: Mapping[str, object], numbered: bool) -> dict[str, object] | None:
    return {
        "type": "explanation",
        "content_html": _render_markdown(_text_or_none(block.get("content")) or ""),
    }


def _worked_example(block: Mapping[str, object], numbered: bool) -> dict[str, object] | None:
    return {
        "type": "worked_example",
        "problem_html": _render_markdown(_text_or_none(block.get("problem")) or ""),
        "steps_html": [
            _render_markdown(_worked_step_text(cast(Mapping[str, object], step)))
            for step in _sequence(block.get("steps"))
            if isinstance(step, Mapping)
        ],
        "final_answer_html": _render_markdown(_text_or_none(block.get("final_answer")) or ""),
    }


def _practice(block: Mapping[str, object], numbered: bool) -> dict[str, object] | None:
    hints = _string_list(block.get("hints"))
    answer = _text_or_none(block.get("answer"))
    question = _text_or_none(block.get("question")) or ""
    if numbered:
        question = under_supplied_number(question)
        answer = under_supplied_number(answer) if answer else None
    return {
        "type": "practice",
        "question_html": _render_markdown(question),
        "hints_html": [_render_markdown(hint) for hint in hints],
        "answer_html": _render_markdown(answer) if answer else None,
    }


def _visual(block: Mapping[str, object], numbered: bool) -> dict[str, object] | None:
    caption = _text_or_none(block.get("caption"))
    # The prose cites the figure by its label — "as fig-01 shows" — so the label
    # is printed with it, in the form the teacher's own note writes it.
    if caption and (label := _text_or_none(block.get("figure_ref"))):
        caption = f"**{label}.** {caption}"
    url = _text_or_none(block.get("url"))
    drawing = _drawing(block)
    if not (caption or url or drawing):
        return None
    return {
        "type": "visual",
        "url": url,
        "svg": drawing,
        "caption": caption,
        "caption_html": _render_markdown(caption) if caption else None,
    }


_BLOCKS: dict[str, Callable[[Mapping[str, object], bool], dict[str, object] | None]] = {
    "explanation": _explanation,
    "worked_example": _worked_example,
    "practice": _practice,
    "visual": _visual,
}


def _block(block: Mapping[str, object], *, numbered: bool = False) -> dict[str, object] | None:
    """One manifest block, rendered.

    ``numbered`` says the caller prints the item's number itself — the practice set and
    the answer key do, every other surface labels the item instead ("Question:"). Only
    a caller that supplies a number can know that a number in the text duplicates it.
    """
    render = _BLOCKS.get(_text_or_none(block.get("type")) or "")
    return render(block, numbered) if render is not None else None


def _drawing(block: Mapping[str, object]) -> str | None:
    """The figure's own drawing, for a note whose diagrams are TikZ rather than images.

    Her construction lessons are drawings with sentences around them, and the worksheet
    printed the caption alone — "slide the set square along the ruler towards P" with
    nothing to slide. Falls back to that caption wherever TeX cannot draw it.
    """
    source = _text_or_none(block.get("source_tikz"))
    return tikz_to_svg(source) if source else None


def _worked_step_text(step: Mapping[str, object]) -> str:
    label = _text_or_none(step.get("label")) or ""
    content = _text_or_none(step.get("content")) or ""
    if label and content:
        return f"**{label}:** {content}"
    return label or content


def _major_issue_flags() -> list[dict[str, object]]:
    flags: list[dict[str, object]] = []
    for key, label, gloss in H1_MAJOR_ISSUE_FLAGS:
        flags.append({"is_other": key == "other", "label": label, "gloss": gloss})
    return flags


# --- Markdown + text helpers ------------------------------------------------

# Source citations are stripped from reading-note prose before markdown
# conversion: the H1/H2 raters judge fit-to-objective, not source grounding (that
# is the separate audit pack, which keeps its citations). We remove two shapes
# here; the parenthesised ``(Source: …)`` form (including the contentless
# ``(Source:)``) is handled separately by ``_EDITORIAL_SOURCES_RE``, applied
# unconditionally in :func:`_render_markdown`:
#   1. Whole "Sources: …" lines — the trailing citation list a revision note often
#      ends with — including an optional leading/trailing markdown emphasis ``_``.
#   2. Inline citation markers — ``(REF-1)``, ``[REF-1]``, ``⟦REF-1⟧``, ``【REF-1】``,
#      and a bare ``REF-1`` — wherever they appear mid-prose.
# After removal we tidy any double spaces / stray space-before-punctuation the cut
# leaves behind so surrounding prose reads naturally.
_SOURCES_LINE_RE = re.compile(
    r"^[ \t]*_?\s*sources?\s*:.*?_?[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)
# The separator is matched as a CHARACTER CLASS, not a literal "-". The model writes
# "REF‑1" with U+2011 NON-BREAKING HYPHEN, so a pattern keyed on ASCII hyphen-minus
# stripped 0 of 25 markers from a C2 pack and every one reached the rater — while C0 and
# C1 carry none, which identifies the condition on sight. Any dash-like character counts,
# as does none at all. Source ids that are not "REF"-shaped are handled by
# ``_source_ref_pattern`` below, which is built from the refs actually issued.
_DASHES = r"[-‐-―−­\s]*"
_INLINE_CITATION_RE = re.compile(
    rf"""
    \s*                          # absorb a leading space so we don't orphan one
    [(\[⟦【]?\s*                  # optional opening bracket of any flavour
    REF{_DASHES}\d+
    (?:\s*[)\]⟧】])?              # and its closing partner, if any
    """,
    # No trailing ``\s*``: it would swallow the space AFTER the marker too and weld the
    # neighbouring words together — "30 cm REF-1 and" became "30 cmand".
    re.IGNORECASE | re.VERBOSE,
)


def _source_ref_pattern(source_refs: Iterable[str]) -> re.Pattern[str] | None:
    r"""Match the exact refs handed to the model, dash-insensitively.

    Guessing at citation shapes is what failed before. The caller knows precisely which
    ``source_ref`` strings went into the prompt — under scoped note evidence they are step
    ids like ``step-t3w02-04`` and match no ``REF-\d+`` pattern at all — so the safe
    stripper is one built from that list rather than from a guess about format.
    """
    # Longest first, so a ref that is a prefix of another cannot match it away.
    named = {ref for ref in source_refs if ref.strip()}
    refs = sorted(named, key=lambda ref: len(ref), reverse=True)
    parts = [re.escape(ref).replace(r"\-", _DASHES) for ref in refs]
    if not parts:
        return None
    return re.compile(
        rf"\s*[(\[⟦【]?\s*(?:{'|'.join(parts)})(?:\s*[)\]⟧】])?",
        re.IGNORECASE,
    )


# Editorial parenthesised "(Source: REF-1 for X; REF-2 for Y.)" annotations the
# LLM occasionally appends to a paragraph — and the contentless "(Source:)" it
# sometimes leaves behind. These are not citations the rater needs to verify —
# they are meta-commentary about which reference covers what. ``[^()]*`` matches
# any (or no) content between the colon and the closing paren, so every
# parenthesised form is dropped. Stripped in every surface (including the audit
# pack, where the inline REF-N markers we *do* want to keep are not affected by
# this rule). The frontend ``EDITORIAL_SOURCES_RE`` mirrors this exactly.
_EDITORIAL_SOURCES_RE = re.compile(
    r"\s*\(\s*sources?\s*:[^()]*\)",
    re.IGNORECASE,
)
_MULTISPACE_RE = re.compile(r"[ \t]{2,}")
_SPACE_BEFORE_PUNCT_RE = re.compile(r"[ \t]+([,.;:!?])")


def _strip_source_citations(text: str) -> str:
    """Remove source citations from reading-note prose (see module notes above).

    Drops whole ``Sources: …`` lines and inline ``REF-N`` markers in their various
    bracketings, then collapses the double spaces / space-before-punctuation the
    removals can leave so the surrounding prose is not mangled. Markdown structure
    (headings, lists, emphasis) is untouched. Parenthesised ``(Source: …)``
    annotations are removed separately by ``_EDITORIAL_SOURCES_RE`` in
    :func:`_render_markdown`.
    """
    without_lines = _SOURCES_LINE_RE.sub("", text)
    without_inline = _INLINE_CITATION_RE.sub("", without_lines)
    tidied = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", without_inline)
    # Collapse runs of spaces line-by-line so leading indentation (markdown list /
    # code nesting) survives but mid-line double spaces from a cut are removed.
    tidied = "\n".join(
        _MULTISPACE_RE.sub(" ", line) if line[:1] not in (" ", "\t") else line
        for line in tidied.split("\n")
    )
    return tidied


# Computer Modern (the worksheet font) carries no emoji, so any emoji WeasyPrint
# cannot draw renders as a missing-glyph box. Reading-note prose occasionally uses
# emoji keycap digits ("1️⃣ 2️⃣ …") as ad-hoc numbered markers; normalise those to
# plain "1." text and drop stray emoji variation/keycap selectors so numbered steps
# read cleanly in print (the reportlab path did the same via its ASCII sanitiser).
# U+FE0F/FE0E = emoji/text variation selectors; U+20E3 = combining enclosing keycap.
_KEYCAP_RE = re.compile("([0-9#*])️?⃣")
_EMOJI_SELECTOR_RE = re.compile("[︎️⃣]")


def _normalize_text_glyphs(text: str) -> str:
    """Map emoji the Computer Modern font cannot render to plain-text equivalents."""
    text = _KEYCAP_RE.sub(r"\1.", text)
    return _EMOJI_SELECTOR_RE.sub("", text)


# Revision notes use underscore runs ("____" / "_ _ _") as fill-in answer blanks.
# Markdown mis-reads those underscores as emphasis (``<strong><em>_</em>…``), so
# we swap each run for a private-use sentinel before conversion and turn it into a
# single underlined blank afterwards — a clean connected fill-in line.
_BLANK_RE = re.compile(r"(?<!\w)_(?: ?_)+")


# LaTeX math markers emitted by ``pymdownx.arithmatex`` (``generic=True``):
# inline ``$…$`` becomes ``<span class="arithmatex">\(…\)</span>`` and display
# ``$$…$$`` becomes ``<div class="arithmatex">\[…\]</div>``. We convert each one
# to an inline ``<svg>`` of glyph outlines (via :mod:`.math_svg`) so WeasyPrint —
# which has no MathML support and no JavaScript engine (so neither the frontend's
# KaTeX nor a ``<math>`` element works) — renders real fractions/superscripts
# instead of bare digits (``\frac{3}{4}`` had been collapsing to "34"). The inner
# LaTeX is HTML-entity-escaped because it passed through our ``html.escape``
# pre-pass; unescape it before the converter so ``<``/``>``/``&`` reach mathtext as
# the characters they represent.
_INLINE_MATH_RE = re.compile(
    r'<span class="arithmatex">\\\((.*?)\\\)</span>',
    re.DOTALL,
)
_BLOCK_MATH_RE = re.compile(
    r'<div class="arithmatex">\\\[(.*?)\\\]</div>',
    re.DOTALL,
)


def _convert_arithmatex_to_svg(html: str) -> str:
    r"""Replace arithmatex marker spans/divs with inline SVG math.

    Inline ``\(…\)`` becomes an inline ``<svg class="math-svg math-svg--inline">``
    baseline-aligned to the text, and block ``\[…\]`` a centred
    ``<svg class="math-svg math-svg--block">`` on its own line. If mathtext cannot
    parse a snippet — bad or unsupported LaTeX from the LLM — leave the original
    arithmatex marker in place so the PDF still renders something (the raw ``\(…\)``
    text) rather than crashing the export.
    """
    from app.domains.evaluation.application.worksheet_html.math_svg import (
        render_latex_svg,
    )

    def _render(match: re.Match[str], *, display: bool) -> str:
        latex = unescape(match.group(1))
        try:
            return render_latex_svg(latex, display=display)
        except Exception:  # noqa: BLE001 — mathtext raises ad-hoc parse exceptions with no shared base (render_latex_svg normalises to ValueError, but stay defensive); LLM-authored LaTeX must never crash a PDF export, so fall back to the original marker.
            return match.group(0)

    html = _INLINE_MATH_RE.sub(lambda m: _render(m, display=False), html)
    return _BLOCK_MATH_RE.sub(lambda m: _render(m, display=True), html)


_BLANK_SENTINEL = ""


# Display math opening a line that continues the paragraph above it. Markdown reads the
# two as one paragraph, so arithmatex never wraps the run in the block it marks and the
# reader gets raw `\[P = 6 \times 4\text{ cm}\]` — which a blinded judge found sitting in
# an answer key, beside formulas that had rendered cleanly (issue #131).
_DISPLAY_MATH_RUN_ON = re.compile(r"(?<=\S)\n(?=\\\[)")


def _detach_display_math(text: str) -> str:
    r"""Give a line-initial ``\[`` the blank line markdown needs to see it as a block."""
    return _DISPLAY_MATH_RUN_ON.sub("\n\n", text)


def _render_markdown(text: str, *, strip_citations: bool = True) -> Markup:
    """Convert trusted reading-note markdown to safe inline HTML.

    Safety model: XML-escape the raw text *first* so any literal ``<``/``>``/``&``
    (or an injected ``<script>``) becomes inert entities, then run the markdown
    converter over the escaped text. The converter only ever sees our escaped
    string, so the only HTML in the result is the markup markdown itself emits
    (``<strong>``, ``<em>``, ``<ul>``, …) — no passthrough of attacker HTML. The
    result is wrapped in ``Markup`` so Jinja emits it without re-escaping.

    ``strip_citations`` (default on for the H1/H2 revision notes) removes source
    citations (``Sources: …`` lines + inline ``REF-N`` markers): those raters judge
    fit-to-objective, not source grounding. The source-grounding audit pack passes
    ``strip_citations=False`` because the cited reference *is* what it audits.
    """
    # Always strip the editorial parenthesised `(Sources: REF-x for …)`
    # annotations — even with `strip_citations=False`, those are meta-
    # commentary, not the inline REF-N markers the audit pack relies on.
    # Strip the full Sources line + inline REF markers only when the surface
    # is judging fit-to-objective (i.e. not the source-grounding audit).
    source = _EDITORIAL_SOURCES_RE.sub("", text)
    if strip_citations:
        source = _strip_source_citations(source)
    source = _normalize_text_glyphs(source)
    # Generation supplies the delimiters the model left off, but a pack stored before
    # it did — every pack in the two judged H1 runs, and every pack already in the
    # database — still carries `4 \times side` as prose. Idempotent, so a pack that
    # was cleaned at generation passes through unchanged.
    source = reader_ready(source)
    source = _detach_display_math(source)
    source = _BLANK_RE.sub(_BLANK_SENTINEL, source)
    stripped = source.strip()
    if not stripped:
        return Markup("—")
    escaped = escape(stripped)
    converter = _markdown_converter()
    converter.reset()
    html = converter.convert(escaped)
    # arithmatex (in the converter above) only marks math with sentinel spans/divs;
    # convert those sentinels to inline SVG now so WeasyPrint can render the math.
    html = _convert_arithmatex_to_svg(html)
    html = html.replace(_BLANK_SENTINEL, '<span class="fill-blank"></span>')
    # WeasyPrint PDF render of system-generated, already-escaped content.
    return Markup(html)  # nosec B704


def _as_mapping(value: object) -> Mapping[str, object]:
    return cast(Mapping[str, object], value) if isinstance(value, Mapping) else {}


def _sequence(value: object) -> Sequence[object]:
    """Return a non-string sequence, or an empty list — guards iteration over JSON values."""
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return value
    return []


def _text_or_none(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text or None
    return str(value)


def _text_or_dash(value: object) -> str:
    return _text_or_none(value) or "—"


def _string_list(value: object) -> list[str]:
    items: list[str] = []
    for item in _sequence(value):
        text = _text_or_none(item)
        if text is not None:
            items.append(text)
    return items
