"""Validation-guided revision orchestration for review packs."""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.section_generation import (
    SectionCritic,
    SectionGenerator,
    SectionRepairer,
    SectionReviser,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.outcome import (
    evaluate_validation,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    unit_for_personalisation_repair,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.unit_index import (
    SectionUnitIndex,
)

from .decisions import (
    evaluate_revision,
    finding_counts,
    implicated_objectives,
    issue_messages,
    issues_for_section,
    select_repair_strategy,
)


class FinaliseReviewPack:
    """Validate and revise a pack until it passes or exhausts its retry budget."""

    def __init__(
        self,
        *,
        generator: SectionGenerator,
        repairer: SectionRepairer,
        critic: SectionCritic,
        validator: ReviewPackStructuralValidator | None = None,
        reviser: SectionReviser | None = None,
    ) -> None:
        self._generator = generator
        self._repairer = repairer
        self._critic = critic
        self._validator = validator or ReviewPackStructuralValidator()
        self._reviser = reviser

    async def finalise(
        self,
        *,
        policy: ReviewPackGenerationPolicy,
        request: ReviewPackRequest,
        sections: list[ReviewPackSection],
        base_sections: list[ReviewPackSection] | None = None,
    ) -> GeneratedReviewPack:
        """Validate and revise a generated pack under its product policy."""
        if not policy.validation.enabled:
            return GeneratedReviewPack(request=request, sections=sections)

        validation = await self._validate(
            policy=policy,
            sections=sections,
            request=request,
            base_sections=base_sections,
        )
        first_pass = validation
        round_results = [validation]
        retries_completed = 0
        regenerated: list[str] = []

        while True:
            decision = evaluate_revision(
                validation_passed=validation.passed,
                retry_on_failure=policy.validation.retry_on_failure,
                retries_completed=retries_completed,
                max_retries=policy.validation.max_retries,
            )
            if decision.action != "revise":
                break
            sections = await self._revise(
                policy=policy,
                request=request,
                sections=sections,
                validation=validation,
                base_sections=base_sections,
                rewritten=regenerated,
            )
            retries_completed += 1
            validation = await self._validate(
                policy=policy,
                sections=sections,
                request=request,
                base_sections=base_sections,
            )
            round_results.append(validation)

        return GeneratedReviewPack(
            request=request,
            sections=sections,
            validation=validation,
            validation_before_repair=first_pass,
            validation_rounds=round_results,
            repaired=retries_completed > 0,
            regenerated=regenerated,
        )

    async def _validate(
        self,
        *,
        policy: ReviewPackGenerationPolicy,
        request: ReviewPackRequest,
        sections: list[ReviewPackSection],
        base_sections: list[ReviewPackSection] | None,
    ) -> ValidationResult:
        structural = self._validator.validate(
            policy=policy,
            sections=sections,
            request=request,
            base_sections=base_sections,
        )
        critiques = await self._critic.review(
            request=request,
            sections=sections,
            checks=policy.validation.checks,
        )
        return evaluate_validation(structural=structural, critiques=critiques).as_result()

    async def _regenerate(
        self,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        section_id: str,
        issues: list[str],
        rewritten: list[str] | None,
    ) -> ReviewPackSection:
        """The section written again from its unit, told what the failed draft got wrong.

        ``rewritten`` gains the section's id, so a caller can say which sections were replaced.
        """
        if rewritten is not None and section_id not in rewritten:
            rewritten.append(section_id)
        constraints = "\n".join(f"- {issue}" for issue in issues)
        constrained = unit.model_copy(
            update={
                "objective_text": (
                    unit.objective_text + "\n\nA previous draft of this section failed review. "
                    "Do not repeat these mistakes:\n" + constraints
                )
            }
        )
        return await self._generator.generate_section(request=request, unit=constrained)

    async def _revise(
        self,
        *,
        policy: ReviewPackGenerationPolicy,
        request: ReviewPackRequest,
        sections: list[ReviewPackSection],
        validation: ValidationResult,
        base_sections: list[ReviewPackSection] | None,
        rewritten: list[str] | None = None,
    ) -> list[ReviewPackSection]:
        """The sections after one repair round; ``rewritten`` gains the ids written from scratch."""
        issues = issue_messages(validation)
        if not issues:
            return sections

        implicated = implicated_objectives(validation, sections)
        counts = finding_counts(validation)
        units = SectionUnitIndex.of(request.units)
        base_by_section = {section.section_id: section for section in (base_sections or [])}
        section_ids = [section.lesson_objective_id for section in sections]
        revised: list[ReviewPackSection] = []

        for section in sections:
            objective_id = section.lesson_objective_id
            unit = units.resolve(section)
            decision = select_repair_strategy(
                implicated=implicated is None or objective_id in implicated,
                finding_count=counts.get(objective_id, 0),
                max_patchable_findings=policy.execution.max_patchable_findings,
                has_unit=unit is not None,
                has_reviser=self._reviser is not None,
            )
            section_issues = issues_for_section(objective_id, section_ids, issues)

            if decision.strategy == "preserve":
                revised.append(section)
            elif decision.strategy == "regenerate":
                if unit is None:
                    raise RuntimeError("regeneration strategy requires a generation unit")
                revised.append(
                    await self._regenerate(
                        request, unit, section.section_id, section_issues, rewritten
                    )
                )
            elif decision.strategy == "edit":
                if self._reviser is None:
                    raise RuntimeError("edit strategy requires a section reviser")
                revised.append(
                    await self._reviser.revise(
                        section=section,
                        findings=section_issues,
                    )
                )
            else:
                if unit is None:
                    raise RuntimeError("repair strategy requires a generation unit")
                if request.generation_policy.personalisation.adapts_to_learner_state:
                    unit = unit_for_personalisation_repair(
                        unit,
                        base_by_section.get(section.section_id) or section,
                    )
                revised.append(
                    await self._repairer.repair_section(
                        request=request,
                        unit=unit,
                        failed_section=section,
                        issues=section_issues,
                    )
                )
        return revised
