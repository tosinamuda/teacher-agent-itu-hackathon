"""Flatten a typed ``SessionContext`` into the four generation-time scopes.

``SessionContextPayloadBuilder.build`` owns the mapping from the rich,
domain-internal ``SessionContext`` to the four scope DTOs the generator + the
validator consume: ``SessionScope`` (lesson identity), ``CurriculumScope``
(curriculum-derived state), ``ValidationScope`` (the identity fields the
validator must check), and the assembled ``reference_context`` list. The
output is the ``PlanGenerationPayloads`` frozen dataclass.

The curriculum-objective-id mapping is the most-likely-to-change part: when
curated linkage is present we use its authoritative ids (so the generator's
``lesson_objectives`` match by construction); otherwise we synthesise ids
from the curriculum performance/session objectives.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domains.artefacts.types.lesson_plan.application.schemas import (
    CurriculumScope,
    SessionScope,
    ValidationScope,
)
from app.domains.artefacts.types.lesson_plan.domain.objective_ids import performance_objective_id
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class PlanGenerationPayloads:
    """The four-scope generation payload assembled from a typed SessionContext."""

    session_scope: SessionScope
    curriculum_scope: CurriculumScope
    reference_context: list[JsonObject]
    validation_scope: ValidationScope
    grounding_mode: str = "manual_linkage"
    curated_objectives: list[JsonObject] = field(default_factory=list)


class SessionContextPayloadBuilder:
    """Build the four-scope ``PlanGenerationPayloads`` from a ``SessionContext``."""

    def build(self, session_context: SessionContext) -> PlanGenerationPayloads:
        """Assemble the four scopes + reference context for one generation call."""
        curriculum_objectives = self._curriculum_objective_refs(session_context)
        return PlanGenerationPayloads(
            session_scope=self._session_scope(session_context),
            curriculum_scope=self._curriculum_scope(session_context, curriculum_objectives),
            reference_context=self._reference_context(session_context),
            validation_scope=self._validation_scope(session_context),
            grounding_mode=session_context.grounding_mode,
            curated_objectives=list(session_context.curated_objectives),
        )

    @staticmethod
    def _curriculum_objective_refs(session_context: SessionContext) -> list[JsonObject]:
        """Surface the curated linkage ids (or synthesise from performance/session objectives)."""
        # The curated linkage carries the AUTHORITATIVE curriculum_objective_id. Expose
        # those same ids on the plan's curriculum_objectives so the lesson objectives
        # (which reference them) match by construction — no synthetic cur_objNN id and
        # no heuristic text/order remap. Dedupe by id, keep first-seen order, and pair
        # each with its performance-objective text when available.
        performance = [
            text.strip()
            for text in session_context.performance_objectives
            if isinstance(text, str) and text.strip()
        ]
        curated_refs: list[JsonObject] = []
        seen: set[str] = set()
        for objective in session_context.curated_objectives:
            curriculum_objective_id = str(objective.get("curriculum_objective_id") or "").strip()
            if not curriculum_objective_id or curriculum_objective_id in seen:
                continue
            seen.add(curriculum_objective_id)
            order = len(curated_refs)
            objective_text = (
                performance[order]
                if order < len(performance)
                else str(objective.get("objective_text") or "").strip()
            )
            curated_refs.append(
                {
                    "curriculum_objective_id": curriculum_objective_id,
                    "objective_text": objective_text,
                    "objective_order": order + 1,
                }
            )
        if curated_refs:
            return curated_refs

        # Fallback (no curated linkage, e.g. curriculum_only): synthesise ids from the
        # performance/session objectives, which carry no canonical id of their own.
        source_objectives = performance or [
            text.strip()
            for text in session_context.session_objectives
            if isinstance(text, str) and text.strip()
        ]
        return [
            {
                "curriculum_objective_id": (
                    performance_objective_id(session_context.subtopic_id, index)
                    if session_context.subtopic_id
                    else f"cur_obj{index:02d}"
                ),
                "objective_text": objective,
                "objective_order": index,
            }
            for index, objective in enumerate(source_objectives, start=1)
        ]

    @staticmethod
    def _reference_context(session_context: SessionContext) -> list[JsonObject]:
        """Concatenate reference materials + textbook records into a single list."""
        reference_context = list(session_context.reference_materials)
        for textbook_ref in session_context.textbook_references:
            reference_context.append(
                {
                    "type": "textbook_record",
                    "record_id": textbook_ref.get("record_id")
                    or textbook_ref.get("section_ref", ""),
                    "title": textbook_ref.get("title", ""),
                    "section_ref": textbook_ref.get("section_ref", ""),
                    "content": textbook_ref.get("content", ""),
                    "prompt_text": textbook_ref.get("prompt_text", ""),
                    "answer_text": textbook_ref.get("answer_text", ""),
                    "retrieval_text": textbook_ref.get("retrieval_text", ""),
                    "record_type": textbook_ref.get("record_type"),
                    "primary_subtopic_id": textbook_ref.get("primary_subtopic_id"),
                    "matched_subtopic_id": textbook_ref.get("matched_subtopic_id"),
                    "source_html_path": textbook_ref.get("source_html_path"),
                    "source_anchor_id": textbook_ref.get("source_anchor_id"),
                    "asset_refs": textbook_ref.get("asset_refs"),
                }
            )
        return reference_context

    @staticmethod
    def _session_scope(session_context: SessionContext) -> SessionScope:
        """Lesson-identity fields the generator + generation log need."""
        return SessionScope(
            session_id=session_context.session_id,
            subject=session_context.subject,
            track=session_context.track,
            grade=session_context.grade,
            term=session_context.term,
            week=session_context.week,
            day_index=session_context.day_index,
            topic=session_context.topic,
            subtopic=session_context.subtopic,
            duration_minutes=session_context.duration_minutes,
            session_objectives=session_context.session_objectives,
            theme=session_context.theme,
            performance_objectives=session_context.performance_objectives,
            entry_behaviour=session_context.entry_behaviour,
            instructional_materials=session_context.instructional_materials,
            average_age=session_context.average_age,
        )

    @staticmethod
    def _curriculum_scope(
        session_context: SessionContext,
        curriculum_objectives: list[JsonObject],
    ) -> CurriculumScope:
        """Curriculum-derived state the generator reads while drafting the lesson."""
        return CurriculumScope(
            subject=session_context.subject,
            track=session_context.track,
            grade=session_context.grade,
            term=session_context.term,
            week=session_context.week,
            theme=session_context.theme,
            topic=session_context.topic,
            subtopic=session_context.subtopic,
            curriculum_objectives=curriculum_objectives,
            general_objectives=session_context.general_objectives,
            session_objectives=session_context.session_objectives,
            performance_objectives=session_context.performance_objectives,
            teacher_activities=session_context.teacher_activities,
            student_activities=session_context.student_activities,
            instructional_materials=session_context.instructional_materials,
            evaluation_guide=session_context.evaluation_guide,
            entry_behaviour=session_context.entry_behaviour,
        )

    @staticmethod
    def _validation_scope(session_context: SessionContext) -> ValidationScope:
        """Identity fields the validator must confirm the generated plan preserves."""
        return ValidationScope(
            session_id=session_context.session_id,
            subject=session_context.subject,
            track=session_context.track,
            grade=session_context.grade,
            term=session_context.term,
            week=session_context.week,
            topic=session_context.topic,
            subtopic=session_context.subtopic,
        )
