"""Decide whether an application callable is a transport-neutral operation.

The shape the boundary rule asks for is one immutable input, one explicit output, and
collaborators bound when the operation is constructed. Anything a caller has to supply
per call other than that single input is the caller doing the wiring, so this reads the
source and names each departure rather than returning a bare verdict.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

from tests.mechanism_types import import_origins, mechanism_types


@dataclass(frozen=True)
class OperationShape:
    """Why one application callable does or does not satisfy the boundary rule."""

    symbol: str
    location: str
    reasons: tuple[str, ...]

    @property
    def conforms(self) -> bool:
        return not self.reasons


def _per_call_parameters(
    node: ast.FunctionDef | ast.AsyncFunctionDef, *, skip_self: bool
) -> list[ast.arg]:
    positional = [*node.args.posonlyargs, *node.args.args]
    if skip_self:
        positional = positional[1:]
    return [*positional, *node.args.kwonlyargs]


def _input_reasons(
    node: ast.FunctionDef | ast.AsyncFunctionDef, origins: dict[str, str], *, skip_self: bool
) -> list[str]:
    parameters = _per_call_parameters(node, skip_self=skip_self)
    if len(parameters) != 1:
        reasons = [f"takes {len(parameters)} per-call parameters; an operation takes one input"]
    else:
        reasons = []
    for parameter in parameters:
        if parameter.annotation is None:
            reasons.append(f"parameter '{parameter.arg}' is unannotated")
            continue
        reasons.extend(
            f"parameter '{parameter.arg}' carries {found}"
            for found in mechanism_types(parameter.annotation, origins)
        )
    return reasons


def _output_reasons(
    node: ast.FunctionDef | ast.AsyncFunctionDef, origins: dict[str, str]
) -> list[str]:
    if node.returns is None:
        return ["has no return annotation"]
    rendered = ast.unparse(node.returns)
    if rendered in {"None", "object"}:
        return [f"returns {rendered}; an operation returns an explicit output"]
    return [f"output carries {found}" for found in mechanism_types(node.returns, origins)]


def _construction_reasons(node: ast.ClassDef, origins: dict[str, str]) -> list[str]:
    initialiser = next(
        (
            member
            for member in node.body
            if isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef)
            and member.name == "__init__"
        ),
        None,
    )
    if initialiser is None:
        return []
    return [
        f"collaborator '{parameter.arg}' carries {found}"
        for parameter in _per_call_parameters(initialiser, skip_self=True)
        if parameter.annotation is not None
        for found in mechanism_types(parameter.annotation, origins)
    ]


def _is_protocol(node: ast.ClassDef) -> bool:
    return any(isinstance(base, ast.Name) and base.id == "Protocol" for base in node.bases)


def _class_shape(node: ast.ClassDef, path: Path, origins: dict[str, str]) -> OperationShape:
    call = next(
        (
            member
            for member in node.body
            if isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef)
            and member.name == "__call__"
        ),
        None,
    )
    if _is_protocol(node):
        reasons = ["is a Protocol; it describes a collaborator, not an operation"]
    elif call is None:
        reasons = ["defines no __call__; an operation is invoked as one callable"]
    else:
        reasons = [
            *_input_reasons(call, origins, skip_self=True),
            *_output_reasons(call, origins),
            *_construction_reasons(node, origins),
        ]
    return OperationShape(node.name, f"{path}:{node.lineno}", tuple(reasons))


def operation_shape(path: Path, symbol: str) -> OperationShape:
    """Read ``symbol`` from ``path`` and report every departure from the operation shape."""
    tree = ast.parse(path.read_text(), filename=str(path))
    origins = import_origins(path)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == symbol:
            return _class_shape(node, path, origins)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == symbol:
            reasons = (
                *_input_reasons(node, origins, skip_self=False),
                *_output_reasons(node, origins),
            )
            return OperationShape(symbol, f"{path}:{node.lineno}", reasons)
    raise AssertionError(f"{symbol} not found in {path}")
