"""Global application config (non-secret tunables).

Secrets stay in the environment (API keys, DB credentials — the LLM keys are
named in app/infra/llm_models.py, DB creds via app/db/config.py). Everything else —
model name, generation modes, loop bounds, paths — lives here in code so the
environment stays small and config is discoverable in one place.

Import the singleton `CONFIG`; do not read these values from `os.getenv`.

These settings are intentionally code-only: they do **not** read from the
environment or a ``.env`` file (see ``_NoEnvSettings`` below). This preserves
the historical behaviour of the frozen-dataclass tree this module replaced —
the only env-sourced config lives in ``app/db/config.py``.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class _NoEnvSettings(BaseSettings):
    """A ``BaseSettings`` base that reads only code defaults — never the env.

    The non-secret application tunables are deliberately *not* environment
    driven. Overriding the settings sources to the empty tuple guarantees no
    field is ever populated from ``os.environ`` or a ``.env`` file, keeping the
    exact behaviour of the frozen dataclasses this replaced.
    """

    model_config = SettingsConfigDict(frozen=True)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Only honour values passed at construction; ignore env, .env, secrets.
        return (init_settings,)


#: ``apps/backend``: the backend's local, untracked working data lives under it.
BACKEND_DIR = Path(__file__).resolve().parents[2]

#: Files the API serves at /static: local copies of the textbook's figures. The frontend
#: points each figure at its copy under /static/figures/, and at the original URL for the rest.
STATIC_DIR = Path(__file__).resolve().parent / "static"


class LessonPlanConfig(BaseModel):
    """Lesson-plan generation tunables."""

    model_config = ConfigDict(frozen=True)

    final_writer_mode: str = "chain_of_thought"
    evidence_selection_strategy: str = "cached"
    # Bounded in-loop self-correction (refine) attempts, shared by both layers.
    max_refine_attempts: int = 3
    # One markdown log per plan generation, for reading a generation back.
    diagnostics_dir: Path = BACKEND_DIR / ".diagnostics" / "lesson-plans"
    # Planning infrastructure precomputed per subtopic (docs/lesson-plan-infrastructure-cache.md).
    infrastructure_cache_dir: Path = BACKEND_DIR / ".cache" / "lesson-plan-infrastructure"
    # Observability toggles (were LESSON_PLAN_DSPY_STATUS / LESSON_PLAN_RLM_VERBOSE).
    dspy_status_logging: bool = True
    rlm_verbose: bool = True
    # No-linkage (monolithic) layer: load the GEPA-optimized program instead of
    # the default un-optimized one. Enabled after manual review on the no-linkage
    # JSS1-maths stratum (n=3): the *cleaned* GEPA artifact is 3/3 clean (vs 2/3
    # baseline) and adds worked-examples + gradual release on 3/3 (vs 1/3) at
    # comparable cost. The raw GEPA artifact's grounded "worksheet" hallucination
    # was removed first (see whole_lesson_gepa_nolinkage.json). Expert eval is the
    # final arbiter; flip back to False to compare against baseline.
    use_optimized_program: bool = True
    # None -> the no-linkage-safe artifact bundled next to the monolithic module
    # (infrastructure/dspy/optimized/whole_lesson_gepa_nolinkage.json).
    optimized_program_path: str | None = None


class ResearchDefaultsConfig(BaseModel):
    """Default lesson context for the synthetic experiment harness.

    The teacher-in-the-loop synthetic flow starts by selecting the lesson context
    (school · term · subject · class · subtopic). These values are the canonical
    default a researcher seeds with — deliberately a *third-term* subtopic, so the
    demo exercises a post-foundational topic. Change the default subtopic here.
    """

    model_config = ConfigDict(frozen=True)

    grade: str = "JSS1"
    subject: str = "Mathematics"
    term: str = "Third Term"
    subtopic: str = "Area of regular plane shapes such as: squares, rectangles, parallelogram, etc."


class JobsConfig(BaseModel):
    """How the API process runs the background jobs queued in the ``jobs`` table."""

    model_config = ConfigDict(frozen=True)

    # Jobs run at once, each in a process of its own.
    slots: int = 4
    # How often the runner looks for work and at its running jobs.
    poll_seconds: float = 1.0
    # A running job's claim lasts this long unless renewed; a job whose claim lapses is
    # taken to have died and is run again.
    lease_seconds: int = 120
    # How often a running job renews its claim: well inside the lease.
    heartbeat_seconds: int = 30
    # A job still running after this is stopped and run again. A task makes at most
    # about 16 LLM calls, each capped at 300s, so the worst legitimate run is ~80 min.
    time_limit_seconds: int = 2 * 60 * 60


class AppConfig(_NoEnvSettings):
    """Top-level non-secret application config."""

    # The model each role runs is declared in app/infra/llm_models.ROLES, not here:
    # it is an experimental condition, and it must be one fact rather than a default
    # that call sites can reach around. Build LMs with dspy_lm.build_dspy_lm().
    # Display name of the single source textbook the corpus was ingested from.
    # Shown to expert raters as the source of grounded references (the internal
    # per-block ids like ``ch01-b029`` are collapsed away on the rater worksheet).
    # Set this to the real published title.
    textbook_name: str = "JSS1 Mathematics Textbook"
    # Institution + study identity printed on the expert rater packs (H1/H2
    # worksheets + source-grounding audit packs) AND the rater web banner. Single
    # source of truth.
    #
    # BLINDING: the title is deliberately neutral — it must NOT reveal that the
    # content is system/AI-generated or framework-driven, or raters could be biased
    # for/against it. The real thesis title ("Design and Evaluation of a Lesson-
    # Plan-Driven Framework for Curriculum-Constrained Personalised Learning") lives
    # in the thesis/docs, never on rater-facing materials.
    institution_name: str = "University of Lagos"
    study_title: str = "A research study of revision-note quality"
    # Teacher-friendly aliases for the technical thesis rubric dimensions, shown
    # to raters on the worksheets/forms (math teachers, not researchers). Keyed by
    # rubric ``criterion_id``. The technical labels in H1_RUBRIC/H2_RUBRIC stay
    # canonical for the dataset/thesis; these are display-only and safe to reword.
    rater_term_aliases: dict[str, str] = Field(
        default_factory=lambda: {
            # H1 — class-level reading-note quality
            "objective_curriculum_alignment": "Covers the right topics",
            "taught_lesson_alignment": "Matches the taught lesson",
            "scope_conceptual_correctness": "On-topic and correct",
            "clarity_usefulness": "Clear and useful for students",
            # H2 — personalised-version quality (mirrors the H2 form's copy)
            "learner_state_suitability": "Fit for this learner",
            "scaffolding_appropriateness": "Teaching support",
            "challenge_calibration": "Challenge level",
            "misconception_support": "Misconception help",
            "objective_preservation": "Keeps the lesson goal",
        }
    )
    lesson_plan: LessonPlanConfig = Field(default_factory=LessonPlanConfig)
    # Default lesson context the synthetic harness starts from (a 3rd-term subtopic).
    research_defaults: ResearchDefaultsConfig = Field(default_factory=ResearchDefaultsConfig)
    jobs: JobsConfig = Field(default_factory=JobsConfig)
    # Persist every LLM call, prompt and reply in full, to the generation_events table.
    # Off by default because the table grows with every call and nothing reads it
    # day to day; set true to capture calls for a research run.
    log_model_calls: bool = False


CONFIG = AppConfig()
