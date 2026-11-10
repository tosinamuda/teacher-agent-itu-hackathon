import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.db.deps import get_db
from app.domains.evaluation.api import routes as evaluation_routes
from app.domains.evaluation.application.h1_worksheet_pdf import (
    _pdf_safe,
    render_h1_packet_worksheet_pdf,
)
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor

client = TestClient(app)

_TEST_RATER = Actor(role="rater", auth_id="code|rater-1", full_name="Rater One")


async def _noop_enforce(*_args, **_kwargs) -> None:
    """Allow every call — the Casbin layer has its own tests in ``test_authz.py``."""


def _sample_detail() -> dict[str, object]:
    return {
        "evaluation_packet_id": "EPK-TEST",
        "packet_code": "EPK-TEST",
        "hypothesis": "H1",
        "status": "ready",
        "lesson_title": "JSS1 Mathematics Week 3 Session 1: LCM of whole numbers",
        "lesson_subtitle": "LCM of whole numbers",
        "objectives": [
            {
                "lesson_objective_id": "obj-1",
                "objective_text": "Identify common multiples of two or more whole numbers",
            }
        ],
        "reference_sheet": {
            "subject": "Mathematics",
            "grade": "JSS1",
            "term": "First Term",
            "week": 3,
            "topic": "LCM / HCF",
            "subtopic": "LCM of whole numbers",
            "theme": "Number and Numeration",
            "curriculum_objectives": [
                "Identify common multiples of two or more whole numbers",
                "Find the LCM of whole numbers",
            ],
            "instructional_materials": ["Board", "Markers"],
            "references": [
                "Siyavula. (2023). JSS1 Mathematics. Retrieved from https://siyavula.com/resources/jss1-mathematics/very/long/reference/path"
            ],
        },
        "candidate_pack": {
            "scope": "class_level",
            "manifest": {
                "steps": [
                    {
                        "step_id": "step-1",
                        "title": "Introduction",
                        "step_kind": "core",
                        "instructional_type": "explain",
                        "estimated_minutes": 10,
                        "blocks": [
                            {
                                "type": "explanation",
                                "id": "block-1",
                                "content": (
                                    "### Explain common multiples and the LCM.\n"
                                    "Use **clear examples** and remind learners that "
                                    "\\(0\\) is not used for the least common multiple."
                                ),
                            }
                        ],
                    }
                ]
            },
        },
        "rubric": [
            {
                "criterion_id": "objective_coverage",
                "label": "Objective coverage",
                "description": (
                    "Judge how fully the review pack covers the intended lesson objectives."
                ),
                "scale_min": 1,
                "scale_max": 5,
            }
        ],
        "existing_rating": None,
    }


def test_render_h1_packet_worksheet_pdf_contains_expected_text() -> None:
    pdf_bytes = render_h1_packet_worksheet_pdf(_sample_detail())

    assert pdf_bytes.startswith(b"%PDF")
    extracted_text = _extract_pdf_text(pdf_bytes)
    assert "Revision-Note Review Worksheet for Expert Rater" in extracted_text.replace("\n", " ")
    assert "prepared by a teacher" in extracted_text.replace("\n", " ")
    assert "Student revision note" in extracted_text
    assert "Objective" in extracted_text
    assert "coverage" in extracted_text
    assert "LCM of whole numbers" in extracted_text
    assert "<br/>" not in extracted_text
    assert "&#8203;" not in extracted_text
    assert "Hypothesis" not in extracted_text


def test_render_h1_packet_worksheet_pdf_avoids_blank_middle_pages() -> None:
    pdf_bytes = render_h1_packet_worksheet_pdf(_multi_page_detail())
    page_texts = _extract_pdf_page_texts(pdf_bytes)

    assert len(page_texts) >= 3
    assert all(text.strip() for text in page_texts)
    # Lesson objectives live on the instruction cover (page 1), not repeated on
    # the rating sheet.
    assert "Identify common multiples of two or more whole numbers" in page_texts[0]
    # The rating sheet is the final section of the booklet.
    tail = "\n".join(page_texts[-2:])
    assert "Rating sheet" in tail
    assert "Flag any problems" in tail


def test_download_h1_packet_worksheet_returns_pdf_attachment(monkeypatch) -> None:
    async def _fake_db():
        yield SimpleNamespace()

    async def _fake_export(_packets, *, evaluation_packet_id, rater_id):
        return b"%PDF-1.4\n%worksheet", "EPK-TEST-worksheet.pdf"

    # The download route is guarded by ``requires(obj="rating:*", act="read")``;
    # this is a transport-layer test, so act as a rater and short-circuit the
    # Casbin enforcer (its own behaviour is covered in test_authz.py).
    app.dependency_overrides[get_actor] = lambda: _TEST_RATER
    monkeypatch.setattr(authz, "enforce", _noop_enforce)
    app.dependency_overrides[get_db] = _fake_db
    monkeypatch.setattr(evaluation_routes, "generate_h1_worksheet", _fake_export)

    response = client.get(
        "/evaluation/h1/packets/EPK-TEST/worksheet.pdf",
        params={"rater_id": "RATER-TEST"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"] == (
        'attachment; filename="EPK-TEST-worksheet.pdf"'
    )
    assert response.content.startswith(b"%PDF")

    app.dependency_overrides.clear()


def test_evaluation_meta_endpoint_returns_study_identity() -> None:
    # The rater workspace header reads institution + study title from this
    # endpoint, keeping the digital home in sync with the printed packs.
    response = client.get("/evaluation/meta")
    assert response.status_code == 200
    body = response.json()
    assert body["institution_name"] == "University of Lagos"
    # Blinded: the rater-facing study title must be neutral (no framework/AI hint).
    assert "research study of revision-note quality" in body["study_title"]
    assert "Lesson-Plan-Driven" not in body["study_title"]
    assert body["textbook_name"]


def test_pdf_safe_maps_unicode_offenders_to_renderable_ascii() -> None:
    # Superscripts/subscripts -> caret/underscore notation.
    assert _pdf_safe("10⁹") == "10^9"
    assert _pdf_safe("H₂O") == "H_2O"
    # Non-breaking hyphen, arrow, narrow no-break space -> plain ASCII.
    assert _pdf_safe("powers‑of‑ten") == "powers-of-ten"
    assert _pdf_safe("million → billion") == "million -> billion"
    assert _pdf_safe("ten million") == "ten million"
    # Exotic bracketed inline citation -> readable, separated [REF-N].
    assert _pdf_safe("down a column⟦REF-3⟧") == "down a column [REF-3]"
    # Already-clean citations and the Sources footer are left intact.
    assert _pdf_safe("a thousand (REF-1).") == "a thousand (REF-1)."
    assert _pdf_safe("Sources: REF-1, REF-2") == "Sources: REF-1, REF-2"
    # CP1252-native glyphs survive untouched; nothing maps to a missing-glyph box.
    safe = _pdf_safe("11½ days, 10×10 chart — “quote”")
    assert "½" in safe and "×" in safe and "■" not in safe


def test_render_has_no_missing_glyph_boxes_for_unicode_content() -> None:
    detail = _sample_detail()
    steps = detail["candidate_pack"]["manifest"]["steps"]  # type: ignore[index]
    steps[0]["blocks"][0]["content"] = (
        "A billion equals 10⁹. This is the powers‑of‑ten table "
        "(million → ten million → billion)⟦REF-1⟧.\n\n_Sources: REF-1_"
    )
    extracted_text = _extract_pdf_text(render_h1_packet_worksheet_pdf(detail))
    assert "■" not in extracted_text
    assert "10^9" in extracted_text
    assert "powers-of-ten" in extracted_text
    assert "[REF-1]" in extracted_text
    # The single-underscore emphasis markers should not leak as literal text.
    assert "_Sources" not in extracted_text


def test_worksheet_has_no_references_row() -> None:
    # Textbook references were removed from the H1/H2 rater worksheet (Final
    # Evaluation Protocol) — they belong to the separate source-grounding audit.
    extracted_text = _extract_pdf_text(render_h1_packet_worksheet_pdf(_sample_detail()))
    assert "References" not in extracted_text


def test_worksheet_renders_major_issue_flag_section() -> None:
    # The H1 rating worksheet carries the Final Evaluation Protocol §3.4
    # major-issue checklist — a categorical failure-mode tag captured alongside
    # the 1-5 scores. Labels are plain (no jargon); markers are drawn, not glyphs.
    extracted_text = _extract_pdf_text(render_h1_packet_worksheet_pdf(_sample_detail()))
    assert "Flag any problems" in extracted_text
    assert "Misses a required objective" in extracted_text
    assert "Goes beyond this lesson" in extracted_text
    assert "Wrong or misleading content" in extracted_text
    assert "Too hard for JSS1 to follow" in extracted_text
    assert "■" not in extracted_text


def test_worksheet_renders_markdown_emphasis_not_literal_markers() -> None:
    # Reading-note prose uses markdown emphasis; it must render as bold/italic
    # (Computer Modern faces), never leak as literal * / ** / _ markers.
    detail = _sample_detail()
    steps = detail["candidate_pack"]["manifest"]["steps"]  # type: ignore[index]
    steps[0]["blocks"][0]["content"] = (
        "The millions digit(s) - *million*; the thousands digit(s) - *thousand*. "
        "Use **clear examples** when teaching."
    )
    extracted_text = _extract_pdf_text(render_h1_packet_worksheet_pdf(detail))
    assert "million" in extracted_text
    assert "thousand" in extracted_text
    assert "clear examples" in extracted_text
    assert "*million*" not in extracted_text
    assert "*thousand*" not in extracted_text
    assert "**clear examples**" not in extracted_text
    assert "■" not in extracted_text


def test_worksheet_renders_institution_band() -> None:
    # Printed rater packs carry the institution + study title (Computer Modern,
    # print-safe monochrome) so they match the thesis report.
    extracted_text = _extract_pdf_text(render_h1_packet_worksheet_pdf(_sample_detail()))
    assert "UNIVERSITY OF LAGOS" in extracted_text
    assert "research study of revision-note quality" in extracted_text


def _extract_pdf_text(pdf_bytes: bytes) -> str:
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


def _multi_page_detail() -> dict[str, object]:
    detail = _sample_detail()
    detail["candidate_pack"] = {
        "scope": "class_level",
        "manifest": {
            "steps": [
                {
                    "step_id": f"step-{index}",
                    "title": f"Section {index}",
                    "step_kind": "core",
                    "instructional_type": "explain_example_practice",
                    "estimated_minutes": 8,
                    "blocks": [
                        {
                            "type": "explanation",
                            "id": f"ex-{index}",
                            "content": "\n".join(
                                [
                                    "### Multiple method",
                                    (
                                        "Use **long enough explanation text** to force "
                                        "the export onto several pages."
                                    ),
                                    "Write the multiples and compare them carefully.",
                                ]
                                * 8
                            ),
                        },
                        {
                            "type": "practice",
                            "id": f"pr-{index}",
                            "question": "Find the LCM of 15 and 20.",
                            "answer": "60",
                            "hints": [
                                "List a few multiples of each number.",
                                "Look for the smallest shared multiple.",
                            ],
                        },
                    ],
                }
                for index in range(1, 4)
            ]
        },
    }
    return detail
