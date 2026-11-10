from datetime import datetime, timezone

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.evaluation.application.source_audit_builder import (
    candidate_audit_items,
    figures_by_record_id,
    reference_record_map,
    sample_items,
)


def _pack(*, steps: list[dict]) -> PostClassReviewPack:
    """Build a minimum-valid PostClassReviewPack carrying ``steps``."""
    return PostClassReviewPack.model_validate(
        {
            "artefact_id": "AT-test",
            "plan_version_id": "LPV-test",
            "scope": ArtefactScope.CLASS_LEVEL,
            "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "steps": steps,
        }
    )


def test_reference_record_map_parses_record_ids() -> None:
    refs = [
        "Chapter 1: Numbers big and small (ch01-b029)",
        "Chapter 1: Numbers big and small (ch01-b037-i01)",
        "Plain reference with no id",
    ]
    assert reference_record_map(refs) == {
        "REF-1": "ch01-b029",
        "REF-2": "ch01-b037-i01",
    }


def test_candidate_audit_items_one_per_cited_ref() -> None:
    pack = _pack(
        steps=[
            {
                "step_id": "s1",
                "lesson_objective_id": "lop01",
                "blocks": [
                    {
                        "id": "b1",
                        "type": "explanation",
                        "content": (
                            "A billion equals 10^9 (REF-1). The chart counts in steps "
                            "(REF-2).\n\n_Sources: REF-1, REF-2_"
                        ),
                    }
                ],
            }
        ]
    )
    items = candidate_audit_items(
        condition_code="C2",
        condition_run_id="ECR-1",
        lesson_id="LPV-1",
        pack=pack,
        objective_text_by_id={"lop01": "Count in billions"},
        scope_boundary="Millions and billions",
    )
    assert [item["source_ref"] for item in items] == ["REF-1", "REF-2"]
    assert all(item["condition_code"] == "C2" for item in items)
    assert all(item["lesson_objective_id"] == "lop01" for item in items)
    assert all(item["objective_text"] == "Count in billions" for item in items)
    # The trailing "_Sources: …_" footer is stripped from the excerpt.
    assert "Sources:" not in str(items[0]["generated_excerpt"])
    assert "10^9" in str(items[0]["generated_excerpt"])


def test_candidate_audit_items_ignores_blocks_without_citations() -> None:
    pack = _pack(
        steps=[
            {
                "step_id": "s1",
                "lesson_objective_id": "lop01",
                "blocks": [{"id": "b1", "type": "explanation", "content": "No citations here."}],
            }
        ]
    )
    assert (
        candidate_audit_items(
            condition_code="C3",
            condition_run_id="ECR-2",
            lesson_id=None,
            pack=pack,
            objective_text_by_id={},
            scope_boundary=None,
        )
        == []
    )


def test_sample_items_caps_and_balances_across_conditions() -> None:
    items = [
        {"condition_code": code, "source_ref": f"REF-{i}", "generated_excerpt": "x"}
        for code in ("C2", "C3", "C4")
        for i in range(10)
    ]
    kept, dropped = sample_items(items, cap=6)
    assert len(kept) == 6
    assert dropped == len(items) - 6
    # Balanced: round-robin keeps two of each condition in the first six.
    counts = {
        code: sum(1 for k in kept if k["condition_code"] == code) for code in ("C2", "C3", "C4")
    }
    assert counts == {"C2": 2, "C3": 2, "C4": 2}


def test_figures_by_record_id_maps_visual_blocks_with_grounded_url() -> None:
    pack = _pack(
        steps=[
            {
                "step_id": "s1",
                "lesson_objective_id": "lop01",
                "blocks": [
                    {"id": "b1", "type": "explanation", "content": "Multiples (REF-1)."},
                    {
                        "id": "b2",
                        "type": "visual",
                        "variant": "image",
                        "caption": "Common multiples on a number line.",
                        "url": "https://electricbookworks.github.io/figures/ebw-jss1-01-002.png",
                        "source_record_id": "ch01-b042-i01",
                    },
                ],
            }
        ]
    )
    figures = figures_by_record_id(pack)
    assert figures == {
        "ch01-b042-i01": {
            "url": "https://electricbookworks.github.io/figures/ebw-jss1-01-002.png",
            "caption": "Common multiples on a number line.",
        },
    }


def test_figures_by_record_id_skips_non_image_variants_and_text_only_blocks() -> None:
    # ``variant != "image"`` skips the grounded-url model_validator on
    # VisualBlock (clock/number-line variants have no url to render), so the
    # lookup just doesn't index them. Explanation blocks carry no figure.
    pack = _pack(
        steps=[
            {
                "step_id": "s1",
                "lesson_objective_id": "lop01",
                "blocks": [
                    {"id": "b1", "type": "explanation", "content": "Text only."},
                    {
                        "id": "b2",
                        "type": "visual",
                        "variant": "diagram_clock",
                        "caption": "A clock face.",
                        "data": {"hour": 3, "minute": 30},
                        # No url + no source_record_id — skipped.
                    },
                ],
            }
        ]
    )
    assert figures_by_record_id(pack) == {}


def test_sample_items_under_cap_keeps_all() -> None:
    items = [{"condition_code": "C2", "source_ref": "REF-1", "generated_excerpt": "x"}]
    kept, dropped = sample_items(items, cap=45)
    assert kept == items
    assert dropped == 0
