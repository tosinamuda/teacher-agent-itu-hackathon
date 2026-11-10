"""Study design configuration — one config drives both pilot and publication runs.

eval-plan §5, §8. The pilot mode (1 lesson) proves the workflow; publication mode
(12 lessons) yields the 48 H1 / 96 H2 packets the thesis reports. Same code, two
configs.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.domains.experiments.domain.types import ConditionCode, Hypothesis

from .profiles import H1_CONDITION_PROFILES, condition_codes, h1_main_condition_codes

# Derived from the profile registry (the single source of truth): the default study design
# runs whatever conditions exist, so adding/removing a condition needs no change here.
_H1_CONDITIONS = condition_codes(Hypothesis.H1)
_H2_CONDITIONS = condition_codes(Hypothesis.H2)


class StudyDesignConfig(BaseModel):
    """Reproducible knobs for the experiment scale and blinding."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str

    lesson_count: int
    focal_learners_per_lesson: int
    target_raters_per_packet: int

    h1_conditions: tuple[ConditionCode, ...] = _H1_CONDITIONS
    h2_conditions: tuple[ConditionCode, ...] = _H2_CONDITIONS

    require_blinding: bool = True
    randomise_packet_order: bool = True

    def conditions_to_generate(self) -> tuple[ConditionCode, ...]:
        """The configured H1 conditions that generate their own pack — C0–C3."""
        return tuple(
            code for code in self.h1_conditions if H1_CONDITION_PROFILES[code].generated_by == code
        )

    def conditions_to_fork(self) -> tuple[tuple[ConditionCode, ConditionCode], ...]:
        """Each configured H1 condition that takes another's pack, with the one that made it.

        C4 takes C3's: its only addition is the teacher-validation gate, so generating it
        separately would make the C3-vs-C4 difference model noise rather than the gate.
        """
        return tuple(
            (code, H1_CONDITION_PROFILES[code].generated_by)
            for code in self.h1_conditions
            if H1_CONDITION_PROFILES[code].generated_by != code
        )

    def expected_h1_packets(self) -> int:
        """One H1 rater packet per lesson × main C-condition (C0–C3).

        C4 is teacher-governance evidence, not a rater packet, so it is excluded
        from the H1 packet count (June-5 settled design).
        """
        main = set(h1_main_condition_codes())
        return self.lesson_count * sum(1 for code in self.h1_conditions if code in main)

    def expected_h2_packets(self) -> int:
        """One H2 packet per lesson × focal learner × P condition."""
        return self.lesson_count * self.focal_learners_per_lesson * len(self.h2_conditions)


PILOT_ONE_LESSON_CONFIG = StudyDesignConfig(
    name="pilot_one_lesson",
    lesson_count=1,
    focal_learners_per_lesson=4,
    target_raters_per_packet=3,
)

PUBLICATION_CONFIG = StudyDesignConfig(
    name="publication_12_lesson",
    lesson_count=12,
    focal_learners_per_lesson=4,
    target_raters_per_packet=3,
)

STUDY_DESIGN_CONFIGS: dict[str, StudyDesignConfig] = {
    PILOT_ONE_LESSON_CONFIG.name: PILOT_ONE_LESSON_CONFIG,
    PUBLICATION_CONFIG.name: PUBLICATION_CONFIG,
}
