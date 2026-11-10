"""Construction boundaries for split conditioned study-pack generation."""

from __future__ import annotations

import inspect

import dspy
import pytest

from app.domains.artefacts.types.post_class_review_pack.application.generate_base import (
    GenerateBaseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.personalise import (
    PersonaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.section_generation import (
    SectionCritic,
    SectionGenerator,
    SectionPersonaliser,
    SectionReviser,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import ReviewPackPipeline
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    clear_unit_fields,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure import (
    generation_wiring as deps_module,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CritiqueSections,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)


class _Marker:
    """Identity-only stand-in for the shared LM client."""


def test_model_backed_collaborators_are_required_at_their_real_boundaries() -> None:
    base = inspect.signature(GenerateBaseReviewPack).parameters
    learner = inspect.signature(PersonaliseReviewPack).parameters
    revision = inspect.signature(FinaliseReviewPack).parameters

    assert base["generator"].default is inspect.Parameter.empty
    assert base["finalise"].default is inspect.Parameter.empty
    assert learner["personaliser"].default is inspect.Parameter.empty
    assert learner["finalise"].default is inspect.Parameter.empty
    assert revision["generator"].default is inspect.Parameter.empty
    assert revision["critic"].default is inspect.Parameter.empty


@pytest.mark.parametrize(
    ("constructor", "missing"),
    [
        (GenerateBaseReviewPack, "generator"),
        (PersonaliseReviewPack, "personaliser"),
        (FinaliseReviewPack, "generator"),
    ],
)
def test_forgetting_a_model_collaborator_fails_at_construction(
    constructor: type,
    missing: str,
) -> None:
    with pytest.raises(TypeError) as raised:
        constructor()  # type: ignore[call-arg]
    assert missing in str(raised.value)


@pytest.mark.parametrize(
    "port", [SectionGenerator, SectionPersonaliser, SectionCritic, SectionReviser]
)
def test_every_model_backed_port_declares_only_async_operations(port: type) -> None:
    members = [name for name in vars(port) if not name.startswith("_")]
    assert members
    for name in members:
        assert inspect.iscoroutinefunction(getattr(port, name))


def test_live_composition_wires_each_collaborator_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    built: dict[str, object] = {}

    def _stub(name: str) -> type:
        class _Stub:
            def __init__(self, *, lm: object, **kwargs: object) -> None:
                built[name] = self
                self.lm = lm
                self.kwargs = kwargs

        return _Stub

    for name, attribute in (
        ("generator", "ComposeSection"),
        ("personaliser", "PersonaliseSection"),
        ("critic", "CritiqueSections"),
    ):
        monkeypatch.setattr(deps_module, attribute, _stub(name))

    collaborators = deps_module.live_section_collaborators()
    condition_packs = deps_module.build_base_review_pack_generator(collaborators)
    learner_packs = deps_module.build_review_pack_personaliser(collaborators)

    assert condition_packs._generator is built["generator"]
    # The generator is not a free choice: it is the harness the H1 evaluation judged,
    # so that the evidence base describes the system that ships. Changing it means
    # revisiting HARNESS-DECISION.md, not editing this line.
    assert built["generator"].kwargs == {
        "contract_mode": "leveled",
        "loop": dspy.ReActV2,
        "pipeline": ReviewPackPipeline.V2026_09_02,
    }
    assert learner_packs._personaliser is built["personaliser"]
    assert condition_packs._finalise._critic is built["critic"]
    assert learner_packs._finalise._critic is built["critic"]


@pytest.mark.parametrize(
    "program",
    [GenerateSection, PersonaliseSection, CritiqueSections],
)
def test_each_model_program_is_a_real_dspy_module(program: type) -> None:
    assert issubclass(program, dspy.Module)
    assert "aforward" in vars(program)


def test_live_composition_shares_one_language_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marker = _Marker()
    monkeypatch.setattr(deps_module, "build_dspy_lm", lambda: marker)

    collaborators = deps_module.live_section_collaborators()

    clients = {
        id(collaborators.generator.lm),
        id(collaborators.repairer.lm),
        id(collaborators.personaliser.lm),
        id(collaborators.critic.lm),
    }
    assert clients == {id(marker)}


def test_clearing_an_unknown_unit_field_is_an_error() -> None:
    unit = SectionGenerationUnit(
        unit_id="u",
        lesson_objective_id="o",
        objective_text="t",
    )
    with pytest.raises(AttributeError, match="step_contentt"):
        clear_unit_fields(unit, {"step_contentt": None})
    assert clear_unit_fields(unit, {"objective_text": ""}).objective_text == ""
