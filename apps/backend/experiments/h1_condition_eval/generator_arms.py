"""Generator treatments compared by the H1 evaluation harness."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import dspy

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    ComposeSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    ContractMode,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section_from_sources import (  # noqa: E501
    GenerateSectionFromSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.source_reading import (  # noqa: E501
    evidence_toolset,
)
from app.domains.experiments.review_pack_study.conditions.policies import ConditionProfile
from app.infra.dspy_lm import build_dspy_lm
from experiments.h1_condition_eval.frameworks.adk_arm import AdkComposeSection
from experiments.h1_condition_eval.frameworks.composer import FrameworkComposer
from experiments.h1_condition_eval.frameworks.deepagents_arm import DeepAgentsComposeSection
from experiments.h1_condition_eval.frameworks.langgraph_arm import LangGraphComposeSection
from experiments.h1_condition_eval.harness import Harness, require_harness
from experiments.h1_condition_eval.source_workspace import (
    materialize_workspace,
    workspace_toolset,
)


def _noted_steps(profile: ConditionProfile, case: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the steps this condition may read."""
    if not profile.retrieval.enabled:
        return []
    return [step for step in case["plan"]["steps"] if step.get("note")]


def notes_per_step(profile: ConditionProfile, case: dict[str, Any]) -> dict[str, str]:
    """Materialise one approved note per lesson step."""
    return {step["step_id"]: step["note"] for step in _noted_steps(profile, case)}


def notes_per_lesson(profile: ConditionProfile, case: dict[str, Any]) -> dict[str, str]:
    """Materialise all approved step notes as one lesson notebook."""
    steps = _noted_steps(profile, case)
    if not steps:
        return {}
    body = "\n\n".join(f"## {step['title']}\n\n{step['note']}" for step in steps)
    return {case["lesson"]: body}


@dataclass(frozen=True)
class GeneratorArm:
    """One generator treatment and its evidence-delivery strategy."""

    description: str
    build_generator: Callable[..., Any]
    harness: Harness | None = None
    """What produced the pack, as a dimension. Declared, never defaulted."""
    notes: Callable[[ConditionProfile, dict[str, Any]], dict[str, str]] | None = None
    reads_evidence: bool = False

    def supports(self, profile: ConditionProfile) -> bool:
        """Return whether the arm can run under this condition's evidence policy."""
        return profile.retrieval.enabled or not self.reads_evidence

    def build(
        self,
        *,
        profile: ConditionProfile,
        case: dict[str, Any],
        workspace_root: Path,
        signatures: ContractMode,
    ) -> Any:  # noqa: ANN401
        root = (
            materialize_workspace(self.notes(profile, case), workspace_root) if self.notes else None
        )
        return self.build_generator(root=root, signatures=signatures)


def _packed(*, root: Path | None, signatures: ContractMode) -> GenerateSection:
    del root
    return GenerateSection(lm=build_dspy_lm(), contract_mode=signatures)


def _composing(*, root: Path | None, signatures: ContractMode) -> ComposeSection:
    del root
    return ComposeSection(lm=build_dspy_lm(), contract_mode=signatures)


def _composing_v2(*, root: Path | None, signatures: ContractMode) -> ComposeSection:
    del root
    return ComposeSection(
        lm=build_dspy_lm(),
        contract_mode=signatures,
        loop=dspy.ReActV2,
    )


def _composing_reader(*, root: Path | None, signatures: ContractMode) -> ComposeSection:
    del root
    return ComposeSection(
        lm=build_dspy_lm(),
        contract_mode=signatures,
        source_tools=evidence_toolset(),
    )


def _reader(loop: type[dspy.Module], label: str) -> Callable[..., GenerateSectionFromSources]:
    def build(*, root: Path | None, signatures: ContractMode) -> GenerateSectionFromSources:
        del root, signatures
        return GenerateSectionFromSources(
            lm=build_dspy_lm(),
            tools=evidence_toolset(),
            loop=loop,
            label=label,
        )

    return build


def _workspace_reader(label: str) -> Callable[..., GenerateSectionFromSources]:
    def build(*, root: Path | None, signatures: ContractMode) -> GenerateSectionFromSources:
        del signatures
        if root is None:
            raise ValueError(f"{label} needs a materialized workspace")
        return GenerateSectionFromSources(
            lm=build_dspy_lm(),
            tools=workspace_toolset(root),
            label=label,
        )

    return build


def _framework(composer: type[FrameworkComposer]) -> Callable[..., FrameworkComposer]:
    """An arm that swaps dspy's loop for another framework's, holding the rest fixed."""

    def build(*, root: Path | None, signatures: ContractMode) -> FrameworkComposer:
        del root
        return composer(contract_mode=signatures)

    return build


GENERATOR_ARMS: dict[str, GeneratorArm] = {
    "packed": GeneratorArm(
        "note serialized in, section returned in one shot",
        _packed,
        harness=Harness("dspy", "GenerateSection", "none", "shared", "in_prompt"),
    ),
    "compose": GeneratorArm(
        "section written block-by-block through tools",
        _composing,
        harness=Harness("dspy", "ComposeSection", "ReAct", "composed", "in_prompt"),
    ),
    "compose-v2": GeneratorArm(
        "native tool-calling composition; the turn is a tool_calls field",
        _composing_v2,
        harness=Harness("dspy", "ComposeSection", "ReActV2", "composed", "in_prompt"),
    ),
    "compose-read": GeneratorArm(
        "read tools plus writing tools",
        _composing_reader,
        harness=Harness("dspy", "ComposeSection", "ReAct", "composed", "read_tools"),
        reads_evidence=True,
    ),
    "agentic": GeneratorArm(
        "ReAct reads the note via tools",
        _reader(dspy.ReAct, "agentic"),
        harness=Harness(
            "dspy", "GenerateSectionFromSources", "ReAct", "from_sources", "read_tools"
        ),
        reads_evidence=True,
    ),
    "agentic2": GeneratorArm(
        "ReActV2 reads the note through native tool calling",
        _reader(dspy.ReActV2, "agentic2"),
        harness=Harness(
            "dspy", "GenerateSectionFromSources", "ReActV2", "from_sources", "read_tools"
        ),
        reads_evidence=True,
    ),
    "agentic-file": GeneratorArm(
        "one note file per step, read from disk",
        _workspace_reader("agentic-file"),
        harness=Harness(
            "dspy", "GenerateSectionFromSources", "ReAct", "from_sources", "workspace_files"
        ),
        notes=notes_per_step,
        reads_evidence=True,
    ),
    "langgraph": GeneratorArm(
        "the same composition tools, driven by a langgraph model/tools cycle",
        _framework(LangGraphComposeSection),
        harness=Harness(
            "langgraph", "LangGraphComposeSection", "StateGraph", "composed", "in_prompt"
        ),
    ),
    "adk": GeneratorArm(
        "the same composition tools, driven by a Google ADK agent",
        _framework(AdkComposeSection),
        harness=Harness("google-adk", "AdkComposeSection", "LlmAgent", "composed", "in_prompt"),
    ),
    "deepagents": GeneratorArm(
        "the same composition tools, inside the deepagents harness and its own toolset",
        _framework(DeepAgentsComposeSection),
        harness=Harness(
            "deepagents", "DeepAgentsComposeSection", "create_deep_agent", "composed", "in_prompt"
        ),
    ),
    "agentic-notebook": GeneratorArm(
        "one note per lesson, read from disk",
        _workspace_reader("agentic-notebook"),
        harness=Harness(
            "dspy", "GenerateSectionFromSources", "ReAct", "from_sources", "workspace_files"
        ),
        notes=notes_per_lesson,
        reads_evidence=True,
    ),
}


def harness_for(arm_name: str) -> Harness:
    """The declared harness for an arm, refusing one that never declared it."""
    return require_harness(arm_name, GENERATOR_ARMS[arm_name].harness)
