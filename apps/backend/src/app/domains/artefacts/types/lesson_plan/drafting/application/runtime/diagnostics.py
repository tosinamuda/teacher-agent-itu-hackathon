from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

from pydantic import BaseModel

from app.config import CONFIG
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.types import (
    NormalizedLessonDraft,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonGenerationSession,
    PreparedGenerationInputs,
    TextbookRecordPayload,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.artifacts import (
    GenerationArtifacts,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.generator import (
    LessonGenerationArtifacts,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CandidateKC,
    activities_of,
)
from app.shared.json_types import JsonObject


def _safe_markdown_text(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "-"
    return text.replace("```", "'''")


def _append_labeled_value(lines: list[str], label: str, value: object) -> None:
    lines.extend([f"**{label}**  \n{_safe_markdown_text(value)}", ""])


def _json_ready(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump()
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


def _object_list(value: object) -> list[object]:
    return cast(list[object], value) if isinstance(value, list) else []


def _string_list(value: object) -> list[str]:
    return [str(item) for item in _object_list(value)]


def _object_dict(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    return cast(dict[str, object], value)


def _append_json_block(lines: list[str], heading: str, value: object) -> None:
    lines.extend(
        [
            f"### {heading}",
            "",
            "```json",
            _safe_markdown_text(
                json.dumps(_json_ready(value), indent=2, ensure_ascii=False, default=str)
            ),
            "```",
            "",
        ]
    )


class DiagnosticLogWriter:
    def output_dir(self) -> Path:
        return CONFIG.lesson_plan.diagnostics_dir

    def write(
        self,
        *,
        session: LessonGenerationSession,
        inputs: PreparedGenerationInputs,
        artifacts: GenerationArtifacts,
        draft: NormalizedLessonDraft,
        consistency_checks: list[str],
        session_plan: JsonObject,
    ) -> str:
        output_dir = self.output_dir()
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        output_path = output_dir / f"{session.session_id}-{timestamp}.md"
        output_path.write_text(
            self.render(
                session=session,
                inputs=inputs,
                artifacts=artifacts,
                draft=draft,
                consistency_checks=consistency_checks,
                session_plan=session_plan,
            ),
            encoding="utf-8",
        )
        return str(output_path)

    def render(
        self,
        *,
        session: LessonGenerationSession,
        inputs: PreparedGenerationInputs,
        artifacts: GenerationArtifacts,
        draft: NormalizedLessonDraft,
        consistency_checks: list[str],
        session_plan: JsonObject,
    ) -> str:
        record_map = {record.record_id: record for record in inputs.textbook_records}
        lines = [
            "# Lesson Plan Diagnostic",
            "",
            "## Original Input",
            "",
        ]
        _append_labeled_value(lines, "Session ID", session.session_id)
        _append_labeled_value(lines, "Subject", session.subject)
        _append_labeled_value(lines, "Track", session.track)
        _append_labeled_value(lines, "Grade", session.grade)
        _append_labeled_value(lines, "Term", session.term)
        _append_labeled_value(lines, "Week", session.week)
        _append_labeled_value(lines, "Theme", session.theme)
        _append_labeled_value(lines, "Topic", session.topic)
        _append_labeled_value(lines, "Subtopic / Lesson Unit", session.subtopic)
        _append_labeled_value(lines, "Duration Minutes", session.duration_minutes)
        lines.extend(["## Original Curriculum Context", ""])
        _append_labeled_value(
            lines,
            "Teacher Activities",
            "; ".join(inputs.curriculum.teacher_activities),
        )
        _append_labeled_value(
            lines,
            "Student Activities",
            "; ".join(inputs.curriculum.student_activities),
        )
        _append_labeled_value(
            lines,
            "Instructional Materials",
            "; ".join(inputs.curriculum.instructional_materials),
        )
        _append_labeled_value(
            lines,
            "Entry Behaviour",
            "; ".join(inputs.curriculum.entry_behaviour),
        )
        _append_labeled_value(
            lines,
            "Evaluation Guide",
            "; ".join(inputs.curriculum.evaluation_guide),
        )
        _append_json_block(lines, "Curriculum Context JSON", inputs.curriculum)
        lines.extend(["## Original Curriculum Objectives", ""])
        for objective in inputs.curriculum_objectives:
            lines.extend([f"### {objective.curriculum_objective_id}", ""])
            _append_labeled_value(lines, "Objective Text", objective.objective_text)
            _append_labeled_value(lines, "Objective Order", objective.objective_order)

        lines.extend(["## Original Subtopic Textbook Content", ""])
        for textbook_record in inputs.textbook_records:
            self._append_textbook_record(lines, textbook_record)

        lines.extend(["## Intermediate Data", ""])
        _append_json_block(lines, "Candidate KC Plan JSON", artifacts.kc_plan)
        lines.extend(["## New Lesson Objectives", ""])
        for lesson_objective in artifacts.lesson_plan_objectives:
            lines.extend([f"### {lesson_objective.lesson_objective_id}", ""])
            _append_labeled_value(lines, "Objective Text", lesson_objective.objective_text)
            _append_labeled_value(lines, "KC Type", lesson_objective.kc_type)
            _append_labeled_value(lines, "KC Focus", lesson_objective.kc_focus)
            _append_labeled_value(lines, "Source Form", lesson_objective.source_form)
            _append_labeled_value(lines, "Target Form", lesson_objective.target_form)
            _append_labeled_value(
                lines,
                "Curriculum Objective ID",
                lesson_objective.curriculum_objective_id,
            )
            _append_labeled_value(
                lines,
                "Curriculum Objective Text",
                lesson_objective.curriculum_objective_text,
            )

        lines.extend(["## New Knowledge Components", ""])
        for candidate_kc in artifacts.resolved_kcs:
            self._append_kc(lines, candidate_kc, record_map)

        # Core-step blueprints exist only on the staged pipeline; the single-call
        # no-linkage layer (WholeLessonArtifacts) drafts steps without them.
        if isinstance(artifacts, LessonGenerationArtifacts):
            _append_json_block(
                lines,
                "Core Step Blueprints",
                [blueprint.model_dump() for blueprint in artifacts.core_step_blueprints],
            )
        if artifacts.assessment_items:
            lines.extend(["## Assessment Items", ""])
            _append_json_block(lines, "Assessment Items JSON", artifacts.assessment_items)
        lines.extend(["## Step Evidence Plans", ""])
        for lesson_objective_id, evidence_plan in artifacts.step_evidence_plans.items():
            lines.extend([f"### {lesson_objective_id}", ""])
            _append_labeled_value(
                lines,
                "Selected Record IDs",
                ", ".join(evidence_plan.selected_record_ids),
            )
            _append_labeled_value(
                lines,
                "Concept Record IDs",
                ", ".join(evidence_plan.concept_record_ids),
            )
            _append_labeled_value(
                lines,
                "Modeling Record IDs",
                ", ".join(evidence_plan.modeling_record_ids),
            )
            _append_labeled_value(
                lines,
                "Practice Record IDs",
                ", ".join(evidence_plan.practice_record_ids),
            )
            _append_labeled_value(
                lines,
                "Visual Record IDs",
                ", ".join(evidence_plan.visual_record_ids),
            )
            lines.extend(["**Evidence Records**", ""])
            for record_id in evidence_plan.selected_record_ids:
                record = record_map.get(record_id)
                if record is not None:
                    self._append_textbook_record(lines, record, level="####")

        _append_json_block(lines, "Evidence Summaries", artifacts.evidence_summaries)
        _append_json_block(lines, "Draft Core Steps", draft.core_steps)
        _append_json_block(lines, "Draft Global Steps", draft.global_steps)
        lines.extend(["## Consistency Checks", ""])
        if consistency_checks:
            for check in consistency_checks:
                lines.append(f"- {check}")
            lines.append("")
        else:
            lines.extend(["- none", ""])
        lines.extend(["## Final Output", ""])
        _append_json_block(lines, "Final Session Plan JSON", session_plan)
        lines.extend(["## Final Session Plan Steps", ""])
        for raw_step in _object_list(session_plan.get("steps")):
            step = _object_dict(raw_step)
            if step is None:
                continue
            lines.extend([f"### {step.get('step_id') or '-'}", "", "**Blocks**", ""])
            _append_labeled_value(lines, "Step Kind", step.get("step_kind"))
            _append_labeled_value(lines, "Instructional Type", step.get("instructional_type"))
            _append_labeled_value(lines, "KC Type", step.get("kc_type"))
            _append_labeled_value(lines, "Lesson Objective ID", step.get("lesson_objective_id"))
            _append_labeled_value(lines, "Title", step.get("title"))
            _append_labeled_value(lines, "Content", step.get("content"))
            _append_labeled_value(
                lines,
                "Teacher Activities",
                "; ".join(activities_of(step, "teacher")),
            )
            _append_labeled_value(
                lines,
                "Student Activities",
                "; ".join(activities_of(step, "student")),
            )
            self._append_blocks(lines, _object_list(step.get("blocks")))
        return "\n".join(lines).strip() + "\n"

    def _append_textbook_record(
        self,
        lines: list[str],
        record: TextbookRecordPayload,
        *,
        level: str = "###",
    ) -> None:
        lines.extend([f"{level} {record.record_id}", ""])
        _append_labeled_value(lines, "Title", record.title)
        _append_labeled_value(lines, "Record Type", record.record_type)
        _append_labeled_value(lines, "Section Ref", record.section_ref)
        _append_labeled_value(lines, "Source HTML Path", record.source_html_path)
        _append_labeled_value(lines, "Source Anchor ID", record.source_anchor_id)
        lines.extend(
            [
                "**Content**",
                "",
                "```text",
                _safe_markdown_text(record.preferred_text()),
                "```",
                "",
            ]
        )

    def _append_kc(
        self,
        lines: list[str],
        candidate_kc: CandidateKC,
        record_map: dict[str, TextbookRecordPayload],
    ) -> None:
        lines.extend([f"### {candidate_kc.kc_id}", "", "**Supporting Records**", ""])
        _append_labeled_value(lines, "Objective Text", candidate_kc.objective_text)
        _append_labeled_value(lines, "KC Type", candidate_kc.kc_type)
        _append_labeled_value(lines, "KC Focus", candidate_kc.kc_focus)
        _append_labeled_value(lines, "Source Form", candidate_kc.source_form)
        _append_labeled_value(lines, "Target Form", candidate_kc.target_form)
        _append_labeled_value(
            lines,
            "Curriculum Objective ID",
            candidate_kc.curriculum_objective_id,
        )
        _append_labeled_value(lines, "Ordering Notes", candidate_kc.ordering_notes)
        for record_id in candidate_kc.supporting_record_ids:
            record = record_map.get(record_id)
            if record is not None:
                self._append_textbook_record(lines, record, level="####")

    def _append_blocks(self, lines: list[str], blocks: list[object]) -> None:
        for raw_block in blocks:
            block = _object_dict(raw_block)
            if block is None:
                continue
            lines.extend(
                [
                    f"#### {block.get('id') or '-'}",
                    "",
                    f"**Type**  \n{_safe_markdown_text(block.get('type'))}",
                    "",
                ]
            )
            block_type = block.get("type")
            if block_type == "explanation":
                lines.extend(["```text", _safe_markdown_text(block.get("content")), "```", ""])
                continue
            if block_type == "worked_example":
                lines.extend(
                    [
                        f"**Problem**  \n{_safe_markdown_text(block.get('problem'))}",
                        "",
                    ]
                )
                for index, raw_step in enumerate(_object_list(block.get("steps")), start=1):
                    worked_step = _object_dict(raw_step)
                    if worked_step is None:
                        continue
                    lines.extend(
                        [
                            f"**Worked Step {index}**  "
                            f"\n{_safe_markdown_text(worked_step.get('content'))}",
                            "",
                        ]
                    )
                lines.extend(
                    [
                        f"**Final Answer**  \n{_safe_markdown_text(block.get('final_answer'))}",
                        "",
                    ]
                )
                continue
            if block_type == "practice":
                lines.extend(
                    [
                        f"**Question**  \n{_safe_markdown_text(block.get('question'))}",
                        "",
                        f"**Answer**  \n{_safe_markdown_text(block.get('answer'))}",
                        "",
                        f"**Lesson Objective ID**  "
                        f"\n{_safe_markdown_text(block.get('lesson_objective_id'))}",
                        "",
                        f"**Hints**  "
                        f"\n{_safe_markdown_text('; '.join(_string_list(block.get('hints'))))}",
                        "",
                    ]
                )
                continue
            if block_type == "visual":
                lines.extend(
                    [
                        f"**Variant**  \n{_safe_markdown_text(block.get('variant'))}",
                        "",
                        f"**Caption**  \n{_safe_markdown_text(block.get('caption'))}",
                        "",
                        f"**Source Record ID**  "
                        f"\n{_safe_markdown_text(block.get('source_record_id'))}",
                        "",
                        f"**URL**  \n{_safe_markdown_text(block.get('url'))}",
                        "",
                    ]
                )
