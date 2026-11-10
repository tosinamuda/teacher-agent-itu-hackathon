"""Figures reach a reader in the order the prose cites them."""

from app.domains.artefacts.types.post_class_review_pack.domain.section.figures import (
    append_grounded_figures,
)


class _Figure:
    def __init__(self, ref: str) -> None:
        self.figure_id = f"block-{ref}"
        self.figure_ref = ref
        self.url = None
        self.caption = f"a drawing for {ref}"
        self.variant = "diagram_tikz"
        self.source_tikz = f"\\begin{{tikzpicture}} % {ref}"
        self.source_record_id = "rec-1"


class _Block:
    def __init__(self, text: str, block_type: str = "explanation") -> None:
        self.text = text
        self.block_type = block_type


class _Section:
    def __init__(self, blocks: list) -> None:
        self.blocks = blocks
        self.practice: list = []


class _Unit:
    def __init__(self, figures: list) -> None:
        self.source_figures = figures
        self.lesson_objective_id = "lo-1"


def _refs(section: _Section) -> list[str]:
    return [b.figure_ref for b in section.blocks if getattr(b, "block_type", "") == "visual"]


def test_figures_citing_one_block_keep_their_cited_order():
    """The defect: each was inserted at the anchor, so each landed in front of the last."""
    section = _Section([_Block("Examples cite fig-05, then fig-06, then fig-07.")])
    figures = [_Figure("fig-05"), _Figure("fig-06"), _Figure("fig-07")]
    append_grounded_figures(section, _Unit(figures))
    assert _refs(section) == ["fig-05", "fig-06", "fig-07"]


def test_a_figure_follows_the_block_that_cites_it():
    section = _Section(
        [_Block("First passage, see fig-01."), _Block("Second passage, see fig-02.")]
    )
    append_grounded_figures(section, _Unit([_Figure("fig-01"), _Figure("fig-02")]))
    kinds = [(getattr(b, "block_type", ""), getattr(b, "figure_ref", None)) for b in section.blocks]
    assert kinds == [
        ("explanation", None),
        ("visual", "fig-01"),
        ("explanation", None),
        ("visual", "fig-02"),
    ]


def test_a_figure_no_prose_cites_goes_to_the_end():
    """Personalisation can rewrite a passage and drop the citation; the figure still shows."""
    section = _Section([_Block("A passage citing fig-01 only.")])
    append_grounded_figures(section, _Unit([_Figure("fig-01"), _Figure("fig-09")]))
    assert _refs(section) == ["fig-01", "fig-09"]
