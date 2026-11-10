"""The researcher's copy of a pack is the same pack the learner gets.

``pack_renderer`` renders the post-class review pack from the rater worksheet's own
template so the two never drift. It kept a second ``_step`` anyway, and when practice
items were regrouped into a numbered set the template's ``practice`` branch went with
them — the branch that copy was still feeding. Every activity and every answer dropped
silently out of the researcher export, which is the surface C0–C4 packs are read on.
"""

from __future__ import annotations

from app.domains.evaluation.application.worksheet_html.pack_renderer import render_pack_html

MANIFEST = {
    "subtopic": "Order of operations",
    "grade": "JSS1",
    "subject": "Mathematics",
    "week": "9",
    "steps": [
        {
            "step_id": "s1",
            "title": "Order of operations",
            "blocks": [
                {"type": "explanation", "content": "Work through brackets first."},
                {
                    "type": "practice",
                    "question": "1. Simplify 4n + 3n x 10.",
                    "answer": "34n",
                },
                {
                    "type": "practice",
                    "question": "2. Simplify 32 + 8x / 2.",
                    "answer": "32 + 4x",
                },
            ],
        }
    ],
}


def test_the_pack_carries_its_activities() -> None:
    html = render_pack_html(MANIFEST, pack_label="C0-TEST")
    assert "Work through brackets first." in html
    assert "Simplify 4n + 3n x 10." in html
    assert "Simplify 32 + 8x / 2." in html


def test_the_pack_carries_its_answer_key() -> None:
    html = render_pack_html(MANIFEST, pack_label="C0-TEST")
    assert "Check your work" in html
    assert html.index("34n") > html.index("Check your work"), "answers come after the activities"
    assert "32 + 4x" in html


def test_the_pack_numbers_a_practice_item_once() -> None:
    """It renders the practice set the worksheet does, so it inherits its numbering."""
    html = render_pack_html(MANIFEST, pack_label="C0-TEST")
    assert '<ol class="markdown">' in html
    assert "<li><ol>" not in html, "the prompt's own number stacked on the set's"
