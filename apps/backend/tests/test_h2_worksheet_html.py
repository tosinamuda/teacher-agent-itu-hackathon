"""Tests for the WeasyPrint H2 blinded revision-note worksheet renderer.

These exercise the *active* H2 download path
(``service.export_h2_packet_worksheet`` calls ``render_h2_worksheet_html_pdf``).
Like the H1 worksheet, WeasyPrint needs native libs
(pango/cairo/gdk-pixbuf/fontconfig/harfbuzz); each test skips cleanly when the
import fails so the suite stays green on a box without them.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient

from app.db.deps import get_db
from app.domains.evaluation.api import routes as evaluation_routes
from app.domains.evaluation.application.constants import H2_RUBRIC, rubric_for_display
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor

client = TestClient(app)

_TEST_RATER = Actor(role="rater", auth_id="code|rater-1", full_name="Rater One")


async def _noop_enforce(*_args, **_kwargs) -> None:
    """Allow every call — the Casbin layer has its own tests in ``test_authz.py``."""


def _explanation_step(
    step_id: str, title: str, objective_id: str, content: str
) -> dict[str, object]:
    return {
        "step_id": step_id,
        "title": title,
        "step_kind": "core",
        "instructional_type": "explain",
        "lesson_objective_id": objective_id,
        "blocks": [
            {
                "type": "explanation",
                "id": f"{step_id}-block-1",
                "content": content,
            }
        ],
    }


def _h2_detail() -> dict[str, object]:
    """A representative BLINDED H2 detail mirroring ``_build_h2_packet_detail``.

    Two anonymous candidates in a scrambled display order; two sections preserved by
    both candidates plus one that Candidate A has no content for. The rubric carries
    ``display_label`` via the real ``rubric_for_display(H2_RUBRIC)`` so the §4.4
    column headers + key render.
    """
    base_step_1 = _explanation_step(
        "step-1",
        "Common multiples",
        "obj-1",
        "### Common multiples\nUse **clear examples** to show shared multiples of two numbers.",
    )
    base_step_2 = _explanation_step(
        "step-2",
        "Finding the LCM",
        "obj-2",
        "The *least* common multiple is the smallest shared multiple. Note \\(0\\) is excluded.",
    )
    base_step_3 = _explanation_step(
        "step-3",
        "Applying the LCM",
        "obj-3",
        "Apply the LCM to word problems about repeating events.",
    )
    candidate_step_1 = _explanation_step(
        "step-1",
        "Common multiples",
        "obj-1",
        "### Common multiples (for you)\nStart from **lists of multiples** and circle shared ones.",
    )
    candidate_step_2 = _explanation_step(
        "step-2",
        "Finding the LCM",
        "obj-2",
        "The *least* common multiple is the smallest one you both share. Skip-count to find it.",
    )
    return {
        "evaluation_packet_id": "EPK-H2-TEST",
        "packet_code": "EPK-H2-TEST",
        "hypothesis": "H2",
        "status": "ready",
        "lesson_title": "JSS1 Mathematics Week 3 Session 1: LCM of whole numbers",
        "lesson_subtitle": "LCM of whole numbers",
        "objectives": [
            {"lesson_objective_id": "obj-1", "objective_text": "Identify common multiples"},
            {"lesson_objective_id": "obj-2", "objective_text": "Find the LCM of whole numbers"},
            {"lesson_objective_id": "obj-3", "objective_text": "Apply the LCM to word problems"},
        ],
        # Blinded candidates in a deliberately scrambled display order (the
        # personalised run first) to mirror the per-rater randomisation.
        "candidates": [
            {
                "candidate_id": "run-p1",
                "label": "Candidate A",
                "display_order": 0,
                "pack": {
                    "manifest": {
                        "subject": "Mathematics",
                        "grade": "JSS1",
                        "term": "First Term",
                        "week": 3,
                        "topic": "LCM / HCF",
                        "subtopic": "LCM of whole numbers",
                        "theme": "Number and Numeration",
                        "misconceptions": ["Confusing LCM with HCF"],
                        "steps": [candidate_step_1, candidate_step_2],
                    }
                },
            },
            {
                "candidate_id": "run-p0",
                "label": "Candidate B",
                "display_order": 1,
                "pack": {
                    "manifest": {
                        "subject": "Mathematics",
                        "grade": "JSS1",
                        "term": "First Term",
                        "week": 3,
                        "topic": "LCM / HCF",
                        "subtopic": "LCM of whole numbers",
                        "theme": "Number and Numeration",
                        "misconceptions": ["Confusing LCM with HCF"],
                        "steps": [base_step_1, base_step_2, base_step_3],
                    }
                },
            },
        ],
        "focal_learner": {
            "focal_case_type": "needs_remediation",
            "curriculum_profile": {"field_of_study": "Science"},
            "preferences": {"language_level": "simple", "pace_preference": "slow"},
            "mastered_sections": [],
            "objective_states": [
                {
                    "lesson_objective_id": "obj-1",
                    "objective_text": "Identify common multiples",
                    "band": "reinforce",
                    "mastery_score": 0.6,
                    "confidence": "medium",
                    "perceived_difficulty": "medium",
                    "misconception_code": None,
                    "misconception_description": None,
                    "evidence_refs": ["q1", "q2"],
                },
                {
                    "lesson_objective_id": "obj-2",
                    "objective_text": "Find the LCM of whole numbers",
                    "band": "remediate",
                    "mastery_score": 0.3,
                    "confidence": "low",
                    "perceived_difficulty": "high",
                    "misconception_code": "lcm_hcf_swap",
                    "misconception_description": "Treats the LCM as the HCF",
                    "evidence_refs": ["q4"],
                },
                {
                    "lesson_objective_id": "obj-3",
                    "objective_text": "Apply the LCM to word problems",
                    "band": "extend",
                    "mastery_score": 0.85,
                    "confidence": "high",
                    "perceived_difficulty": "low",
                    "misconception_code": None,
                    "misconception_description": None,
                    "evidence_refs": [],
                },
            ],
            "selection_metadata": {"selection_rank": 1},
        },
        "sections": [
            {
                "section_id": "step-1",
                "step_id": "step-1",
                "title": "Common multiples",
                "step_kind": "core",
                "instructional_type": "explain",
                "lesson_objective_id": "obj-1",
                "objective_text": "Identify common multiples",
                "candidate_steps": {"run-p0": base_step_1, "run-p1": candidate_step_1},
            },
            {
                "section_id": "step-2",
                "step_id": "step-2",
                "title": "Finding the LCM",
                "step_kind": "core",
                "instructional_type": "explain",
                "lesson_objective_id": "obj-2",
                "objective_text": "Find the LCM of whole numbers",
                "candidate_steps": {"run-p0": base_step_2, "run-p1": candidate_step_2},
            },
            {
                "section_id": "step-3",
                "step_id": "step-3",
                "title": "Applying the LCM",
                "step_kind": "core",
                "instructional_type": "explain",
                "lesson_objective_id": "obj-3",
                "objective_text": "Apply the LCM to word problems",
                "candidate_steps": {"run-p0": base_step_3, "run-p1": None},
            },
        ],
        "rubric": rubric_for_display(H2_RUBRIC),
        "existing_rating": None,
    }


def _render(detail: dict[str, object]) -> bytes:
    """Render via WeasyPrint, skipping if the native libs are unavailable."""
    try:
        from app.domains.evaluation.application.worksheet_html.h2_renderer import (
            render_h2_worksheet_html_pdf,
        )

        return render_h2_worksheet_html_pdf(detail)
    except (ImportError, OSError) as exc:  # WeasyPrint or its native deps missing
        pytest.skip(f"WeasyPrint unavailable: {exc}")


def test_h2_html_worksheet_contains_expected_text() -> None:
    pdf_bytes = _render(_h2_detail())

    assert pdf_bytes.startswith(b"%PDF")
    text = " ".join(_extract_pdf_text(pdf_bytes).split())
    # The H2 title (not the H1 one) — blinded, no "Personalised".
    assert "Revision-Note Review Worksheet for Expert Rater" in text
    # Task framing — blinded: judge each anonymous candidate for this learner.
    assert "two candidate versions of a student revision note" in text
    assert "Score every candidate independently" in text
    # Per-objective learner state card: header + rater-friendly band labels.
    # The thesis taxonomy (remediate / reinforce / extend) is hidden from
    # raters; they see the suggested study direction in plain English.
    assert "Per-objective learner state" in text
    assert "On track" in text
    assert "Needs more practice" in text
    assert "Ready for extension" in text
    # Both candidate versions appear, section-aligned, under anonymous labels
    # (the thesis BASE / PERSONALISED roles are never surfaced to raters).
    assert "Candidate A" in text
    assert "Candidate B" in text
    # A candidate's dropped section is shown as missing so it can be penalised.
    assert "This candidate has no section for this objective" in text
    # Each section is rated inline, right after its comparison — there is no
    # consolidated rating form at the end.
    assert "Rate this section" in text
    assert "Section-level rating form" not in text
    # The how-to-score reference + per-section call-out wording.
    assert "How to rate each section" in text
    assert "left out of that section's average" in text
    # The five H2 dimensions appear as teacher-friendly headers (no technical term).
    assert "Fit for this learner" in text
    assert "Teaching support" in text
    assert "Challenge level" in text
    assert "Misconception help" in text
    assert "Keeps the lesson goal" in text
    assert "N/A" in text
    # Institution band.
    assert "UNIVERSITY OF LAGOS" in text


def test_h2_html_worksheet_uses_objective_ordinals_not_raw_ids() -> None:
    text = " ".join(_extract_pdf_text(_render(_h2_detail())).split())
    # Raw internal objective ids must never reach the rater...
    assert "obj-1" not in text
    assert "obj-2" not in text
    assert "obj-3" not in text
    # ...they are shown as "Objective N" (learner-state card + section headings/form).
    assert "Objective 1" in text
    assert "Objective 2" in text
    assert "Objective 3" in text


def test_h2_html_worksheet_drops_explanation_label_and_citations() -> None:
    detail = _h2_detail()
    # Give one candidate's section a citation-laden explanation with its own heading.
    section = cast(list[dict[str, object]], detail["sections"])[0]
    steps = cast(dict[str, dict[str, object]], section["candidate_steps"])
    section_blocks = cast(list[dict[str, object]], steps["run-p0"]["blocks"])
    section_blocks[0]["content"] = (
        "### Common multiples\nShared multiples of two numbers (REF-1).\nSources: REF-1"
    )
    text = " ".join(_extract_pdf_text(_render(detail)).split())
    # The content heading survives; the redundant "Explanation" block label is gone.
    assert "Common multiples" in text
    assert "Explanation" not in text
    # Source citations are stripped from the revision note (the audit checks those).
    assert "REF-1" not in text
    assert "Sources" not in text


def test_h2_html_worksheet_uses_teacher_friendly_rubric_labels() -> None:
    text = " ".join(_extract_pdf_text(_render(_h2_detail())).split())
    # The dimension-description key uses the teacher-friendly labels; the full
    # technical research term is not shown to raters.
    assert "Fit for this learner" in text
    assert "Keeps the lesson goal" in text
    assert "Learner-state suitability" not in text


def test_h2_html_worksheet_renders_markdown_emphasis_not_literal_markers() -> None:
    text = _extract_pdf_text(_render(_h2_detail()))
    # Emphasis renders as bold/italic, never leaking as literal markers.
    assert "clear examples" in text
    assert "*least*" not in text
    assert "**clear examples**" not in text
    assert "**lists of multiples**" not in text


def test_h2_html_worksheet_has_no_missing_glyph_boxes() -> None:
    detail = _h2_detail()
    candidate = cast(list[dict[str, object]], detail["candidates"])[1]
    manifest = cast(dict[str, object], cast(dict[str, object], candidate["pack"])["manifest"])
    steps = cast(list[dict[str, object]], manifest["steps"])
    blocks = cast(list[dict[str, object]], steps[0]["blocks"])
    blocks[0]["content"] = "A billion equals 10⁹ (million → ten million → billion)."
    # Keep the section's step block in sync with the manifest step it mirrors.
    section = cast(list[dict[str, object]], detail["sections"])[0]
    section_steps = cast(dict[str, dict[str, object]], section["candidate_steps"])
    section_blocks = cast(list[dict[str, object]], section_steps["run-p0"]["blocks"])
    section_blocks[0]["content"] = "A billion equals 10⁹ (million → ten million → billion)."
    text = _extract_pdf_text(_render(detail))
    assert "■" not in text  # no missing-glyph box


def test_h2_html_worksheet_renders_to_multiple_pages() -> None:
    page_texts = _extract_pdf_page_texts(_render(_h2_detail()))
    assert len(page_texts) >= 2
    assert all(page.strip() for page in page_texts)
    # The per-objective learner state card lives on the cover (page 1).
    assert "Per-objective learner state" in page_texts[0]
    full = " ".join("\n".join(page_texts).split())
    # The how-to-score reference is shown once, near the top (before the sections),
    # not on the cover.
    assert "How to rate each section" not in page_texts[0]
    assert "How to rate each section" in full
    # Every section is rated inline (one "Rate this section" block per section),
    # and there is no consolidated end-form.
    assert full.count("Rate this section") == 3
    assert "Section-level rating form" not in full


def test_h2_html_worksheet_has_one_rating_strip_per_candidate_per_section() -> None:
    full = " ".join("\n".join(_extract_pdf_page_texts(_render(_h2_detail()))).split())
    # Each section gets ONE "Rate this section" header and one scoring strip per
    # blinded candidate, so the offline rater scores each candidate independently.
    assert full.count("Rate this section") == 3
    assert full.count("Rate Candidate A") == 3
    assert full.count("Rate Candidate B") == 3


def test_h2_html_worksheet_never_leaks_condition_labels() -> None:
    # Blinding: no P0/P1 roles or base-vs-personalised wording anywhere.
    text = " ".join(_extract_pdf_text(_render(_h2_detail())).split())
    lowered = text.lower()
    assert "personalised" not in lowered
    assert "class version" not in lowered
    assert "base version" not in lowered
    assert "P0" not in text
    assert "P1" not in text


def test_h2_html_worksheet_calls_out_per_section_misconception() -> None:
    text = " ".join(_extract_pdf_text(_render(_h2_detail())).split())
    # The section whose objective records a misconception calls it out so the rater
    # knows to score Misconception help (obj-2: "Treats the LCM as the HCF").
    assert "Recorded misconception: Treats the LCM as the HCF" in text
    # Sections whose objective has no recorded misconception tell the rater to mark
    # Misconception help as N/A instead of scoring it.
    assert "No misconception recorded for this objective" in text
    assert "mark Misconception help as N/A" in text


def test_h2_html_worksheet_keeps_visual_label_with_its_figure_across_pages() -> None:
    """Regression: in the landscape compare-table, a tall row can span two pages.
    The "Visual" label must never end up on a different page from its image +
    caption — WeasyPrint silently ignores `break-inside: avoid` on block elements
    inside a paginated table-cell, so the renderer instead makes ``.block-visual``
    an atomic inline-block. This test injects enough section content to force a
    multi-page row and asserts the label travels with the figure.
    """
    detail = _h2_detail()
    # Pad section 1's base + candidate steps with explanation blocks so the
    # compare-row in the rendered worksheet runs taller than a single landscape
    # page, then bolt a Visual block onto the end of each cell. The orphan would
    # appear precisely at the boundary where the row splits across pages.
    long_prose = " ".join(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        for _ in range(20)
    )
    visual_block = {
        "type": "visual",
        "id": "visual-1",
        "variant": "figure",
        "caption": "Distinctive caption marker XYZZY for grounding",
        "url": "https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-004.png",
    }
    sections = cast(list[dict[str, object]], detail["sections"])
    for section in sections[:2]:
        steps = cast(dict[str, dict[str, object] | None], section["candidate_steps"])
        for cell in steps.values():
            if cell is None:
                continue
            blocks = cast(list[dict[str, object]], cell["blocks"])
            blocks.append({"type": "explanation", "id": "pad-1", "content": long_prose})
            blocks.append({"type": "explanation", "id": "pad-2", "content": long_prose})
            blocks.append(dict(visual_block))

    page_texts = _extract_pdf_page_texts(_render(detail))
    # Each "Visual" label must land on the same page as the caption marker, which
    # appears only on the figure-caption div (not anywhere else in the doc).
    visual_pages = {i for i, page in enumerate(page_texts) if "Visual" in page}
    caption_pages = {i for i, page in enumerate(page_texts) if "XYZZY" in page}
    # There should be visual blocks AND captions rendered — otherwise the test
    # didn't actually exercise the pagination path it claims to.
    assert visual_pages, "no Visual labels rendered — test setup is wrong"
    assert caption_pages, "no figure captions rendered — image/caption missing"
    orphaned = visual_pages - caption_pages
    assert not orphaned, (
        f"'Visual' label appeared on page(s) {sorted(p + 1 for p in orphaned)} "
        f"without its figure caption; captions are on page(s) "
        f"{sorted(p + 1 for p in caption_pages)}"
    )


def test_h2_html_worksheet_module_skips_without_weasyprint(monkeypatch: Any) -> None:
    import app.domains.evaluation.application.worksheet_html.h2_renderer as renderer_mod

    def _boom(*_args: object, **_kwargs: object) -> bytes:
        raise OSError("cannot load library 'libgobject-2.0-0'")

    monkeypatch.setattr(renderer_mod, "render_h2_worksheet_html_pdf", _boom)
    with pytest.raises(pytest.skip.Exception):
        _render(_h2_detail())


def test_download_h2_packet_worksheet_returns_pdf_attachment(monkeypatch: Any) -> None:
    async def _fake_db() -> Any:
        yield SimpleNamespace()

    async def _fake_export(
        _packets: Any, *, evaluation_packet_id: str, rater_id: str
    ) -> tuple[bytes, str]:
        return b"%PDF-1.4\n%h2-worksheet", "EPK-H2-TEST-h2-worksheet.pdf"

    # The download route is guarded by ``requires(obj="rating:*", act="read")``;
    # this is a transport-layer test, so act as a rater and short-circuit the
    # Casbin enforcer (its own behaviour is covered in test_authz.py).
    app.dependency_overrides[get_actor] = lambda: _TEST_RATER
    monkeypatch.setattr(authz, "enforce", _noop_enforce)
    app.dependency_overrides[get_db] = _fake_db
    monkeypatch.setattr(evaluation_routes, "generate_h2_worksheet", _fake_export)

    response = client.get(
        "/evaluation/h2/packets/EPK-H2-TEST/worksheet.pdf",
        params={"rater_id": "RATER-TEST"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"] == (
        'attachment; filename="EPK-H2-TEST-h2-worksheet.pdf"'
    )
    assert response.content.startswith(b"%PDF")

    app.dependency_overrides.clear()


# --- pdftotext helpers (mirror test_h1_worksheet_html) -----------------------


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
