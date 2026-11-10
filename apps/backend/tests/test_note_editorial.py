"""The clean-notes arm: hand-edited note files replacing the frozen transcription.

Round 8 spent 5 of 12 critic findings removing review commentary the generator
should never have read. These pin that the edited files removed it and kept the
teaching content — several captions are load-bearing, so the edit has to be
provably conservative.
"""

from __future__ import annotations

import json
import re

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (
    drawings_as_references,
    without_review_markup,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.note_editorial import (
    CLEAN_DIR,
    DECLARED_ADDITIONS,
    _cleaned_source,
    addition_digest,
    additions,
    clean_plan,
    note_path,
    orphans,
    verify,
)

CASES = {c["lesson"]: c for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}

# Commentary about the document rather than the mathematics. None of it may survive
# into what the generator reads.
EDITORIAL = re.compile(
    r"not (?:marked|labelled) |carries no label|carried over from|placed approximately|"
    r"only one line is visible|\*\*layered\*\*|No procedure is written|"
    r"the point of this panel|^\s*Teacher (?:explains|asks|introduces)",
    re.IGNORECASE | re.MULTILINE,
)


def _flat(text: str) -> str:
    """Whitespace-collapsed, so re-wrapping a caption is not a content change."""
    return " ".join(text.split())


def _model_sees(lesson: str, cleaned: bool) -> str:
    plan = dict(CASES[lesson]["plan"])
    plan["lesson_key"] = lesson
    if cleaned:
        plan, _ = clean_plan(plan)
    return "\n".join(
        drawings_as_references(without_review_markup(s.get("note") or ""), s["step_id"])
        for s in plan["steps"]
    )


@pytest.mark.parametrize("lesson", sorted(CASES))
def test_no_editorial_commentary_survives(lesson: str) -> None:
    assert not EDITORIAL.findall(_model_sees(lesson, cleaned=True))


@pytest.mark.parametrize("lesson", sorted(CASES))
def test_every_step_has_an_edited_file(lesson: str) -> None:
    for step in CASES[lesson]["plan"]["steps"]:
        if step.get("note"):
            assert note_path(lesson, step["step_id"]).exists()


def test_load_bearing_captions_survive() -> None:
    """t3-w05's prism is dimensioned ONLY on its figure; none of it may be lost.

    Her working writes the numbers bare — "$\\frac{1}{2} \\times 5 \\times 3$", then
    "$\\times 10m$" — so the triangular face's base and height carry a unit nowhere but
    fig-03, which is itself reconstructed from those numbers.
    """
    note = _flat(_model_sees("t3-w05", cleaned=True))
    for quantity in ("5 m", "3 m", "10 m"):
        assert quantity in note, quantity


def test_the_bisector_step_survives() -> None:
    """Her steps stop at the arcs; the join and the midpoint complete the method."""
    note = _flat(_model_sees("t3-w06", cleaned=True))
    assert "Join $P$ to $Q$ with a ruler." in note
    assert "$M$ is the midpoint of $AB$" in note
    assert "$P$ joined to $Q$" in note


def test_content_inside_an_editorial_frame_is_kept() -> None:
    note = _flat(_model_sees("t3-w06", cleaned=True))
    assert "inclination does not affect the construction" in note
    assert "running from lower left to upper right" in note
    assert "Two lines are said to be perpendicular" in note


def test_the_redrawn_set_squares_carry_a_real_right_angle() -> None:
    """fig-03 and fig-05 marked a right angle on a ~62 degree corner.

    The set square rested on the ruler by its sloping edge, and the mark was placed at
    that junction rather than at the corner where the edge on AB meets the upright edge.
    Both are redrawn from a right-angled triangle, and fig-05's two positions are one
    translation apart — a slide along a held ruler cannot rotate it.
    """
    drawn = _flat(note_path("t3-w06", "step-t3w06-02").read_text(encoding="utf-8"))
    for triangle in (
        "(1.72,0) -- (1.72,-1.9) -- (5.4,0)",
        "(0.6,0) -- (0.6,-1.6) -- (3.4,0)",
        "(4.45,2.2) -- (4.45,0.6) -- (7.25,2.2)",
    ):
        assert triangle in drawn, triangle


def test_lessons_without_editorial_are_untouched() -> None:
    """t3-w02 left this set when its 14 drawings were labelled — see DECLARED_ADDITIONS."""
    for lesson in ("t2-w09", "t3-w09"):
        assert _model_sees(lesson, cleaned=True) == _model_sees(lesson, cleaned=False), lesson


def test_a_missing_file_fails_loudly(monkeypatch) -> None:  # noqa: ANN001
    """An arm claiming to be cleaned must not silently fall back to the raw note."""
    monkeypatch.setattr(
        "experiments.h1_condition_eval.note_editorial.CLEAN_DIR", CLEAN_DIR / "nope"
    )
    plan = dict(CASES["t3-w06"]["plan"])
    plan["lesson_key"] = "t3-w06"
    with pytest.raises(SystemExit, match="no cleaned note"):
        clean_plan(plan)


def test_the_model_reads_the_edited_file_minus_only_marked_commentary() -> None:
    """The ONLY thing between the file and the model is what the file marks itself.

    Every content defect found in the 2026-08-04 audit except one came from a script
    transforming the note in flight — a deleted construction method, a lesson's worth
    of circle vocabulary, seven sets of dimensions. Now the only removal is of spans
    that declare themselves commentary, which is structural and cannot take teaching
    text with it.
    """
    builder = BaseReviewPackRequestBuilder(figures="source")
    for lesson, case in CASES.items():
        plan = dict(case["plan"])
        plan["lesson_key"] = lesson
        cleaned, _ = clean_plan(plan)
        session_plan = SessionPlanView.model_validate(cleaned)
        request = builder.build(
            session_plan=session_plan,
            policy=H1_CONDITION_PROFILES[ConditionCode.C2],
            sources=LessonSources.unresolved(session_plan.references),
        )
        steps = [s for s in cleaned["steps"] if s.get("note") and s["step_kind"] == "core"]
        for unit, step in zip(request.units, steps, strict=True):
            on_disk = note_path(lesson, step["step_id"]).read_text(encoding="utf-8")
            expected = without_review_markup(on_disk)
            assert unit.source_evidence[0].excerpt == expected, f"{lesson}/{step['step_id']}"


def test_the_split_carries_every_teaching_paragraph() -> None:
    """The one remaining scripted step must not drop content.

    Her document is split into per-step notes by ``build_session_plan.py``, and the
    hand-edited files are seeded from that split — so anything it drops was never
    available to edit. This reads her cleaned document and fails if any paragraph
    that is not a heading, a cleaner's remark or classroom choreography is absent
    from every note. Skipped where the source tree is not present.
    """
    if not any(_cleaned_source(lesson) for lesson in CASES):
        pytest.skip("thesis transcripts not on this machine")
    assert verify() == 0


def test_every_addition_to_the_generation_copy_is_declared() -> None:
    """Cleaning removes. Anything added is an edit and has to name itself.

    This replaces a list of banned phrases, which passed while four copies of an
    agent's caption commentary sat in the tree — a blocklist only recognises what
    has already leaked. The digest is over the added paragraphs, so it is blind to
    wording: any addition fails, naming the step. Re-declare with
    ``note_editorial declare`` after reading the diff.
    """
    for lesson, case in CASES.items():
        for step in case["plan"]["steps"]:
            if not step.get("note"):
                continue
            clean = note_path(lesson, step["step_id"]).read_text(encoding="utf-8")
            declared = DECLARED_ADDITIONS.get((lesson, step["step_id"]), ("", ""))[0]
            added = additions(step["note"], clean)
            assert addition_digest(step["note"], clean) == declared, (
                f"{lesson}/{step['step_id']} adds text no one declared:\n"
                + "\n".join(f"  + {para[:110]}" for para in added)
            )


def test_the_generation_copy_carries_no_review_markup() -> None:
    """The review record lives in the transcript, not in what the generator reads."""
    for lesson, case in CASES.items():
        for step in case["plan"]["steps"]:
            if not step.get("note"):
                continue
            text = note_path(lesson, step["step_id"]).read_text(encoding="utf-8")
            prose = re.sub(
                r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "", text, flags=re.DOTALL
            )
            assert "<!-- review" not in prose, f"{lesson}/{step['step_id']}"
            assert not EDITORIAL.findall(prose), f"{lesson}/{step['step_id']}"


def test_removing_marked_commentary_cannot_touch_teaching_text() -> None:
    note = "Area is length x breadth. <!-- review: the label is missing --> Try 6 x 4."
    assert without_review_markup(note) == "Area is length x breadth.  Try 6 x 4."


def test_step_ids_line_up_across_copies_declarations_and_plans() -> None:
    """A renumbered step must not leave anything behind pointing at the old id.

    Three things key off a step id and none of them failed loudly when one changed:
    a generation copy for a dead id lingers with stale content and is never read again,
    a live step with no copy only raises when a run reaches it, and a declaration keyed
    to a dead id silently stops guarding anything. Splitting t3-w06's compound objective
    moved five ids and hit all three on the same day t3-w05's new intro step shifted two.
    """
    found = orphans()
    assert found == {
        "orphaned_copies": [],
        "missing_copies": [],
        "orphaned_declarations": [],
    }, found


def test_a_renumbered_step_is_caught_in_all_three_places(monkeypatch) -> None:  # noqa: ANN001
    """The guard above passes on a tree I repaired by hand, so prove it can fail.

    One id moves in the frozen plan and nowhere else — the shape of every renumber so
    far. All three categories have to light up, or the clean result means only that
    nothing was looked at.
    """
    cases = json.loads(EVAL_SET_PATH.read_text())["cases"]
    for case in cases:
        for step in case["plan"]["steps"]:
            if step["step_id"] == "step-t3w06-02":
                step["step_id"] = "step-t3w06-99"
    monkeypatch.setattr("experiments.h1_condition_eval.note_editorial._frozen", lambda: cases)
    assert orphans() == {
        "orphaned_copies": [("t3-w06", "step-t3w06-02")],
        "missing_copies": [("t3-w06", "step-t3w06-99")],
        "orphaned_declarations": [("t3-w06", "step-t3w06-02")],
    }
