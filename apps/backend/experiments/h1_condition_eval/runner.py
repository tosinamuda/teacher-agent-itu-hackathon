"""Run C0-C3 over the frozen lesson set and record a labelled evaluation run.

Each run writes to a folder of its own, named for its label (or its inputs' fingerprint)
and the UTC second it started; `--resume <run>` carries on with an interrupted one.

Examples:

    uv run python -m experiments.h1_condition_eval.runner
    uv run python -m experiments.h1_condition_eval.runner --label pre
    uv run python -m experiments.h1_condition_eval.runner --lessons t3-w02
    uv run python -m experiments.h1_condition_eval.runner --resume pre-20260925T183005Z
"""

import argparse
import asyncio
from typing import get_args

from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    FigureSource,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    ContractMode,
)
from app.domains.experiments.review_pack_study.conditions.variants import CONTEXT_VARIANTS
from experiments.h1_condition_eval.config import RunConfig
from experiments.h1_condition_eval.execution import run_evaluation
from experiments.h1_condition_eval.fingerprints import diff_fingerprints
from experiments.h1_condition_eval.generator_arms import GENERATOR_ARMS
from experiments.run_folders import add_run_arguments


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_run_arguments(parser, stem_help="name this run instead of fingerprinting its inputs")
    parser.add_argument("--lessons", nargs="*", help="restrict to these lesson keys")
    parser.add_argument("--notes", default="", help="what this run is testing")
    parser.add_argument(
        "--diff",
        nargs=2,
        metavar=("LEFT", "RIGHT"),
        help="name the inputs two runs differ on",
    )
    parser.add_argument("--model", help="LM override, e.g. deepseek/deepseek-v4-flash")
    parser.add_argument(
        "--generator",
        # Production wires this arm; a run left on a different default measures a
        # system that does not ship. See HARNESS-DECISION.md.
        default="compose-v2",
        choices=tuple(GENERATOR_ARMS),
        help="; ".join(f"{name} = {arm.description}" for name, arm in GENERATOR_ARMS.items()),
    )
    parser.add_argument("--conditions", nargs="*", help="restrict to these condition codes")
    parser.add_argument(
        "--context-variant",
        default="v3",
        choices=tuple(CONTEXT_VARIANTS),
        help="which definition of the lesson-plan conditions to run; v3 is the frozen one",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="draws per cell; every arm is stochastic",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="pin sampling rather than using a provider default",
    )
    parser.add_argument(
        "--figures",
        default="source",
        choices=get_args(FigureSource),
        help="source keeps note drawings; reference replaces them with pointers",
    )
    parser.add_argument(
        "--note-source",
        default="clean",
        choices=("raw", "clean"),
        help="clean uses hand-edited notes; raw uses the frozen transcription",
    )
    parser.add_argument(
        "--provider",
        nargs="*",
        help="pin the run to these OpenRouter providers",
    )
    parser.add_argument(
        "--ignore-provider",
        nargs="*",
        help="provider slugs to route around",
    )
    parser.add_argument(
        "--require-parameters",
        action="store_true",
        help="only use providers declaring support for every sent parameter",
    )
    parser.add_argument(
        "--repair",
        default="rewrite",
        choices=("rewrite", "edit"),
        help="whole-section rewrite or anchored agentic editing",
    )
    parser.add_argument(
        "--signatures",
        default="leveled",
        choices=get_args(ContractMode),
        help="shared contract or per-condition-level contracts",
    )
    return parser


def main() -> int:
    """Parse CLI controls and run or compare an H1 evaluation."""
    args = _parser().parse_args()
    if args.diff:
        return diff_fingerprints(*args.diff)
    return asyncio.run(
        run_evaluation(
            RunConfig(
                label=args.label,
                resume=args.resume,
                lessons=tuple(args.lessons or ()),
                notes=args.notes,
                model=args.model,
                generator=args.generator,
                conditions=tuple(args.conditions or ()),
                repair=args.repair,
                signatures=args.signatures,
                note_source=args.note_source,
                figures=args.figures,
                repeats=args.repeats,
                temperature=args.temperature,
                context_variant=args.context_variant,
                providers=tuple(args.provider or ()),
                ignored_providers=tuple(args.ignore_provider or ()),
                require_parameters=args.require_parameters,
            )
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
