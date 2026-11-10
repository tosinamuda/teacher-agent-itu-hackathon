"""Every judged section can be read beside the inputs its call was given.

A maths error or an ungrounded claim could be read in a recorded run and not explained,
because what went in was never kept. Rebuilding it is only sound if it is rebuilt through
the arm the run recorded and against the plan whose hash it recorded — a rebuild through
today's default would describe a call that run never made.

    uv run python -m scripts.prompt_snapshots.pairing [run-label]
"""

from __future__ import annotations

from collections import Counter

import pytest

from scripts.prompt_snapshots.pairing import Pair, pairs, run_path

JUDGED = "c0c3-worksheet"
if not run_path(JUDGED).exists():
    pytest.skip(f"{JUDGED} is versioned by DVC; run `dvc pull` first", allow_module_level=True)
PAIRS = pairs(JUDGED)
BY_CONDITION = Counter(pair.condition for pair in PAIRS)


def test_the_judged_run_is_pairable_at_all() -> None:
    assert run_path(JUDGED).exists()
    assert PAIRS, "the run H1a was judged on produced no pairs"


def test_every_arm_h1a_compares_is_covered() -> None:
    """C0 and C1 are the endpoint; C2 and C3 carry the evidence step."""
    assert set(BY_CONDITION) == {"C0", "C1", "C2", "C3"}
    assert len(set(BY_CONDITION.values())) == 1, "the arms are unevenly paired"


@pytest.mark.parametrize("condition", ["C0", "C1", "C2", "C3"])
def test_each_pair_carries_both_halves(condition: str) -> None:
    for pair in (p for p in PAIRS if p.condition == condition):
        assert pair.inputs, f"{pair.unit_id} has no inputs"
        assert pair.section.get("title"), f"{pair.unit_id} has no section"


def test_the_pairing_uses_the_arm_the_run_recorded_not_the_default() -> None:
    """The judged run used compose-v2 with leveled contracts; the snapshots pin packed
    with the shared contract. Pairing through the default would be a different call."""
    arms = {pair.arm for pair in PAIRS}
    contracts = {pair.contract for pair in PAIRS}

    assert arms == {"compose-v2"}
    assert contracts == {"ComposeWriteObjectiveSection", "ComposeWriteGroundedSection"}


def test_the_ungrounded_and_grounded_arms_were_given_different_contracts() -> None:
    """The evidence step, as the judged run actually ran it."""
    ungrounded = {p.contract for p in PAIRS if p.condition in {"C0", "C1"}}
    grounded = {p.contract for p in PAIRS if p.condition in {"C2", "C3"}}

    assert ungrounded == {"ComposeWriteObjectiveSection"}
    assert grounded == {"ComposeWriteGroundedSection"}
    assert not ungrounded & grounded


def test_only_the_grounded_arms_were_given_lesson_content() -> None:
    for pair in PAIRS:
        has_content = "lesson_content" in pair.inputs
        assert has_content == (pair.condition in {"C2", "C3"}), pair.unit_id


def test_c1_calls_carry_the_plan_fields_c0_calls_do_not() -> None:
    """The H1a manipulation, in the inputs of the run that was judged."""
    plan_keys = {"current_step", "instructional_events", "student_tasks", "assessment_points"}

    def carried(condition: str) -> set[str]:
        return {
            key
            for pair in PAIRS
            if pair.condition == condition
            for key in pair.inputs["unit_context"]
        }

    assert carried("C0") & plan_keys == set()
    assert carried("C1") & plan_keys == plan_keys


def test_a_re_frozen_plan_refuses_to_pair(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pairing against a changed plan would attach a response to inputs it never saw."""
    import scripts.prompt_snapshots.pairing as pairing

    original = pairing._plans_as_run_saw_them

    def tampered(record: dict) -> dict:
        record = {**record, "plans": {lesson: "0" * 16 for lesson in record["plans"]}}
        return original(record)

    monkeypatch.setattr(pairing, "_plans_as_run_saw_them", tampered)

    with pytest.raises(ValueError, match="re-frozen"):
        pairing.pairs(JUDGED)


def test_a_findings_carrying_pack_shows_its_findings_beside_the_inputs() -> None:
    """Where the critic flagged something, the prompt is inspectable beside it."""
    flagged = [pair for pair in PAIRS if pair.findings]

    if not flagged:
        pytest.skip("no critic findings recorded in this run")
    for pair in flagged:
        assert pair.inputs and pair.section


def test_a_pair_names_the_unit_it_belongs_to() -> None:
    assert all(isinstance(pair, Pair) and pair.unit_id for pair in PAIRS)
