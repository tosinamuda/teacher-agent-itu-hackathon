"""No-LLM tests for the OPT/HELD-OUT check split (experiment integrity backbone).

If this split is wrong, the whole bake-off is compromised (the optimiser could
see a held-out check, or a real failure could be silently ignored), so these
invariants are tested deterministically.
"""

from __future__ import annotations

from experiments.strategy_bakeoff.check_split import (
    ALL_CHECK_CODES,
    GENERATION_ERROR_CODE,
    HELD_OUT_CHECK_CODES,
    OPT_CHECK_CODES,
    code_of,
    is_errored,
    opt_reward,
    split_violations,
)


def test_split_is_a_true_partition() -> None:
    assert OPT_CHECK_CODES.isdisjoint(HELD_OUT_CHECK_CODES)
    assert OPT_CHECK_CODES | HELD_OUT_CHECK_CODES == ALL_CHECK_CODES


def test_code_of_parses_violation_string() -> None:
    assert code_of("reused_modeling_record: foo -> ['a','b']") == "reused_modeling_record"
    assert code_of("ungrounded_evaluation_material: mentions 'worksheet'") == (
        "ungrounded_evaluation_material"
    )


def test_split_routes_each_code_to_correct_bucket() -> None:
    violations = [
        "reused_modeling_record: x",  # OPT
        "mixed_direction_evidence: y",  # OPT
        "ungrounded_evaluation_material: z",  # HELD-OUT
        "duplicate_kc_focus: w",  # HELD-OUT
        "some_unknown_future_check: q",  # UNKNOWN
    ]
    split = split_violations(violations)
    assert len(split.opt) == 2
    assert len(split.held_out) == 2
    assert len(split.unknown) == 1


def test_unknown_codes_count_against_held_out_not_opt() -> None:
    split = split_violations(["brand_new_check: q"])
    assert split.opt_passed is True  # unknown does NOT pollute the OPT target
    assert split.held_out_passed is False  # but it does fail held-out (strict)
    assert split.fully_passed is False


def test_opt_reward_is_one_only_when_opt_clean() -> None:
    # Held-out violations present but no OPT violations -> reward 1.0 (correct:
    # the optimiser must not be rewarded or penalised for held-out checks).
    assert opt_reward(["ungrounded_evaluation_material: z"]) == 1.0
    assert opt_reward([]) == 1.0
    # OPT violations drive the reward down, monotonically.
    one = opt_reward(["reused_modeling_record: x"])
    two = opt_reward(["reused_modeling_record: x", "mixed_direction_evidence: y"])
    assert 0.0 <= two < one < 1.0


def test_fully_passed_requires_both_sets_clean() -> None:
    assert split_violations([]).fully_passed is True
    assert split_violations(["reused_modeling_record: x"]).fully_passed is False
    assert split_violations(["duplicate_kc_focus: x"]).fully_passed is False


def test_generation_error_sentinel_is_not_in_the_partition() -> None:
    # The crash sentinel must NOT be a check code, or it would break the partition.
    assert GENERATION_ERROR_CODE not in OPT_CHECK_CODES
    assert GENERATION_ERROR_CODE not in HELD_OUT_CHECK_CODES
    assert GENERATION_ERROR_CODE not in ALL_CHECK_CODES


def test_is_errored_detects_only_the_crash_sentinel() -> None:
    assert is_errored(["generation_error: ValueError: boom"]) is True
    assert is_errored(["reused_modeling_record: x"]) is False
    assert is_errored([]) is False


def test_errored_attempt_scores_zero_reward_not_one() -> None:
    # The bug being fixed: a generation_error carries no OPT code, so without the
    # guard opt_reward would return 1.0 and an errored attempt would win/early-stop.
    assert opt_reward(["generation_error: ValueError: boom"]) == 0.0
    # An errored attempt still routes to UNKNOWN -> not held-out-clean.
    split = split_violations(["generation_error: ValueError: boom"])
    assert split.opt_passed is True  # no OPT code present
    assert split.held_out_passed is False  # but unknown bucket fails held-out
