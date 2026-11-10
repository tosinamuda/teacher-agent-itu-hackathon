"""Which generation unit a produced section came from.

Both the repair/personalise passes and the deterministic validator need to get
from a section back to the unit that produced it — to rebuild it against the
right context, and to judge it against the evidence it was actually shown.
Shared here so the two agree on the answer.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)

from .schemas import ReviewPackSection


@dataclass(frozen=True)
class SectionUnitIndex:
    """Resolves a section to its unit by id, then by objective.

    ``assemble_section`` stamps ``section_id = unit.unit_id``, so the id is an
    exact match; the objective is the fallback for sections recovered from an
    approved pack that was built under a different unit shape. Matching on the
    objective ALONE collides whenever one objective owns several core steps, and
    the personalise/repair passes then rebuild both sections from a single step —
    duplicating its content under one ``section_id`` and dropping the other
    step's grounded figures.
    """

    by_unit_id: dict[str, SectionGenerationUnit]
    by_objective: dict[str, SectionGenerationUnit]

    @classmethod
    def of(cls, units: Sequence[SectionGenerationUnit]) -> SectionUnitIndex:
        by_objective: dict[str, SectionGenerationUnit] = {}
        for unit in units:
            by_objective.setdefault(unit.lesson_objective_id, unit)
        return cls(
            by_unit_id={unit.unit_id: unit for unit in units},
            by_objective=by_objective,
        )

    def resolve(self, section: ReviewPackSection) -> SectionGenerationUnit | None:
        return self.by_unit_id.get(section.section_id) or self.by_objective.get(
            section.lesson_objective_id
        )
