"""Fingerprint every input that can change an H1 evaluation result."""

import hashlib
import inspect
import json
from pathlib import Path

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    SourceEvidenceProjector,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.policy import (
    instruction_summary,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (
    block_text,
    drawings_as_references,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    COMPOSITION_INSTRUCTIONS,
    COMPOSITION_MAX_ITERATIONS,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.critique_sections import (  # noqa: E501
    critique_contract,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.edit_section import (  # noqa: E501
    ResolveSectionFindings,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.repair_section import (  # noqa: E501
    RepairSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteGroundedSection,
    WriteGroundedSectionFromSources,
    WriteObjectiveSection,
    WriteSection,
    WriteSectionFromSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    learner_view,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.edit_section import (
    DEFAULT_EDITING_LOOP,
    editing_tools,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    prompt_unit,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.section_draft import (  # noqa: E501
    SectionDraft,
    composition_tools,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.source_reading import (  # noqa: E501
    reading_tools,
)
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant
from app.infra.dspy_lm import active_model_name, sampling_settings
from experiments.h1_condition_eval.config import H1_EVAL_CONDITIONS, RUNS_DIR
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.note_editorial import CLEAN_DIR
from experiments.h1_condition_eval.source_workspace import file_tools

_SPECIMEN_UNIT = SectionGenerationUnit(
    unit_id="specimen",
    lesson_objective_id="specimen",
    objective_text="specimen",
)


def _tool_material(tools: list) -> str:
    """Render a tool roster exactly as the model sees it."""
    return "\n".join(f"{tool.__name__}: {inspect.getdoc(tool)}" for tool in tools)


def fingerprint_material(
    model: str | None = None,
    generator: str = "packed",
    repair: str = "rewrite",
    signatures: str = "shared",
    note_source: str = "raw",
    figures: str = "reference",
    context_variant: str = "v3",
    pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
) -> dict[str, str]:
    """Return every named input that decides what the model sees or produces."""
    profiles = profiles_for_variant(context_variant)
    return {
        "arm.model": model or active_model_name(),
        "arm.generator": generator,
        "arm.context_variant": context_variant,
        "arm.repair": repair,
        "arm.signatures": signatures,
        **{
            f"leveled.{contract.__name__}": str(contract.instructions)
            + "|"
            + ",".join(contract.input_fields)
            for contract in (
                WriteObjectiveSection,
                WriteGroundedSection,
                WriteGroundedSectionFromSources,
            )
        },
        "artefact_spec": revision_pack_spec("JSS1").model_dump_json(),
        "generate.instructions": str(WriteSection.instructions),
        **{
            f"instruction_summary.{code.value}": instruction_summary(
                profiles[code].generation_policy()
            )
            for code in H1_EVAL_CONDITIONS
        },
        "evidence.block_text": inspect.getsource(block_text),
        "evidence.drawings_as_references": inspect.getsource(drawings_as_references),
        "prompt.prompt_unit": inspect.getsource(prompt_unit),
        "evidence.for_step": inspect.getsource(SourceEvidenceProjector.for_step),
        "critique.instructions": str(critique_contract(pipeline).instructions),
        "repair.instructions": str(RepairSection.instructions),
        "critique.learner_view": inspect.getsource(learner_view),
        "agentic.instructions": str(WriteSectionFromSources.instructions),
        "agentic.tools": _tool_material(reading_tools(_SPECIMEN_UNIT)),
        "agentic.file_tools": _tool_material(file_tools(Path("."))),
        "compose.task": COMPOSITION_INSTRUCTIONS,
        "compose.max_iterations": str(COMPOSITION_MAX_ITERATIONS),
        "compose.tools": _tool_material(composition_tools(SectionDraft(_SPECIMEN_UNIT), pipeline)),
        "repair.edit.instructions": str(ResolveSectionFindings.instructions),
        "repair.edit.tools": _tool_material(editing_tools({"text": ""})),
        "arm.loops": DEFAULT_EDITING_LOOP.__name__,
        "arm.note_source": note_source,
        "arm.figures": figures,
        "arm.sampling": json.dumps(sampling_settings(), sort_keys=True),
        "notes.clean": "".join(
            sorted(path.read_text(encoding="utf-8") for path in CLEAN_DIR.rglob("*.md"))
        )
        if note_source == "clean"
        else "",
        **{
            f"validation.{code.value}": profiles[code].validation.model_dump_json()
            for code in H1_EVAL_CONDITIONS
        },
        **{
            f"plan.{case['lesson']}": case["plan_sha256"]
            for case in json.loads(EVAL_SET_PATH.read_text())["cases"]
        },
    }


def material_digests(
    model: str | None = None,
    generator: str = "packed",
    repair: str = "rewrite",
    signatures: str = "shared",
    note_source: str = "raw",
    figures: str = "reference",
    context_variant: str = "v3",
    pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
) -> dict[str, str]:
    """Return one short digest per named run input."""
    return {
        name: hashlib.sha256(value.encode()).hexdigest()[:12]
        for name, value in fingerprint_material(
            model,
            generator,
            repair,
            signatures,
            note_source,
            figures,
            context_variant=context_variant,
            pipeline=pipeline,
        ).items()
    }


def fingerprint(
    model: str | None = None,
    generator: str = "packed",
    repair: str = "rewrite",
    signatures: str = "shared",
    note_source: str = "raw",
    figures: str = "reference",
    context_variant: str = "v3",
    pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
) -> str:
    """Return one label digest over every named run input."""
    material = [
        f"{name}\n{value}"
        for name, value in fingerprint_material(
            model,
            generator,
            repair,
            signatures,
            note_source,
            figures,
            context_variant=context_variant,
            pipeline=pipeline,
        ).items()
    ]
    digest = hashlib.sha256("\n".join(material).encode()).hexdigest()[:10]
    return f"h1-{digest}"


def write_fingerprint(
    run_dir: Path,
    label: str,
    *,
    note: str = "",
    model: str | None = None,
    generator: str = "packed",
    repair: str = "rewrite",
    signatures: str = "shared",
    note_source: str = "raw",
    figures: str = "reference",
    context_variant: str = "v3",
    pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
) -> None:
    """Record the label's named input digests beside the generated run."""
    record = {
        "label": label,
        "inputs": material_digests(
            model,
            generator,
            repair,
            signatures,
            note_source,
            figures,
            context_variant=context_variant,
            pipeline=pipeline,
        ),
    }
    if note:
        record["note"] = note
    (run_dir / "fingerprint.json").write_text(
        json.dumps(record, indent=2) + "\n",
        encoding="utf-8",
    )


def diff_fingerprints(left: str, right: str) -> int:
    """Print the named inputs that differ between two recorded runs."""
    loaded = {}
    for label in (left, right):
        path = RUNS_DIR / label / "fingerprint.json"
        if not path.exists():
            print(f"{label}: no fingerprint.json (run predates per-input recording)")
            return 1
        loaded[label] = json.loads(path.read_text())["inputs"]
    names = sorted(set(loaded[left]) | set(loaded[right]))
    changed = [name for name in names if loaded[left].get(name) != loaded[right].get(name)]
    if not changed:
        print(f"{left} and {right} were produced from identical inputs")
        return 0
    print(f"{len(changed)} of {len(names)} inputs differ:")
    for name in changed:
        print(f"  {name:34s} {loaded[left].get(name, '—')} -> {loaded[right].get(name, '—')}")
    return 0
