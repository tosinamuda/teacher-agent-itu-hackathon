"""api/ transport never imports ORM models AT RUNTIME (#10 / Rule for api ↛ models).

The transport layer's job is to convert HTTP <-> domain DTOs. The route may
shape an ORM row into a response DTO (the ``_summary``/``_response`` private
helpers in several routes do this), but it must do so without taking a
**runtime** dependency on the ORM class. Type-only annotations under
``if TYPE_CHECKING:`` are fine — the type-checker needs them, the runtime
graph doesn't.

Why this test instead of an import-linter contract
--------------------------------------------------

import-linter parses imports at the AST level — it sees ``if TYPE_CHECKING:``
blocks the same as top-level imports and would flag legitimate type-only
hoists. This test walks each api/ file's AST and only counts top-level
imports, ignoring ``if TYPE_CHECKING:``-gated ones.

The complementary contract ``api transport does not directly import
peer-domain code`` lives in pyproject.toml — that one IS expressible via
import-linter because the question (peer-domain coupling) doesn't depend on
runtime vs type-only.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from scripts.layer_paths import api_files

pytestmark = pytest.mark.architecture

_BACKEND_DIR = Path(__file__).resolve().parents[1]

# Every ORM-models module across domains. Forbidden as a runtime import from
# any api/ file.
_FORBIDDEN_MODEL_PACKAGES = (
    "app.domains.artefact_revision.models",
    "app.domains.artefacts.core.infrastructure.models",
    "app.domains.artefacts.types.lesson_plan.infrastructure.models",
    "app.domains.artefacts.types.post_class_review_pack.infrastructure.models",
    "app.domains.assessments.models",
    "app.domains.curriculum.models",
    "app.domains.evaluation.infrastructure.models",
    "app.domains.experiments.infrastructure.models",
    "app.domains.expert_content.models",
    "app.domains.learners.models",
    "app.domains.school.models",
    "app.domains.teaching.models",
    "app.domains.users.models",
)


def _api_files() -> list[Path]:
    """Every *.py under any app/domains/**/api/ tree, package markers aside."""
    return [path for path in api_files() if path.name != "__init__.py"]


def _is_in_type_checking_block(node: ast.AST, tree: ast.Module) -> bool:
    """True iff ``node`` is nested under ``if TYPE_CHECKING:``."""
    for parent in ast.walk(tree):
        if not isinstance(parent, ast.If):
            continue
        test = parent.test
        is_type_checking = (isinstance(test, ast.Name) and test.id == "TYPE_CHECKING") or (
            isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING"
        )
        if not is_type_checking:
            continue
        for stmt in ast.walk(parent):
            if stmt is node:
                return True
    return False


def _runtime_model_imports(file_path: Path) -> list[tuple[int, str]]:
    """Imports of forbidden model packages that AREN'T under ``if TYPE_CHECKING:``."""
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    violations: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module is None:
            continue
        if not any(node.module.startswith(pkg) for pkg in _FORBIDDEN_MODEL_PACKAGES):
            continue
        if _is_in_type_checking_block(node, tree):
            continue
        violations.append((node.lineno, node.module))
    return violations


@pytest.mark.parametrize("api_file", _api_files(), ids=lambda p: str(p.relative_to(_BACKEND_DIR)))
def test_api_file_does_not_runtime_import_orm_models(api_file: Path) -> None:
    violations = _runtime_model_imports(api_file)
    assert not violations, (
        f"{api_file.relative_to(_BACKEND_DIR)} runtime-imports ORM models:\n"
        + "\n".join(f"  line {line}: from {mod} ..." for line, mod in violations)
        + "\n\nApi transport must not depend on ORM at runtime. Either:\n"
        "  (a) move the import inside ``if TYPE_CHECKING:`` if used only for "
        "type annotations,\n"
        "  (b) move the converter helper to ``application/`` if it needs the ORM "
        "at runtime, or\n"
        "  (c) take a Pydantic schema / Protocol intermediate instead of the ORM type."
    )
