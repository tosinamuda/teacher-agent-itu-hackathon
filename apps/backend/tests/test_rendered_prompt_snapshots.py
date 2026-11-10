"""The prompt each condition sends is committed, so a change to it is a reviewable diff.

A prompt that nobody can see changing is how an arm's result stops being attributable: the
H1a null cannot be read against the manipulation without knowing what the manipulation put
in front of the model. These snapshots are the rendered ChatAdapter messages, not the
Pydantic schema and not the signature definition — the schema said the right thing while
`entry_behaviour: []` reached C0 anyway.

Regenerate an intended change with one command:

    uv run python -m scripts.prompt_snapshots
"""

from __future__ import annotations

import pytest

from scripts.prompt_snapshots import SNAPSHOT_DIR
from scripts.prompt_snapshots.arms import Arm, every_arm
from scripts.prompt_snapshots.render import snapshot_name, snapshot_text

ARMS = {arm.condition.value: arm for arm in every_arm()}
REGENERATE = "regenerate with: uv run python -m scripts.prompt_snapshots"


def _arm(code: str) -> Arm:
    return ARMS[code]


@pytest.mark.parametrize("code", sorted(ARMS))
def test_the_rendered_prompt_matches_its_committed_snapshot(code: str) -> None:
    arm = _arm(code)
    path = SNAPSHOT_DIR / snapshot_name(arm)
    assert path.exists(), f"{code} has no committed snapshot — {REGENERATE}"
    assert path.read_text(encoding="utf-8") == snapshot_text(arm), (
        f"{code} renders a different prompt than its snapshot. If the change was "
        f"intended, {REGENERATE}"
    )


def test_every_arm_the_study_reports_has_a_snapshot() -> None:
    """A condition with no snapshot is a condition whose prompt nobody reviewed."""
    assert sorted(ARMS) == ["C0", "C1", "C2", "C3", "P0", "P1"]


def test_the_snapshot_is_the_rendered_prompt_not_the_schema() -> None:
    """ChainOfThought's reasoning field only exists in the render, so it proves the source."""
    rendered = snapshot_text(_arm("C1"))

    assert "[[ ## reasoning ## ]]" in rendered
    assert "## system" in rendered and "## user" in rendered


def test_p0_records_that_it_sends_no_prompt() -> None:
    """Reuse-base is not a missing snapshot; it is a condition with no model call."""
    assert _arm("P0").call is None
    assert "No model call" in snapshot_text(_arm("P0"))


def test_the_grounded_conditions_carry_evidence_the_ungrounded_ones_do_not() -> None:
    """The manipulation must be visible in the render, not only in the profile."""
    ungrounded = [_arm(code).call for code in ("C0", "C1")]
    grounded = [_arm(code).call for code in ("C2", "C3")]

    assert all(call is not None and call.inputs["source_evidence"] == [] for call in ungrounded)
    assert all(call is not None and call.inputs["source_evidence"] for call in grounded)
