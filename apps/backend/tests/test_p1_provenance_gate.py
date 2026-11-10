"""The P1 provenance gate: generated problems must not claim textbook solutions.

The gate was a phrase pattern that matched 1 of 4 real leaks the critic caught,
so P1 routes this class to ``learner_facing_register`` instead. These pin the
routing and the repair plumbing, not a lexicon.
"""

from __future__ import annotations

import pytest
from condition_leakage_support import EchoModel

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    GenerationPolicyContext,
    LessonContextForGeneration,
    PersonalisedReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.decisions import (
    implicated_objectives,
    issue_messages,
    issues_for_section,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.critique_sections import (  # noqa: E501
    ContentFinding,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CONTENT_CHECKS,
    _as_check_result,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.experiment_enums import Hypothesis

# Every provenance leak observed in a real run: the first four grew the retired
# pattern, the last three are what it missed.
PROVENANCE_CORPUS = (
    "Verify your answer against the solution in the textbook.",
    "Answers for the first two items are given in the textbook.",
    "The first three items are based on the textbook exercise on counting.",
    "This mirrors the textbook exercise (REF-3).",
    "The source material shows a frequency table of favourite colours as an illustration.",
    "(If the lesson content expects 32 cm, use the given answer)",
    "Write your answers on a separate sheet before checking the answer key.",
)

_OBJECTIVE = "lop01"


def _section(
    objective_id: str = _OBJECTIVE, text: str = "Find the LCM of 4 and 6."
) -> ReviewPackSection:
    return ReviewPackSection(
        section_id=f"objective:{objective_id}",
        title="LCM",
        lesson_objective_id=objective_id,
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="worked_example",
                text=text,
                lesson_objective_id=objective_id,
            )
        ],
    )


def _request(sections: list[ReviewPackSection]) -> PersonalisedReviewPackRequest:
    return PersonalisedReviewPackRequest(
        artefact_spec=revision_pack_spec("JSS1"),
        generation_policy=profile_for(Hypothesis.H2, ConditionCode.P1).generation_policy(),
        policy=GenerationPolicyContext(
            require_source_refs=False,
            use_only_provided_sources=True,
            preserve_lesson_objective=True,
            instruction_summary="",
        ),
        lesson_context=LessonContextForGeneration(
            subject="Mathematics", grade_level="JSS1", topic="LCM", lesson_objectives=[]
        ),
        units=[
            SectionGenerationUnit(
                unit_id=f"unit:{section.lesson_objective_id}",
                lesson_objective_id=section.lesson_objective_id,
                objective_text="find the LCM",
            )
            for section in sections
        ],
        base_pack_id="PACK-1",
        focal_learner_id="LEARNER-1",
    )


class _StubCritic:
    """Reports one queued round of findings, then nothing."""

    def __init__(self, rounds: list[list[tuple[str, ContentFinding]]]) -> None:
        self.rounds = rounds
        self.calls = 0

    async def review(self, *, request, sections, checks):  # noqa: ANN001, ANN003
        findings = self.rounds[min(self.calls, len(self.rounds) - 1)]
        self.calls += 1
        return [
            _as_check_result(
                check, [pair for pair in findings if CONTENT_CHECKS[pair[1].defect] == check]
            )
            for check in checks
            if check in CONTENT_CHECKS.values()
        ]


def _finding(quote: str) -> ContentFinding:
    return ContentFinding(
        defect="audience",
        quote=quote,
        problem="tells the reader where the content came from instead of teaching it",
    )


def test_p1_routes_provenance_to_the_critic() -> None:
    profile = profile_for(Hypothesis.H2, ConditionCode.P1)
    assert "learner_facing_register" in profile.validation.checks
    # The retired lexicon must not come back as a profile check.
    assert not any(check.startswith("no_invented") for check in profile.validation.checks)


def test_structural_validator_reads_no_prose() -> None:
    """Every check the deterministic validator still runs is id/field-shaped."""
    result = ReviewPackStructuralValidator().validate(
        policy=profile_for(Hypothesis.H2, ConditionCode.P1).generation_policy(),
        sections=[_section(text=PROVENANCE_CORPUS[0])],
        request=_request([_section()]),
        base_sections=[_section()],
    )
    assert {check.check for check in result.checks} <= {
        "objective_coverage",
        "scope_compliance",
        "source_refs_present",
        "source_refs_valid",
        "objective_preservation",
    }


@pytest.mark.parametrize("claim", PROVENANCE_CORPUS)
def test_every_corpus_claim_reaches_repair_as_its_own_issue(claim: str) -> None:
    check = _as_check_result("learner_facing_register", [(_OBJECTIVE, _finding(claim))])
    assert check.passed is False

    validation = ValidationResult(passed=False, checks=[check])
    assert implicated_objectives(validation, [_section(), _section("lop02")]) == {_OBJECTIVE}

    issues = issue_messages(validation)
    assert len(issues) == 1
    assert claim in issues[0]
    assert issues_for_section(_OBJECTIVE, [_OBJECTIVE, "lop02"], issues) == issues


@pytest.mark.asyncio
async def test_provenance_finding_drives_a_repair_round(monkeypatch) -> None:  # noqa: ANN001
    leak = PROVENANCE_CORPUS[4]
    critic = _StubCritic([[(_OBJECTIVE, _finding(leak))], []])
    sections = [_section(text=leak)]
    revision = FinaliseReviewPack(
        generator=EchoModel(),
        repairer=EchoModel(),
        critic=critic,
    )
    repairs: list[str] = []

    async def _repair(**kwargs: object) -> list[ReviewPackSection]:
        repairs.append("called")
        return kwargs["sections"]  # type: ignore[return-value]

    monkeypatch.setattr(revision, "_revise", _repair)
    result = await revision.finalise(
        policy=profile_for(Hypothesis.H2, ConditionCode.P1).generation_policy(),
        request=_request(sections),
        sections=sections,
        base_sections=[_section()],
    )

    assert repairs == ["called"]
    assert result.repaired is True
    assert result.validation.passed is True
