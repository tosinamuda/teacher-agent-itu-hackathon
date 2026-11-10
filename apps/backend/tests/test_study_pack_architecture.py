"""Executable ownership boundaries for review-pack generation."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import dspy
import pytest

from app.domains.artefacts.types.post_class_review_pack.application.generation_roles import (
    BaseReviewPackGenerator,
    ReviewPackPersonaliser,
)
from app.domains.artefacts.types.post_class_review_pack.application.materialisation import (
    ReviewPackArtefactWriter,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    ComposeSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CritiqueSections,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.edit_section import (
    EditSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section_from_sources import (  # noqa: E501
    GenerateSectionFromSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.repair_section import (
    RepairGeneratedSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.revise_review_pack import (  # noqa: E501
    ReviseReviewPack,
)
from app.domains.experiments.application.store import ExperimentStore, ExperimentStoreFactory
from app.domains.experiments.review_pack_study.condition_runs.store import ConditionRuns

pytestmark = pytest.mark.architecture

BACKEND_ROOT = Path(__file__).parents[1]
PRODUCT_ROOT = BACKEND_ROOT / "src/app/domains/artefacts/types/post_class_review_pack"
OLD_STUDY_PACK_ROOT = BACKEND_ROOT / "src/app/domains/experiments/study_pack"
STUDY_ROOT = BACKEND_ROOT / "src/app/domains/experiments/review_pack_study"


def test_each_section_generation_method_is_one_dspy_module() -> None:
    for operation in (GenerateSection, GenerateSectionFromSources, ComposeSection):
        assert issubclass(operation, dspy.Module)
        assert "aforward" in vars(operation)


def test_other_model_operations_use_product_names() -> None:
    for operation in (
        RepairGeneratedSection,
        PersonaliseSection,
        CritiqueSections,
        EditSection,
        ReviseReviewPack,
    ):
        assert issubclass(operation, dspy.Module)
        assert "StudyPack" not in operation.__name__


def test_generation_unit_names_its_one_to_one_output_boundary() -> None:
    assert SectionGenerationUnit.__doc__
    assert "one generated section" in SectionGenerationUnit.__doc__.lower()


def test_product_does_not_import_experiments() -> None:
    offenders = _imports_with_prefix(PRODUCT_ROOT, "app.domains.experiments")
    assert offenders == []


def test_old_experiment_study_pack_package_is_absent() -> None:
    # Source, not the directory: stale __pycache__ from a pre-move checkout outlives the
    # package and would fail this for a reason that is not the one it guards.
    assert not list(OLD_STUDY_PACK_ROOT.glob("**/*.py"))


def test_experiment_study_contains_only_study_behaviour() -> None:
    assert {path.name for path in STUDY_ROOT.iterdir() if path.name != "__pycache__"} == {
        "__init__.py",
        "condition_runs",
        "conditions",
        "h1",
        "h2",
        "progress.py",
        "run.py",
        "wiring.py",
    }
    forbidden = ("dspy", "request", "validation", "section")
    assert not any(part in forbidden for path in STUDY_ROOT.rglob("*.py") for part in path.parts)


def test_product_application_names_use_review_pack_vocabulary() -> None:
    offenders: list[str] = []
    for path in (PRODUCT_ROOT / "application").rglob("*.py"):
        if "helper" in path.stem.lower() or "study_pack" in path.stem.lower():
            offenders.append(str(path.relative_to(PRODUCT_ROOT)))
        tree = ast.parse(path.read_text())
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and (
                "Helper" in node.name or "StudyPack" in node.name
            ):
                offenders.append(f"{path.relative_to(PRODUCT_ROOT)}:{node.name}")
    assert offenders == []


def test_generation_and_materialisation_roles_are_narrow() -> None:
    assert _operations(BaseReviewPackGenerator) == {"generate"}
    assert _operations(ReviewPackPersonaliser) == {"personalise"}
    assert _operations(ReviewPackArtefactWriter) == {"stage"}


def test_condition_runs_are_records_behind_one_store() -> None:
    assert _operations(ConditionRuns) == {"record"}
    assert _operations(ExperimentStore) == {"commit", "rollback"}
    assert _operations(ExperimentStoreFactory) == set()


def _imports_with_prefix(root: Path, prefix: str) -> list[str]:
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            if any(module == prefix or module.startswith(f"{prefix}.") for module in modules):
                offenders.append(str(path.relative_to(BACKEND_ROOT)))
    return offenders


def _operations(port: type) -> set[str]:
    return {
        name
        for name, value in vars(port).items()
        if not name.startswith("_") and inspect.isfunction(value)
    }
