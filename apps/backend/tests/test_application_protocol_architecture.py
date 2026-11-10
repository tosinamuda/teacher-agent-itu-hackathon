"""Mechanical guards for application protocol and store boundaries."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path
from typing import Protocol

import pytest

from app.domains.evaluation.application.assignment_ports import AssignmentStore
from app.domains.evaluation.application.audit_ports import (
    AuditItemBuildStore,
    AuditRatingStore,
)
from app.domains.evaluation.application.identity_ports import RaterRegistrationStore
from app.domains.evaluation.application.rating_ports import (
    RatingImportStore,
    RatingSubmissionStore,
)
from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
    SqlAlchemyEvaluationStore,
)
from scripts.layer_paths import application_files

pytestmark = pytest.mark.architecture

APPLICATION_ROOT = Path("src/app/domains")
EVALUATION_ROOT = APPLICATION_ROOT / "evaluation/application"
PROTOCOL_METHOD_LIMIT = 10
DELETED_EXPERIMENT_PORT_PATH = Path("src/app/domains/experiments/application/ports.py")
DELETED_EXPERIMENT_PORT = "Experiment" + "RepositoryPort"
EXPERIMENT_REPOSITORY_PATH = Path("src/app/domains/experiments/infrastructure/repository.py")
DEAD_EXPERIMENT_READ_APIS = {
    "get_artefact",
    "get_experiment_for_workspace_plan",
    "list_artefacts_by_ids",
    "list_experiments_by_public_ids",
}
EXPERIMENT_DASHBOARD_PROTOCOL_FILES = {
    Path("src/app/domains/experiments/application/c4_base_pack.py"),
    Path("src/app/domains/experiments/application/experiment_list_loader.py"),
    Path("src/app/domains/experiments/application/experiment_views/execution.py"),
    Path("src/app/domains/experiments/application/experiment_views/experiment.py"),
    Path("src/app/domains/experiments/application/focal_case_records.py"),
    Path("src/app/domains/experiments/application/focal_learner_selection.py"),
    Path("src/app/domains/experiments/application/results_summary_query.py"),
}
EXPERIMENT_DASHBOARD_ROUTE_HANDLERS = {
    "get_execution",
    "get_experiment",
    "get_experiment_summary",
    "get_experiment_workflow",
    "list_experiment_workspaces",
    "list_experiments",
    "list_workspace_lesson_versions",
    "list_workspace_lessons",
    "trigger_synthetic_loop",
    "trigger_synthetic_rate",
    "trigger_synthetic_students",
    "trigger_synthetic_teacher",
}


def _application_files() -> list[Path]:
    return application_files()


def _protocol_classes(path: Path) -> list[ast.ClassDef]:
    tree = ast.parse(path.read_text(), filename=str(path))
    return [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(isinstance(base, ast.Name) and base.id == "Protocol" for base in node.bases)
    ]


def _public_members(node: ast.ClassDef) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    return [
        member
        for member in node.body
        if isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef)
        and not member.name.startswith("_")
    ]


def _class_definition(path: Path, class_name: str) -> ast.ClassDef:
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise AssertionError(f"{class_name} not found in {path}")


def _deleted_experiment_port_references() -> list[str]:
    references: list[str] = []
    roots = (Path("src/app"), Path("tests"), Path("scripts"), Path("experiments"))
    for path in (path for root in roots for path in root.rglob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == (
                "app.domains.experiments.application.ports"
            ):
                references.append(f"{path}:{node.lineno}:import")
            if isinstance(node, ast.arg) and node.annotation is not None:
                if DELETED_EXPERIMENT_PORT in ast.unparse(node.annotation):
                    references.append(f"{path}:{node.lineno}:annotation")
    return references


def test_application_protocols_have_a_ten_member_ceiling() -> None:
    oversized: list[str] = []
    for path in _application_files():
        for protocol in _protocol_classes(path):
            size = len(_public_members(protocol))
            if size > PROTOCOL_METHOD_LIMIT:
                oversized.append(f"{path}:{protocol.name}={size}")
    assert oversized == []


def test_experiment_mega_port_and_its_imports_are_deleted() -> None:
    assert not DELETED_EXPERIMENT_PORT_PATH.exists()
    assert _deleted_experiment_port_references() == []


def test_experiment_dashboard_roles_are_caller_owned() -> None:
    for path in EXPERIMENT_DASHBOARD_PROTOCOL_FILES:
        for protocol in _protocol_classes(path):
            assert len(protocol.bases) == 1, f"{path}:{protocol.name} must be caller-owned"
            base = protocol.bases[0]
            assert isinstance(base, ast.Name) and base.id == "Protocol"


def test_experiment_dashboard_routes_inject_application_roles() -> None:
    routes = ast.parse(Path("src/app/domains/experiments/api/routes.py").read_text())
    found: set[str] = set()
    for node in routes.body:
        if not isinstance(node, ast.AsyncFunctionDef):
            continue
        if node.name not in EXPERIMENT_DASHBOARD_ROUTE_HANDLERS:
            continue
        found.add(node.name)
        annotations = [
            argument.annotation
            for argument in [*node.args.args, *node.args.kwonlyargs]
            if argument.annotation is not None
        ]
        assert all("ExperimentRepository" not in ast.unparse(value) for value in annotations)
    assert found == EXPERIMENT_DASHBOARD_ROUTE_HANDLERS


def test_evaluation_experiment_statistics_role_has_a_responsibility_name() -> None:
    path = Path("src/app/domains/evaluation/application/experiment_statistics.py")
    class_names = {
        node.name
        for node in ast.parse(path.read_text(), filename=str(path)).body
        if isinstance(node, ast.ClassDef)
    }
    assert "ExperimentStatisticsReader" in class_names
    assert "ExperimentStatisticsExperiments" not in class_names


def test_experiment_store_exposes_worker_roles_not_a_repository() -> None:
    path = Path("src/app/domains/experiments/application/store.py")
    store = _class_definition(path, "ExperimentStore")
    members = {member.name for member in _public_members(store)}
    assert "experiments" not in members
    assert {
        "condition_recovery",
        "condition_runs",
        "execution_lifecycle",
        "execution_progress",
        "focal_cases",
        "h1_inputs",
        "h2_inputs",
    } <= members


def test_dead_experiment_read_apis_are_absent() -> None:
    repository_methods = {
        member.name
        for member in _public_members(
            _class_definition(EXPERIMENT_REPOSITORY_PATH, "ExperimentRepository")
        )
    }

    assert DEAD_EXPERIMENT_READ_APIS.isdisjoint(repository_methods)


def test_evaluation_protocols_do_not_inherit_other_protocols() -> None:
    paths = sorted(EVALUATION_ROOT.glob("**/*.py"))
    protocol_names = {protocol.name for path in paths for protocol in _protocol_classes(path)}
    for path in paths:
        for protocol in _protocol_classes(path):
            assert len(protocol.bases) == 1, f"{path}:{protocol.name} must be caller-owned"
            base = protocol.bases[0]
            assert isinstance(base, ast.Name) and base.id == "Protocol"
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            inherited_protocols = {
                base.id
                for base in node.bases
                if isinstance(base, ast.Name) and base.id in protocol_names
            }
            assert inherited_protocols == set(), (
                f"{path}:{node.name} inherits shared protocols {inherited_protocols}"
            )


def test_transaction_capability_is_exposed_only_by_stores() -> None:
    for path in _application_files():
        for protocol in _protocol_classes(path):
            members = {member.name for member in _public_members(protocol)}
            owns_commit = "commit" in members or "rollback" in members
            if owns_commit:
                assert protocol.name.endswith("Store"), f"{path}:{protocol.name}"
                assert {"commit", "rollback"} <= members, f"{path}:{protocol.name}"


def test_public_application_vocabulary_uses_store_not_transaction_jargon() -> None:
    banned = ("uow", "unitofwork", "transaction")
    violations: list[str] = []
    for path in _application_files():
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                if not node.name.startswith("_"):
                    normalized = node.name.lower().replace("_", "")
                    if any(term in normalized for term in banned):
                        violations.append(f"{path}:{node.name}")
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                    arguments = [
                        *node.args.posonlyargs,
                        *node.args.args,
                        *node.args.kwonlyargs,
                    ]
                    for argument in arguments:
                        normalized = argument.arg.lower().replace("_", "")
                        if any(term in normalized for term in banned):
                            violations.append(f"{path}:{node.name}({argument.arg})")
    assert violations == []


def test_evaluation_protocol_names_describe_roles() -> None:
    violations = [
        f"{path}:{protocol.name}"
        for path in sorted(EVALUATION_ROOT.glob("**/*.py"))
        for protocol in _protocol_classes(path)
        if protocol.name.endswith(("Persistence", "RepositoryPort"))
    ]
    assert violations == []


def test_application_modules_and_classes_are_not_named_helper() -> None:
    violations: list[str] = []
    for path in _application_files():
        if "helper" in path.stem.lower():
            violations.append(str(path))
        tree = ast.parse(path.read_text(), filename=str(path))
        violations.extend(
            f"{path}:{node.name}"
            for node in tree.body
            if isinstance(node, ast.ClassDef) and "helper" in node.name.lower()
        )
    assert violations == []


def test_sqlalchemy_evaluation_store_has_no_unconstrained_public_surface() -> None:
    store_protocols: tuple[type[Protocol], ...] = (
        RatingSubmissionStore,
        RatingImportStore,
        RaterRegistrationStore,
        AssignmentStore,
        AuditItemBuildStore,
        AuditRatingStore,
    )
    expected = {
        name
        for protocol in store_protocols
        for name, value in protocol.__dict__.items()
        if not name.startswith("_") and (inspect.isfunction(value) or isinstance(value, property))
    }
    actual = {
        name
        for name, value in SqlAlchemyEvaluationStore.__dict__.items()
        if not name.startswith("_") and (inspect.isfunction(value) or isinstance(value, property))
    }
    assert actual == expected
