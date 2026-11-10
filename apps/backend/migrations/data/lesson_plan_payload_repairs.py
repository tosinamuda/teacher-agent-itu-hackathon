from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import sqlalchemy as sa
from pydantic import ValidationError

from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import SessionPlan
from app.shared.json_types import JsonObject, JsonValue

ShapeFamily = str

_CONCEPT_KEYWORDS = (
    "understand",
    "explain",
    "identify",
    "define",
    "describe",
    "state",
    "recall",
    "introduction",
    "know",
)
_PROCEDURE_KEYWORDS = (
    "solve",
    "convert",
    "calculate",
    "apply",
    "perform",
    "simplify",
    "evaluate",
    "add",
    "subtract",
    "multiply",
    "divide",
    "find",
    "determine",
    "write",
)
_REPRESENTATION_KEYWORDS = (
    "represent",
    "representation",
    "diagram",
    "graph",
    "table",
    "chart",
    "number line",
    "clock",
    "plot",
    "illustrate",
)
_REVIEW_NOTE_MAP = {
    "legacy_objectives_migrated": (
        "Legacy objectives converted into strict curriculum and lesson-plan objectives."
    ),
    "legacy_items_migrated": "Legacy step items were normalized into strict blocks.",
    "legacy_step_type_migrated": "Legacy step type values were rewritten into strict step kinds.",
    "misconceptions_migrated": "Legacy anticipated misconceptions were moved into misconceptions.",
    "assignment_embedded": "Top-level assignment content was embedded inside the step list.",
    "assignment_step_retyped": "Assignment steps were preserved as strict intro steps.",
    "ungrounded_visual_removed": (
        "Ungrounded image blocks were removed instead of fabricating provenance."
    ),
    "objective_kc_type_filled": (
        "Missing lesson objective KC types were inferred from the stored plan content."
    ),
    "objective_kc_focus_filled": (
        "Missing lesson objective KC focus values were inferred from the stored plan content."
    ),
    "core_explanation_synthesized": (
        "Missing explanation coverage was synthesized from existing step content."
    ),
    "core_worked_example_synthesized": (
        "Missing worked examples were derived from existing practice content."
    ),
    "core_practice_synthesized": (
        "Missing practice blocks were derived from existing worked examples."
    ),
    "core_step_demoted_to_concept": (
        "Core steps without recoverable modeling or practice evidence "
        "were narrowed to concept coverage."
    ),
    "evaluation_practice_synthesized": (
        "Evaluation practice blocks were derived from stored worked examples."
    ),
    "evaluation_step_demoted_to_intro": (
        "Stored evaluation-like rows without recoverable checks were preserved as intro steps."
    ),
}


@dataclass(frozen=True)
class PlanVersionPayloadSnapshot:
    version_id: str
    plan_id: str
    session_plan: JsonObject


@dataclass(frozen=True)
class PayloadAuditRecord:
    version_id: str
    plan_id: str
    original_shape_family: ShapeFamily
    valid: bool
    validation_error_codes: tuple[str, ...]
    validation_errors: tuple[JsonObject, ...]

    def to_json(self) -> JsonObject:
        return {
            "version_id": self.version_id,
            "plan_id": self.plan_id,
            "original_shape_family": self.original_shape_family,
            "valid": self.valid,
            "validation_error_codes": list(self.validation_error_codes),
            "validation_errors": list(self.validation_errors),
        }


@dataclass(frozen=True)
class PayloadRepairRecord:
    version_id: str
    plan_id: str
    original_shape_family: ShapeFamily
    repair_reason_codes: tuple[str, ...]
    review_notes: str
    repaired_session_plan: JsonObject

    def to_json(self) -> JsonObject:
        return {
            "version_id": self.version_id,
            "plan_id": self.plan_id,
            "original_shape_family": self.original_shape_family,
            "repair_reason_codes": list(self.repair_reason_codes),
            "review_notes": self.review_notes,
            "repaired_session_plan": self.repaired_session_plan,
        }


class ObjectiveSelector:
    def __init__(self, lesson_objectives: list[JsonObject]) -> None:
        self._lesson_objectives = lesson_objectives
        self._by_id = {
            str(objective["lesson_objective_id"]): objective for objective in lesson_objectives
        }
        self._by_kc_type: dict[str, list[JsonObject]] = {
            "concept": [],
            "procedure": [],
            "representation": [],
        }
        for objective in lesson_objectives:
            self._by_kc_type[str(objective["kc_type"])].append(objective)
        self._next_index = {"concept": 0, "procedure": 0, "representation": 0}
        self._last_for_kc: dict[str, str] = {}
        self._last_used_id: str | None = None

    def select_for_core(self, *, kc_type: str, preferred_id: str | None = None) -> str:
        if preferred_id and preferred_id in self._by_id:
            selected_id = preferred_id
        else:
            pool = self._by_kc_type.get(kc_type) or self._lesson_objectives
            index = min(self._next_index.get(kc_type, 0), max(len(pool) - 1, 0))
            selected_id = str(pool[index]["lesson_objective_id"])
            if pool and index < len(pool) - 1:
                self._next_index[kc_type] = index + 1

        self._last_for_kc[kc_type] = selected_id
        self._last_used_id = selected_id
        return selected_id

    def select_for_evaluation(self, *, kc_type: str | None, preferred_id: str | None = None) -> str:
        if preferred_id and preferred_id in self._by_id:
            selected_id = preferred_id
        elif kc_type and kc_type in self._last_for_kc:
            selected_id = self._last_for_kc[kc_type]
        elif self._last_used_id is not None:
            selected_id = self._last_used_id
        else:
            selected_id = str(self._lesson_objectives[-1]["lesson_objective_id"])

        if kc_type:
            self._last_for_kc[kc_type] = selected_id
        self._last_used_id = selected_id
        return selected_id


def classify_session_plan_shape(session_plan: JsonObject) -> ShapeFamily:
    if _list_of_strings(session_plan.get("objectives")) and not _object_list(
        session_plan.get("curriculum_objectives")
    ):
        return "old_objectives"
    return "modernish"


def audit_session_plan_snapshot(snapshot: PlanVersionPayloadSnapshot) -> PayloadAuditRecord:
    payload = deepcopy(snapshot.session_plan)
    validation_error_codes: list[str] = []
    validation_errors: list[JsonObject] = []
    try:
        SessionPlan.model_validate(payload)
        valid = True
    except ValidationError as exc:
        valid = False
        validation_errors = [_normalized_error(error) for error in exc.errors()]
        validation_error_codes = sorted(
            {_error_code(error) for error in validation_errors},
        )
    return PayloadAuditRecord(
        version_id=snapshot.version_id,
        plan_id=snapshot.plan_id,
        original_shape_family=classify_session_plan_shape(payload),
        valid=valid,
        validation_error_codes=tuple(validation_error_codes),
        validation_errors=tuple(validation_errors),
    )


def repair_session_plan_snapshot(snapshot: PlanVersionPayloadSnapshot) -> PayloadRepairRecord:
    payload = deepcopy(snapshot.session_plan)
    repair_reason_codes: set[str] = set()
    repaired_payload = _repair_session_plan_payload(
        payload,
        repair_reason_codes=repair_reason_codes,
    )
    repaired_payload["plan_id"] = snapshot.plan_id
    validated = SessionPlan.model_validate(repaired_payload)
    canonical = cast(
        JsonObject,
        validated.model_dump(mode="json", exclude_none=True),
    )
    reason_codes = tuple(sorted(repair_reason_codes))
    return PayloadRepairRecord(
        version_id=snapshot.version_id,
        plan_id=snapshot.plan_id,
        original_shape_family=classify_session_plan_shape(payload),
        repair_reason_codes=reason_codes,
        review_notes=_build_review_notes(reason_codes),
        repaired_session_plan=canonical,
    )


def build_audit_report(snapshots: Iterable[PlanVersionPayloadSnapshot]) -> JsonObject:
    records = [audit_session_plan_snapshot(snapshot) for snapshot in snapshots]
    invalid_records = [record for record in records if not record.valid]

    family_counts: dict[str, int] = {}
    error_counts: dict[str, int] = {}
    for record in invalid_records:
        family_counts[record.original_shape_family] = (
            family_counts.get(record.original_shape_family, 0) + 1
        )
        for code in record.validation_error_codes:
            error_counts[code] = error_counts.get(code, 0) + 1

    by_family: JsonObject = dict(family_counts)
    ranked_errors: JsonObject = {
        code: count
        for code, count in sorted(error_counts.items(), key=lambda item: (-item[1], item[0]))
    }
    invalid_rows: list[JsonValue] = [record.to_json() for record in invalid_records]
    return {
        "summary": {
            "total_rows": len(records),
            "invalid_rows": len(invalid_records),
            "invalid_rows_by_family": by_family,
            "validation_error_counts": ranked_errors,
        },
        "invalid_rows": invalid_rows,
    }


_PLAN_VERSIONS = sa.table(
    "plan_versions",
    sa.column("version_id", sa.String()),
    sa.column("plan_id", sa.String()),
    sa.column("session_plan", sa.JSON()),
)


def load_plan_version_snapshots(connection: sa.Connection) -> list[PlanVersionPayloadSnapshot]:
    """Read every stored lesson-plan payload through an existing connection."""
    result = connection.execute(
        sa.select(
            _PLAN_VERSIONS.c.version_id,
            _PLAN_VERSIONS.c.plan_id,
            _PLAN_VERSIONS.c.session_plan,
        )
    )
    return [
        PlanVersionPayloadSnapshot(
            version_id=str(row.version_id),
            plan_id=str(row.plan_id),
            session_plan=cast(JsonObject, row.session_plan or {}),
        )
        for row in result
    ]


def apply_payload_repairs(connection: sa.Connection) -> list[PayloadRepairRecord]:
    """Repair every invalid ``plan_versions`` payload in place; report what changed.

    Each fix is derived from the row's *current* content via
    ``repair_session_plan_snapshot`` — there is no frozen version_id list — so the
    pass is idempotent: once payloads are strict, a re-run audits clean and writes
    nothing. Already-valid rows are left untouched. ``repair_session_plan_snapshot``
    validates its output, so a payload that cannot be repaired raises rather than
    persisting a still-invalid row.
    """
    applied: list[PayloadRepairRecord] = []
    for snapshot in load_plan_version_snapshots(connection):
        if audit_session_plan_snapshot(snapshot).valid:
            continue
        repair = repair_session_plan_snapshot(snapshot)
        connection.execute(
            sa.update(_PLAN_VERSIONS)
            .where(_PLAN_VERSIONS.c.version_id == snapshot.version_id)
            .values(session_plan=repair.repaired_session_plan)
        )
        applied.append(repair)
    return applied


def load_payload_repairs_jsonl(path: str | Path) -> list[PayloadRepairRecord]:
    records: list[PayloadRepairRecord] = []
    repair_path = Path(path)
    for raw_line in repair_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        payload = json.loads(line)
        records.append(
            PayloadRepairRecord(
                version_id=str(payload["version_id"]),
                plan_id=str(payload["plan_id"]),
                original_shape_family=str(payload["original_shape_family"]),
                repair_reason_codes=tuple(str(code) for code in payload["repair_reason_codes"]),
                review_notes=str(payload["review_notes"]),
                repaired_session_plan=cast(JsonObject, payload["repaired_session_plan"]),
            )
        )
    return records


def write_payload_repairs_jsonl(records: Iterable[PayloadRepairRecord], path: str | Path) -> None:
    repair_path = Path(path)
    repair_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record.to_json(), ensure_ascii=True, sort_keys=True) for record in records]
    repair_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _repair_session_plan_payload(
    session_plan: JsonObject,
    *,
    repair_reason_codes: set[str],
) -> JsonObject:
    repaired = deepcopy(session_plan)

    if _list_of_strings(repaired.get("anticipated_misconceptions")):
        if not _list_of_strings(repaired.get("misconceptions")):
            repaired["misconceptions"] = list(
                _list_of_strings(repaired.get("anticipated_misconceptions"))
            )
        repair_reason_codes.add("misconceptions_migrated")
    repaired.pop("anticipated_misconceptions", None)

    curriculum_objectives = _repair_curriculum_objectives(
        repaired,
        repair_reason_codes=repair_reason_codes,
    )
    lesson_objectives = _repair_lesson_objectives(
        repaired,
        curriculum_objectives=curriculum_objectives,
        repair_reason_codes=repair_reason_codes,
    )
    objective_selector = ObjectiveSelector(lesson_objectives)
    steps = _repair_steps(
        repaired,
        lesson_objectives=lesson_objectives,
        objective_selector=objective_selector,
        repair_reason_codes=repair_reason_codes,
    )

    assignment_text = _clean_text(repaired.pop("assignment", None))
    if assignment_text:
        repair_reason_codes.add("assignment_embedded")
        steps.append(
            {
                "step_id": f"assignment-{len(steps) + 1:02d}",
                "step_kind": "intro",
                "title": "Assignment",
                "content": assignment_text,
                "blocks": [],
                "estimated_minutes": 5,
                "activities": [],
            }
        )

    repaired["curriculum_objectives"] = list(curriculum_objectives)
    repaired["lesson_plan_objectives"] = list(lesson_objectives)
    repaired["steps"] = list(steps)
    repaired["misconceptions"] = list(_list_of_strings(repaired.get("misconceptions")))
    repaired["entry_behaviour"] = list(_list_of_strings(repaired.get("entry_behaviour")))
    repaired["instructional_materials"] = list(
        _list_of_strings(repaired.get("instructional_materials"))
    )
    repaired["references"] = list(_list_of_strings(repaired.get("references")))
    repaired["assessments"] = list(_repair_assessments(repaired.get("assessments")))
    repaired.pop("objectives", None)

    return repaired


def _repair_activities(step: Mapping[str, Any]) -> list[JsonObject]:
    """Ordered ``{who, what}`` activities, from either shape.

    Stored plans carry the superseded parallel ``teacher_activities`` /
    ``student_activities`` lists, which could not express the order the step runs in.
    Interleaving is unrecoverable from two lists, so the teacher's actions are placed
    first and the students' after — the common case and the order the NERDC form prints
    them in. Already-migrated plans pass through untouched, keeping this idempotent.

    ``mode`` is dropped rather than migrated: it is not represented in the data collected
    from the expert, being absent from every field lesson plan.
    """
    existing = step.get("activities")
    if isinstance(existing, list) and existing:
        out: list[JsonObject] = []
        for item in existing:
            if not isinstance(item, Mapping):
                continue
            who = str(item.get("who") or "").strip()
            what = _clean_text(item.get("what"))
            if who in {"teacher", "student"} and what:
                out.append({"who": who, "what": what})
        return out
    return [
        {"who": who, "what": what}
        for who, key in (("teacher", "teacher_activities"), ("student", "student_activities"))
        for what in _list_of_strings(step.get(key))
    ]


def _repair_curriculum_objectives(
    session_plan: JsonObject,
    *,
    repair_reason_codes: set[str],
) -> list[JsonObject]:
    raw_curriculum_objectives = _object_list(session_plan.get("curriculum_objectives"))
    if raw_curriculum_objectives:
        repaired: list[JsonObject] = []
        for index, raw_objective in enumerate(raw_curriculum_objectives, start=1):
            objective = cast(JsonObject, raw_objective)
            objective_text = _require_text(
                objective.get("objective_text"),
                field_name=f"curriculum_objectives[{index}].objective_text",
            )
            repaired.append(
                {
                    "curriculum_objective_id": _clean_text(objective.get("curriculum_objective_id"))
                    or f"cur_obj{index:02d}",
                    "objective_text": objective_text,
                    "objective_order": _int_or_default(
                        objective.get("objective_order"),
                        default=index,
                    ),
                }
            )
        return repaired

    legacy_objectives = _list_of_strings(session_plan.get("objectives"))
    if not legacy_objectives:
        raise ValueError("session_plan is missing curriculum objectives and legacy objectives")

    repair_reason_codes.add("legacy_objectives_migrated")
    return [
        {
            "curriculum_objective_id": f"cur_obj{index:02d}",
            "objective_text": objective_text,
            "objective_order": index,
        }
        for index, objective_text in enumerate(legacy_objectives, start=1)
    ]


def _repair_lesson_objectives(
    session_plan: JsonObject,
    *,
    curriculum_objectives: list[JsonObject],
    repair_reason_codes: set[str],
) -> list[JsonObject]:
    raw_lesson_objectives = _object_list(session_plan.get("lesson_plan_objectives"))
    curriculum_by_id = {
        str(objective["curriculum_objective_id"]): objective for objective in curriculum_objectives
    }

    if raw_lesson_objectives:
        repaired: list[JsonObject] = []
        for index, raw_objective in enumerate(raw_lesson_objectives, start=1):
            objective = cast(JsonObject, raw_objective)
            curriculum_id = _clean_text(objective.get("curriculum_objective_id")) or str(
                curriculum_objectives[min(index - 1, len(curriculum_objectives) - 1)][
                    "curriculum_objective_id"
                ]
            )
            curriculum_objective = curriculum_by_id.get(curriculum_id) or curriculum_objectives[0]

            kc_type = _clean_text(objective.get("kc_type"))
            if kc_type not in {"concept", "procedure", "representation"}:
                kc_type = _infer_objective_kc_type(
                    objective_text=_clean_text(objective.get("objective_text")),
                    fallback_text=_clean_text(curriculum_objective.get("objective_text")),
                )
                repair_reason_codes.add("objective_kc_type_filled")

            kc_focus = _clean_text(objective.get("kc_focus"))
            if not kc_focus:
                kc_focus = _infer_objective_kc_focus(
                    objective_text=_clean_text(objective.get("objective_text")),
                    curriculum_text=_clean_text(curriculum_objective.get("objective_text")),
                )
                repair_reason_codes.add("objective_kc_focus_filled")

            repaired.append(
                {
                    "lesson_objective_id": _clean_text(objective.get("lesson_objective_id"))
                    or f"lop{index:02d}",
                    "objective_text": _require_text(
                        objective.get("objective_text")
                        or curriculum_objective.get("objective_text"),
                        field_name=f"lesson_plan_objectives[{index}].objective_text",
                    ),
                    "objective_order": _int_or_default(
                        objective.get("objective_order"),
                        default=index,
                    ),
                    "curriculum_objective_id": str(curriculum_objective["curriculum_objective_id"]),
                    "curriculum_objective_text": str(curriculum_objective["objective_text"]),
                    "kc_type": kc_type,
                    "kc_focus": kc_focus,
                    "source_form": _clean_text(objective.get("source_form")),
                    "target_form": _clean_text(objective.get("target_form")),
                }
            )
        return repaired

    repair_reason_codes.add("legacy_objectives_migrated")
    legacy_objectives = _list_of_strings(session_plan.get("objectives"))
    return [
        {
            "lesson_objective_id": f"lop{index:02d}",
            "objective_text": objective_text,
            "objective_order": index,
            "curriculum_objective_id": str(
                curriculum_objectives[min(index - 1, len(curriculum_objectives) - 1)][
                    "curriculum_objective_id"
                ]
            ),
            "curriculum_objective_text": str(
                curriculum_objectives[min(index - 1, len(curriculum_objectives) - 1)][
                    "objective_text"
                ]
            ),
            "kc_type": _infer_objective_kc_type(
                objective_text=objective_text,
                fallback_text=objective_text,
            ),
            "kc_focus": _infer_objective_kc_focus(
                objective_text=objective_text,
                curriculum_text=objective_text,
            ),
            "source_form": None,
            "target_form": None,
        }
        for index, objective_text in enumerate(legacy_objectives, start=1)
    ]


def _repair_steps(
    session_plan: JsonObject,
    *,
    lesson_objectives: list[JsonObject],
    objective_selector: ObjectiveSelector,
    repair_reason_codes: set[str],
) -> list[JsonObject]:
    repaired_steps: list[JsonObject] = []
    lesson_objective_lookup = {
        str(objective["lesson_objective_id"]): objective for objective in lesson_objectives
    }

    for index, raw_step in enumerate(_object_list(session_plan.get("steps")), start=1):
        step = cast(JsonObject, raw_step)
        repaired_steps.append(
            _repair_step(
                step,
                step_index=index,
                lesson_objective_lookup=lesson_objective_lookup,
                objective_selector=objective_selector,
                repair_reason_codes=repair_reason_codes,
            )
        )

    if not repaired_steps:
        raise ValueError("session_plan must contain at least one step")
    return repaired_steps


def _repair_step(
    step: JsonObject,
    *,
    step_index: int,
    lesson_objective_lookup: dict[str, JsonObject],
    objective_selector: ObjectiveSelector,
    repair_reason_codes: set[str],
) -> JsonObject:
    blocks = _repair_blocks(step, repair_reason_codes=repair_reason_codes)
    step_kind = _infer_step_kind(step, blocks)
    if _clean_text(step.get("type")) or _clean_text(step.get("step_kind")) == "assignment":
        repair_reason_codes.add("legacy_step_type_migrated")

    title = _derive_step_title(step, step_index=step_index)
    content = _derive_step_content(step, blocks)
    repaired: JsonObject = {
        "step_id": _clean_text(step.get("step_id")) or f"step-{step_index:02d}",
        "step_kind": step_kind,
        "title": title,
        "content": content,
        "blocks": list(blocks),
        "estimated_minutes": _int_or_default(step.get("estimated_minutes"), default=5),
        "activities": list(_repair_activities(step)),
    }

    if step_kind == "core":
        kc_type = _infer_step_kc_type(step, blocks)
        lesson_objective_id = objective_selector.select_for_core(
            kc_type=kc_type,
            preferred_id=_clean_text(step.get("lesson_objective_id")),
        )
        repaired["kc_type"] = kc_type
        repaired["lesson_objective_id"] = lesson_objective_id
        core_blocks = _repair_core_blocks(
            step=repaired,
            blocks=blocks,
            repair_reason_codes=repair_reason_codes,
        )
        if kc_type == "concept":
            core_blocks = [
                block for block in core_blocks if _clean_text(block.get("type")) != "worked_example"
            ]
        repaired["blocks"] = list(core_blocks)
        return repaired

    if step_kind == "evaluation":
        lesson_objective_id = objective_selector.select_for_evaluation(
            kc_type=_clean_text(step.get("kc_type")),
            preferred_id=_clean_text(step.get("lesson_objective_id")),
        )
        evaluation_blocks = _repair_evaluation_blocks(
            blocks=blocks,
            lesson_objective_id=lesson_objective_id,
            repair_reason_codes=repair_reason_codes,
        )
        if not evaluation_blocks:
            repair_reason_codes.add("evaluation_step_demoted_to_intro")
            repaired["step_kind"] = "intro"
            repaired["blocks"] = list(blocks)
            return repaired
        repaired["blocks"] = list(evaluation_blocks)
        return repaired

    if (
        _clean_text(step.get("type")) == "assignment"
        or _clean_text(step.get("step_kind")) == "assignment"
    ):
        repair_reason_codes.add("assignment_step_retyped")
        repaired["title"] = _clean_text(step.get("title")) or "Assignment"
    return repaired


def _repair_blocks(step: JsonObject, *, repair_reason_codes: set[str]) -> list[JsonObject]:
    raw_blocks = _object_list(step.get("blocks")) or _object_list(step.get("items"))
    if _object_list(step.get("items")):
        repair_reason_codes.add("legacy_items_migrated")

    repaired: list[JsonObject] = []
    for raw_block in raw_blocks:
        if not isinstance(raw_block, dict):
            continue
        block = cast(JsonObject, deepcopy(raw_block))
        block_type = _clean_text(block.get("type"))
        if block_type == "explanation":
            content = _clean_text(block.get("content"))
            if not content:
                continue
            repaired.append(
                {
                    "id": _clean_text(block.get("id")) or "exp",
                    "type": "explanation",
                    "content": content,
                }
            )
            continue

        if block_type == "practice":
            question = _clean_text(block.get("question"))
            answer = _clean_text(block.get("answer"))
            if not question or not answer:
                continue
            practice: JsonObject = {
                "id": _clean_text(block.get("id")) or "pr",
                "type": "practice",
                "question": question,
                "answer": answer,
            }
            hints = _list_of_strings(block.get("hints"))
            if hints:
                practice["hints"] = list(hints)
            lesson_objective_id = _clean_text(block.get("lesson_objective_id"))
            if lesson_objective_id:
                practice["lesson_objective_id"] = lesson_objective_id
            repaired.append(practice)
            continue

        if block_type == "worked_example":
            problem = _clean_text(block.get("problem"))
            final_answer = _clean_text(block.get("final_answer"))
            steps = _repair_worked_example_steps(block.get("steps"))
            if not problem or not final_answer or not steps:
                continue
            repaired.append(
                {
                    "id": _clean_text(block.get("id")) or "we",
                    "type": "worked_example",
                    "problem": problem,
                    "steps": list(steps),
                    "final_answer": final_answer,
                }
            )
            continue

        if block_type == "visual":
            variant = _clean_text(block.get("variant"))
            if not variant:
                variant = "image" if _clean_text(block.get("url")) else ""
            if variant == "image":
                url = _clean_text(block.get("url"))
                source_record_id = _clean_text(block.get("source_record_id"))
                if not url or not source_record_id:
                    repair_reason_codes.add("ungrounded_visual_removed")
                    continue
            visual: JsonObject = {
                "id": _clean_text(block.get("id")) or "visual",
                "type": "visual",
                "variant": variant or "diagram_number_line",
            }
            for field_name in (
                "caption",
                "url",
                "source_record_id",
                "source_html_path",
                "source_anchor_id",
            ):
                value = _clean_text(block.get(field_name))
                if value:
                    visual[field_name] = value
            data = block.get("data")
            if isinstance(data, dict):
                visual["data"] = data
            repaired.append(visual)
            continue

    return repaired


def _repair_worked_example_steps(raw_steps: object) -> list[JsonObject]:
    repaired_steps: list[JsonObject] = []
    for index, raw_step in enumerate(_object_list(raw_steps), start=1):
        if not isinstance(raw_step, dict):
            continue
        step = cast(JsonObject, raw_step)
        content = _clean_text(step.get("content"))
        if not content:
            continue
        repaired_steps.append(
            {
                "label": _clean_text(step.get("label")) or f"Step {index}",
                "content": content,
            }
        )
    return repaired_steps


def _repair_core_blocks(
    *,
    step: JsonObject,
    blocks: list[JsonObject],
    repair_reason_codes: set[str],
) -> list[JsonObject]:
    repaired_blocks = [deepcopy(block) for block in blocks]
    explanation_blocks = [
        block for block in repaired_blocks if _clean_text(block.get("type")) == "explanation"
    ]
    worked_example_blocks = [
        block for block in repaired_blocks if _clean_text(block.get("type")) == "worked_example"
    ]
    practice_blocks = [
        block for block in repaired_blocks if _clean_text(block.get("type")) == "practice"
    ]

    if not explanation_blocks:
        repaired_blocks.insert(
            0,
            {
                "id": f"{step['step_id']}-exp01",
                "type": "explanation",
                "content": str(step["content"]),
            },
        )
        repair_reason_codes.add("core_explanation_synthesized")
        explanation_blocks = [repaired_blocks[0]]

    kc_type = str(step["kc_type"])
    if kc_type not in {"procedure", "representation"}:
        return repaired_blocks

    if not worked_example_blocks and practice_blocks:
        source_practice = practice_blocks[0]
        repaired_blocks.append(
            {
                "id": f"{step['step_id']}-we01",
                "type": "worked_example",
                "problem": str(source_practice["question"]),
                "steps": [
                    {
                        "label": "Step 1",
                        "content": str(explanation_blocks[0]["content"]),
                    }
                ],
                "final_answer": str(source_practice["answer"]),
            }
        )
        repair_reason_codes.add("core_worked_example_synthesized")
        worked_example_blocks = [repaired_blocks[-1]]

    if not practice_blocks and worked_example_blocks:
        source_example = worked_example_blocks[0]
        repaired_blocks.append(
            {
                "id": f"{step['step_id']}-pr01",
                "type": "practice",
                "question": str(source_example["problem"]),
                "answer": str(source_example["final_answer"]),
            }
        )
        repair_reason_codes.add("core_practice_synthesized")
        practice_blocks = [repaired_blocks[-1]]

    if not worked_example_blocks and not practice_blocks:
        step["kc_type"] = "concept"
        repair_reason_codes.add("core_step_demoted_to_concept")

    return repaired_blocks


def _repair_evaluation_blocks(
    *,
    blocks: list[JsonObject],
    lesson_objective_id: str,
    repair_reason_codes: set[str],
) -> list[JsonObject]:
    practice_blocks = [
        deepcopy(block) for block in blocks if _clean_text(block.get("type")) == "practice"
    ]
    if not practice_blocks:
        worked_examples = [
            block for block in blocks if _clean_text(block.get("type")) == "worked_example"
        ]
        if worked_examples:
            source_example = worked_examples[0]
            practice_blocks.append(
                {
                    "id": f"{_clean_text(source_example.get('id')) or 'eval'}-pr01",
                    "type": "practice",
                    "question": str(source_example["problem"]),
                    "answer": str(source_example["final_answer"]),
                }
            )
            repair_reason_codes.add("evaluation_practice_synthesized")

    repaired: list[JsonObject] = []
    for block in practice_blocks:
        block["lesson_objective_id"] = lesson_objective_id
        repaired.append(block)
    return repaired


def _repair_assessments(raw_assessments: object) -> list[JsonObject]:
    repaired: list[JsonObject] = []
    for raw_assessment in _object_list(raw_assessments):
        if not isinstance(raw_assessment, dict):
            continue
        assessment = cast(JsonObject, raw_assessment)
        question = _clean_text(assessment.get("question"))
        answer = _clean_text(assessment.get("answer"))
        if not question or not answer:
            continue
        repaired_assessment: JsonObject = {"question": question, "answer": answer}
        rubric = _clean_text(assessment.get("rubric"))
        if rubric:
            repaired_assessment["rubric"] = rubric
        repaired.append(repaired_assessment)
    return repaired


def _infer_step_kind(step: JsonObject, blocks: list[JsonObject]) -> str:
    raw_step_kind = _clean_text(step.get("step_kind"))
    if raw_step_kind in {"intro", "core", "evaluation"}:
        return raw_step_kind
    if raw_step_kind == "assignment":
        return "intro"

    legacy_type = _clean_text(step.get("type"))
    if legacy_type in {"assignment", "introduction", "review"}:
        return "intro"
    if legacy_type == "check":
        has_practice = any(_clean_text(block.get("type")) == "practice" for block in blocks)
        return "evaluation" if has_practice else "intro"
    if legacy_type in {
        "explain",
        "example",
        "practice",
        "explain_only",
        "explain_practice",
        "explain_example_practice",
    }:
        return "core"
    return "intro"


def _infer_step_kc_type(step: JsonObject, blocks: list[JsonObject]) -> str:
    raw_kc_type = _clean_text(step.get("kc_type"))
    if raw_kc_type in {"concept", "procedure", "representation"}:
        return raw_kc_type

    block_types = {_clean_text(block.get("type")) for block in blocks}
    searchable_text = " ".join(
        part
        for part in (
            _clean_text(step.get("title")),
            _clean_text(step.get("content")),
            _clean_text(step.get("type")),
        )
        if part
    )
    if _contains_keyword(searchable_text, _REPRESENTATION_KEYWORDS):
        return "representation"
    if (
        "worked_example" in block_types
        or "practice" in block_types
        or _contains_keyword(
            searchable_text,
            _PROCEDURE_KEYWORDS,
        )
    ):
        return "procedure"
    return "concept"


def _infer_objective_kc_type(*, objective_text: str | None, fallback_text: str | None) -> str:
    searchable_text = " ".join(part for part in (objective_text, fallback_text) if part)
    if _contains_keyword(searchable_text, _REPRESENTATION_KEYWORDS):
        return "representation"
    if _contains_keyword(searchable_text, _PROCEDURE_KEYWORDS):
        return "procedure"
    if _contains_keyword(searchable_text, _CONCEPT_KEYWORDS):
        return "concept"
    return "concept"


def _infer_objective_kc_focus(*, objective_text: str | None, curriculum_text: str | None) -> str:
    return _require_text(
        objective_text or curriculum_text,
        field_name="lesson objective kc_focus",
    )


def _derive_step_title(step: JsonObject, *, step_index: int) -> str:
    title = _clean_text(step.get("title"))
    if title:
        return title
    content = _clean_text(step.get("content"))
    if content:
        first_sentence = re.split(r"(?<=[.!?])\s+", content, maxsplit=1)[0].strip()
        return first_sentence[:120]
    raise ValueError(f"step {step_index} is missing title and content")


def _derive_step_content(step: JsonObject, blocks: list[JsonObject]) -> str:
    content = _clean_text(step.get("content"))
    if content:
        return content
    for block in blocks:
        block_type = _clean_text(block.get("type"))
        if block_type == "explanation":
            return str(block["content"])
        if block_type == "worked_example":
            return str(block["problem"])
        if block_type == "practice":
            return str(block["question"])
    raise ValueError("step is missing content and recoverable blocks")


def _list_of_strings(value: object) -> list[str]:
    return [text for raw in _object_list(value) if (text := _clean_text(raw))]


def _object_list(value: object) -> list[object]:
    if not isinstance(value, list):
        return []
    return cast(list[object], value)


def _clean_text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _require_text(value: object, *, field_name: str) -> str:
    cleaned = _clean_text(value)
    if not cleaned:
        raise ValueError(f"{field_name} is required to repair session plan payload")
    return cleaned


def _int_or_default(value: object, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default


def _contains_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    normalized = text.lower()
    return any(keyword in normalized for keyword in keywords)


def _normalized_error(error: Mapping[str, Any]) -> JsonObject:
    loc = [str(part) for part in error.get("loc", ())]
    return {
        "loc": list(loc),
        "msg": str(error.get("msg") or ""),
        "type": str(error.get("type") or ""),
    }


def _error_code(error: JsonObject) -> str:
    loc = ".".join(str(part) for part in cast(list[str], error["loc"]))
    msg = str(error["msg"])
    error_type = str(error["type"])
    if "Field required" in msg:
        return f"missing:{loc}"
    if "extra_forbidden" in error_type:
        return f"extra:{loc}"
    return f"{loc}:{msg}"


def _build_review_notes(reason_codes: tuple[str, ...]) -> str:
    if not reason_codes:
        return "Stored payload was re-encoded into the strict schema without content changes."
    note_parts = [
        _REVIEW_NOTE_MAP.get(code, code.replace("_", " ").capitalize() + ".")
        for code in reason_codes
    ]
    return " ".join(note_parts)
