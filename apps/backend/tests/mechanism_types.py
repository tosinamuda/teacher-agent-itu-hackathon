"""Tell which names in a type annotation come from a framework or an infrastructure module.

A boundary contract is judged by where its types are declared, not by how they are spelled,
so this resolves each name in an annotation back to the module the file imported it from.
"""

from __future__ import annotations

import ast
from functools import cache
from pathlib import Path

MECHANISM_PACKAGES = ("sqlalchemy", "fastapi", "starlette", "dspy")
MECHANISM_LAYER = ".infrastructure."


@cache
def import_origins(path: Path) -> dict[str, str]:
    """Map each imported name in ``path`` to the module it came from."""
    tree = ast.parse(path.read_text(), filename=str(path))
    origins: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                origins[alias.asname or alias.name] = node.module
        if isinstance(node, ast.Import):
            for alias in node.names:
                origins[alias.asname or alias.name.split(".")[0]] = alias.name
    return origins


def is_mechanism_module(origin: str) -> bool:
    """A module is a mechanism when it is a framework package or an infrastructure layer."""
    return MECHANISM_LAYER in origin or origin.split(".")[0] in MECHANISM_PACKAGES


def mechanism_types(annotation: ast.expr, origins: dict[str, str]) -> list[str]:
    """Name every mechanism type reachable from ``annotation``, with where it came from."""
    named = {node.id for node in ast.walk(annotation) if isinstance(node, ast.Name)}
    return sorted(
        f"{name} from {origins[name]}"
        for name in named
        if name in origins and is_mechanism_module(origins[name])
    )


def mechanism_types_in_source(annotation: str, origins: dict[str, str]) -> list[str]:
    """Same as :func:`mechanism_types` for an annotation already rendered back to source."""
    return mechanism_types(ast.parse(annotation, mode="eval").body, origins)
