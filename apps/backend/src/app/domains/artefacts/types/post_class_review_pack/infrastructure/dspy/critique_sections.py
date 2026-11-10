"""Critique generated content when a policy requests prose validation.

eval-plan §20. The checks in ``validator`` compare id sets and field presence;
none of them reads a sentence, so a pack can invent a causal claim, contradict
its own worked example, or address the teacher instead of the learner and still
pass every one. This module supplies the checks that must read prose. It reports
in the same ``CheckResult`` shape, so the repair path consumes them unchanged.
"""

from __future__ import annotations

import asyncio

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    learner_setting,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    CheckResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ValidationCheck,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)

from .contracts.critique_sections import (
    ContentDefect,
    ContentFinding,
    SectionCritique,
    critique_contract,
)
from .prompt_fingerprint import record_prompt

# What the critic is asked to look for, and the policy check each one answers.
CONTENT_CHECKS: dict[ContentDefect, ValidationCheck] = {
    "grounding": "content_grounding",
    "consistency": "internal_consistency",
    "audience": "learner_facing_register",
}


def learner_view(section: ReviewPackSection) -> str:
    """The section as the learner reads it — prose only.

    Handing the critic the section MODEL made it review the serialised JSON:
    on ``t3-w06`` it reported ``"block_id"`` and ``"block_type"`` as text shown
    to the learner, 17 findings of pure noise. It can only judge what reaches a
    reader if it is given what reaches a reader.
    """
    parts = [section.title, *(block.text or block.caption or "" for block in section.blocks)]
    # Practice is learner-facing, so a critic blind to it reviews half the section. The
    # answer goes in as its own part: a wrong answer key is a defect the critic should
    # find, and it is what the blinded judges hit hardest.
    for item in section.practice:
        parts += [item.prompt, item.answer, item.worked_solution or ""]
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def _evidence_text(unit: SectionGenerationUnit | None) -> str:
    if unit is None:
        return ""
    return "\n\n".join(item.excerpt for item in unit.source_evidence if item.excerpt)


def _describe(finding: ContentFinding) -> str:
    return f'"{finding.quote.strip()}" — {finding.problem.strip()}'


def _as_check_result(
    check: ValidationCheck, findings: list[tuple[str, ContentFinding]]
) -> CheckResult:
    """Fold every finding of one kind into the single result the repair path reads."""
    if not findings:
        return CheckResult(check=check, passed=True)
    # Each finding names its section, so a section's repair reads only its own.
    described = [f"{objective_id}: {_describe(finding)}" for objective_id, finding in findings]
    return CheckResult(
        check=check,
        passed=False,
        message="; ".join(described),
        details={
            "sections_with_findings": sorted({objective_id for objective_id, _ in findings}),
            "findings": described,
        },
    )


class CritiqueSections(dspy.Module):
    """Reads each generated section against the teaching evidence behind it."""

    def __init__(self, *, lm: dspy.BaseLM, pipeline: ReviewPackPipeline = CURRENT_PIPELINE) -> None:
        super().__init__()
        self.lm = lm
        self.critique_predictor = dspy.ChainOfThought(critique_contract(pipeline))

    async def review(
        self,
        *,
        request: ReviewPackRequest,
        sections: list[ReviewPackSection],
        checks: tuple[ValidationCheck, ...],
    ) -> list[CheckResult]:
        """Critique every section in parallel, as one result per enabled check."""
        wanted = {defect: check for defect, check in CONTENT_CHECKS.items() if check in checks}
        if not wanted:
            return []
        units = {unit.lesson_objective_id: unit for unit in request.units}
        reviewed = await asyncio.gather(
            *(
                self._review_section(
                    unit=units.get(s.lesson_objective_id),
                    section=s,
                    setting=learner_setting(request.lesson_context),
                )
                for s in sections
            )
        )
        found = [pair for section_findings in reviewed for pair in section_findings]
        return [
            _as_check_result(check, [pair for pair in found if pair[1].defect == defect])
            for defect, check in wanted.items()
        ]

    async def _review_section(
        self,
        *,
        unit: SectionGenerationUnit | None,
        section: ReviewPackSection,
        setting: str,
    ) -> list[tuple[str, ContentFinding]]:
        with dspy.settings.context(lm=self.lm):
            findings: list[tuple[str, ContentFinding]] = await self.acall(
                unit=unit,
                section=section,
                setting=setting,
            )
        return findings

    async def aforward(
        self,
        *,
        unit: SectionGenerationUnit | None,
        section: ReviewPackSection,
        setting: str,
    ) -> list[tuple[str, ContentFinding]]:
        """Run the critique predictor for one learner-visible section."""
        view = learner_view(section)
        record_prompt("quality_critique", SectionCritique)
        result = await self.critique_predictor.acall(
            setting=setting,
            lesson_objective=unit.objective_text if unit else section.title,
            teaching_evidence=_evidence_text(unit),
            section_to_review=view,
        )
        # Precision filter: a finding whose quote does not occur in the learner
        # view is a finding about text the learner never sees — hallucinated or
        # aimed at serialization. R5's 11-finding over-fire shipped repairs for
        # exactly such findings; dropping them is mechanical and free.
        findings = [finding for finding in (result.findings or []) if finding.quote.strip() in view]
        return [(section.lesson_objective_id, finding) for finding in findings]
