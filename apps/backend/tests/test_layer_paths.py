"""No guard spells its own layer walk.

The census and the protocol architecture test each resolved the application layer with their
own glob, and one of them was wrong: `*/application/**` stops at a top-level domain and misses
every artefact type. Widening both patterns closed the instance; this closes the class.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from scripts.layer_paths import DOMAINS, LAYERS, application_files, layer_files

pytestmark = pytest.mark.architecture

_TESTS = Path(__file__).resolve().parent
_SCRIPTS = _TESTS.parent / "scripts"
# Owns the definition, so it is the one place allowed to name a layer directory in a glob.
_OWNER = _SCRIPTS / "layer_paths.py"


def _glob_literals(path: Path) -> list[str]:
    """Every string literal passed to `.glob(...)` or `.rglob(...)` in a module."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return [
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"glob", "rglob"}
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]


def test_the_layer_walk_has_one_owner() -> None:
    offenders: list[str] = []
    for path in sorted([*_TESTS.rglob("*.py"), *_SCRIPTS.rglob("*.py")]):
        if path == _OWNER:
            continue
        for pattern in _glob_literals(path):
            if any(f"{layer}/" in pattern for layer in LAYERS):
                offenders.append(f"{path.name}: {pattern!r}")
    assert offenders == [], (
        "these spell their own layer walk instead of importing `scripts.layer_paths`:\n  "
        + "\n  ".join(offenders)
    )


@pytest.mark.parametrize("layer", LAYERS)
def test_a_layer_walk_reaches_nested_subdomains(layer: str) -> None:
    """The bug that started this: a walk that stops one level down finds no artefact type."""
    reached = layer_files(layer)
    shallow = set(DOMAINS.glob(f"*/{layer}/**/*.py"))
    nested = [path for path in reached if path not in shallow]
    assert nested, f"no nested {layer}/ modules found — the walk regressed to one level"


def test_the_application_walk_covers_the_artefact_types() -> None:
    walked = {str(path.relative_to(DOMAINS)) for path in application_files()}
    for artefact_type in ("post_class_review_pack", "lesson_plan", "lesson_note"):
        assert any(f"{artefact_type}/application/" in path for path in walked), (
            f"{artefact_type} has application modules that no guard is walking"
        )
