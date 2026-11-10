"""A condition's workspace holds exactly what it may read, so nothing gates it.

An evidence-less condition must not merely be refused the note — it must not
have one on disk. Otherwise ``--generator agentic-file --conditions C1`` turns
C1 into C2 while still labelling, fingerprinting and rating cleanly.
"""

from __future__ import annotations

from pathlib import Path

import dspy
import pytest
from recording_lm import RecordingLM

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.policy import (
    build_generation_policy,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    LessonContextForGeneration,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import DraftSection
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section_from_sources import (  # noqa: E501
    GenerateSectionFromSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.source_reading import (  # noqa: E501
    reading_tools,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES
from experiments.h1_condition_eval.generator_arms import (
    GENERATOR_ARMS,
    notes_per_lesson,
    notes_per_step,
)
from experiments.h1_condition_eval.source_workspace import file_tools, materialize_workspace

_NOTE = "A cylinder has two circular faces and one curved surface."
_CASE = {
    "lesson": "t3-w05",
    "plan": {"steps": [{"step_id": "t3-w05-s1", "title": "Cylinders", "note": _NOTE}]},
}


@pytest.mark.parametrize("notes", [notes_per_step, notes_per_lesson])
@pytest.mark.parametrize("code", [ConditionCode.C0, ConditionCode.C1])
def test_evidence_less_conditions_materialize_nothing(notes, code: ConditionCode) -> None:  # noqa: ANN001
    assert H1_CONDITION_PROFILES[code].retrieval.enabled is False
    assert notes(H1_CONDITION_PROFILES[code], _CASE) == {}


@pytest.mark.parametrize("code", [ConditionCode.C2, ConditionCode.C3])
def test_grounded_conditions_materialize_their_notes(code: ConditionCode) -> None:
    profile = H1_CONDITION_PROFILES[code]
    assert notes_per_step(profile, _CASE) == {"t3-w05-s1": _NOTE}
    assert _NOTE in notes_per_lesson(profile, _CASE)["t3-w05"]


@pytest.mark.parametrize("code", [ConditionCode.C0, ConditionCode.C1])
def test_an_evidence_less_workspace_has_nothing_to_open(
    code: ConditionCode, tmp_path: Path
) -> None:
    root = materialize_workspace(notes_per_step(H1_CONDITION_PROFILES[code], _CASE), tmp_path)
    list_notes, read_note = file_tools(root)
    assert list_notes() == []
    assert _NOTE not in read_note("t3-w05-s1.md")


def test_reading_is_confined_to_the_workspace(tmp_path: Path) -> None:
    """A path out of the directory is a name that does not exist in it."""
    (tmp_path / "outside.md").write_text(_NOTE, encoding="utf-8")
    root = materialize_workspace({"t3-w05-s1": _NOTE}, tmp_path / "workspace")
    _, read_note = file_tools(root)
    assert _NOTE not in read_note("../outside.md")
    assert _NOTE in read_note("t3-w05-s1.md")


def test_workspace_arms_are_the_ones_that_materialize() -> None:
    materialising = {name for name, arm in GENERATOR_ARMS.items() if arm.notes}
    assert materialising == {"agentic-file", "agentic-notebook"}


@pytest.mark.parametrize("code", [ConditionCode.C0, ConditionCode.C1])
def test_reading_arms_refuse_the_conditions_they_cannot_serve(code: ConditionCode) -> None:
    """Reading tools are the evidence channel; write tools are the output channel."""
    profile = H1_CONDITION_PROFILES[code]
    reading = {name for name, arm in GENERATOR_ARMS.items() if arm.reads_evidence}
    assert reading == {
        "agentic",
        "agentic2",
        "agentic-file",
        "agentic-notebook",
        "compose-read",
    }
    assert not any(GENERATOR_ARMS[name].supports(profile) for name in reading)
    # Varying only the OUTPUT channel is an arm at every condition.
    assert GENERATOR_ARMS["compose"].supports(profile)
    assert GENERATOR_ARMS["packed"].supports(profile)


@pytest.mark.parametrize("code", [ConditionCode.C2, ConditionCode.C3])
def test_every_arm_serves_a_grounded_condition(code: ConditionCode) -> None:
    profile = H1_CONDITION_PROFILES[code]
    assert all(arm.supports(profile) for arm in GENERATOR_ARMS.values())


def test_a_unit_without_evidence_lists_no_documents() -> None:
    unit = SectionGenerationUnit(
        unit_id="unit:lo-1", lesson_objective_id="lo-1", objective_text="cylinders"
    )
    list_documents, read_document = reading_tools(unit)
    assert list_documents() == []
    assert "No document named" in read_document("t3-w05-s1")


@pytest.mark.asyncio
async def test_agentic_loop_uses_the_persisted_condition_iteration_budget() -> None:
    observed: dict[str, int] = {}

    class _Loop(dspy.Module):
        def __init__(
            self,
            _signature: type[dspy.Signature],
            *,
            tools: list,
            max_iters: int,
        ) -> None:
            super().__init__()
            observed["max_iters"] = max_iters

        async def aforward(self, **_kwargs: object) -> dspy.Prediction:
            raise AssertionError("run_agent should call acall")

        async def acall(self, **_kwargs: object) -> dspy.Prediction:
            return dspy.Prediction(
                section=DraftSection(
                    title="Cylinders",
                    instructional_support="A cylinder has circular faces.",
                    worked_examples=[],
                    practice=[],
                )
            )

    profile = H1_CONDITION_PROFILES[ConditionCode.C2].model_copy(
        update={
            "execution": H1_CONDITION_PROFILES[ConditionCode.C2].execution.model_copy(
                update={"agent_max_iterations": 5}
            )
        }
    )
    unit = SectionGenerationUnit(
        unit_id="u1",
        lesson_objective_id="o1",
        objective_text="Describe a cylinder",
    )
    request = BaseReviewPackRequest(
        artefact_spec=revision_pack_spec("JSS1"),
        generation_policy=profile.generation_policy(),
        policy=build_generation_policy(profile),
        lesson_context=LessonContextForGeneration(
            subject="Mathematics",
            grade_level="JSS1",
            topic="Shapes",
            lesson_objectives=["Describe a cylinder"],
        ),
        units=[unit],
    )
    generator = GenerateSectionFromSources(
        lm=RecordingLM(),
        tools=lambda _request, _unit: [],
        loop=_Loop,
    )

    await generator.generate_section(request=request, unit=unit)

    assert observed == {"max_iters": 5}
