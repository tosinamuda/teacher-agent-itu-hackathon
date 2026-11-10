"""The backend's local working data lives under apps/backend, never inside the app package."""

from __future__ import annotations

from pathlib import Path

from app.config import BACKEND_DIR, CONFIG
from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.cache import (
    InfrastructureArtifactCache,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.diagnostics import (
    DiagnosticLogWriter,
)


def test_the_backend_dir_is_the_project_root() -> None:
    assert (BACKEND_DIR / "pyproject.toml").is_file()
    assert (BACKEND_DIR / "src" / "app" / "config.py").is_file()


def test_diagnostics_and_the_infrastructure_cache_sit_at_the_backend_root() -> None:
    assert DiagnosticLogWriter().output_dir() == BACKEND_DIR / ".diagnostics" / "lesson-plans"
    cache_dir = CONFIG.lesson_plan.infrastructure_cache_dir
    assert cache_dir == BACKEND_DIR / ".cache" / "lesson-plan-infrastructure"
    assert InfrastructureArtifactCache()._dir == cache_dir
    assert Path(BACKEND_DIR / "src" / "app") not in cache_dir.parents
