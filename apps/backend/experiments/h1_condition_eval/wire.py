"""What a condition actually sends over the wire, captured rather than reconstructed.

``fingerprints.py`` hashes the pieces — instructions, tools, sampling, the spec.
``dump_inputs.py`` renders the input objects. Neither is the request: the adapter
assembles the system and user messages, converts the tool list to function
schemas, deletes the tool fields from the signature it renders, and may add
native-feature kwargs, and each of those is a place a difference can live that no
component hash sees.

So this reads the request at the one point it is fully assembled: a stand-in LM
that records the first call and stops. What it records is byte-for-byte what
``dspy.LM.forward`` would have handed to litellm, under the same configuration the
run uses, because it is the same code path up to that call.

The use is equivalence. When one arm's payload is meant to be the only difference
between two runs, this shows whether that is true — per unit, with the differing
message spans — rather than asserting it from the policy that was intended.

    uv run python -m experiments.h1_condition_eval.wire --variant v3 --variant v4-activities
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    ComposeSection,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.policies import ConditionProfile
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant
from app.infra.dspy_lm import build_dspy_lm
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "wire"

# Keys left out of the fingerprint. Caching and retries are client-side and never
# reach the provider. The key is a secret: it authenticates the request without
# being part of it, and a fingerprint file that carried it would be a credential
# on disk in a tracked directory.
NOT_ON_THE_WIRE = frozenset({"cache", "num_retries", "cache_in_memory", "callbacks", "api_key"})


class Captured(Exception):  # noqa: N818 — a control-flow signal, deliberately not an error
    """Raised by the stand-in LM once the first request is recorded."""


@dataclass
class WireRequest:
    model: str
    messages: list[dict[str, Any]]
    kwargs: dict[str, Any]

    def body(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "messages": self.messages,
            "kwargs": {k: v for k, v in sorted(self.kwargs.items()) if k not in NOT_ON_THE_WIRE},
        }

    def canonical(self) -> str:
        return json.dumps(self.body(), sort_keys=True, ensure_ascii=False, default=str)

    def readable(self) -> str:
        """The same request, one line per value, so a diff lands on the changed field.

        Message content is split on its own newlines as well: a system message is
        one JSON string, and a diff that reports "the system message changed" has
        said nothing a reader can act on.
        """
        text = json.dumps(self.body(), sort_keys=True, ensure_ascii=False, default=str, indent=1)
        return text.replace("\\n", "\\n\n")

    def digest(self) -> str:
        return hashlib.sha256(self.canonical().encode()).hexdigest()[:16]

    @property
    def tools_in_prompt(self) -> bool:
        """Under the run's adapter, tools are rendered into the user message rather
        than sent as function schemas; the fingerprint covers them either way."""
        return "tools" not in self.kwargs and any(
            "[[ ## tools ## ]]" in str(m.get("content", "")) for m in self.messages
        )


class Wiretap(dspy.BaseLM):
    """Records the assembled request in place of sending it.

    Built from the run's real LM so that ``model`` and the call-level kwargs it
    carries — sampling, token limits, drop-params — merge into the recorded
    request exactly as ``dspy.LM.forward`` would merge them.
    """

    def __init__(self, real: dspy.LM) -> None:
        super().__init__(model=real.model, model_type=real.model_type, cache=False, **real.kwargs)
        self.recorded: WireRequest | None = None

    def _record(self, messages: list[dict[str, Any]] | None, kwargs: dict[str, Any]) -> None:
        merged = {**self.kwargs, **kwargs}
        self.recorded = WireRequest(self.model, list(messages or []), merged)
        raise Captured

    def forward(
        self,
        prompt: str | None = None,
        messages: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> Any:
        self._record(messages, kwargs)

    async def aforward(
        self,
        prompt: str | None = None,
        messages: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> Any:
        self._record(messages, kwargs)


@dataclass
class UnitWire:
    lesson: str
    condition: str
    objective_id: str
    request: WireRequest

    @property
    def digest(self) -> str:
        return self.request.digest()


@dataclass
class ArmWire:
    variant: str
    units: list[UnitWire] = field(default_factory=list)

    def by_key(self) -> dict[tuple[str, str, str], UnitWire]:
        return {(u.lesson, u.condition, u.objective_id): u for u in self.units}


async def _capture(composer: ComposeSection, request: Any, unit: Any) -> WireRequest:
    tap = composer.lm
    assert isinstance(tap, Wiretap)
    tap.recorded = None
    try:
        await composer.generate_section(request=request, unit=unit)
    except Captured:
        pass
    if tap.recorded is None:
        raise RuntimeError("the compose loop finished without calling the LM")
    return tap.recorded


async def render_arm(
    variant: str,
    *,
    plans: dict[str, SessionPlanView],
    conditions: tuple[ConditionCode, ...],
) -> ArmWire:
    """Every unit's first request under one context variant, as it would be sent."""
    profiles: dict[ConditionCode, ConditionProfile] = profiles_for_variant(variant)
    composer = ComposeSection(
        lm=Wiretap(build_dspy_lm()), contract_mode="leveled", loop=dspy.ReActV2
    )
    arm = ArmWire(variant)
    for lesson, plan in sorted(plans.items()):
        for code in conditions:
            request = BaseReviewPackRequestBuilder().build(
                session_plan=plan,
                policy=profiles[code].generation_policy(),
                sources=LessonSources.unresolved(plan.references),
            )
            for unit in request.units:
                wire = await _capture(composer, request, unit)
                arm.units.append(UnitWire(lesson, code.value, str(unit.lesson_objective_id), wire))
    return arm


FIELD_HEADER = re.compile(r"\[\[ ## ([a-z_]+) ## \]\]\n", re.I)


def _fields_in(messages: list[dict[str, Any]]) -> dict[str, Any]:
    """The adapter's own field blocks, parsed where they are JSON.

    The request is one string per message, and a field added to a unit's context
    lands wherever the model's field order puts it — usually in the middle. A
    text diff of that reports the whole shifted tail as removed-and-re-added,
    and a character-level one invents alignments inside the JSON. The adapter
    delimits its fields, so the honest comparison is per field, structural where
    the field is structured.
    """
    out: dict[str, Any] = {}
    for index, message in enumerate(messages):
        role = str(message.get("role", "?"))
        content = str(message.get("content", ""))
        parts = FIELD_HEADER.split(content)
        # Namespaced by MESSAGE, not by field name. The system message describes
        # `unit_context` and the user message carries its value, so a flat key let
        # the value overwrite the description and dropped most of the system
        # message from every comparison — a unit could differ with an empty diff.
        prefix = f"{role}[{index}]"
        if len(parts) == 1:
            out[prefix] = content
            continue
        out[f"{prefix}.preamble"] = parts[0]
        for name, body in zip(parts[1::2], parts[2::2], strict=True):
            body = body.strip()
            try:
                out[f"{prefix}.{name}" if role != "user" else name] = json.loads(body)
            except (ValueError, TypeError):
                out[f"{prefix}.{name}" if role != "user" else name] = body
    return out


def _diff_value(name: str, before: Any, after: Any) -> list[dict[str, Any]]:
    """One entry per difference, naming the key rather than the byte offset."""
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        out = []
        for key in sorted(set(before) | set(after)):
            if key not in before:
                out.append({"field": name, "key": key, "added": _short(after[key])})
            elif key not in after:
                out.append({"field": name, "key": key, "removed": _short(before[key])})
            elif before[key] != after[key]:
                out.append(
                    {
                        "field": name,
                        "key": key,
                        "removed": _short(before[key]),
                        "added": _short(after[key]),
                    }
                )
        return out
    return [{"field": name, "removed": _short(before), "added": _short(after)}]


def _short(value: Any, limit: int = 300) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    return text if len(text) <= limit else text[:limit] + "…"


def _span_diff(left: WireRequest, right: WireRequest) -> list[dict[str, Any]]:
    """Every difference between two requests, by name and key."""
    before, after = _fields_in(left.messages), _fields_in(right.messages)
    out: list[dict[str, Any]] = []
    for name in sorted(set(before) | set(after)):
        if name not in before:
            out.append({"field": name, "added": _short(after[name])})
        elif name not in after:
            out.append({"field": name, "removed": _short(before[name])})
        else:
            out += _diff_value(name, before[name], after[name])
    for key in sorted(set(left.body()["kwargs"]) | set(right.body()["kwargs"])):
        a, b = left.body()["kwargs"].get(key), right.body()["kwargs"].get(key)
        if a != b:
            out.append({"field": f"kwargs.{key}", "removed": _short(a), "added": _short(b)})
    return out


def compare(left: ArmWire, right: ArmWire) -> dict[str, Any]:
    """Per unit: identical, or the spans that differ. Missing units are named."""
    a, b = left.by_key(), right.by_key()
    rows = []
    for key in sorted(set(a) | set(b)):
        lesson, condition, objective = key
        if key not in a or key not in b:
            rows.append(
                {
                    "lesson": lesson,
                    "condition": condition,
                    "objective": objective,
                    "status": "only in " + (left.variant if key in a else right.variant),
                }
            )
            continue
        same = a[key].digest == b[key].digest
        row: dict[str, Any] = {
            "lesson": lesson,
            "condition": condition,
            "objective": objective,
            "status": "identical" if same else "differs",
            left.variant: a[key].digest,
            right.variant: b[key].digest,
        }
        if not same:
            row["diff"] = _span_diff(a[key].request, b[key].request)
        rows.append(row)
    return {"left": left.variant, "right": right.variant, "units": rows}


def _summary(comparison: dict[str, Any]) -> str:
    rows = comparison["units"]
    by_cond: dict[str, list[str]] = {}
    for r in rows:
        by_cond.setdefault(r["condition"], []).append(r["status"])
    lines = [f"  {comparison['left']} vs {comparison['right']}:"]
    for cond, statuses in sorted(by_cond.items()):
        ident = statuses.count("identical")
        lines.append(f"    {cond}: {ident}/{len(statuses)} units identical")
    return "\n".join(lines)


def _shown(path: Path) -> str:
    try:
        return str(path.relative_to(HERE))
    except ValueError:
        return str(path)


def load_plans() -> dict[str, SessionPlanView]:
    cases = json.loads(EVAL_SET_PATH.read_text())["cases"]
    return {c["lesson"]: SessionPlanView.model_validate(c["plan"]) for c in cases}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--variant",
        action="append",
        required=True,
        help="a context variant; give two or more to compare",
    )
    parser.add_argument("--conditions", nargs="*", default=["C0", "C1"])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    conditions = tuple(ConditionCode(c) for c in args.conditions)
    plans = load_plans()
    arms = [asyncio.run(render_arm(v, plans=plans, conditions=conditions)) for v in args.variant]

    args.out.mkdir(parents=True, exist_ok=True)
    for arm in arms:
        path = args.out / f"{arm.variant}.json"
        path.write_text(
            json.dumps(
                [
                    {
                        "lesson": u.lesson,
                        "condition": u.condition,
                        "objective": u.objective_id,
                        "digest": u.digest,
                        "request": u.request.body(),
                    }
                    for u in arm.units
                ],
                indent=1,
                ensure_ascii=False,
            )
        )
        print(f"  {_shown(path)}: {len(arm.units)} unit requests")

    for left, right in zip(arms, arms[1:], strict=False):
        comparison = compare(left, right)
        path = args.out / f"{left.variant}--vs--{right.variant}.json"
        path.write_text(json.dumps(comparison, indent=1, ensure_ascii=False))
        print(_summary(comparison))
        print(f"  {_shown(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
