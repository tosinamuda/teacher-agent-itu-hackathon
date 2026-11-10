"""Offline source-grounding audit pack PDF (Final Evaluation Protocol §5.4).

**FROZEN FALLBACK — do not grow.** Sibling of ``h1_worksheet_pdf.py``: kept as a
reportlab fallback for environments without the WeasyPrint native libs (see
``worksheet_html/README.md``). New audit-pack work goes in the WeasyPrint
renderer; only bug fixes that keep WeasyPrint + reportlab outputs in parity
belong here.

Self-contained printable pack: instructions + the 0/1/2 scale legend, then one card
per audit item (lesson objective, generated excerpt, cited source id + snippet, scope
boundary, and a 4-criteria 0/1/2 grid + comment). Shares the worksheet renderer's
Computer Modern fonts, print-safe monochrome palette, drawn markers, and text
sanitiser so the audit pack matches the H1/H2 worksheets (no ■ glyph boxes).
"""

# pylint: disable=duplicate-code
# Intentionally-independent reportlab fallback renderer (the active path is
# WeasyPrint). It shares small setup snippets with its sibling h1_worksheet_pdf by
# design and they are kept decoupled — see AGENTS.md "PDF rendering".

from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import cast
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.config import CONFIG
from app.domains.evaluation.application.h1_worksheet_pdf import (
    _ACCENT,
    _FILL,
    _GRID,
    _INK,
    _MUTED,
    _MUTED_SOFT,
    _RULE,
    _deep_pdf_safe,
    _Marker,
)
from app.domains.evaluation.application.pdf_fonts import (
    FONT_BOLD,
    FONT_REGULAR,
    ensure_fonts_registered,
)
from app.shared.json_types import JsonObject

_CRITERIA = (
    ("Source relevance", "Cited source is about the same concept/objective as the excerpt."),
    ("Support sufficiency", "Source actually supports the generated claim/example/item."),
    ("Faithfulness", "Generated text does not distort the source or add unsupported claims."),
    ("Scope correctness", "Source is within the approved lesson/topic/scope boundary."),
)


def render_source_audit_pack_pdf(detail: Mapping[str, object]) -> bytes:
    """Render the source-grounding audit pack for one experiment's sampled items."""
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
        title="Source-Grounding Audit Pack",
        author="Plan-to-Tutor",
        pageCompression=0,
    )
    styles = _styles()
    textbook_name = str(detail.get("textbook_name") or "the source textbook")
    items = cast(list[JsonObject], detail.get("items") or [])

    story: list = [
        Paragraph(escape(CONFIG.institution_name.upper()), styles["institution"]),
        Paragraph(escape(CONFIG.study_title), styles["study_title"]),
        Spacer(1, 1.5 * mm),
        HRFlowable(color=_RULE, thickness=0.8, width="100%"),
        Spacer(1, 3 * mm),
        Paragraph("Source-Grounding Audit Pack", styles["title"]),
        Paragraph("Expert source-audit worksheet", styles["eyebrow"]),
        Spacer(1, 3 * mm),
        Paragraph(
            (
                "For each item below, judge whether the cited source from "
                f"<b>{escape(textbook_name)}</b> supports the generated excerpt. Score every "
                "criterion <b>0</b> (fail), <b>1</b> (partial/unclear), or <b>2</b> (pass). "
                "This is a separate check from the H1/H2 quality rating."
            ),
            styles["body"],
        ),
        Spacer(1, 2 * mm),
        Paragraph(
            "0 = criterion not met · 1 = some support, incomplete/ambiguous · 2 = clearly met",
            styles["legend"],
        ),
        Spacer(1, 4 * mm),
    ]

    if not items:
        story.append(
            Paragraph("No audit items have been built for this experiment yet.", styles["body"])
        )
    for index, item in enumerate(items, start=1):
        story.extend(_item_card(index, item, styles))

    document.build(story)
    return buffer.getvalue()


def _item_card(index: int, item: Mapping[str, object], styles: dict[str, ParagraphStyle]) -> list:
    condition = str(item.get("condition_code") or "—")
    source_ref = str(item.get("source_ref") or "—")
    source_id = str(item.get("source_record_id") or "—")
    objective = str(item.get("objective_text") or item.get("lesson_objective_id") or "—")
    excerpt = str(item.get("generated_excerpt") or "—")
    snippet = str(
        item.get("source_excerpt") or "Source snippet unavailable — consult the textbook."
    )
    scope = str(item.get("scope_boundary") or "—")
    audit_id = str(item.get("audit_item_id") or f"SG-{index}")

    return [
        Paragraph(
            f"Audit item {index} · {escape(condition)} · cited {escape(source_ref)}",
            styles["item_head"],
        ),
        Paragraph(f"{escape(audit_id)}", styles["meta"]),
        HRFlowable(color=_GRID, thickness=0.6, width="100%"),
        Spacer(1, 1.5 * mm),
        Paragraph("Lesson objective", styles["label"]),
        Paragraph(escape(objective), styles["body"]),
        Spacer(1, 1.5 * mm),
        Paragraph("Generated excerpt", styles["label"]),
        Paragraph(escape(excerpt), styles["body"]),
        Spacer(1, 1.5 * mm),
        Paragraph(f"Cited source ({escape(source_id)})", styles["label"]),
        Paragraph(escape(snippet), styles["source"]),
        Spacer(1, 1.5 * mm),
        Paragraph(f"Topic/scope boundary: {escape(scope)}", styles["meta"]),
        Spacer(1, 2 * mm),
        _criteria_table(styles),
        Spacer(1, 5 * mm),
    ]


def _criteria_table(styles: dict[str, ParagraphStyle]) -> Table:
    rows: list[list[object]] = [
        [
            Paragraph("Criterion", styles["th"]),
            Paragraph("0", styles["th_c"]),
            Paragraph("1", styles["th_c"]),
            Paragraph("2", styles["th_c"]),
            Paragraph("Comment", styles["th"]),
        ]
    ]
    for label, description in _CRITERIA:
        rows.append(
            [
                Paragraph(f"<b>{escape(label)}</b><br/>{escape(description)}", styles["crit"]),
                _Marker(shape="circle"),
                _Marker(shape="circle"),
                _Marker(shape="circle"),
                Paragraph("", styles["body"]),
            ]
        )
    table = Table(rows, colWidths=[78 * mm, 12 * mm, 12 * mm, 12 * mm, 64 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, _RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, _GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("VALIGN", (1, 1), (3, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (3, -1), "CENTER"),
                ("BACKGROUND", (0, 0), (-1, 0), _FILL),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    ink = _INK
    muted = _MUTED
    return {
        "institution": ParagraphStyle(
            "AuditInstitution",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=13,
            textColor=ink,
            alignment=TA_LEFT,
            spaceAfter=1,
        ),
        "study_title": ParagraphStyle(
            "AuditStudyTitle",
            parent=sample["Normal"],
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=11.5,
            textColor=muted,
            alignment=TA_LEFT,
        ),
        "title": ParagraphStyle(
            "AuditTitle",
            parent=sample["Title"],
            fontName=FONT_BOLD,
            fontSize=18,
            leading=22,
            textColor=ink,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "eyebrow": ParagraphStyle(
            "AuditEyebrow",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=9,
            leading=11,
            textColor=_ACCENT,
            uppercase=True,
        ),
        "body": ParagraphStyle(
            "AuditBody",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=9.5,
            leading=12.5,
            textColor=ink,
            alignment=TA_LEFT,
        ),
        "source": ParagraphStyle(
            "AuditSource",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=12,
            textColor=_MUTED_SOFT,
            backColor=_FILL,
            borderPadding=4,
        ),
        "legend": ParagraphStyle(
            "AuditLegend",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=11,
            textColor=muted,
        ),
        "item_head": ParagraphStyle(
            "AuditItemHead",
            parent=sample["Heading3"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=14,
            textColor=ink,
            spaceAfter=1,
        ),
        "meta": ParagraphStyle(
            "AuditMeta",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=8,
            leading=10,
            textColor=muted,
        ),
        "label": ParagraphStyle(
            "AuditLabel",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=10.5,
            textColor=_ACCENT,
            spaceAfter=1,
        ),
        "crit": ParagraphStyle(
            "AuditCrit",
            parent=sample["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=8.5,
            leading=10.5,
            textColor=ink,
        ),
        "th": ParagraphStyle(
            "AuditTh",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=10.5,
            textColor=ink,
        ),
        "th_c": ParagraphStyle(
            "AuditThC",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=10.5,
            textColor=ink,
            alignment=1,
        ),
        "box": ParagraphStyle(
            "AuditBox",
            parent=sample["BodyText"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=13,
            textColor=ink,
            alignment=1,
        ),
    }
