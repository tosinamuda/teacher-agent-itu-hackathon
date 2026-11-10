"""Structural post-generation validation for review-pack policies.

eval-plan §20. These run outside DSPy so the validated conditions are real
executable differences from their unvalidated siblings. Prose defects belong
to :mod:`critic`, which reports the same ``CheckResult`` into the same path.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    MIN_EXPLANATION_CHARS,
    PROSE_CHECKS,
    ReviewPackGenerationPolicy,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.unit_index import (
    SectionUnitIndex,
)

from .schemas import CheckResult, ValidationResult


def _unit_refs(units: Sequence[SectionGenerationUnit]) -> set[str]:
    """Every source_ref the given units carried."""
    return {
        evidence.source_ref
        for unit in units
        for evidence in unit.source_evidence
        if evidence.source_ref
    }


def _section_source_refs(section: ReviewPackSection) -> set[str]:
    refs = set(section.source_refs)
    for block in section.blocks:
        refs.update(block.source_refs)
    return {ref for ref in refs if ref}


def _explanation_chars(section: ReviewPackSection) -> int:
    return sum(
        len(block.text.strip()) for block in section.blocks if block.block_type == "explanation"
    )


class ReviewPackStructuralValidator:
    """Run the policy's deterministic checks against a generated pack."""

    def validate(
        self,
        *,
        policy: ReviewPackGenerationPolicy,
        sections: list[ReviewPackSection],
        request: ReviewPackRequest,
        base_sections: list[ReviewPackSection] | None = None,
    ) -> ValidationResult:
        """Evaluate every check the policy enables; pass iff all pass."""
        dispatch = {
            "objective_coverage": lambda: self._objective_coverage(sections, request),
            "scope_compliance": lambda: self._scope_compliance(sections, request),
            "source_refs_present": lambda: self._source_refs_present(sections),
            "source_refs_valid": lambda: self._source_refs_valid(sections, request),
            "objective_preservation": lambda: self._objective_preservation(sections, base_sections),
            "practice_is_checkable": lambda: self._practice_is_checkable(sections),
            "explanation_present": lambda: self._explanation_present(sections),
            "no_added_objectives": lambda: self._no_added_objectives(sections, base_sections),
        }
        mine = [check for check in policy.validation.checks if check not in PROSE_CHECKS]
        missing = [check for check in mine if check not in dispatch]
        if missing:
            raise NotImplementedError(
                f"generation policy declares unsupported checks {missing}: they are neither "
                "prose checks answered by the critic nor implemented structurally"
            )
        results = [dispatch[check]() for check in mine]
        return ValidationResult(passed=all(item.passed for item in results), checks=results)

    def _objective_coverage(
        self,
        sections: list[ReviewPackSection],
        request: ReviewPackRequest,
    ) -> CheckResult:
        expected = {unit.lesson_objective_id for unit in request.units}
        covered = {section.lesson_objective_id for section in sections}
        missing = sorted(expected - covered)
        return CheckResult(
            check="objective_coverage",
            passed=not missing,
            message=None if not missing else f"missing objectives: {missing}",
            details={"missing": missing},
        )

    def _scope_compliance(
        self,
        sections: list[ReviewPackSection],
        request: ReviewPackRequest,
    ) -> CheckResult:
        allowed = {unit.lesson_objective_id for unit in request.units}
        extra = sorted({section.lesson_objective_id for section in sections} - allowed)
        return CheckResult(
            check="scope_compliance",
            passed=not extra,
            message=None if not extra else f"out-of-scope objectives: {extra}",
            details={"out_of_scope": extra},
        )

    def _source_refs_present(
        self,
        sections: list[ReviewPackSection],
    ) -> CheckResult:
        missing = sorted(
            section.lesson_objective_id for section in sections if not _section_source_refs(section)
        )
        return CheckResult(
            check="source_refs_present",
            passed=not missing,
            message=None if not missing else f"sections without source refs: {missing}",
            details={"sections_without_refs": missing},
        )

    def _source_refs_valid(
        self,
        sections: list[ReviewPackSection],
        request: ReviewPackRequest,
    ) -> CheckResult:
        """Each section may cite only the evidence ITS unit was shown.

        Under objective-scoped retrieval two units hold different excerpts, so
        judging every section against the union would accept a section citing a
        source it never saw. A section that maps to no unit is judged against
        the union — an unattributable section cannot be scoped any tighter.
        """
        units = SectionUnitIndex.of(request.units)
        everything = _unit_refs(request.units)
        per_section: dict[str, list[str]] = {}
        for section in sections:
            unit = units.resolve(section)
            allowed = _unit_refs([unit]) if unit is not None else everything
            unexpected = sorted(_section_source_refs(section) - allowed)
            if unexpected:
                per_section[section.section_id or section.lesson_objective_id] = unexpected
        invalid = sorted({ref for refs in per_section.values() for ref in refs})
        return CheckResult(
            check="source_refs_valid",
            passed=not invalid,
            message=(
                None
                if not invalid
                else f"refs not in the evidence the section was shown: {per_section}"
            ),
            # Every ref the request offered anywhere. Per-section allowances are
            # narrower, so this is the ceiling, and it survives an empty pack.
            details={"invalid_refs": invalid, "allowed_count": len(everything)},
        )

    def _practice_is_checkable(
        self,
        sections: list[ReviewPackSection],
    ) -> CheckResult:
        """Every practice item carries the answer the learner checks it against.

        The brief has always said so; nothing could enforce it while the question and
        the answer were one paragraph of prose, and the model put the answer under its
        own question in 9 of 12 lesson/condition cells (issue #163). Now the answer is
        a field, this is a shape rather than a hope: an item with no answer, or a
        section with no practice at all, fails.
        """
        empty = sorted(
            item.item_id or section.section_id
            for section in sections
            for item in section.practice
            if not item.answer.strip()
        )
        without = sorted(section.section_id for section in sections if not section.practice)
        broken = empty + without
        return CheckResult(
            check="practice_is_checkable",
            passed=not broken,
            message=None if not broken else f"practice a learner cannot check: {broken}",
            details={"unanswered": empty, "sections_without_practice": without},
        )

    def _objective_preservation(
        self,
        sections: list[ReviewPackSection],
        base_sections: list[ReviewPackSection] | None,
    ) -> CheckResult:
        base_objectives = {section.lesson_objective_id for section in (base_sections or [])}
        candidate_objectives = {section.lesson_objective_id for section in sections}
        dropped = sorted(base_objectives - candidate_objectives)
        return CheckResult(
            check="objective_preservation",
            passed=not dropped,
            message=None if not dropped else f"dropped base objectives: {dropped}",
            details={"dropped": dropped},
        )

    def _explanation_present(self, sections: list[ReviewPackSection]) -> CheckResult:
        """Every section teaches the idea before it works it: its explanation is not a line."""
        thin = {
            section.section_id or section.lesson_objective_id: chars
            for section in sections
            if (chars := _explanation_chars(section)) < MIN_EXPLANATION_CHARS
        }
        by_objective = {
            section.lesson_objective_id: chars
            for section in sections
            if (chars := _explanation_chars(section)) < MIN_EXPLANATION_CHARS
        }
        return CheckResult(
            check="explanation_present",
            passed=not thin,
            message=(
                None
                if not thin
                else f"explanation shorter than {MIN_EXPLANATION_CHARS} characters "
                f"(write about 500), by objective: {by_objective}"
            ),
            details={"explanation_characters": thin, "minimum": MIN_EXPLANATION_CHARS},
        )

    def _no_added_objectives(
        self,
        sections: list[ReviewPackSection],
        base_sections: list[ReviewPackSection] | None,
    ) -> CheckResult:
        """A personalised pack serves the base pack's objectives and no others."""
        base = {section.lesson_objective_id for section in (base_sections or [])}
        added = sorted({s.lesson_objective_id for s in sections} - base) if base_sections else []
        return CheckResult(
            check="no_added_objectives",
            passed=not added,
            message=None if not added else f"objectives the base pack does not have: {added}",
            details={"added": added},
        )
