"""Offline H1 reading-note worksheet PDF (Final Evaluation Protocol §5.3).

**FROZEN FALLBACK — do not grow.** The active rater-pack renderer is WeasyPrint
(``worksheet_html/renderer.py``); this reportlab implementation is kept as a
fallback for environments without the WeasyPrint native libs (Pango, cairo,
gdk-pixbuf, fontconfig, HarfBuzz — see ``worksheet_html/README.md``). New rater-pack
work goes in the WeasyPrint renderer; only bug fixes that keep WeasyPrint + reportlab
outputs in parity belong here.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable, Mapping, Sequence
from io import BytesIO
from typing import Any, cast
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.config import CONFIG
from app.domains.evaluation.application.pdf_fonts import (
    FONT_BOLD,
    FONT_REGULAR,
    ensure_fonts_registered,
)
from app.shared.json_types import JsonObject

# H1 major-issue flag (Final Evaluation Protocol §3.4): a categorical "what
# specifically broke" tag the rater ticks alongside the 1-5 dimension scores —
# a fast failure-mode signal, not a graded dimension. Persisted in the rating's
# notes under "major_issues" (list of keys) + "major_issue_other" (text).
# Each entry is (stable key for the dataset, plain rater-facing label, one-line
# gloss). The plain labels avoid jargon; the keys keep the analysis rigorous.
H1_MAJOR_ISSUE_FLAGS: tuple[tuple[str, str, str], ...] = (
    (
        "objective_missing",
        "Misses a required objective",
        "Skips something the lesson was meant to teach.",
    ),
    (
        "scope_drift",
        "Goes beyond this lesson",
        "Includes material outside this lesson's scope (e.g. next week's topic).",
    ),
    (
        "conceptual_error",
        "Wrong or misleading content",
        "Contains a mathematical or factual mistake.",
    ),
    (
        "unclear_for_learners",
        "Too hard for JSS1 to follow",
        "Likely confusing for the students.",
    ),
    (
        "other",
        "Other",
        "Something else — write it in.",
    ),
)

# Print-safe monochrome palette. These worksheets are routinely printed in black
# and white, so the design uses ink + grays only (no colour accents).
_INK = colors.HexColor("#111111")  # primary text + drawn marks
_MUTED = colors.HexColor("#555555")  # secondary text / table labels
_MUTED_SOFT = colors.HexColor("#444444")  # small print
_ACCENT = colors.HexColor("#333333")  # eyebrows / block labels (was terracotta)
_RULE = colors.HexColor("#9a9a9a")  # box borders / hairlines
_GRID = colors.HexColor("#cfcfcf")  # inner grid lines
_FILL = colors.HexColor("#f2f2f2")  # light panel fill


class _Marker(Flowable):
    """A drawn tick mark — a circle for single-select, a square for multi-select.

    Drawn as vector geometry rather than a font glyph, so it is crisp at any size
    and immune to missing-glyph boxes. The shape encodes selection semantics:
    ``circle`` = choose exactly one (the 1-5 score rows, the 0/1/2 audit rows),
    ``square`` = choose any that apply (the major-issue flags).
    """

    def __init__(self, *, shape: str = "square", size: float = 3.4 * mm) -> None:
        super().__init__()
        self.shape = shape
        self.size = size
        self.width = size
        self.height = size
        self.hAlign = "CENTER"

    def draw(self) -> None:
        canvas = self.canv
        canvas.setStrokeColor(_INK)
        canvas.setLineWidth(0.9)
        if self.shape == "circle":
            radius = self.size / 2.0
            canvas.circle(radius, radius, radius, stroke=1, fill=0)
        else:
            canvas.rect(0, 0, self.size, self.size, stroke=1, fill=0)


def render_h1_packet_worksheet_pdf(detail: Mapping[str, object]) -> bytes:
    # The reading-note text is LLM-generated and routinely contains glyphs the
    # built-in Helvetica font (WinAnsi/CP1252) cannot draw — superscripts, arrows,
    # non-breaking hyphens, exotic spaces, bracketed citation markers — each of
    # which reportlab renders as a ■ box. Normalise the whole detail tree once,
    # up front, so every downstream Paragraph receives renderable text.
    ensure_fonts_registered()
    detail = cast(Mapping[str, object], _deep_pdf_safe(detail))
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=15 * mm,
        title="Revision-Note Review Worksheet",
        author="Plan-to-Tutor",
        pageCompression=0,
    )
    styles = _styles()
    story = _worksheet_story(detail, styles)
    document.build(
        story,
        onFirstPage=_page_template(detail, styles),
        onLaterPages=_page_template(detail, styles),
    )
    return buffer.getvalue()


def _worksheet_story(detail: Mapping[str, object], styles: dict[str, ParagraphStyle]) -> list:
    reference_sheet = cast(Mapping[str, object], detail["reference_sheet"])
    candidate_pack = cast(Mapping[str, object], detail["candidate_pack"])
    manifest = cast(Mapping[str, object], candidate_pack["manifest"])

    # Page 1 is the instruction cover: welcome + lesson context + objectives +
    # what to do. The revision note itself starts on the next page, and the rating
    # sheet follows it.
    story: list = [
        *_institution_band(styles),
        Paragraph("Revision-Note Review Worksheet for Expert Rater", styles["title"]),
        Spacer(1, 3 * mm),
        Paragraph(_welcome_note(detail), styles["body"]),
        Spacer(1, 4 * mm),
        _section_heading("Lesson and revision-note context", styles),
        _reference_sheet_table(reference_sheet, styles),
        Spacer(1, 4 * mm),
        _section_heading("Lesson objectives", styles),
        _objectives_table(cast(list[JsonObject], detail["objectives"]), styles),
        Spacer(1, 4 * mm),
        Paragraph(
            (
                "Read the student revision note on the following pages, then complete "
                "the rating sheet at the end of this booklet."
            ),
            styles["body"],
        ),
        PageBreak(),
        _section_heading("Student revision note", styles),
        Spacer(1, 2 * mm),
    ]

    for step in cast(list[JsonObject], manifest["steps"]):
        story.extend(_step_section(step, styles))

    story.extend(
        [
            PageBreak(),
            Paragraph("Rating sheet", styles["section"]),
            Paragraph(
                (
                    "Mark one score per criterion, then use the notes section for "
                    "strengths, concerns, and recommendations. The lesson objectives "
                    "are on the first page for reference."
                ),
                styles["body"],
            ),
            Spacer(1, 4 * mm),
            _rating_header(detail, styles),
            Spacer(1, 4 * mm),
            _rating_worksheet(detail, styles),
            Spacer(1, 4 * mm),
            _rating_notes_table(styles),
            Spacer(1, 4 * mm),
        ]
    )
    story.extend(_major_issue_flag(styles))
    return story


def _institution_band(styles: dict[str, ParagraphStyle]) -> list:
    """Institution + study-title header band shown atop the rater pack."""
    return [
        Paragraph(escape(CONFIG.institution_name.upper()), styles["institution"]),
        Paragraph(escape(CONFIG.study_title), styles["study_title"]),
        Spacer(1, 1.5 * mm),
        HRFlowable(color=_RULE, thickness=0.8, width="100%"),
        Spacer(1, 3 * mm),
    ]


def _welcome_note(detail: Mapping[str, object]) -> str:
    reference_sheet = cast(Mapping[str, object], detail["reference_sheet"])
    grade = _value_or_dash(reference_sheet.get("grade"))
    subject = _value_or_dash(reference_sheet.get("subject"))
    subtopic = _value_or_dash(reference_sheet.get("subtopic"))
    return (
        "This booklet contains one student revision note to review. It is a "
        f"take-home revision note prepared by a teacher for a {grade} {subject} "
        f"class on {subtopic}. Judge how well it covers the intended objectives "
        "and curriculum, follows the teacher's lesson plan, stays on topic and is "
        "conceptually correct, and is clear and useful for the students."
    )


def _section_heading(text: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    return Paragraph(escape(text), styles["section"])


def _reference_sheet_table(
    reference_sheet: Mapping[str, object],
    styles: dict[str, ParagraphStyle],
) -> Table:
    rows = [
        [_table_label("Subject", styles), _table_value(reference_sheet.get("subject"), styles)],
        [_table_label("Grade", styles), _table_value(reference_sheet.get("grade"), styles)],
        [_table_label("Term", styles), _table_value(reference_sheet.get("term"), styles)],
        [_table_label("Week", styles), _table_value(reference_sheet.get("week"), styles)],
        [_table_label("Subtopic", styles), _table_value(reference_sheet.get("subtopic"), styles)],
        [_table_label("Theme", styles), _table_value(reference_sheet.get("theme"), styles)],
        [
            _table_label("Curriculum objectives", styles),
            _table_value(cast(list, reference_sheet.get("curriculum_objectives", [])), styles),
        ],
        [
            _table_label("Previous knowledge", styles),
            _table_value(cast(list, reference_sheet.get("entry_behaviour", [])), styles),
        ],
        [
            _table_label("Lesson sequence", styles),
            _table_value(cast(list, reference_sheet.get("lesson_sequence", [])), styles),
        ],
        [
            _table_label("Instructional materials", styles),
            _table_value(cast(list, reference_sheet.get("instructional_materials", [])), styles),
        ],
        [
            _table_label("Evaluation", styles),
            _table_value(cast(list, reference_sheet.get("evaluation", [])), styles),
        ],
        # Textbook references are not shown to H1/H2 raters (they are not part of what
        # H1/H2 measures) — source faithfulness is checked in the source-grounding audit.
    ]
    table = Table(rows, colWidths=[38 * mm, 138 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), _FILL),
                ("TEXTCOLOR", (0, 0), (0, -1), _MUTED),
                ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
                ("FONTNAME", (1, 0), (1, -1), FONT_REGULAR),
                ("BOX", (0, 0), (-1, -1), 0.6, _RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, _GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _objectives_table(objectives: list[JsonObject], styles: dict[str, ParagraphStyle]) -> Table:
    rows = [
        [
            Paragraph(f"{index + 1}.", styles["body_bold"]),
            Paragraph(escape(str(objective.get("objective_text") or "—")), styles["body"]),
        ]
        for index, objective in enumerate(objectives)
    ]
    table = Table(
        rows or [[Paragraph("No objectives available.", styles["body"]), ""]],
        colWidths=[12 * mm, 164 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, _RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, _GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _step_section(step: JsonObject, styles: dict[str, ParagraphStyle]) -> list:
    blocks = cast(list[JsonObject], step.get("blocks", []))
    parts: list = [
        Paragraph(
            escape(str(step.get("title") or step.get("step_id") or "Step")),
            styles["step_title"],
        ),
        HRFlowable(color=_GRID, thickness=0.6, width="100%"),
        Spacer(1, 2 * mm),
    ]
    for block in blocks:
        parts.extend(_render_block(block, styles))
    parts.extend(
        [
            Spacer(1, 2 * mm),
            HRFlowable(color=_GRID, thickness=0.6, width="100%"),
            Spacer(1, 3 * mm),
        ]
    )
    return parts


def _render_block(block: JsonObject, styles: dict[str, ParagraphStyle]) -> list:
    block_type = str(block.get("type") or "")
    if block_type == "explanation":
        return [
            Spacer(1, 2 * mm),
            Paragraph("Explanation", styles["block_label"]),
            Paragraph(_paragraph_text(str(block.get("content") or "")), styles["body"]),
        ]
    if block_type == "worked_example":
        steps = cast(list[JsonObject], block.get("steps", []))
        return [
            Spacer(1, 2 * mm),
            Paragraph("Worked example", styles["block_label"]),
            Paragraph(
                f"<b>Problem:</b> {_paragraph_text(str(block.get('problem') or ''))}",
                styles["body"],
            ),
            Spacer(1, 1.5 * mm),
            Paragraph("<b>Steps:</b>", styles["body_bold"]),
            *[
                Paragraph(_paragraph_text(_worked_step_text(step)), styles["body"])
                for step in steps
            ],
            Spacer(1, 1.5 * mm),
            Paragraph(
                f"<b>Final answer:</b> {_paragraph_text(str(block.get('final_answer') or ''))}",
                styles["body"],
            ),
        ]
    if block_type == "practice":
        hints = cast(list, block.get("hints", []) or [])
        parts = [
            Spacer(1, 2 * mm),
            Paragraph("Practice", styles["block_label"]),
            Paragraph(
                f"<b>Question:</b> {_paragraph_text(str(block.get('question') or ''))}",
                styles["body"],
            ),
        ]
        if hints:
            parts.extend(
                [
                    Spacer(1, 1.5 * mm),
                    Paragraph("<b>Hints:</b>", styles["body_bold"]),
                    Paragraph(_bullet_text(hints), styles["body"]),
                ]
            )
        answer = str(block.get("answer") or "").strip()
        if answer:
            parts.extend(
                [
                    Spacer(1, 1.5 * mm),
                    Paragraph(f"<b>Answer:</b> {_paragraph_text(answer)}", styles["body"]),
                ]
            )
        return parts
    if block_type == "visual":
        caption = str(block.get("caption") or "").strip()
        if caption:
            return [
                Spacer(1, 2 * mm),
                Paragraph("Visual", styles["block_label"]),
                Paragraph(_paragraph_text(caption), styles["body"]),
            ]
    return []


def _worked_step_text(step: Mapping[str, object]) -> str:
    label = str(step.get("label") or "").strip()
    content = str(step.get("content") or "").strip()
    if label and content:
        return f"{label}: {content}"
    return label or content


def _rating_header(detail: Mapping[str, object], styles: dict[str, ParagraphStyle]) -> Table:
    rows = [
        [
            _table_label("Revision note ID", styles),
            _table_value(detail.get("packet_code"), styles, allow_breaks=False),
            _table_label("Date", styles),
            Paragraph("", styles["table_value"]),
        ],
        [
            _table_label("Subtopic", styles),
            _table_value(
                cast(Mapping[str, object], detail["reference_sheet"]).get("subtopic"),
                styles,
                allow_breaks=False,
            ),
            _table_label("Rater", styles),
            Paragraph("", styles["table_value"]),
        ],
    ]
    table = Table(rows, colWidths=[26 * mm, 64 * mm, 20 * mm, 70 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, _RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, _GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BACKGROUND", (0, 0), (0, -1), _FILL),
                ("BACKGROUND", (2, 0), (2, -1), _FILL),
                ("LINEBELOW", (3, 0), (3, 0), 0.8, _INK),
                ("LINEBELOW", (3, 1), (3, 1), 0.8, _INK),
            ]
        )
    )
    return table


def _rating_worksheet(detail: Mapping[str, object], styles: dict[str, ParagraphStyle]) -> Table:
    rubric_rows: list[list[object]] = [
        [
            Paragraph(
                "Criterion <font size=7>(select one score per row)</font>",
                styles["worksheet_header"],
            ),
            *[
                Paragraph(label, styles["worksheet_scale_header"])
                for label in (
                    "1<br/>Poor",
                    "2<br/>Weak",
                    "3<br/>Adequate",
                    "4<br/>Strong",
                    "5<br/>Excellent",
                )
            ],
        ]
    ]
    for criterion in cast(list[JsonObject], detail["rubric"]):
        display_label = escape(str(criterion.get("display_label") or criterion.get("label") or ""))
        rubric_rows.append(
            [
                Paragraph(
                    (
                        f"<b>{display_label}</b><br/>"
                        f"{_rich_text(str(criterion.get('description') or ''))}"
                    ),
                    styles["worksheet_criterion"],
                ),
                *[_Marker(shape="circle") for _ in range(5)],
            ]
        )

    table = Table(
        rubric_rows,
        colWidths=[70 * mm, 22 * mm, 22 * mm, 22 * mm, 22 * mm, 22 * mm],
        hAlign="LEFT",
        repeatRows=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, _RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, _GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("VALIGN", (1, 1), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (-1, 0), _FILL),
                ("BACKGROUND", (0, 1), (0, -1), _FILL),
            ]
        )
    )
    return table


def _rating_notes_table(styles: dict[str, ParagraphStyle]) -> Table:
    rows = [
        [_table_label("Strengths", styles), Paragraph("", styles["note_box"])],
        [_table_label("Concerns", styles), Paragraph("", styles["note_box"])],
        [_table_label("Recommendation", styles), Paragraph("", styles["note_box"])],
    ]
    table = Table(rows, colWidths=[36 * mm, 144 * mm], hAlign="LEFT", rowHeights=[18 * mm] * 3)
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, _RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, _GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (0, -1), _FILL),
            ]
        )
    )
    return table


def _major_issue_flag(styles: dict[str, ParagraphStyle]) -> list:
    """Render the Protocol §3.4 major-issue checklist as a blank tick-box panel.

    A categorical failure-mode tag the rater ticks alongside the 1-5 dimension
    scores — it records *what specifically broke*, not a graded quality. On the
    offline worksheet it is a blank checklist; the digital form captures it as
    checkboxes persisted in the rating's notes.
    """
    rows = []
    for key, label, gloss in H1_MAJOR_ISSUE_FLAGS:
        if key == "other":
            text = f"<b>{escape(label)}:</b> ______________________________"
        else:
            text = f"<b>{escape(label)}</b> — {escape(gloss)}"
        rows.append([_Marker(shape="square"), Paragraph(text, styles["body"])])
    table = Table(rows, colWidths=[9 * mm, 171 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, _RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 0), (-1, -1), _FILL),
            ]
        )
    )
    # Keep the heading, helper line, and checklist on the same page — otherwise
    # the section can orphan its heading at a page break.
    return [
        KeepTogether(
            [
                Paragraph("Flag any problems (optional)", styles["section"]),
                Paragraph(
                    (
                        "Tick all that apply. These are separate from the scores above "
                        "— leave blank if none apply."
                    ),
                    styles["body"],
                ),
                Spacer(1, 2 * mm),
                table,
            ]
        )
    ]


def _page_template(
    detail: Mapping[str, object], styles: dict[str, ParagraphStyle]
) -> Callable[[Any, Any], None]:
    packet_code = str(detail.get("packet_code") or "H1")

    def _draw(canvas: Any, doc: Any) -> None:
        canvas.saveState()
        canvas.setStrokeColor(_RULE)
        canvas.line(
            doc.leftMargin,
            doc.height + doc.topMargin + 6,
            A4[0] - doc.rightMargin,
            doc.height + doc.topMargin + 6,
        )
        canvas.setFont(FONT_REGULAR, 8)
        canvas.setFillColor(_MUTED)
        canvas.drawString(doc.leftMargin, 10 * mm, packet_code)
        canvas.drawRightString(A4[0] - doc.rightMargin, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    return _draw


def _styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    return {
        "institution": ParagraphStyle(
            "H1WorksheetInstitution",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=13,
            textColor=_INK,
            alignment=TA_LEFT,
            spaceAfter=1,
        ),
        "study_title": ParagraphStyle(
            "H1WorksheetStudyTitle",
            parent=sample["Normal"],
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=11.5,
            textColor=_MUTED,
            alignment=TA_LEFT,
            spaceAfter=0,
        ),
        "title": ParagraphStyle(
            "H1WorksheetTitle",
            parent=sample["Title"],
            fontName=FONT_BOLD,
            fontSize=18,
            leading=22,
            textColor=_INK,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "eyebrow": ParagraphStyle(
            "H1WorksheetEyebrow",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=9,
            leading=11,
            textColor=_ACCENT,
            uppercase=True,
            spaceAfter=0,
        ),
        "heading": ParagraphStyle(
            "H1WorksheetHeading",
            parent=sample["Heading1"],
            fontName=FONT_BOLD,
            fontSize=14,
            leading=17,
            textColor=_INK,
            spaceAfter=2,
        ),
        "subheading": ParagraphStyle(
            "H1WorksheetSubheading",
            parent=sample["Normal"],
            fontName=FONT_REGULAR,
            fontSize=10,
            leading=13,
            textColor=_MUTED,
            spaceAfter=0,
        ),
        "subheading_strong": ParagraphStyle(
            "H1WorksheetSubheadingStrong",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=14,
            textColor=_INK,
            spaceAfter=2,
        ),
        "section": ParagraphStyle(
            "H1WorksheetSection",
            parent=sample["Heading2"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=14,
            textColor=_INK,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "H1WorksheetBody",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=9.5,
            leading=12,
            textColor=_INK,
            alignment=TA_LEFT,
        ),
        "body_bold": ParagraphStyle(
            "H1WorksheetBodyBold",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=9.5,
            leading=12,
            textColor=_INK,
            alignment=TA_LEFT,
        ),
        "body_small": ParagraphStyle(
            "H1WorksheetBodySmall",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=8.5,
            leading=10.5,
            textColor=_MUTED_SOFT,
            splitLongWords=1,
        ),
        "table_label": ParagraphStyle(
            "H1WorksheetTableLabel",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=10.5,
            textColor=_MUTED,
        ),
        "table_value": ParagraphStyle(
            "H1WorksheetTableValue",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=8.5,
            leading=10.5,
            textColor=_INK,
            splitLongWords=1,
            wordWrap="CJK",
        ),
        "step_title": ParagraphStyle(
            "H1WorksheetStepTitle",
            parent=sample["Heading3"],
            fontName=FONT_BOLD,
            fontSize=10.5,
            leading=13,
            textColor=_INK,
            spaceAfter=1,
        ),
        "step_meta": ParagraphStyle(
            "H1WorksheetStepMeta",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=10,
            textColor=_MUTED,
            spaceAfter=2,
        ),
        "block_label": ParagraphStyle(
            "H1WorksheetBlockLabel",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=10,
            textColor=_ACCENT,
            spaceAfter=1,
        ),
        "worksheet_header": ParagraphStyle(
            "H1WorksheetHeader",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=10.5,
            textColor=_INK,
        ),
        "worksheet_scale_header": ParagraphStyle(
            "H1WorksheetScaleHeader",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8,
            leading=9.5,
            alignment=TA_LEFT,
            textColor=_INK,
        ),
        "worksheet_criterion": ParagraphStyle(
            "H1WorksheetCriterion",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=8.5,
            leading=10.5,
            textColor=_INK,
        ),
        "worksheet_checkbox": ParagraphStyle(
            "H1WorksheetCheckbox",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=13,
            textColor=_INK,
            alignment=TA_LEFT,
        ),
        "note_box": ParagraphStyle(
            "H1WorksheetNoteBox",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=8.5,
            leading=10.5,
            textColor=colors.white,
        ),
    }


def _paragraph_text(value: str) -> str:
    text = value.strip()
    if not text:
        return "—"
    return _content_markup(text)


def _bullet_text(items: Sequence[object]) -> str:
    texts = [str(item).strip() for item in items if str(item).strip()]
    if not texts:
        return "—"
    return "<br/>".join(f"- {_content_markup(text)}" for text in texts)


def _table_label(text: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    return Paragraph(escape(text), styles["table_label"])


def _table_value(
    value: object,
    styles: dict[str, ParagraphStyle],
    *,
    allow_breaks: bool = True,
) -> Paragraph:
    if isinstance(value, list):
        text = _bullet_text(value)
    else:
        text = _rich_text(_value_or_dash(value), allow_breaks=allow_breaks)
    return Paragraph(text, styles["table_value"])


def _normalize_markdown(text: str) -> str:
    """Strip block-level markdown noise (headings, code spans, escaped brackets).

    Inline emphasis (``**bold**`` / ``*italic*`` / ``_italic_``) is intentionally
    left in place here — it is converted to reportlab ``<b>``/``<i>`` markup after
    XML escaping by :func:`_apply_emphasis`, so it renders in the proper Computer
    Modern bold/italic face rather than leaking as literal ``*`` / ``_`` markers.
    """
    normalized = text.replace("\r\n", "\n")
    normalized = re.sub(r"(?m)^#{1,6}\s*", "", normalized)
    normalized = re.sub(r"`([^`]*)`", r"\1", normalized)
    normalized = normalized.replace("\\(", "(").replace("\\)", ")")
    normalized = normalized.replace("\\[", "[").replace("\\]", "]")
    return normalized


def _apply_emphasis(text: str) -> str:
    """Convert markdown emphasis in already XML-escaped text to reportlab markup.

    Bold runs before italic so ``**x**`` is not mis-split by the single-``*`` pass.
    Single ``*``/``_`` delimiters are anchored on non-word boundaries, so prose
    like ``*million*`` becomes italic while ``3 * 4`` and ``snake_case`` are left
    untouched. Delimiters must hug their content (no inner leading/trailing space).
    """
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w_])__(?=\S)(.+?)(?<=\S)__(?![\w_])", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_(?=\S)([^_\n]+?)(?<=\S)_(?!\w)", r"<i>\1</i>", text)
    return text


def _content_markup(value: str) -> str:
    """Render reading-note prose: normalise → XML-escape → emphasis → line breaks."""
    normalized = _normalize_markdown(value)
    escaped = escape(normalized.strip() or "—")
    escaped = _apply_emphasis(escaped)
    return escaped.replace("\n", "<br/>")


def _rich_text(value: str, *, allow_breaks: bool = False) -> str:
    escaped = escape(value.strip() or "—")
    if allow_breaks:
        for token in ("/", ".", "-", "_", "?", "&", "="):
            escaped = escaped.replace(token, f"{token}\u200b")
    return escaped.replace("\n", "<br/>")


def _value_or_dash(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, str):
        text = value.strip()
        return text or "—"
    return str(value)


# --- Helvetica-safe text normalisation -------------------------------------
#
# reportlab's built-in fonts only carry the WinAnsi (CP1252) glyph repertoire,
# so any character outside it renders as a ■ "missing glyph" box. LLM-generated
# reading-note prose regularly reaches outside that set. We map the meaningful
# offenders to readable ASCII equivalents, then drop anything still unrenderable.

_SUPERSCRIPT_MAP = {
    "²": "2",
    "³": "3",
    "¹": "1",
    "⁰": "0",
    "ⁱ": "i",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
    "⁺": "+",
    "⁻": "-",
    "⁼": "=",
    "⁽": "(",
    "⁾": ")",
    "ⁿ": "n",
}
_SUBSCRIPT_MAP = {
    "₀": "0",
    "₁": "1",
    "₂": "2",
    "₃": "3",
    "₄": "4",
    "₅": "5",
    "₆": "6",
    "₇": "7",
    "₈": "8",
    "₉": "9",
    "₊": "+",
    "₋": "-",
    "₌": "=",
    "₍": "(",
    "₎": ")",
}
_SUPERSCRIPT_RUN = re.compile("[" + re.escape("".join(_SUPERSCRIPT_MAP)) + "]+")
_SUBSCRIPT_RUN = re.compile("[" + re.escape("".join(_SUBSCRIPT_MAP)) + "]+")

# Single-character substitutions for glyphs CP1252 lacks but that carry meaning.
# (En/em dashes, curly quotes, ½, ×, ÷, …, • are already in CP1252 — left alone.)
_GLYPH_REPLACEMENTS = {
    "‐": "-",
    "‑": "-",
    "‒": "-",
    "―": "-",
    "−": "-",
    "→": "->",
    "←": "<-",
    "↔": "<->",
    "⇒": "=>",
    "⇐": "<=",
    "⇔": "<=>",
    "≠": "!=",
    "≤": "<=",
    "≥": ">=",
    "≈": "~=",
    "≡": "=",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    "​": "",
    "‌": "",
    "‍": "",
    "﻿": "",
    "′": "'",
    "″": '"',
    "⁄": "/",
    "⋅": "·",
    "∗": "*",
    # Exotic citation-wrapping brackets -> plain square brackets, so an inline
    # marker like ``⟦REF-1⟧`` survives as a readable ``[REF-1]``.
    "⟦": "[",
    "⟧": "]",
    "【": "[",
    "】": "]",
    "〔": "[",
    "〕": "]",
    "「": "[",
    "」": "]",
    "⌈": "[",
    "⌉": "]",
    "⌊": "[",
    "⌋": "]",
}
_TRANSLATION_TABLE = {ord(key): value for key, value in _GLYPH_REPLACEMENTS.items()}

# An inline ``REF-N`` citation glued to the preceding word (its wrapping bracket
# having been mapped or dropped). Insert a separating space — but not after an
# opening bracket or whitespace, so ``(REF-1)`` and the ``Sources: REF-1`` footer
# are left intact.
_GLUED_REF = re.compile(r"(?<=[^\s(\[{])(\[?REF-\d)")


def _pdf_safe(text: str) -> str:
    if not text:
        return text
    text = _SUPERSCRIPT_RUN.sub(
        lambda m: "^" + "".join(_SUPERSCRIPT_MAP[c] for c in m.group()), text
    )
    text = _SUBSCRIPT_RUN.sub(lambda m: "_" + "".join(_SUBSCRIPT_MAP[c] for c in m.group()), text)
    text = text.translate(_TRANSLATION_TABLE)
    if not text.isascii():
        text = "".join(_renderable(char) for char in text)
    return _GLUED_REF.sub(r" \1", text)


def _renderable(char: str) -> str:
    if char in "\n\r\t":
        return char
    try:
        char.encode("cp1252")
    except UnicodeEncodeError:
        # Strip accents/compatibility forms down to CP1252-encodable pieces;
        # if nothing survives, drop the character rather than draw a box.
        decomposed = unicodedata.normalize("NFKD", char)
        kept = []
        for part in decomposed:
            if unicodedata.combining(part):
                continue
            try:
                part.encode("cp1252")
            except UnicodeEncodeError:
                continue
            kept.append(part)
        return "".join(kept)
    return char


def _deep_pdf_safe(value: object) -> object:
    if isinstance(value, str):
        return _pdf_safe(value)
    if isinstance(value, Mapping):
        return {key: _deep_pdf_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_deep_pdf_safe(item) for item in value]
    return value
