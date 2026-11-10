"""Configuration and fixed paths for one H1 condition evaluation run."""

from dataclasses import dataclass
from pathlib import Path

from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    FigureSource,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    ContractMode,
)
from app.domains.experiments.domain.types import ConditionCode

RUNS_DIR = Path(__file__).parent / "runs"
H1_EVAL_CONDITIONS = (
    ConditionCode.C0,
    ConditionCode.C1,
    ConditionCode.C2,
    ConditionCode.C3,
)


@dataclass(frozen=True)
class RunConfig:
    """Every controlled input selected through the H1 evaluation CLI."""

    label: str | None
    lessons: tuple[str, ...]
    notes: str
    model: str | None = None
    generator: str = "packed"
    conditions: tuple[str, ...] = ()
    repair: str = "rewrite"
    signatures: ContractMode = "shared"
    note_source: str = "raw"
    figures: FigureSource = "reference"
    repeats: int = 1
    temperature: float = 0.0
    context_variant: str = "v3"
    #: The full label of an interrupted run to carry on with, rather than starting one.
    resume: str | None = None
    providers: tuple[str, ...] = ()
    ignored_providers: tuple[str, ...] = ()
    require_parameters: bool = False
