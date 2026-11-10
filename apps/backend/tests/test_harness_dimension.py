"""Every arm declares what produced it, and a run that does not record it is refused.

`compose-v2` is a label. Five things vary behind it — the framework, the generator module,
the agent loop, the contract family and how evidence is delivered — and a sixth, the
library version, changed a result on its own: a half-adopted dspy upgrade turned
prompt-parsed ReAct into native tool calling and produced five duds out of six while the
arm name stayed the same.
"""

from __future__ import annotations

import pytest

from experiments.h1_condition_eval.generator_arms import GENERATOR_ARMS, harness_for
from experiments.h1_condition_eval.harness import (
    DISTRIBUTIONS,
    Harness,
    framework_version,
    require_harness,
    require_recorded,
)

ARM_NAMES = sorted(GENERATOR_ARMS)


@pytest.mark.parametrize("name", ARM_NAMES)
def test_every_arm_declares_its_harness(name: str) -> None:
    harness = harness_for(name)

    assert harness.module
    assert harness.framework in DISTRIBUTIONS
    assert harness.loop


def test_an_arm_with_no_declared_harness_is_refused() -> None:
    """A silent default is the failure this exists to prevent."""
    with pytest.raises(ValueError, match="declares no harness"):
        require_harness("invented-arm", None)


def test_the_recorded_harness_carries_the_library_version() -> None:
    recorded = harness_for("compose-v2").recorded()

    assert recorded["framework"] == "dspy"
    assert recorded["framework_version"] == framework_version("dspy")
    assert recorded["loop"] == "ReActV2"


@pytest.mark.parametrize("name", ARM_NAMES)
def test_the_version_recorded_is_the_framework_that_ran(name: str) -> None:
    """Reading dspy's version off a langgraph run would record a library that never ran."""
    harness = harness_for(name)

    assert harness.recorded()["framework_version"] == framework_version(harness.framework)
    assert harness.recorded()["framework_version"] != "unknown"


def test_a_framework_run_does_not_record_dspys_version() -> None:
    """The one number that has to move when the driver does."""
    dspy_arm, langgraph_arm = harness_for("compose-v2"), harness_for("langgraph")

    assert dspy_arm.recorded()["framework_version"] != langgraph_arm.recorded()["framework_version"]


def test_the_two_compose_arms_differ_only_in_the_loop() -> None:
    """The pair whose confusion cost five of six runs."""
    one, two = harness_for("compose"), harness_for("compose-v2")

    assert one.loop == "ReAct"
    assert two.loop == "ReActV2"
    assert (one.module, one.contract_family, one.evidence_delivery) == (
        two.module,
        two.contract_family,
        two.evidence_delivery,
    )


def test_the_arm_names_no_longer_carry_the_meaning_alone() -> None:
    """Every distinct arm is a distinct point in the dimension, or it is a duplicate."""
    seen: dict[tuple, list[str]] = {}
    for name in ARM_NAMES:
        harness = harness_for(name)
        seen.setdefault(
            (
                harness.framework,
                harness.module,
                harness.loop,
                harness.contract_family,
                harness.evidence_delivery,
            ),
            [],
        ).append(name)
    duplicates = {point: names for point, names in seen.items() if len(names) > 1}

    # agentic-file and agentic-notebook share a harness and differ only in how the notes
    # were materialised, which is a dataset shape rather than a harness dimension.
    assert list(duplicates.values()) == [["agentic-file", "agentic-notebook"]]


def test_a_run_record_without_a_harness_is_refused() -> None:
    with pytest.raises(ValueError, match="records no harness"):
        require_recorded({"generator": "compose-v2"}, "run c0c3-worksheet")


def test_a_partial_harness_record_is_refused_too() -> None:
    """Half a record would let a run claim reproducibility it does not have."""
    with pytest.raises(ValueError, match="framework_version"):
        require_recorded({"harness": {"module": "ComposeSection", "loop": "ReActV2"}}, "a run")


def test_a_record_from_before_the_framework_dimension_is_refused() -> None:
    """It says which dspy ran and not that dspy ran, which is no longer the same claim."""
    stale = {
        "module": "ComposeSection",
        "loop": "ReActV2",
        "contract_family": "composed",
        "evidence_delivery": "in_prompt",
        "dspy_version": "3.3.0",
    }

    with pytest.raises(ValueError, match="framework"):
        require_recorded({"harness": stale}, "a run recorded before frameworks")


def test_a_complete_record_round_trips() -> None:
    record = {"harness": harness_for("packed").recorded()}

    assert require_recorded(record, "a run")["module"] == "GenerateSection"


def test_a_harness_is_frozen_so_a_run_cannot_edit_what_produced_it() -> None:
    harness = Harness("dspy", "GenerateSection", "none", "shared", "in_prompt")

    with pytest.raises(AttributeError):
        harness.loop = "ReActV2"  # type: ignore[misc]
