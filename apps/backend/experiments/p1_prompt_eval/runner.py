"""Run a P1 personalise prompt over the frozen eval set.

By default this measures the CURRENT production prompt — the real path:
request builder + learner-state mapper + ``PersonaliseReviewPack``
(validator + repair included). A CANDIDATE prompt authored under
``experiments/`` runs via ``--variant module:SignatureClass`` (same
input/output fields as ``SectionPersonalisation``); compare it
against the production run before promoting it into production code — git is
the version history, the run label (signature-instructions hash) is the id.

Outputs land under ``runs/<label>/``: ``run.json`` (everything, prompts
included) and one readable ``cases/<case>.md`` per case for manual review.

Usage:
    cd apps/backend
    uv run python -m experiments.p1_prompt_eval.runner             # production
    uv run python -m experiments.p1_prompt_eval.runner \
      --variant experiments.my_prompt_idea.signature:PersonaliseV3  # candidate
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib
import json
from pathlib import Path

import dspy

import app.db.metadata  # noqa: F401  (DSPy generation imports pull ORM models)
from app.domains.artefacts.types.post_class_review_pack.application.learner_state_input import (
    to_session_signals,
    to_spec_objective_state,
)
from app.domains.artefacts.types.post_class_review_pack.application.personalise import (
    PersonaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSource,
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.personalise_section import (  # noqa: E501
    SectionPersonalisation,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CritiqueSections,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.repair_section import (
    RepairGeneratedSection,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.learner_state.domain.models import LearnerState
from app.infra.dspy_lm import build_dspy_lm
from app.shared.experiment_enums import Hypothesis
from app.shared.session_plan_view import SessionPlanView
from experiments.p1_prompt_eval.dataset import EVAL_SET_PATH
from experiments.run_folders import add_run_arguments, open_run

RUNS_DIR = Path(__file__).parent / "runs"


def label_for(signature: type[dspy.Signature]) -> str:
    """Hash of the signature's instruction block — the run's identity.

    Any prompt edit changes the hash, so two runs with different prompts can
    never silently share a label; git holds the history behind each hash.
    """
    digest = hashlib.sha256(str(signature.instructions).encode()).hexdigest()[:10]
    return f"p1-{digest}"


def load_variant(spec: str) -> object:
    """Resolve ``module.path:Attr`` to a candidate.

    The attr may be a ``dspy.Signature`` subclass (wrapped in the production
    ChainOfThought personaliser) or a zero-arg factory returning a personaliser
    object (``.lm`` + async ``personalise_section`` — e.g. a dspy.ReAct
    variant).
    """
    module_path, _, attr = spec.partition(":")
    return getattr(importlib.import_module(module_path), attr)


def resolve_personaliser(variant: object | None) -> PersonaliseSection:
    """Production personaliser, signature-swapped, or a full custom variant."""
    if variant is None:
        return PersonaliseSection(lm=build_dspy_lm())
    if isinstance(variant, type) and issubclass(variant, dspy.Signature):
        return PersonaliseSection(lm=build_dspy_lm(), contract=variant)
    return variant()  # factory for module-level variants (e.g. ReAct)


def _prompts_since(lm: dspy.LM, start: int) -> list[str]:
    rendered = []
    for entry in lm.history[start:]:
        messages = entry.get("messages") or []
        rendered.append("\n\n".join(f"[{m.get('role')}]\n{m.get('content')}" for m in messages))
    return rendered


def _usage_since(lm: dspy.LM, start: int) -> list[dict]:
    """Real token usage per LM call (provider-reported), for cost comparisons."""
    usage = []
    for entry in lm.history[start:]:
        raw = entry.get("usage") or {}
        usage.append(
            {
                "input_tokens": raw.get("prompt_tokens"),
                "output_tokens": raw.get("completion_tokens"),
            }
        )
    return usage


def _section_markdown(section: dict) -> str:
    lines = [f"#### {section.get('title', '')}"]
    for block in section.get("blocks", []):
        if block.get("text"):
            lines.append(f"*{block.get('block_type')}*\n\n{block['text']}")
    return "\n\n".join(lines)


async def run_case(service: PersonaliseReviewPack, case: dict) -> dict:
    learner_state = LearnerState.model_validate(case["learner_state"])
    spec_states = {
        s.lesson_objective_id: to_spec_objective_state(s) for s in learner_state.objective_states
    }
    base_sections = [ReviewPackSection.model_validate(section) for section in case["base_sections"]]
    prompt_start = len(service._personaliser.lm.history)
    result = await service.personalise(
        session_plan=SessionPlanView.model_validate(case["session_plan"]),
        base_sections=base_sections,
        learner_states=spec_states,
        base_pack_id=f"eval:{case['case_id']}",
        focal_learner_id=case["student_id"],
        policy=profile_for(Hypothesis.H2, ConditionCode.P1),
        session_signals=to_session_signals(learner_state),
        sources=LessonSources(items=tuple(LessonSource(**source) for source in case["sources"])),
    )
    return {
        "case_id": case["case_id"],
        "student_id": case["student_id"],
        "learner_state_inputs": {
            objective_id: state.model_dump(mode="json", exclude_none=True)
            for objective_id, state in spec_states.items()
        },
        "sections": [section.model_dump(mode="json") for section in result.sections],
        "validation": (result.validation.model_dump(mode="json") if result.validation else None),
        "repaired": result.repaired,
        "prompts": _prompts_since(service.personaliser.lm, prompt_start),
        "usage": _usage_since(service.personaliser.lm, prompt_start),
    }


def _write_case_markdown(run_dir: Path, case: dict, outcome: dict) -> None:
    lines = [
        f"# {outcome['case_id']} — {outcome['student_id']}",
        "",
        "## Learner state (as the model saw it)",
        "```json",
        json.dumps(outcome["learner_state_inputs"], indent=2),
        "```",
    ]
    base_by_objective = {
        section["lesson_objective_id"]: section for section in case["base_sections"]
    }
    for section in outcome["sections"]:
        objective_id = section["lesson_objective_id"]
        lines += [
            "",
            f"## Objective {objective_id}",
            "",
            "### Base (approved)",
            _section_markdown(base_by_objective.get(objective_id, {})),
            "",
            "### Personalised output",
            _section_markdown(section),
        ]
    if outcome["validation"]:
        lines += [
            "",
            f"## Validation — passed: {outcome['validation']['passed']}"
            f" (repaired: {outcome['repaired']})",
        ]
    cases_dir = run_dir / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)
    (cases_dir / f"{outcome['case_id']}.md").write_text("\n".join(lines))


async def run(label: str, variant: object | None = None) -> Path:
    eval_set = json.loads(EVAL_SET_PATH.read_text())
    run_dir = RUNS_DIR / label
    run_dir.mkdir(parents=True, exist_ok=True)
    lm = build_dspy_lm()
    generator = GenerateSection(lm=lm)
    service = PersonaliseReviewPack(
        personaliser=resolve_personaliser(variant),
        finalise=FinaliseReviewPack(
            generator=generator,
            repairer=RepairGeneratedSection(lm=lm),
            critic=CritiqueSections(lm=lm),
        ),
    )
    outcomes = []
    for case in eval_set["cases"]:
        outcome = await run_case(service, case)
        outcomes.append(outcome)
        _write_case_markdown(run_dir, case, outcome)
        passed = outcome["validation"]["passed"] if outcome["validation"] else "n/a"
        print(
            f"  {outcome['case_id']}: {len(outcome['sections'])} sections, "
            f"validation passed={passed}"
        )
    (run_dir / "run.json").write_text(json.dumps({"label": label, "cases": outcomes}, indent=2))
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_run_arguments(parser, stem_help="what this run is called (default: the prompt's hash)")
    parser.add_argument(
        "--variant",
        default=None,
        help="candidate signature as module.path:ClassName (default: production prompt)",
    )
    args = parser.parse_args()
    variant = load_variant(args.variant) if args.variant else None

    if args.label:
        stem = args.label
    elif variant is None:
        stem = label_for(SectionPersonalisation)
    elif isinstance(variant, type) and issubclass(variant, dspy.Signature):
        stem = label_for(variant)
    else:
        stem = args.variant.rsplit(".", 1)[-1].replace(":", "-").lower()
    label, _folder = open_run(RUNS_DIR, stem=stem, resume=args.resume)
    print(f"run label: {label}")
    run_dir = asyncio.run(run(label, variant=variant))
    print(f"wrote {run_dir}")


if __name__ == "__main__":
    main()
