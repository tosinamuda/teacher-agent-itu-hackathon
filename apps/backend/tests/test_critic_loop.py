"""C3's critic loop: content findings drive repair, and the loop is bounded.

The deterministic checks compare id sets and field presence, so a pack could
invent a cause, contradict its own table or address the teacher and still pass
every one. The critic supplies the checks that read prose; these tests pin how
its findings reach repair and how many rounds the loop is allowed.
"""

from __future__ import annotations

import pytest
from condition_leakage_support import EchoModel
from recording_lm import RecordingLM

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    GenerationPolicyContext,
    LessonContextForGeneration,
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
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.critique_sections import (  # noqa: E501
    ContentFinding,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CONTENT_CHECKS,
    CritiqueSections,
    _as_check_result,
    learner_view,
)
from app.domains.experiments.review_pack_study.conditions.profiles import (
    ConditionProfile,
    ContextPolicy,
    ValidationPolicy,
)

_OBJECTIVE = "lop01"


def _section(
    objective_id: str = _OBJECTIVE, text: str = "Two plus two is four."
) -> ReviewPackSection:
    return ReviewPackSection(
        section_id=f"objective:{objective_id}",
        title="Adding numbers",
        lesson_objective_id=objective_id,
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text=text,
                lesson_objective_id=objective_id,
            )
        ],
    )


def _request(sections: list[ReviewPackSection]) -> BaseReviewPackRequest:
    return BaseReviewPackRequest(
        artefact_spec=revision_pack_spec("JSS1"),
        generation_policy=_profile(("content_grounding",), max_retries=2).generation_policy(),
        policy=GenerationPolicyContext(
            require_source_refs=False,
            use_only_provided_sources=False,
            preserve_lesson_objective=True,
            instruction_summary="",
        ),
        lesson_context=LessonContextForGeneration(
            subject="Mathematics",
            grade_level="JSS1",
            topic="Addition",
            lesson_objectives=["add two numbers"],
        ),
        units=[
            SectionGenerationUnit(
                unit_id=f"unit:{section.lesson_objective_id}",
                lesson_objective_id=section.lesson_objective_id,
                objective_text="add two numbers",
            )
            for section in sections
        ],
    )


def _profile(checks: tuple[str, ...], max_retries: int) -> ConditionProfile:
    return ConditionProfile(
        hypothesis="H1",
        condition_code="C3",
        generated_by="C3",
        description="test",
        context=ContextPolicy(generation_unit="lesson_step"),
        validation=ValidationPolicy(
            enabled=True, checks=checks, retry_on_failure=True, max_retries=max_retries
        ),
    )


class _StubCritic:
    """Returns queued findings, one round at a time, and counts its calls."""

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


class _StubValidator:
    def validate(self, **_: object) -> ValidationResult:
        return ValidationResult(passed=True, checks=[])


class _CountingRepairer:
    def __init__(self) -> None:
        self.calls = 0


def _finding(defect: str = "grounding", quote: str = "the canteen sold 40 pies") -> ContentFinding:
    return ContentFinding(defect=defect, quote=quote, problem="never happened")


def _revision(critic: _StubCritic) -> FinaliseReviewPack:
    return FinaliseReviewPack(
        generator=EchoModel(),
        repairer=EchoModel(),
        critic=critic,
        validator=_StubValidator(),
    )


def testlearner_view_carries_prose_not_model_metadata() -> None:
    view = learner_view(_section())
    assert "Two plus two is four." in view
    assert "block_id" not in view
    assert "lesson_objective_id" not in view


def test_findings_become_one_issue_each_named_by_section() -> None:
    result = _as_check_result(
        "content_grounding",
        [("lop01", _finding()), ("lop02", _finding(quote="prices rose on Wednesday"))],
    )
    assert result.passed is False
    assert result.details["sections_with_findings"] == ["lop01", "lop02"]

    issues = issue_messages(ValidationResult(passed=False, checks=[result]))
    assert len(issues) == 2
    # Each section's repair must read only its own quoted text.
    assert issues_for_section("lop01", ["lop01", "lop02"], issues) == [issues[0]]


def test_content_findings_implicate_only_their_sections() -> None:
    validation = ValidationResult(
        passed=False, checks=[_as_check_result("internal_consistency", [("lop02", _finding())])]
    )
    assert implicated_objectives(validation, [_section("lop01"), _section("lop02")]) == {"lop02"}


@pytest.mark.asyncio
async def test_clean_critic_leaves_the_pack_untouched() -> None:
    critic = _StubCritic([[]])
    sections = [_section()]
    profile = _profile(("content_grounding",), max_retries=2)

    result = await _revision(critic).finalise(
        policy=profile, request=_request(sections), sections=sections
    )

    assert result.validation.passed is True
    assert result.repaired is False
    assert critic.calls == 1  # no repair round, so no re-validation


@pytest.mark.asyncio
async def test_repair_stops_as_soon_as_the_critic_is_satisfied(monkeypatch) -> None:  # noqa: ANN001
    critic = _StubCritic([[(_OBJECTIVE, _finding())], []])
    sections = [_section()]
    revision = _revision(critic)
    repairs = _CountingRepairer()

    async def _repair(**kwargs: object) -> list[ReviewPackSection]:
        repairs.calls += 1
        return kwargs["sections"]  # type: ignore[return-value]

    monkeypatch.setattr(revision, "_revise", _repair)
    result = await revision.finalise(
        policy=_profile(("content_grounding",), max_retries=2),
        request=_request(sections),
        sections=sections,
    )

    assert repairs.calls == 1  # second round never runs
    assert result.repaired is True
    assert result.validation.passed is True
    # The clean final result would otherwise erase what was caught.
    assert result.validation_before_repair.passed is False


@pytest.mark.asyncio
async def test_the_loop_is_bounded_by_max_retries(monkeypatch) -> None:  # noqa: ANN001
    critic = _StubCritic([[(_OBJECTIVE, _finding())]])  # never satisfied
    sections = [_section()]
    revision = _revision(critic)
    repairs = _CountingRepairer()

    async def _repair(**kwargs: object) -> list[ReviewPackSection]:
        repairs.calls += 1
        return kwargs["sections"]  # type: ignore[return-value]

    monkeypatch.setattr(revision, "_revise", _repair)
    result = await revision.finalise(
        policy=_profile(("content_grounding",), max_retries=2),
        request=_request(sections),
        sections=sections,
    )

    assert repairs.calls == 2
    assert result.validation.passed is False


@pytest.mark.asyncio
async def test_a_profile_without_content_checks_costs_no_llm_call() -> None:
    """C0-C2 must not pay for a critique they never asked for."""
    sections = [_section()]

    # A recorder with no scripted reply raises on any call, so "costs no call"
    # is asserted by the LM itself rather than by counting afterwards.
    results = await CritiqueSections(lm=RecordingLM()).review(
        request=_request(sections), sections=sections, checks=("objective_coverage",)
    )

    assert results == []


def test_findings_quoting_absent_text_are_dropped() -> None:
    """A finding whose quote is not in the learner view is about text the
    learner never sees - hallucinated, or aimed at serialization."""
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
        learner_view,
    )

    section = _section(text="The perimeter is the distance round the shape.")
    view = learner_view(section)
    real = _finding(quote="distance round the shape")
    ghost = _finding(quote="block_id: b1")
    assert real.quote in view
    assert ghost.quote not in view


@pytest.mark.asyncio
async def test_heavily_flagged_sections_regenerate_instead_of_patching(monkeypatch) -> None:  # noqa: ANN001
    """Past the profile's patch threshold the section is beyond patching: N blind edits
    is how repair collateral happens, so it regenerates once under constraints."""
    threshold = _profile(("content_grounding",), max_retries=2).execution.max_patchable_findings
    many = [(_OBJECTIVE, _finding(quote=f"bad sentence {i}")) for i in range(threshold + 1)]
    critic = _StubCritic([many, []])
    sections = [_section()]
    revision = _revision(critic)
    calls = {"repair": 0, "regenerate": 0}

    async def _repair(**kwargs: object) -> ReviewPackSection:
        calls["repair"] += 1
        return kwargs["failed_section"]  # type: ignore[return-value]

    async def _generate_section(**kwargs: object) -> ReviewPackSection:
        calls["regenerate"] += 1
        unit = kwargs["unit"]
        assert "Do not repeat these mistakes" in unit.objective_text  # type: ignore[union-attr]
        return _section(text="rewritten cleanly")

    monkeypatch.setattr(revision._repairer, "repair_section", _repair, raising=False)
    monkeypatch.setattr(revision._generator, "generate_section", _generate_section, raising=False)
    result = await revision.finalise(
        policy=_profile(("content_grounding",), max_retries=2),
        request=_request(sections),
        sections=sections,
    )

    assert calls["regenerate"] == 1
    assert result.validation.passed is True


@pytest.mark.asyncio
async def test_a_section_at_the_threshold_is_patched_not_regenerated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The other side of the boundary, which the test above cannot see.

    That test builds its findings as ``MAX_PATCHABLE_FINDINGS + 1``, so it moves
    with the constant: set the threshold to zero and it still regenerates, still
    passes, while every flagged section is now rewritten whole and the editing
    reviser never runs. Pinning the count that must still be PATCHED is what
    makes the boundary a boundary.
    """
    threshold = _profile(("content_grounding",), max_retries=2).execution.max_patchable_findings
    at_limit = [(_OBJECTIVE, _finding(quote=f"bad sentence {i}")) for i in range(threshold)]
    critic = _StubCritic([at_limit, []])
    sections = [_section()]
    revision = _revision(critic)
    calls = {"repair": 0, "regenerate": 0}

    async def _repair(**kwargs: object) -> ReviewPackSection:
        calls["repair"] += 1
        return kwargs["failed_section"]  # type: ignore[return-value]

    async def _generate_section(**kwargs: object) -> ReviewPackSection:
        calls["regenerate"] += 1
        return _section(text="rewritten cleanly")

    monkeypatch.setattr(revision._repairer, "repair_section", _repair, raising=False)
    monkeypatch.setattr(revision._generator, "generate_section", _generate_section, raising=False)
    await revision.finalise(
        policy=_profile(("content_grounding",), max_retries=2),
        request=_request(sections),
        sections=sections,
    )

    assert calls["repair"] == 1, "a section at the limit must be patched"
    assert calls["regenerate"] == 0, "a section at the limit must not be rewritten whole"
