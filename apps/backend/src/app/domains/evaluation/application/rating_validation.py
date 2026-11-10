"""Validate a rater's submission (H1 rubric or H2 sections) against the packet.

Owns the rating-validation lifecycle: the H1 rubric-score check, the H2 per-
section + per-dimension check, the sections-shape lookup that drives the H2
validator, and the not-found policies (review-pack, artefact, primary-run,
H2 base-run) that surface errors when a packet is incomplete.

These helpers are also consumed by the main service for DTO assembly + the
``_packet_is_rater_ready`` check, since the same lookups + sections shape feed
both the rater queue and the validator. Centralising them here keeps the
not-found policy in one place.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol, cast

from pydantic import ValidationError

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.evaluation.application.constants import H1_RUBRIC, H2_RUBRIC
from app.domains.evaluation.application.errors import EvaluationApplicationError, bounded_int
from app.domains.evaluation.application.packet_payloads import PacketDetailPayloads
from app.domains.evaluation.application.packet_runtime import PacketRuntimeContext
from app.domains.evaluation.application.peer_ports import PackArtefactsPort
from app.domains.evaluation.infrastructure.models import EvaluationPacket
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


class SessionPlanRuntime(Protocol):
    """The packet context required to shape H2 rating sections."""

    @property
    def session_plan(self) -> SessionPlanView: ...


def _stripped_text_or_none(value: object) -> str | None:
    """Return ``value`` stripped + non-empty, or ``None`` otherwise.

    Local replacement for the retired ``json_coerce.as_text``. Private to
    this module — the json_coerce shared helper was load-bearing across
    domains; the equivalent narrowing is moved to where each boundary lives.
    """
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


if TYPE_CHECKING:
    from app.domains.experiments.infrastructure.models import ExperimentConditionRun


def mean_score(values: list[float]) -> float:
    """Mean of ``values`` (422 if empty — a rating must score at least one dimension)."""
    if not values:
        raise EvaluationApplicationError(422, "empty_score_set")
    return sum(values) / len(values)


class RatingValidationService:
    """Own the H1/H2 score validation + the sections + not-found policies they need."""

    def __init__(self, artefact_repository: PackArtefactsPort) -> None:
        self.artefact_repository = artefact_repository
        self.payloads = PacketDetailPayloads()

    # ===== Score validation =====

    def validate_h1_rubric_scores(
        self,
        rubric_scores: Mapping[str, int | float],
    ) -> dict[str, float]:
        """Check every H1 rubric dimension is present + 1..5, return as floats."""
        expected_ids = {criterion["criterion_id"] for criterion in H1_RUBRIC}
        if set(rubric_scores) != expected_ids:
            raise EvaluationApplicationError(422, "h1_rubric_dimensions_incomplete")

        normalized: dict[str, float] = {}
        for criterion in H1_RUBRIC:
            criterion_id = cast(str, criterion["criterion_id"])
            normalized[criterion_id] = float(
                bounded_int(
                    rubric_scores.get(criterion_id),
                    minimum=1,
                    maximum=5,
                    error_detail="h1_rubric_score_out_of_range",
                )
            )
        return normalized

    async def validate_h2_scores(
        self,
        *,
        packet: EvaluationPacket,
        runtime: PacketRuntimeContext,
        section_scores: list[dict[str, object]] | None,
        diagnostic_scores: JsonObject | None,
        base_section_scores: list[dict[str, object]] | None = None,
    ) -> tuple[dict[str, float | None], JsonObject, JsonObject, float]:
        """Check every H2 section is scored on the 4 required + 1 optional dimensions.

        Scores the candidate (P1) pack; ``base_section_scores`` optionally carries
        the rater's independent scores for the base (P0) pack. The persisted
        per-section value is nested ``{"candidate": {...}, "base": {...} | None}``;
        the dimensional rubric means + overall score are taken from the candidate
        pack (unchanged). Returns ``(rubric_scores_dimensional, section_scores,
        diagnostic_scores, overall_score)`` ready to persist.
        """
        del diagnostic_scores  # H2 has no separate diagnostic; preserved for the contract.
        if not section_scores:
            raise EvaluationApplicationError(422, "h2_section_scores_required")

        valid_section_ids = await self._h2_valid_section_ids(runtime=runtime, packet=packet)
        candidate_scores, dimension_values, section_means = self._collect_h2_section_scores(
            section_scores=section_scores,
            valid_section_ids=valid_section_ids,
        )
        if set(candidate_scores) != valid_section_ids:
            raise EvaluationApplicationError(422, "h2_section_score_incomplete")

        base_scores: dict[str, JsonObject] = {}
        if base_section_scores:
            base_scores, _, _ = self._collect_h2_section_scores(
                section_scores=base_section_scores,
                valid_section_ids=valid_section_ids,
            )
            if set(base_scores) != valid_section_ids:
                raise EvaluationApplicationError(422, "h2_base_section_score_incomplete")

        merged: dict[str, JsonObject] = {
            section_id: cast(
                JsonObject, {"candidate": candidate_row, "base": base_scores.get(section_id)}
            )
            for section_id, candidate_row in candidate_scores.items()
        }
        rubric_scores = {
            criterion_id: (mean_score(values) if values else None)
            for criterion_id, values in dimension_values.items()
        }
        return (
            rubric_scores,
            cast(JsonObject, merged),
            {},
            mean_score(section_means),
        )

    async def _h2_valid_section_ids(
        self,
        *,
        runtime: PacketRuntimeContext,
        packet: EvaluationPacket,
    ) -> set[str]:
        """Resolve the valid section ids for an H2 packet (the BASE-pack section ids)."""
        primary_run = self.primary_run_or_error(runtime=runtime, packet=packet)
        candidate_artefact = await self.artefact_for_run(run=primary_run)
        candidate_manifest = self.review_pack_or_error(candidate_artefact)
        base_run = self.h2_base_run_or_error(runtime=runtime, packet=packet)
        base_artefact = await self.artefact_for_run(run=base_run)
        base_manifest = self.review_pack_or_error(base_artefact)
        sections = await self.h2_section_payloads(
            runtime=runtime,
            base_artefact=base_artefact,
            base_manifest=base_manifest,
            candidate_artefact=candidate_artefact,
            candidate_manifest=candidate_manifest,
        )
        return {cast(str, section["section_id"]) for section in sections}

    @staticmethod
    def _collect_h2_section_scores(
        *,
        section_scores: list[dict[str, object]],
        valid_section_ids: set[str],
    ) -> tuple[dict[str, JsonObject], dict[str, list[float]], list[float]]:
        """Iterate the submitted section scores, bounds-check each, accumulate dimension means."""
        submitted_scores: dict[str, JsonObject] = {}
        dimension_values: dict[str, list[float]] = {
            cast(str, criterion["criterion_id"]): [] for criterion in H2_RUBRIC
        }
        section_means: list[float] = []
        for raw in section_scores:
            section_id = _stripped_text_or_none(raw.get("section_id"))
            if section_id is None:
                raise EvaluationApplicationError(422, "h2_section_id_required")
            if section_id in submitted_scores:
                raise EvaluationApplicationError(422, "h2_section_duplicate")
            if section_id not in valid_section_ids:
                raise EvaluationApplicationError(422, "h2_section_unknown")
            row = _check_h2_section_row(raw)
            submitted_scores[section_id] = cast(JsonObject, row)
            section_means.append(cast(float, row["section_score"]))
            _accumulate_h2_dimensions(row, dimension_values)
        return submitted_scores, dimension_values, section_means

    # ===== Sections shape =====

    async def h2_section_payloads(
        self,
        *,
        runtime: SessionPlanRuntime,
        base_artefact: Artefact,
        base_manifest: PostClassReviewPack,
        candidate_artefact: Artefact,
        candidate_manifest: PostClassReviewPack,
    ) -> list[JsonObject]:
        """Build the H2 rater-packet sections from the BASE pack (Evaluation Protocol §4).

        Iterates base sections so a personalised section the candidate drops is
        visible + penalised under objective preservation. Each section pairs the
        base step with the candidate step sharing its step_id (stable across
        P0/P1); ``candidate_missing`` flags the drop.
        """
        candidate_plan_steps = await self.plan_steps_by_step_id(artefact=candidate_artefact)
        base_plan_steps = await self.plan_steps_by_step_id(artefact=base_artefact)
        objective_text_by_id = self.payloads.objective_text_by_id(runtime.session_plan)
        candidate_steps_by_id = {step.step_id: step for step in candidate_manifest.steps}

        sections: list[JsonObject] = []
        for base_step in base_manifest.steps:
            plan_step = base_plan_steps.get(base_step.step_id) or candidate_plan_steps.get(
                base_step.step_id
            )
            lesson_objective_id = base_step.lesson_objective_id or (
                _stripped_text_or_none(plan_step.get("lesson_objective_id")) if plan_step else None
            )
            if lesson_objective_id is None:
                continue
            candidate_step = candidate_steps_by_id.get(base_step.step_id)
            sections.append(
                {
                    "section_id": base_step.step_id,
                    "step_id": base_step.step_id,
                    "title": base_step.title,
                    "step_kind": base_step.step_kind,
                    "instructional_type": base_step.instructional_type,
                    "lesson_objective_id": lesson_objective_id,
                    "objective_text": objective_text_by_id.get(lesson_objective_id),
                    "base_step": cast(
                        JsonObject,
                        base_step.model_dump(mode="json", exclude_none=True),
                    ),
                    "candidate_step": (
                        cast(JsonObject, candidate_step.model_dump(mode="json", exclude_none=True))
                        if candidate_step is not None
                        else None
                    ),
                    "candidate_missing": candidate_step is None,
                }
            )
        if not sections:
            raise EvaluationApplicationError(409, "h2_packet_sections_missing")
        return sections

    async def plan_steps_by_step_id(
        self,
        *,
        artefact: Artefact,
    ) -> dict[str, JsonObject]:
        """Build a ``step_id -> plan-step`` index from the artefact's source plan."""
        if not artefact.source_artefact_plan_id:
            return {}
        plan = await self.artefact_repository.get_plan(artefact.source_artefact_plan_id)
        if plan is None:
            return {}
        payload = plan.payload if isinstance(plan.payload, dict) else {}
        raw_steps = payload.get("steps")
        steps: list[JsonObject] = (
            [item for item in raw_steps if isinstance(item, dict)]
            if isinstance(raw_steps, list)
            else []
        )
        indexed_steps: dict[str, JsonObject] = {}
        for raw_step in steps:
            step_id = _stripped_text_or_none(raw_step.get("step_id"))
            if step_id is None:
                continue
            indexed_steps[step_id] = raw_step
        return indexed_steps

    # ===== Not-found policies =====

    @staticmethod
    def review_pack_or_error(artefact: Artefact) -> PostClassReviewPack:
        """Parse the artefact's manifest as a ``PostClassReviewPack``; 409 if invalid."""
        try:
            return PostClassReviewPack.model_validate(artefact.manifest)
        except ValidationError as error:
            raise EvaluationApplicationError(409, "review_pack_manifest_invalid") from error

    async def artefact_for_run(
        self,
        *,
        run: ExperimentConditionRun,
    ) -> Artefact:
        """Fetch the current artefact for a condition run; 409/404 if absent.

        Resolved via the back-pointer (a run's output points back at the run),
        not a stored forward id on the run.
        """
        artefact = await self.artefact_repository.current_artefact_for_condition_run(
            run.experiment_condition_run_id
        )
        if artefact is None:
            raise EvaluationApplicationError(404, "packet_artefact_not_found")
        return artefact

    @staticmethod
    def primary_run_or_error(
        *,
        runtime: PacketRuntimeContext,
        packet: EvaluationPacket,
    ) -> ExperimentConditionRun:
        """Return the packet's primary condition run; raise 404 if not present in the runtime."""
        run = runtime.run_by_id.get(packet.primary_condition_run_id)
        if run is None:
            raise EvaluationApplicationError(404, "packet_primary_run_not_found")
        return run

    @staticmethod
    def h2_base_run_or_error(
        *,
        runtime: PacketRuntimeContext,
        packet: EvaluationPacket,
    ) -> ExperimentConditionRun:
        """Return the P0 (base) run for an H2 packet; fall back to the primary if it is P0."""
        for condition_run_id in packet.condition_run_ids or []:
            run = runtime.run_by_id.get(condition_run_id)
            if run is None:
                continue
            if run.condition_code == "P0":
                return run
        primary_run = RatingValidationService.primary_run_or_error(runtime=runtime, packet=packet)
        if primary_run.condition_code == "P0":
            return primary_run
        raise EvaluationApplicationError(404, "packet_base_run_not_found")


# ===== Module-level helpers for H2 section-row scoring =====


def _check_h2_section_row(raw: dict[str, object]) -> dict[str, object]:
    """Bounds-check the 4 required + 1 optional H2 dimensions for one section row."""
    learner_state = bounded_int(
        raw.get("learner_state_suitability"),
        minimum=1,
        maximum=5,
        error_detail="h2_learner_state_out_of_range",
    )
    scaffolding = bounded_int(
        raw.get("scaffolding_appropriateness"),
        minimum=1,
        maximum=5,
        error_detail="h2_scaffolding_out_of_range",
    )
    challenge = bounded_int(
        raw.get("challenge_calibration"),
        minimum=1,
        maximum=5,
        error_detail="h2_challenge_out_of_range",
    )
    objective = bounded_int(
        raw.get("objective_preservation"),
        minimum=1,
        maximum=5,
        error_detail="h2_objective_preservation_out_of_range",
    )
    misconception_raw = raw.get("misconception_support")
    misconception: int | None = None
    if misconception_raw is not None:
        misconception = bounded_int(
            misconception_raw,
            minimum=1,
            maximum=5,
            error_detail="h2_misconception_out_of_range",
        )
    applicable = [
        float(learner_state),
        float(scaffolding),
        float(challenge),
        float(objective),
    ]
    if misconception is not None:
        applicable.append(float(misconception))
    return {
        "learner_state_suitability": learner_state,
        "scaffolding_appropriateness": scaffolding,
        "challenge_calibration": challenge,
        "misconception_support": misconception,
        "objective_preservation": objective,
        "section_score": mean_score(applicable),
    }


def _accumulate_h2_dimensions(
    row: dict[str, object], dimension_values: dict[str, list[float]]
) -> None:
    """Push each dimension's value (skip ``misconception_support`` when ``None``) onto its list."""
    dimension_values["learner_state_suitability"].append(
        float(cast(int, row["learner_state_suitability"]))
    )
    dimension_values["scaffolding_appropriateness"].append(
        float(cast(int, row["scaffolding_appropriateness"]))
    )
    dimension_values["challenge_calibration"].append(float(cast(int, row["challenge_calibration"])))
    dimension_values["objective_preservation"].append(
        float(cast(int, row["objective_preservation"]))
    )
    misconception = row.get("misconception_support")
    if misconception is not None:
        dimension_values["misconception_support"].append(float(cast(int, misconception)))
