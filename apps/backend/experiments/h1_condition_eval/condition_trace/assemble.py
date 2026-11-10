"""The exact inputs a condition sends, paired with the output it produced.

The inputs are not reconstructed here. ``ComposeSection.inputs`` is the method the
generator itself calls, and it is called here with the same request, so what this
renders and what the model received cannot drift apart. Reconstructing the payload
would produce a document that is right the day it is written and quietly wrong
afterwards, which for an appendix about what the model was given is worse than no
document at all.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    ComposeSection,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

CONDITIONS = (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3)

# Identifiers, dropped from every payload by design. Listing them as withheld
# content would bury the fields that actually carry teaching under record-keeping.
UNIT_RECORD_FIELDS = frozenset({"unit_id", "lesson_objective_id", "source_step_id"})

CONDITION_INTENT = {
    "C0": "The curriculum objective alone. No lesson plan, no note.",
    "C1": "The objective plus the lesson plan's design: position, method labels, "
    "materials, entry behaviour and assessment.",
    "C2": "C1 plus the lesson note as source evidence.",
    "C3": "C2 plus a validation and repair pass over the draft.",
}


@dataclass(frozen=True)
class UnitTrace:
    objective_id: str
    objective_text: str
    inputs: dict
    attachable: dict
    withheld: tuple[str, ...]
    section: dict

    @property
    def probe_view(self) -> dict:
        """Payload plus the channels a tool can reach, for layer presence only.

        Kept separate from ``inputs`` so the rendered payload stays exactly what
        the contract declares — an appendix that quietly folded tool-reachable
        content into the prompt fields would misreport the thing it exists to show.
        """
        return {**self.inputs, "attachable": self.attachable}


@dataclass(frozen=True)
class ConditionTrace:
    lesson: str
    condition: str
    intent: str
    contract: str
    input_fields: tuple[str, ...]
    lesson_context: dict
    units: tuple[UnitTrace, ...]

    @property
    def sections(self) -> list[dict]:
        return [unit.section for unit in self.units if unit.section]


def _composer() -> ComposeSection:
    # ``inputs`` and ``contract`` read only ``contract_mode`` and ``source_tools``.
    # clean-six ran compose-v2, which passes no source tools, so the leveled
    # contract is what shaped every case in the run being traced.
    return ComposeSection(lm=cast("dspy.BaseLM", None), contract_mode="leveled")


def _withheld(unit: SectionGenerationUnit, payload: dict) -> tuple[str, ...]:
    """Unit fields the contract did not carry, so an absent layer reads as absent.

    A key missing from the payload and a key present but empty are different facts
    about a condition, and the payload alone shows only the second. Naming the
    first keeps the page honest without printing fields the model never saw as
    though it saw them blank.
    """
    sent = set(payload.get("unit_context") or {})
    return tuple(
        name
        for name in type(unit).model_fields
        if name not in sent and name not in UNIT_RECORD_FIELDS
    )


def _sections_of(case: dict) -> list[dict]:
    raw = case.get("sections_json")
    parsed = json.loads(raw) if isinstance(raw, str) else raw
    return list(parsed or [])


def load_plans() -> dict[str, SessionPlanView]:
    cases = json.loads(Path(EVAL_SET_PATH).read_text())["cases"]
    return {case["lesson"]: SessionPlanView.model_validate(case["plan"]) for case in cases}


def load_outputs(run: Path, repeat: int = 1) -> dict[tuple[str, str], list[dict]]:
    """One draw per lesson/condition — the trace is about layers, not variance."""
    cases = json.loads(run.read_text())["cases"]
    chosen: dict[tuple[str, str], list[dict]] = {}
    for case in cases:
        if case.get("repeat", 1) != repeat:
            continue
        chosen.setdefault((case["lesson"], case["condition"]), _sections_of(case))
    return chosen


def build(lesson: str, plan: SessionPlanView, outputs: dict) -> list[ConditionTrace]:
    composer = _composer()
    traces: list[ConditionTrace] = []
    for code in CONDITIONS:
        profile = profile_for(Hypothesis.H1, code)
        request = BaseReviewPackRequestBuilder().build(
            session_plan=plan,
            policy=profile.generation_policy(),
            sources=LessonSources.unresolved(plan.references),
        )
        contract = composer.contract(request)
        sections = outputs.get((lesson, code.value), [])
        by_objective = {s.get("lesson_objective_id"): s for s in sections}
        units = tuple(
            UnitTrace(
                objective_id=str(unit.lesson_objective_id),
                objective_text=unit.objective_text or "",
                inputs=composer.inputs(request, unit, contract),
                attachable={
                    "source_figures": [f.model_dump() for f in unit.source_figures],
                },
                withheld=_withheld(unit, composer.inputs(request, unit, contract)),
                section=by_objective.get(unit.lesson_objective_id) or {},
            )
            for unit in request.units
        )
        traces.append(
            ConditionTrace(
                lesson=lesson,
                condition=code.value,
                intent=CONDITION_INTENT[code.value],
                contract=contract.__name__,
                input_fields=tuple(contract.input_fields),
                lesson_context=units[0].inputs.get("lesson_context", {}) if units else {},
                units=units,
            )
        )
    return traces
