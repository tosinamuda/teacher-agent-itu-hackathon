"""Execute an H1 evaluation grid and persist its reproducibility record."""

import asyncio
import json
from pathlib import Path
from typing import Any

import dspy
from dotenv import load_dotenv
from dspy.utils.exceptions import AdapterParseError

from app.domains.artefacts.types.post_class_review_pack.application.generate_base import (
    GenerateBaseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    FigureSource,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy import tracing
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CritiqueSections,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.edit_section import (
    EditSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.repair_section import (
    RepairGeneratedSection,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.policies import ConditionProfile
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant
from app.infra.dspy_lm import (
    build_dspy_lm,
    set_model_override,
    set_responses_api,
    set_sampling_override,
    transport_for,
)
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.cell_store import read_cell, write_cell
from experiments.h1_condition_eval.config import H1_EVAL_CONDITIONS, RUNS_DIR, RunConfig
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.fingerprints import fingerprint, write_fingerprint
from experiments.h1_condition_eval.generator_arms import GENERATOR_ARMS, harness_for
from experiments.h1_condition_eval.log import append_run
from experiments.h1_condition_eval.loop_observer import LoopObserver
from experiments.h1_condition_eval.measurements import (
    eaten_latex_commands,
    evidence_record,
    pack_metrics,
    validation_metrics,
)
from experiments.h1_condition_eval.metrics import notes_by_lesson, score
from experiments.h1_condition_eval.note_editorial import clean_plan, describe_note_source
from experiments.run_folders import open_run

_NOTES = notes_by_lesson(EVAL_SET_PATH) if EVAL_SET_PATH.exists() else {}


async def run_case(
    generator: GenerateBaseReviewPack,
    lesson: str,
    plan_dict: dict[str, Any],
    condition: ConditionCode,
    profile: ConditionProfile,
    arm: dict[str, object],
    *,
    figures: FigureSource,
) -> list[dict[str, Any]]:
    """Generate and measure one lesson-condition cell."""
    plan = SessionPlanView.model_validate(plan_dict)
    sources = LessonSources.unresolved(plan.references)
    units = (
        BaseReviewPackRequestBuilder(figures=figures)
        .build(
            session_plan=plan,
            policy=profile.generation_policy(),
            sources=sources,
        )
        .units
    )
    evidence = [item for unit in units for item in (unit.source_evidence or [])]
    try:
        result = await generator.generate(
            session_plan=plan,
            policy=profile.generation_policy(),
            sources=sources,
        )
    except AdapterParseError as error:
        print(f"  {lesson:8} {condition.value}  DREW A DUD: {type(error).__name__}: {error!s:.90}")
        return []

    row = {
        "lesson": lesson,
        "condition": condition.value,
        **arm,
        "units": len(units),
        "evidence_items": len(evidence),
        "evidence_chars": sum(len(item.excerpt) for item in evidence),
        "evidence_record": evidence_record(units),
        **pack_metrics(result.sections),
        **validation_metrics(result),
        **score(
            _NOTES.get(lesson, ""),
            [section.model_dump(mode="json") for section in result.sections],
        ),
        "sections_json": [section.model_dump(mode="json") for section in result.sections],
    }
    print(
        f"  {lesson:8s} {condition.value}  "
        + "  ".join(
            f"{key}={row[key]}"
            for key in (
                "evidence_items",
                "evidence_chars",
                "chars",
                "inline_ref_markers",
                "findings",
                "repaired",
            )
        )
    )
    for finding in row["findings_text"]:
        print(f"           · {finding}")
    return [row]


def _selected_cases(config: RunConfig) -> list[dict[str, Any]]:
    if not EVAL_SET_PATH.exists():
        raise SystemExit("no frozen eval set — run experiments.h1_condition_eval.dataset first")
    cases: list[dict[str, Any]] = json.loads(EVAL_SET_PATH.read_text())["cases"]
    if config.lessons:
        cases = [case for case in cases if case["lesson"] in config.lessons]
    if config.note_source != "clean":
        return cases

    cleaned = []
    for case in cases:
        plan = dict(case["plan"])
        plan["lesson_key"] = case["lesson"]
        plan, edits = clean_plan(plan)
        for edit in edits:
            print(f"  {case['lesson']}/{edit}")
        cleaned.append({**case, "plan": plan})
    return cleaned


def _selected_conditions(config: RunConfig) -> tuple[ConditionCode, ...]:
    return tuple(
        code
        for code in H1_EVAL_CONDITIONS
        if not config.conditions or code.value in config.conditions
    )


def _configure_model(config: RunConfig) -> None:
    load_dotenv(override=False)
    set_model_override(config.model)
    set_sampling_override(cache=False, temperature=config.temperature)
    # Only the dspy arms. The framework harnesses call chat completions and refuse
    # anything else, so asking for `/responses` on their behalf would exclude them from
    # their own run. Where it IS taken, JSONAdapter comes with it: `/responses` is only
    # worth going to for the enforced schema and the native `function_call`, and
    # ChatAdapter would go on writing `[[ ## tool_calls ## ]]` into prose regardless of
    # which endpoint carried it.
    on_dspy = harness_for(config.generator).recorded().get("framework") == "dspy"
    if on_dspy:
        dspy.configure(adapter=transport_for(config.model or ""))
    else:
        set_responses_api(False)


async def run_evaluation(config: RunConfig) -> int:
    """Execute the configured lesson-condition grid and persist its records."""
    cases = _selected_cases(config)
    conditions = _selected_conditions(config)
    _configure_model(config)
    stem = config.label or fingerprint(
        config.model,
        config.generator,
        config.repair,
        config.signatures,
        config.note_source,
        config.figures,
        context_variant=config.context_variant,
    )
    label, run_dir = open_run(RUNS_DIR, stem=stem, resume=config.resume)
    arm_record: dict[str, object] = {
        "model": config.model or "config-default",
        "generator": config.generator,
        # The harness is an arm dimension beside the condition, not a name. Resolved here
        # so a run refuses to start rather than recording an arm nobody can reconstruct.
        "harness": harness_for(config.generator).recorded(),
        "repair": config.repair,
        "signatures": config.signatures,
        "note_source": config.note_source,
        "figures": config.figures,
        # Which definition of the lesson-plan conditions this run executed. `v3` is the
        # frozen one; anything else is a named diagnostic derived from it (variants.py),
        # and a run that does not say which it ran cannot be compared to one that does.
        "context_variant": config.context_variant,
    }
    profiles = profiles_for_variant(config.context_variant)
    harness = harness_for(config.generator).recorded()
    print(
        f"run label: {label}   arm: {arm_record['generator']}/{arm_record['model']}   "
        f"harness: {harness['loop']} on {harness['framework']} "
        f"{harness['framework_version']}   "
        f"conditions: {[condition.value for condition in conditions]}   "
        f"context: {config.context_variant}   "
        f"lessons: {[case['lesson'] for case in cases]}"
    )
    print(f"  NOTES: {describe_note_source(config.note_source)}")
    arm = GENERATOR_ARMS[config.generator]
    unsupported = [code.value for code in conditions if not arm.supports(profiles[code])]
    if unsupported:
        raise SystemExit(
            f"--generator {config.generator} reads evidence through tools, and "
            f"{unsupported} have none. Use --generator compose for those conditions."
        )

    observer = LoopObserver()
    observer.watch_the_loop()
    dspy.configure(callbacks=[*(getattr(dspy.settings, "callbacks", None) or []), observer])
    dspy.configure(lm=build_dspy_lm())
    tracing.start_capture(stream_to=run_dir / "traces.jsonl")
    gate = asyncio.Semaphore(6)
    lm = build_dspy_lm()

    def generator_for(case: dict[str, Any], code: ConditionCode) -> GenerateBaseReviewPack:
        section_generator = arm.build(
            profile=profiles[code],
            case=case,
            workspace_root=RUNS_DIR / label / "workspace" / code.value / case["lesson"],
            signatures=config.signatures,
        )
        return GenerateBaseReviewPack(
            request_builder=BaseReviewPackRequestBuilder(figures=config.figures),
            generator=section_generator,
            finalise=FinaliseReviewPack(
                generator=section_generator,
                repairer=RepairGeneratedSection(lm=lm),
                critic=CritiqueSections(lm=lm),
                reviser=EditSection(lm=lm) if config.repair == "edit" else None,
            ),
        )

    async def run_cell(
        case: dict[str, Any], code: ConditionCode, repeat: int
    ) -> list[dict[str, Any]]:
        cell = cells_dir / f"{case['lesson']}.{code.value}.r{repeat}.json"
        if (done := read_cell(cell, arm_record)) is not None:
            print(f"  {case['lesson']:8s} {code.value}  already done")
            return done
        async with gate:
            try:
                rows = await run_case(
                    generator_for(case, code),
                    case["lesson"],
                    case["plan"],
                    code,
                    profiles[code],
                    arm_record,
                    figures=config.figures,
                )
            except Exception as error:  # noqa: BLE001 - one controlled stochastic redraw
                print(f"  {case['lesson']:8s} {code.value}  re-drawing after {error!r}")
                rows = await run_case(
                    generator_for(case, code),
                    case["lesson"],
                    case["plan"],
                    code,
                    profiles[code],
                    arm_record,
                    figures=config.figures,
                )
        for row in rows:
            row["repeat"] = repeat
        write_cell(cell, arm_record, rows)
        return rows

    cells_dir = run_dir / "cells"
    cell_rows = []
    for repeat in range(1, config.repeats + 1):
        if config.repeats > 1:
            print(f"  --- repeat {repeat}/{config.repeats}")
        cell_rows += await asyncio.gather(
            *(run_cell(case, code, repeat) for case in cases for code in conditions)
        )

    order = {code.value: index for index, code in enumerate(conditions)}
    rows = sorted(
        (row for cell in cell_rows for row in cell),
        key=lambda row: (row.get("repeat", 1), row["lesson"], order[row["condition"]]),
    )
    _report_run_warnings(observer, rows)
    write_fingerprint(
        run_dir,
        label,
        note=config.notes,
        model=config.model,
        generator=config.generator,
        repair=config.repair,
        signatures=config.signatures,
        note_source=config.note_source,
        figures=config.figures,
        context_variant=config.context_variant,
    )
    _write_traces(run_dir)
    _write_run(run_dir, label, rows, arm_record)
    log_path = append_run(
        label,
        [
            {
                key: value
                for key, value in row.items()
                if key not in ("sections_json", "evidence_record")
            }
            for row in rows
        ],
        notes=config.notes,
    )
    print(f"\nwrote {run_dir}/run.json and appended {len(rows)} rows to {log_path.name}")
    return 0


def _report_run_warnings(observer: LoopObserver, rows: list[dict[str, Any]]) -> None:
    print(f"  loops: {observer.summary()}")
    if detail := observer.detail():
        print("  " + detail.replace("\n", "\n  "))
    if observer.abandoned_loops:
        print(
            f"  WARNING {observer.abandoned_loops} loop(s) gave up without submitting. "
            "Those sections are short, not failed."
        )
    eaten = eaten_latex_commands(rows)
    if eaten:
        print(
            f"  WARNING {len(eaten)} block(s) carry a control character where a LaTeX "
            f"command should be: {sorted(set(eaten))}."
        )


def _write_traces(run_dir: Path) -> None:
    """Close the capture window. The file was written as the loops ran."""
    traces = tracing.drain()
    if traces:
        print(f"captured {len(traces)} agent traces -> {(run_dir / 'traces.jsonl').name}")


def _write_run(
    run_dir: Path, label: str, rows: list[dict[str, Any]], arm: dict[str, object]
) -> None:
    """The run, with the arm written out in words.

    ``fingerprint.json`` records the same settings as SHA-256 digests, which is what a
    fingerprint is for and is unreadable by design. For nine days both judged runs
    carried ``note_source`` = sha256("raw") there and nothing said so anywhere a person
    would look, so the study's headline number was measured on the uncorrected
    transcription without anyone noticing. A run now states what it read.
    """
    plans_used = {
        case["lesson"]: case["plan_sha256"]
        for case in json.loads(EVAL_SET_PATH.read_text())["cases"]
    }
    (run_dir / "run.json").write_text(
        json.dumps(
            {"label": label, "arm": arm, "plans": plans_used, "cases": rows},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
