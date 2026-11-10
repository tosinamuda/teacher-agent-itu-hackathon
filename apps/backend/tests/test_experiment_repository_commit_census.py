"""Ratchets for transaction debt in the experiment repository."""

from __future__ import annotations

import ast
from pathlib import Path

EXPERIMENT_REPOSITORY_PATH = Path("src/app/domains/experiments/infrastructure/repository.py")
DEAD_WRITE_APIS = {
    "save_experiment",
    "save_execution",
    "set_artefact_review_status",
    "set_experiment_plan_version",
    "update_execution",
    "update_experiment",
}


def _class_definition(path: Path, class_name: str) -> ast.ClassDef:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise AssertionError(f"{class_name} not found in {path}")


def _public_method_names(class_definition: ast.ClassDef) -> set[str]:
    return {
        node.name
        for node in class_definition.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("_")
    }


def _transaction_control_owners(class_definition: ast.ClassDef) -> list[tuple[str, str]]:
    owners: list[tuple[str, str]] = []
    for method in class_definition.body:
        if not isinstance(method, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        owners.extend(
            (method.name, node.func.attr)
            for node in ast.walk(method)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"commit", "rollback"}
        )
    return owners


def test_dead_experiment_write_apis_are_absent() -> None:
    repository_methods = _public_method_names(
        _class_definition(EXPERIMENT_REPOSITORY_PATH, "ExperimentRepository")
    )
    assert DEAD_WRITE_APIS.isdisjoint(repository_methods)


def test_experiment_repository_never_controls_transactions() -> None:
    transaction_control_owners = _transaction_control_owners(
        _class_definition(EXPERIMENT_REPOSITORY_PATH, "ExperimentRepository")
    )
    assert transaction_control_owners == []
