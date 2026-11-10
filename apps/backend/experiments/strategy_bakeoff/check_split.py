"""OPT vs HELD-OUT split of the deterministic semantic checks.

The shared `SemanticPlanValidator` emits seven violation codes. To keep the
experiment honest (judge != target, §4 of the pre-registration), we split them:

  * OPT set      — drives self-correction (Refine reward) and GEPA optimisation.
  * HELD-OUT set — evaluation only; the optimiser NEVER sees these, so a passing
                   strategy must satisfy checks it did not train on. This is the
                   generalisation signal.

A violation STRING is classified by its code prefix (`"<code>: ..."`). Anything
unrecognised is treated as HELD-OUT (fail-safe: an unknown failure should never
silently count toward the optimisation target).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# All seven codes the validator can emit (verified against
# runtime/semantic_validation.py on 2026-05-30).
ALL_CHECK_CODES: frozenset[str] = frozenset(
    {
        "duplicate_kc_focus",
        "missing_evidence_plan",
        "missing_resolved_kc",
        "mixed_direction_evidence",
        "reused_modeling_record",
        "missing_evaluation_coverage",
        "ungrounded_evaluation_material",
    }
)

# Drives optimisation / self-correction. These are structural evidence-selection
# decisions a strategy can act on directly.
OPT_CHECK_CODES: frozenset[str] = frozenset(
    {
        "reused_modeling_record",
        "mixed_direction_evidence",
        "missing_evidence_plan",
        "missing_resolved_kc",
    }
)

# Evaluation only — never shown to the optimiser.
HELD_OUT_CHECK_CODES: frozenset[str] = frozenset(
    {
        "ungrounded_evaluation_material",
        "duplicate_kc_focus",
        "missing_evaluation_coverage",
    }
)

# Sentinel emitted by the scored generation when an attempt CRASHES (e.g. a
# pydantic/pipeline failure). It is deliberately NOT a member of either check set
# — adding it would break the OPT/HELD-OUT partition. An errored attempt is
# instead handled explicitly: zero reward and never a pass (see `opt_reward` and
# `StrategyResult` in strategies.py). It naturally lands in the UNKNOWN bucket,
# so `held_out_passed` already fails for it.
GENERATION_ERROR_CODE = "generation_error"


def _assert_partition() -> None:
    """The split must be a true partition of all codes (no overlap, no gaps)."""
    if OPT_CHECK_CODES & HELD_OUT_CHECK_CODES:
        raise ValueError("OPT and HELD-OUT check sets overlap")
    if (OPT_CHECK_CODES | HELD_OUT_CHECK_CODES) != ALL_CHECK_CODES:
        missing = ALL_CHECK_CODES - (OPT_CHECK_CODES | HELD_OUT_CHECK_CODES)
        extra = (OPT_CHECK_CODES | HELD_OUT_CHECK_CODES) - ALL_CHECK_CODES
        raise ValueError(f"split is not a partition; missing={missing} extra={extra}")


_assert_partition()


def code_of(violation: str) -> str:
    """Extract the check code from a violation string (`"<code>: detail"`)."""
    return violation.split(":", 1)[0].strip()


@dataclass(frozen=True)
class SplitViolations:
    """Violations partitioned into OPT / HELD-OUT / UNKNOWN buckets."""

    opt: list[str] = field(default_factory=list)
    held_out: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)

    @property
    def opt_passed(self) -> bool:
        return not self.opt

    @property
    def held_out_passed(self) -> bool:
        # Unknown codes are evaluated on the strict side: they must not appear
        # for a plan to count as held-out-clean.
        return not self.held_out and not self.unknown

    @property
    def fully_passed(self) -> bool:
        return self.opt_passed and self.held_out_passed


def split_violations(violations: list[str]) -> SplitViolations:
    """Partition raw violation strings into OPT / HELD-OUT / UNKNOWN."""
    opt: list[str] = []
    held_out: list[str] = []
    unknown: list[str] = []
    for violation in violations:
        code = code_of(violation)
        if code in OPT_CHECK_CODES:
            opt.append(violation)
        elif code in HELD_OUT_CHECK_CODES:
            held_out.append(violation)
        else:
            unknown.append(violation)
    return SplitViolations(opt=opt, held_out=held_out, unknown=unknown)


def is_errored(violations: list[str]) -> bool:
    """True if any violation is the crash sentinel (`generation_error: ...`).

    A crashed attempt produced no plan; it must never read as progress.
    """
    return any(code_of(v) == GENERATION_ERROR_CODE for v in violations)


def opt_reward(violations: list[str]) -> float:
    """Reward for self-correction / GEPA: 1.0 iff no OPT-set violations.

    Decays per OPT violation so partial progress is visible to a refiner. Only
    OPT-set violations affect this — HELD-OUT and unknown codes are ignored here
    by design (they must not leak into the optimisation target).

    A crashed attempt (`generation_error`) scores 0.0: it carries no OPT code, so
    without this guard it would falsely score 1.0 and win best-of-N / trigger
    early-stop despite having produced no plan.
    """
    if is_errored(violations):
        return 0.0
    split = split_violations(violations)
    if not split.opt:
        return 1.0
    return max(0.0, 1.0 - 0.34 * len(split.opt))
