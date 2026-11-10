"""Type-erasure casts are forbidden in production code and tests."""

from __future__ import annotations

import ast
from pathlib import Path

BACKEND_ROOT = Path(__file__).parents[1]
IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}


def _erases_type_information(path: Path) -> list[int]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    cast_names: set[str] = set()
    any_names: set[str] = set()
    typing_namespaces: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in {"typing", "typing_extensions"}:
            for imported in node.names:
                local_name = imported.asname or imported.name
                if imported.name == "cast":
                    cast_names.add(local_name)
                elif imported.name == "Any":
                    any_names.add(local_name)
        elif isinstance(node, ast.Import):
            for imported in node.names:
                if imported.name in {"typing", "typing_extensions"}:
                    typing_namespaces.add(imported.asname or imported.name)

    offenders: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        direct_cast = isinstance(node.func, ast.Name) and node.func.id in cast_names
        namespaced_cast = (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "cast"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in typing_namespaces
        )
        if not (direct_cast or namespaced_cast):
            continue

        target = node.args[0]
        direct_any = isinstance(target, ast.Name) and target.id in any_names
        namespaced_any = (
            isinstance(target, ast.Attribute)
            and target.attr == "Any"
            and isinstance(target.value, ast.Name)
            and target.value.id in typing_namespaces
        )
        if direct_any or namespaced_any:
            offenders.append(node.lineno)
    return offenders


def test_cast_to_any_is_forbidden() -> None:
    offenders: list[str] = []
    for path in BACKEND_ROOT.rglob("*.py"):
        if any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue
        offenders.extend(
            f"{path.relative_to(BACKEND_ROOT)}:{line}" for line in _erases_type_information(path)
        )
    assert offenders == [], "cast(Any, ...) disables type checking:\n" + "\n".join(offenders)
