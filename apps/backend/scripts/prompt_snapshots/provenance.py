"""Trace each prompt field back to the code that filled it.

Read from the source, never typed out. A hand-kept map is right on the day it is written
and wrong on the first refactor, and the point of having one is to be able to say — for a
field that arrived empty in the frozen cohort — which step could have emptied it.

The chain has four links, and this walks the middle two:

    plan_versions.session_plan (JSON)     the store
      -> SessionPlanView.<attribute>      the parse
      -> <projector>(...) keyword         the extraction step, found here
      -> request schema field             the request builder, found here
      -> rendered prompt key              already pinned by field_map

Resolving a keyword means following what the code does with it: through local assignments,
through helper calls, and through parameters back to the argument each caller passes. A
field that reaches no plan attribute and no literal is reported as untraced, because a
prompt field with no source is a finding rather than an omission.
"""

from __future__ import annotations

import ast
import inspect
from dataclasses import dataclass
from types import ModuleType

from app.domains.artefacts.types.post_class_review_pack.application import learner_state_input
from app.domains.artefacts.types.post_class_review_pack.application.request import (
    evidence,
    lesson,
    units,
)

# Which module builds which request schema, and what the plan-shaped inputs are called in
# it. The names are the parameters the projector already declares, so a rename fails here.
BUILDERS: tuple[tuple[ModuleType, str, tuple[str, ...]], ...] = (
    (lesson, "LessonContextForGeneration", ("plan",)),
    (units, "SectionGenerationUnit", ("step", "objective", "plan")),
    (evidence, "SourceEvidenceItem", ("step", "source")),
    # H2's manipulation. Its roots are a different store entirely, which is why an H1 arm
    # showing a learner field would be a confound rather than a leak of degree.
    (learner_state_input, "SpecObjectiveLearnerState", ("state", "evidence")),
    (learner_state_input, "SessionSignals", ("survey", "learner_state")),
)

STORES = {
    "plan": "plan_versions.session_plan (JSON) -> SessionPlanView",
    "step": "plan_versions.session_plan['steps'][] -> SessionPlanStepView",
    "objective": (
        "plan_versions.session_plan['lesson_plan_objectives'][] -> LessonPlanObjectiveView"
    ),
    "source": "LessonSources — resolved textbook excerpts, or the plan's own citations",
    "state": "learner_state.ObjectiveLearnerState — classwork scores and the objective survey",
    "evidence": "learner_state answer evidence — the diagnostic items the learner missed",
    "survey": "learner_state.session_survey — the end-of-lesson survey answers",
    "learner_state": "learner_state.LearnerState — the focal learner's whole record",
}
"""What fills each root a value can read from. The first three are one JSON column parsed
three ways, so a plan absent from that payload empties every H1 field at once; the learner
roots are a different store, which is why an H1 arm reading one would be a confound."""

_MAX_HOPS = 6
"""How far to follow a value. Deep enough for parameter -> caller -> helper -> attribute;
a cap rather than a claim about the code's shape."""


@dataclass(frozen=True)
class FieldSource:
    """Where one request-schema field's value comes from."""

    schema: str
    field: str
    builder: str
    expression: str
    reads: tuple[str, ...]
    """Plan-shaped attributes the value reaches, e.g. ``step.note``."""
    literal: bool
    """True when the value resolves to something written in the code rather than read
    from the plan — a label, a constant, an empty default."""
    delegated_to: tuple[str, ...]
    """Collaborators this value is handed off to, for a field another projector fills."""

    @property
    def origin(self) -> str:
        if self.reads:
            return "traced"
        if self.delegated_to:
            return "delegated"
        return "literal" if self.literal else "untraced"


def field_sources() -> list[FieldSource]:
    """Every request-schema field, with the plan attributes that fill it."""
    found: list[FieldSource] = []
    for module, schema, roots in BUILDERS:
        tree = ast.parse(inspect.getsource(module))
        walker = _Walker(tree, roots)
        for call, enclosing in _calls_to(tree, schema):
            for keyword in call.keywords:
                if keyword.arg is None:
                    continue
                traced = walker.resolve(keyword.value, enclosing, keyword.arg)
                found.append(
                    FieldSource(
                        schema=schema,
                        field=keyword.arg,
                        builder=enclosing,
                        expression=ast.unparse(keyword.value),
                        reads=traced.reads,
                        literal=traced.literal,
                        delegated_to=traced.delegated_to,
                    )
                )
    return found


def untraced(sources: list[FieldSource]) -> list[FieldSource]:
    """Fields whose value this cannot account for — each one a finding."""
    return [source for source in sources if source.origin == "untraced"]


def stores_for(source: FieldSource) -> tuple[str, ...]:
    """The stores behind one field, named through the roots its value reads."""
    roots = {read.split(".", 1)[0] for read in source.reads}
    return tuple(sorted({STORES[root] for root in roots if root in STORES}))


def provenance_table() -> str:
    """The committed map: one row per request-schema field, derived from the source."""
    rows = ["| Field | Builder | Reads | Store | Origin |", "| --- | --- | --- | --- | --- |"]
    for source in field_sources():
        reads = ", ".join(f"`{read}`" for read in source.reads) or "—"
        stores = "<br>".join(stores_for(source)) or "—"
        delegated = "".join(f"<br>via `{name}`" for name in source.delegated_to)
        rows.append(
            f"| `{source.field}` | `{source.builder}` | {reads}{delegated} "
            f"| {stores} | {source.origin} |"
        )
    return "\n".join(rows)


@dataclass(frozen=True)
class Traced:
    """What following one value turned up."""

    reads: tuple[str, ...]
    literal: bool
    delegated_to: tuple[str, ...]


@dataclass(frozen=True)
class _Step:
    """One expression to follow, and the names bound around it."""

    node: ast.AST
    scope: str
    bound: tuple[tuple[str, _Step], ...] = ()

    def binding(self, name: str) -> _Step | None:
        return next((step for bound, step in self.bound if bound == name), None)


class _Walker:
    """Follows a value through one module: assignments, helpers, and parameters."""

    def __init__(self, tree: ast.Module, roots: tuple[str, ...]) -> None:
        self._roots = roots
        self._functions = {
            node.name: node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        }
        self._bindings = {name: _bindings(node) for name, node in self._functions.items()}
        self._module_bindings = _module_bindings(tree)
        self._arguments = _arguments(self._functions)

    def resolve(self, node: ast.AST, scope: str, field: str, hops: int = _MAX_HOPS) -> Traced:
        return self._follow(_Step(node, scope), field, hops)

    def _follow(self, step: _Step, field: str, hops: int) -> Traced:
        reads = {read for node in ast.walk(step.node) if (read := _root_read(node, self._roots))}
        literal = any(isinstance(node, ast.Constant) for node in ast.walk(step.node))
        delegated = _collaborators(step.node)
        if hops <= 0:
            return Traced(tuple(sorted(reads)), literal, tuple(sorted(delegated)))

        for deferred in self._deferred(step, field):
            deeper = self._follow(deferred, field, hops - 1)
            reads |= set(deeper.reads)
            literal = literal or deeper.literal
            delegated |= set(deeper.delegated_to)
        return Traced(tuple(sorted(reads)), literal, tuple(sorted(delegated)))

    def _deferred(self, step: _Step, field: str) -> list[_Step]:
        """Every expression this value defers to: locals, helper returns, caller arguments."""
        out: list[_Step] = []
        for inner in ast.walk(step.node):
            if isinstance(inner, ast.Name) and inner.id not in self._roots:
                out += self._for_name(inner.id, step)
            if isinstance(inner, ast.Call):
                out += self._for_call(inner, step, field)
        return out

    def _for_name(self, name: str, step: _Step) -> list[_Step]:
        """A local, then a module constant, then — with no call context — every caller."""
        bound = step.binding(name)
        if bound is not None:
            return [bound]
        local = self._bindings.get(step.scope, {}).get(name)
        if local is not None:
            return [_Step(local, step.scope, step.bound)]
        constant = self._module_bindings.get(name)
        if constant is not None:
            return [_Step(constant, step.scope)]
        return [_Step(node, caller) for node, caller in self._arguments.get((step.scope, name), [])]

    def _for_call(self, call: ast.Call, step: _Step, field: str) -> list[_Step]:
        """A helper's returns, with THIS call's arguments bound to its parameters.

        Binding per call rather than per callee is what stops every field that passes
        through a shared helper from claiming every attribute any caller ever passed it.
        """
        helper = self._functions.get(_called_name(call) or "")
        if helper is None:
            return []
        bound = _bind(helper, call, step)
        return [
            _Step(_keyword_for(node.value, field) or node.value, helper.name, bound)
            for node in ast.walk(helper)
            if isinstance(node, ast.Return) and node.value is not None
        ]


def _bindings(function: ast.FunctionDef) -> dict[str, ast.AST]:
    """Local name -> the expression it was last bound to, assignments and for-targets."""
    bound: dict[str, ast.AST] = {}
    for node in ast.walk(function):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                for name in _names(target):
                    bound[name] = node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            for name in _names(node.target):
                bound[name] = node.value
        elif isinstance(node, ast.For | ast.comprehension):
            for name in _names(node.target):
                bound[name] = node.iter
    return bound


def _module_bindings(tree: ast.Module) -> dict[str, ast.AST]:
    """Module-level constants, so a label like ``EVIDENCE_LABEL`` resolves to its text."""
    return {
        name: node.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        for name in _names(target)
    }


def _bind(helper: ast.FunctionDef, call: ast.Call, step: _Step) -> tuple[tuple[str, _Step], ...]:
    """This call's arguments, bound to the helper's parameter names."""
    bound: list[tuple[str, _Step]] = []
    for keyword in call.keywords:
        if keyword.arg:
            bound.append((keyword.arg, _Step(keyword.value, step.scope, step.bound)))
    for position, argument in enumerate(call.args):
        name = _positional(helper, position)
        if name:
            bound.append((name, _Step(argument, step.scope, step.bound)))
    return tuple(bound)


def _collaborators(node: ast.AST) -> set[str]:
    """Calls on an injected collaborator — a value another projector owns."""
    return {
        f"{call.func.value.attr}.{call.func.attr}"
        for call in ast.walk(node)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Attribute)
        and isinstance(call.func.value.value, ast.Name)
        and call.func.value.value.id == "self"
    }


def _arguments(
    functions: dict[str, ast.FunctionDef],
) -> dict[tuple[str, str], list[tuple[ast.AST, str]]]:
    """(callee, parameter) -> the expressions callers pass for it, with each caller's name."""
    passed: dict[tuple[str, str], list[tuple[ast.AST, str]]] = {}
    for caller in functions.values():
        for call in ast.walk(caller):
            if not isinstance(call, ast.Call):
                continue
            callee = functions.get(_called_name(call) or "")
            if callee is None:
                continue
            for keyword in call.keywords:
                if keyword.arg:
                    passed.setdefault((callee.name, keyword.arg), []).append(
                        (keyword.value, caller.name)
                    )
            for position, argument in enumerate(call.args):
                name = _positional(callee, position)
                if name:
                    passed.setdefault((callee.name, name), []).append((argument, caller.name))
    return passed


def _positional(function: ast.FunctionDef, position: int) -> str | None:
    names = [argument.arg for argument in function.args.args if argument.arg != "self"]
    return names[position] if position < len(names) else None


def _names(target: ast.AST) -> list[str]:
    return [node.id for node in ast.walk(target) if isinstance(node, ast.Name)]


def _root_read(node: ast.AST, roots: tuple[str, ...]) -> str | None:
    """``"<root>.<attr>"`` when this node reads an attribute off one of the roots."""
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id in roots
    ):
        return f"{node.value.id}.{node.attr}"
    return None


def _is_attribute_root(name: ast.Name, node: ast.AST) -> bool:
    """Whether this Name is only there as the base of an attribute access."""
    return any(
        isinstance(parent, ast.Attribute) and parent.value is name for parent in ast.walk(node)
    )


def _calls_to(tree: ast.Module, schema: str) -> list[tuple[ast.Call, str]]:
    """Every construction of ``schema``, with the function it sits in."""
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for inner in ast.walk(node):
            if isinstance(inner, ast.Call) and _called_name(inner) == schema:
                found.append((inner, node.name))
    return found


def _called_name(call: ast.Call) -> str | None:
    if isinstance(call.func, ast.Name):
        return call.func.id
    return call.func.attr if isinstance(call.func, ast.Attribute) else None


def _keyword_for(value: ast.AST, field: str) -> ast.AST | None:
    """The keyword of a returned constructor matching ``field``, if there is one."""
    if not isinstance(value, ast.Call):
        return None
    return next((kw.value for kw in value.keywords if kw.arg == field), None)
