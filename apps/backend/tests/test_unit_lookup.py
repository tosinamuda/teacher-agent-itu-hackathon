"""Which unit a section came from, when the obvious answer is ambiguous.

Both the repair pass and the deterministic validator resolve a section back to
its unit — one to rebuild it against the right context, the other to judge it
against the evidence it was actually shown. They must agree, and the answer is
only interesting when one objective owns several steps, which is exactly the
case that used to collide.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.unit_index import (
    SectionUnitIndex,
)


def _unit(unit_id: str, objective: str) -> SectionGenerationUnit:
    return SectionGenerationUnit(
        unit_id=unit_id, lesson_objective_id=objective, objective_text=f"objective {objective}"
    )


def _section(section_id: str, objective: str) -> ReviewPackSection:
    return ReviewPackSection(
        section_id=section_id, title="t", lesson_objective_id=objective, blocks=[]
    )


def test_a_section_resolves_to_the_unit_that_produced_it() -> None:
    """Two steps on one objective: the id decides, because the objective cannot."""
    first, second = _unit("step:sA", "lop01"), _unit("step:sB", "lop01")
    lookup = SectionUnitIndex.of([first, second])

    assert lookup.resolve(_section("step:sA", "lop01")) is first
    assert lookup.resolve(_section("step:sB", "lop01")) is second


def test_the_objective_answers_only_when_the_id_does_not() -> None:
    """A section recovered from a pack built under a different unit shape."""
    first, second = _unit("step:sA", "lop01"), _unit("step:sB", "lop01")
    lookup = SectionUnitIndex.of([first, second])

    # Unknown id, known objective — the FIRST unit for it, not the last.
    assert lookup.resolve(_section("objective:lop01", "lop01")) is first


def test_an_unattributable_section_resolves_to_nothing() -> None:
    """Better no unit than the wrong one: the caller falls back deliberately."""
    lookup = SectionUnitIndex.of([_unit("step:sA", "lop01")])

    assert lookup.resolve(_section("step:sZ", "lop99")) is None
