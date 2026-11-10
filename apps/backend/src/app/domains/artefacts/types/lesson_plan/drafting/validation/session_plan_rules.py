from __future__ import annotations

from typing import cast

from app.domains.artefacts.types.lesson_plan.drafting.validation.types import (
    ObjectiveValidationSnapshot,
    ValidationIssue,
    ValidationPathSegment,
)
from app.shared.json_types import JsonObject

# A lesson plan may define at most this many core lesson objectives. Enforced here
# as the final safety net AND surfaced as a refinable violation by the in-loop
# semantic checker (runtime/semantic_validation.py) so generation self-corrects to
# the cap instead of hard-failing the request with a 422. Single source of truth —
# do not re-hardcode the number elsewhere.
MAX_LESSON_OBJECTIVES = 4


def _issue(path: list[ValidationPathSegment], message: str) -> ValidationIssue:
    return {"path": path, "message": message}


def _as_object_list(value: object) -> list[JsonObject]:
    if not isinstance(value, list):
        return []
    return [cast(JsonObject, item) for item in value if isinstance(item, dict)]


def _string(value: object) -> str:
    return str(value or "").strip()


def _validate_lesson_objectives(
    *,
    curriculum_objectives: list[JsonObject],
    lesson_objectives: list[JsonObject],
) -> tuple[ObjectiveValidationSnapshot, list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    curriculum_ids = {
        _string(item.get("curriculum_objective_id")) for item in curriculum_objectives
    }
    curriculum_ids.discard("")
    lesson_objective_ids: list[str] = []
    lesson_objective_kc_types: dict[str, str] = {}
    lesson_objective_focuses: set[tuple[str, str, str, str]] = set()

    for item in lesson_objectives:
        lesson_objective_id = _string(item.get("lesson_objective_id"))
        curriculum_objective_id = _string(item.get("curriculum_objective_id"))
        kc_type = _string(item.get("kc_type"))
        kc_focus = _string(item.get("kc_focus"))
        source_form = _string(item.get("source_form"))
        target_form = _string(item.get("target_form"))

        if not lesson_objective_id:
            issues.append(
                _issue(
                    ["lesson_plan_objectives"],
                    "lesson_objective_id is required",
                )
            )
            continue

        lesson_objective_ids.append(lesson_objective_id)
        if kc_type not in {"concept", "procedure", "representation"}:
            issues.append(
                _issue(
                    ["lesson_plan_objectives", lesson_objective_id],
                    "kc_type must be concept, procedure, or representation",
                )
            )
        else:
            lesson_objective_kc_types[lesson_objective_id] = kc_type

        if not kc_focus:
            issues.append(
                _issue(
                    ["lesson_plan_objectives", lesson_objective_id],
                    "kc_focus is required",
                )
            )

        focus_key = (
            curriculum_objective_id,
            kc_focus.lower(),
            source_form.lower(),
            target_form.lower(),
        )
        if kc_focus and focus_key in lesson_objective_focuses:
            issues.append(
                _issue(
                    ["lesson_plan_objectives", lesson_objective_id],
                    "sibling lesson objectives must differ in kc_focus or source/target form",
                )
            )
        lesson_objective_focuses.add(focus_key)

        if curriculum_ids and curriculum_objective_id not in curriculum_ids:
            issues.append(
                _issue(
                    ["lesson_plan_objectives", lesson_objective_id],
                    "curriculum_objective_id must match a curriculum objective in the plan",
                )
            )

    if len(lesson_objective_ids) > MAX_LESSON_OBJECTIVES:
        issues.append(
            _issue(
                ["lesson_plan_objectives"],
                f"lesson plan may define at most {MAX_LESSON_OBJECTIVES} core lesson objectives",
            )
        )

    return (
        ObjectiveValidationSnapshot(
            curriculum_ids=curriculum_ids,
            lesson_objective_ids=lesson_objective_ids,
            lesson_objective_kc_types=lesson_objective_kc_types,
        ),
        issues,
    )


def _partition_steps(
    steps: list[JsonObject],
) -> tuple[list[JsonObject], list[JsonObject], list[JsonObject]]:
    intro_steps = [step for step in steps if _string(step.get("step_kind")) == "intro"]
    evaluation_steps = [step for step in steps if _string(step.get("step_kind")) == "evaluation"]
    core_steps = [step for step in steps if _string(step.get("step_kind")) == "core"]
    return intro_steps, evaluation_steps, core_steps


def _validate_required_global_steps(
    *,
    intro_steps: list[JsonObject],
    evaluation_steps: list[JsonObject],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if len(intro_steps) != 1:
        issues.append(_issue(["steps"], "exactly one intro step is required"))
    if len(evaluation_steps) != 1:
        issues.append(_issue(["steps"], "exactly one evaluation step is required"))
    return issues


def _core_blocks(step: JsonObject) -> list[JsonObject]:
    return [block for block in _as_object_list(step.get("blocks")) if _string(block.get("type"))]


def _validate_core_steps(
    *,
    core_steps: list[JsonObject],
    lesson_objective_ids: list[str],
    lesson_objective_kc_types: dict[str, str],
) -> tuple[dict[str, int], list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    core_step_counts: dict[str, int] = {}

    for step in core_steps:
        step_id = _string(step.get("step_id"))
        lesson_objective_id = _string(step.get("lesson_objective_id"))
        if lesson_objective_id not in lesson_objective_ids:
            issues.append(
                _issue(
                    ["steps", step_id],
                    "core step must reference a valid lesson objective",
                )
            )
            continue

        kc_type = _string(step.get("kc_type"))
        if kc_type not in {"concept", "procedure", "representation"}:
            issues.append(_issue(["steps", step_id], "core step must define kc_type"))

        if lesson_objective_kc_types.get(lesson_objective_id) != kc_type:
            issues.append(
                _issue(
                    ["steps", step_id],
                    "core step kc_type must match the linked lesson objective kc_type",
                )
            )

        block_types = {_string(block.get("type")) for block in _core_blocks(step)}
        if "explanation" not in block_types:
            issues.append(
                _issue(
                    ["steps", step_id],
                    "core steps must include an explanation block",
                )
            )
        if kc_type == "concept" and "worked_example" in block_types:
            issues.append(
                _issue(
                    ["steps", step_id],
                    "concept core steps must not include worked_example blocks",
                )
            )
        if kc_type in {"procedure", "representation"} and not {
            "worked_example",
            "practice",
        }.issubset(block_types):
            issues.append(
                _issue(
                    ["steps", step_id],
                    "procedure and representation core steps require worked_example "
                    "and practice blocks",
                )
            )

        derived_instructional_type = (
            "explain_example_practice"
            if "worked_example" in block_types
            else "explain_practice"
            if "practice" in block_types
            else "explain_only"
        )
        if _string(step.get("instructional_type")) != derived_instructional_type:
            issues.append(
                _issue(
                    ["steps", step_id],
                    f"core step instructional_type must be {derived_instructional_type}",
                )
            )

        core_step_counts[lesson_objective_id] = core_step_counts.get(lesson_objective_id, 0) + 1

    return core_step_counts, issues


def _validate_objective_core_step_coverage(
    *,
    lesson_objective_ids: list[str],
    core_step_counts: dict[str, int],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for lesson_objective_id in lesson_objective_ids:
        if core_step_counts.get(lesson_objective_id) != 1:
            issues.append(
                _issue(
                    ["lesson_plan_objectives", lesson_objective_id],
                    "each lesson objective must map to exactly one core step",
                )
            )
    return issues


def _validate_global_step_fields(steps: list[JsonObject]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for step in steps:
        step_id = _string(step.get("step_id"))
        if _string(step.get("lesson_objective_id")):
            issues.append(
                _issue(
                    ["steps", step_id],
                    "global steps must not carry lesson_objective_id",
                )
            )
        if _string(step.get("kc_type")):
            issues.append(
                _issue(
                    ["steps", step_id],
                    "global steps must not carry kc_type",
                )
            )
    return issues


def _validate_evaluation_step(
    *,
    evaluation_step: JsonObject,
    lesson_objective_ids: list[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    step_id = _string(evaluation_step.get("step_id"))
    if _string(evaluation_step.get("instructional_type")) != "check":
        issues.append(
            _issue(
                ["steps", step_id],
                "evaluation steps must use instructional_type='check'",
            )
        )

    evaluation_blocks = _core_blocks(evaluation_step)
    if not evaluation_blocks:
        issues.append(_issue(["steps", step_id], "evaluation must contain practice blocks"))

    covered_objectives: set[str] = set()
    for block in evaluation_blocks:
        if _string(block.get("type")) != "practice":
            issues.append(
                _issue(
                    ["steps", step_id],
                    "evaluation steps may only contain practice blocks",
                )
            )
            continue
        covered_id = _string(block.get("lesson_objective_id"))
        if covered_id not in lesson_objective_ids:
            issues.append(
                _issue(
                    ["steps", step_id],
                    "evaluation practice blocks must reference a valid lesson objective",
                )
            )
            continue
        covered_objectives.add(covered_id)

    missing_coverage = sorted(set(lesson_objective_ids) - covered_objectives)
    if missing_coverage:
        issues.append(
            _issue(
                ["steps", step_id],
                "evaluation must cover every lesson objective: " + ", ".join(missing_coverage),
            )
        )
    return issues


def validate_lesson_objective_step_alignment(session_plan: JsonObject) -> list[ValidationIssue]:
    curriculum_objectives = _as_object_list(session_plan.get("curriculum_objectives"))
    lesson_objectives = _as_object_list(session_plan.get("lesson_plan_objectives"))
    steps = _as_object_list(session_plan.get("steps"))

    snapshot, issues = _validate_lesson_objectives(
        curriculum_objectives=curriculum_objectives,
        lesson_objectives=lesson_objectives,
    )
    intro_steps, evaluation_steps, core_steps = _partition_steps(steps)
    issues.extend(
        _validate_required_global_steps(
            intro_steps=intro_steps,
            evaluation_steps=evaluation_steps,
        )
    )
    core_step_counts, core_step_issues = _validate_core_steps(
        core_steps=core_steps,
        lesson_objective_ids=snapshot.lesson_objective_ids,
        lesson_objective_kc_types=snapshot.lesson_objective_kc_types,
    )
    issues.extend(core_step_issues)
    issues.extend(
        _validate_objective_core_step_coverage(
            lesson_objective_ids=snapshot.lesson_objective_ids,
            core_step_counts=core_step_counts,
        )
    )
    issues.extend(_validate_global_step_fields(intro_steps + evaluation_steps))
    if evaluation_steps:
        issues.extend(
            _validate_evaluation_step(
                evaluation_step=evaluation_steps[0],
                lesson_objective_ids=snapshot.lesson_objective_ids,
            )
        )
    return issues
