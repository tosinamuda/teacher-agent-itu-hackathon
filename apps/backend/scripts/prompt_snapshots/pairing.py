"""Put each generated section beside the exact inputs that produced it.

A claim about why an arm differs needs both halves. The runs record what came back and the
metrics computed on it; what went in was never kept, so a maths error or an ungrounded claim
could be read but not explained.

Rebuilt rather than replayed, and rebuilt from the RUN'S OWN record: `run.json` stores the
plan it used per lesson and the arm it used per case, so the pairing reconstructs the call
that arm would make rather than the call today's default would. That distinction is not
cosmetic — the judged C0-C3 run used `compose-v2` with leveled contracts, and the committed
snapshots pin `packed` with the shared contract, so pairing through the default would have
described a call that run never made.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    ComposeSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.config import RUNS_DIR
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from scripts.prompt_snapshots.arms import _UncallableLM

#: Lesson versions a recorded run was built against that ``eval_set.json`` has
#: since moved past. See ``experiments/h1_condition_eval/frozen/README.md``.
FROZEN_DIR = RUNS_DIR.parent / "frozen"

COMPOSING_ARMS = {"compose", "compose-v2", "compose-reader"}

ContractFor = Callable[[ReviewPackRequest], type]
"""Builds the signature an arm sends for a request."""
InputsFor = Callable[[ReviewPackRequest, SectionGenerationUnit, type], dict[str, Any]]
"""Builds the values an arm fills that signature with."""


@dataclass(frozen=True)
class Pair:
    """One section, and the call that produced it."""

    lesson: str
    condition: str
    arm: str
    unit_id: str
    contract: str
    inputs: dict
    section: dict
    findings: list[str]

    @property
    def objective(self) -> str:
        return str(self.section.get("lesson_objective_id") or "")


def run_path(label: str) -> Path:
    return RUNS_DIR / label / "run.json"


def pairs(label: str) -> list[Pair]:
    """Every recorded section in a run, beside the inputs its call was given."""
    record = json.loads(run_path(label).read_text(encoding="utf-8"))
    plans = _plans_as_run_saw_them(record)
    found: list[Pair] = []
    for case in record["cases"]:
        if not case.get("sections_json"):
            continue
        found += _case_pairs(case, plans[case["lesson"]])
    return found


def _superseded(lesson: str, digest: str) -> dict | None:
    """The archived version of a lesson a run recorded, if the corpus moved on.

    Correcting a lesson would otherwise orphan every run before it: the digest a
    run recorded stops resolving and its prompts can never be rebuilt. The
    archive keeps the version it saw, so the refusal below still fires for a
    plan nobody kept and not for one that was deliberately superseded.
    """
    path = FROZEN_DIR / f"{lesson}-{digest}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _plans_as_run_saw_them(record: dict) -> dict[str, SessionPlanView]:
    """The frozen plans, checked against the hashes this run recorded.

    A run stores the content hash of each plan it used. Rebuilding a prompt against a plan
    that has since been re-frozen would pair a response with inputs it never saw, so the
    mismatch is refused rather than reported.
    """
    frozen = json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))["cases"]
    by_lesson = {case["lesson"]: case for case in frozen}
    plans = {}
    for lesson, digest in record["plans"].items():
        case = by_lesson.get(lesson)
        if case is None:
            raise ValueError(f"{lesson} ran in this experiment and is not in the frozen set")
        if case["plan_sha256"] != digest:
            case = _superseded(lesson, digest) or case
        if case["plan_sha256"] != digest:
            raise ValueError(
                f"{lesson} has been re-frozen since this run: "
                f"recorded {digest}, eval set now {case['plan_sha256']}"
            )
        plans[lesson] = SessionPlanView.model_validate(case["plan"])
    return plans


def _case_pairs(case: dict, plan: SessionPlanView) -> list[Pair]:
    request = _request(plan, ConditionCode(case["condition"]), figures=case.get("figures"))
    contract, inputs_for = _arm(case)
    sections = case["sections_json"]
    return [
        Pair(
            lesson=case["lesson"],
            condition=case["condition"],
            arm=case.get("generator", "?"),
            unit_id=unit.unit_id,
            contract=contract(request).__name__,
            inputs=inputs_for(request, unit, contract(request)),
            section=section,
            findings=list(case.get("findings_text") or []),
        )
        for unit, section in zip(request.units, sections, strict=False)
    ]


def _request(
    plan: SessionPlanView, condition: ConditionCode, *, figures: str | None
) -> ReviewPackRequest:
    builder = BaseReviewPackRequestBuilder(figures=figures or "reference")  # type: ignore[arg-type]
    return builder.build(
        session_plan=plan,
        policy=profile_for(Hypothesis.H1, condition).generation_policy(),
        sources=LessonSources.unresolved(plan.references),
    )


def _arm(case: dict[str, Any]) -> tuple[ContractFor, InputsFor]:
    """The contract and input builders belonging to the arm this case recorded."""
    mode = case.get("signatures", "shared")
    if case.get("generator") in COMPOSING_ARMS:
        composer = ComposeSection(lm=_UncallableLM(), contract_mode=mode)
        return composer.contract, composer.inputs
    generator = GenerateSection(lm=_UncallableLM(), contract_mode=mode)

    def contract(request: ReviewPackRequest) -> type:
        return generator.prepared_call(request=request, unit=request.units[0]).contract

    def inputs(
        request: ReviewPackRequest, unit: SectionGenerationUnit, _contract: type
    ) -> dict[str, Any]:
        return generator.prepared_call(request=request, unit=unit).inputs

    return contract, inputs


def pairing_dir(label: str) -> Path:
    return RUNS_DIR / label / "prompt-response-pairs"


def _section_text(section: dict) -> str:
    parts = [f"**{section.get('title') or '(no title)'}**", ""]
    for block in section.get("blocks") or []:
        parts += [f"_{block.get('block_type')}_: {block.get('text') or ''}", ""]
    for item in section.get("practice") or []:
        parts += [f"_practice_: {item.get('prompt')}  →  {item.get('answer')}", ""]
    return "\n".join(parts)


def pair_document(label: str, lesson: str, condition: str, found: list[Pair]) -> str:
    """One lesson-condition, every call: inputs on the left of what came back."""
    head = [
        f"# {lesson} · {condition} · run `{label}`",
        "",
        "Generated by `uv run python -m scripts.prompt_snapshots.pairing` — do not edit.",
        "Inputs are rebuilt through the arm this run recorded, against the plan whose hash it",
        "recorded, so what is printed is what that call was given.",
        "",
        f"Arm: `{found[0].arm}` · contract: `{found[0].contract}`",
        "",
    ]
    if found[0].findings:
        head += ["## Critic findings on this pack", ""]
        head += [f"- {finding}" for finding in found[0].findings] + [""]
    for pair in found:
        head += [
            f"## {pair.unit_id}",
            "",
            "### Given",
            "",
            "```json",
            json.dumps(pair.inputs, indent=2, default=str),
            "```",
            "",
            "### Returned",
            "",
            _section_text(pair.section),
            "",
        ]
    return "\n".join(head)


def write_pairs(label: str) -> list[Path]:
    """One document per lesson and condition, beside the run they belong to."""
    grouped: dict[tuple[str, str], list[Pair]] = {}
    for pair in pairs(label):
        grouped.setdefault((pair.lesson, pair.condition), []).append(pair)
    target = pairing_dir(label)
    target.mkdir(parents=True, exist_ok=True)
    written = []
    for (lesson, condition), found in sorted(grouped.items()):
        path = target / f"{lesson}-{condition}.md"
        path.write_text(pair_document(label, lesson, condition, found), encoding="utf-8")
        written.append(path)
    return written


def main() -> int:
    import sys

    label = sys.argv[1] if len(sys.argv) > 1 else "c0c3-worksheet"
    written = write_pairs(label)
    print(f"wrote {len(written)} documents to {pairing_dir(label)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
