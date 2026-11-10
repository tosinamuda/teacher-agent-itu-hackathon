"""The first turn production's section composer sends is committed for C0-C3.

``test_rendered_prompt_snapshots`` pins ``GenerateSection``'s shared contract. The prompt a
deployed section call actually sends is ``ComposeSection``'s agent turn, so a change to the
evaluated behaviour only shows up here.

Regenerate an intended change with one command:

    uv run python -m scripts.prompt_snapshots
"""

from __future__ import annotations

import pytest

from scripts.prompt_snapshots import SERVED_DIR
from scripts.prompt_snapshots.render import served_snapshot_text, snapshot_name
from scripts.prompt_snapshots.served import ServedArm, every_served_arm

ARMS = {arm.condition.value: arm for arm in every_served_arm()}
REGENERATE = "regenerate with: uv run python -m scripts.prompt_snapshots"


@pytest.mark.parametrize("code", sorted(ARMS))
def test_the_served_first_turn_matches_its_committed_snapshot(code: str) -> None:
    arm: ServedArm = ARMS[code]
    path = SERVED_DIR / snapshot_name(arm)
    assert path.exists(), f"{code} has no committed served snapshot — {REGENERATE}"
    assert path.read_text(encoding="utf-8") == served_snapshot_text(arm), (
        f"{code} now serves a different prompt than its snapshot. If the change was "
        f"intended, {REGENERATE}"
    )


def test_every_base_condition_has_a_served_snapshot() -> None:
    assert sorted(ARMS) == ["C0", "C1", "C2", "C3"]


def test_the_served_turn_is_the_composer_not_the_shared_contract() -> None:
    """The agent loop's own fields exist only in the composer's render."""
    for arm in ARMS.values():
        system = arm.messages[0]["content"]
        assert arm.contract.startswith("Compose")
        assert "`tool_calls`" in system and "`history`" in system
