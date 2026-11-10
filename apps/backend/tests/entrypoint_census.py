"""Read transport entrypoints out of the source tree.

An entrypoint is anything that starts a use case from outside it: an HTTP handler, or a
job kind, whose handler the job queue calls. The census records what each one injects so a guard can
tell a thin transport adapter from a route that assembles the use case itself.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "websocket"})
AUTHENTICATION_DEPENDENCIES = frozenset({"requires", "get_actor"})

EXPERIMENTS_API = Path("src/app/domains/experiments/api")
EXPERIMENTS = "app.domains.experiments"


@dataclass(frozen=True)
class Entrypoint:
    """One transport-facing callable and the collaborators it is handed."""

    transport: str
    name: str
    location: str
    route: str
    collaborators: tuple[str, ...]
    annotations: tuple[str, ...]


def _parameters(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[tuple[ast.arg, ast.expr | None]]:
    positional = [*node.args.posonlyargs, *node.args.args]
    padding: list[ast.expr | None] = [None] * (len(positional) - len(node.args.defaults))
    pairs = list(zip(positional, [*padding, *node.args.defaults], strict=True))
    return pairs + list(zip(node.args.kwonlyargs, node.args.kw_defaults, strict=True))


def _dependency_name(default: ast.expr | None) -> str | None:
    """Name the provider behind ``Depends(provider)``, ignoring anything else."""
    if not isinstance(default, ast.Call) or not isinstance(default.func, ast.Name):
        return None
    if default.func.id != "Depends" or not default.args:
        return None
    target = default.args[0]
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Call) and isinstance(target.func, ast.Name):
        return target.func.id
    return ast.unparse(target)


def _collaborators(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    names = (_dependency_name(default) for _, default in _parameters(node))
    return tuple(
        name for name in names if name is not None and name not in AUTHENTICATION_DEPENDENCIES
    )


def _annotations(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    return tuple(
        ast.unparse(argument.annotation)
        for argument, _ in _parameters(node)
        if argument.annotation is not None
    )


def _router_prefixes(tree: ast.Module) -> dict[str, str]:
    prefixes: dict[str, str] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
            continue
        if not (isinstance(node.value.func, ast.Name) and node.value.func.id == "APIRouter"):
            continue
        prefix = next(
            (
                keyword.value.value
                for keyword in node.value.keywords
                if keyword.arg == "prefix" and isinstance(keyword.value, ast.Constant)
            ),
            "",
        )
        for target in node.targets:
            if isinstance(target, ast.Name):
                prefixes[target.id] = prefix
    return prefixes


def _http_route(decorator: ast.expr, prefixes: dict[str, str]) -> str | None:
    if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Attribute):
        return None
    if decorator.func.attr not in HTTP_METHODS:
        return None
    if not isinstance(decorator.func.value, ast.Name):
        return None
    prefix = prefixes.get(decorator.func.value.id, "")
    path = decorator.args[0].value if decorator.args else ""
    return f"{decorator.func.attr.upper()} {prefix}{path}"


def _functions(path: Path) -> tuple[ast.Module, list[ast.FunctionDef | ast.AsyncFunctionDef]]:
    tree = ast.parse(path.read_text(), filename=str(path))
    return tree, [
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    ]


def http_entrypoints(package: Path) -> list[Entrypoint]:
    """Every FastAPI handler declared under ``package``."""
    found: list[Entrypoint] = []
    for path in sorted(package.glob("*.py")):
        tree, functions = _functions(path)
        prefixes = _router_prefixes(tree)
        for node in functions:
            routes = (_http_route(decorator, prefixes) for decorator in node.decorator_list)
            route = next((value for value in routes if value is not None), None)
            if route is None:
                continue
            found.append(
                Entrypoint(
                    transport="http",
                    name=node.name,
                    location=f"{path}:{node.lineno}",
                    route=route,
                    collaborators=_collaborators(node),
                    annotations=_annotations(node),
                )
            )
    return found


def job_entrypoints(package: str) -> list[Entrypoint]:
    """Every job kind whose handler lives in ``package``; the job queue is its transport."""
    from app.infra.jobs.kinds import KINDS

    found: list[Entrypoint] = []
    for kind, job in sorted(KINDS.items()):
        module, function = job.handler.split(":")
        if not module.startswith(package):
            continue
        path = Path("src", module.replace(".", "/") + ".py")
        _tree, functions = _functions(path)
        node = next(node for node in functions if node.name == function)
        found.append(
            Entrypoint(
                transport="job",
                name=function,
                location=f"{path}:{node.lineno}",
                route=kind,
                collaborators=_collaborators(node),
                annotations=_annotations(node),
            )
        )
    return found


def experiments_entrypoints() -> list[Entrypoint]:
    """The full experiments transport surface: HTTP handlers and job kinds."""
    return http_entrypoints(EXPERIMENTS_API) + job_entrypoints(EXPERIMENTS)
