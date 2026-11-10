"""Flat H1/H2/source-audit rating dataset export for analysis (protocol §8)."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import Protocol

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.export_schemas import (
    ExperimentDataset,
    H1RatingRow,
    H2RatingRow,
    RatingRowBase,
    SourceAuditRow,
)

# WeasyPrint is the active renderer for the expert rater packs (HTML/CSS -> PDF):
# it renders reading-note / excerpt markdown natively and carries full Unicode, so
# no ``■`` missing-glyph boxes. The reportlab modules (``audit_pack_pdf``,
# ``h1_worksheet_pdf``) are kept in place as a fallback; ``H1_MAJOR_ISSUE_FLAGS``
# still lives in (and is imported from) ``h1_worksheet_pdf`` as its source of truth.
from app.domains.evaluation.application.rating_metrics import is_synthetic
from app.domains.evaluation.infrastructure.models import (
    EvaluationAuditItem,
    EvaluationAuditRating,
    EvaluationPacket,
    EvaluationRating,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.shared.experiment_enums import Hypothesis


async def export_experiment_dataset(
    reader: DatasetProjector, *, experiment_id: str
) -> ExperimentDataset:
    """Return the flat analysis dataset for one experiment."""
    return await reader.export_experiment_dataset(experiment_id=experiment_id)


class DatasetData(Protocol):
    async def list_all_ratings_for_packets(
        self, *, evaluation_packet_db_ids: list[uuid.UUID]
    ) -> list[EvaluationRating]: ...

    async def list_audit_items_for_executions(
        self, *, execution_db_ids: list[uuid.UUID]
    ) -> list[EvaluationAuditItem]: ...

    async def list_audit_ratings_for_items(
        self, *, audit_item_db_ids: list[uuid.UUID]
    ) -> list[EvaluationAuditRating]: ...


class DatasetExperiments(Protocol):
    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def list_packets_for_executions(
        self, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[EvaluationPacket]: ...

    async def list_condition_runs_for_executions(
        self, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentConditionRun]: ...


def _int_or_none(value: object) -> int | None:
    """Coerce a JSON rubric score to int (1-5), or None (bool excluded).

    Rubric scores are normalised to floats on save (``validate_h1_rubric_scores``),
    so whole-valued floats coerce to int rather than being dropped.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _float_or_none(value: object) -> float | None:
    """Coerce a JSON section score to float, or None (bool excluded)."""
    if isinstance(value, bool):
        return None
    return float(value) if isinstance(value, int | float) else None


def _str_or_none(value: object) -> str | None:
    """Coerce a JSON value to a non-empty str, or None."""
    return (value or None) if isinstance(value, str) else None


def _h1_row(base: RatingRowBase, rating: EvaluationRating) -> H1RatingRow:
    rubric = rating.rubric_scores or {}
    notes = rating.notes or {}
    major_issues = notes.get("major_issues")
    return H1RatingRow(
        **base.model_dump(),
        h1_composite=rating.overall_score,
        major_issues=(
            [str(flag) for flag in major_issues] if isinstance(major_issues, list) else []
        ),
        major_issue_other=_str_or_none(notes.get("major_issue_other")),
        objective_curriculum_alignment=_int_or_none(rubric.get("objective_curriculum_alignment")),
        taught_lesson_alignment=_int_or_none(rubric.get("taught_lesson_alignment")),
        scope_conceptual_correctness=_int_or_none(rubric.get("scope_conceptual_correctness")),
        clarity_usefulness=_int_or_none(rubric.get("clarity_usefulness")),
        learner_state_suitability=_int_or_none(rubric.get("learner_state_suitability")),
        scaffolding_appropriateness=_int_or_none(rubric.get("scaffolding_appropriateness")),
        challenge_calibration=_int_or_none(rubric.get("challenge_calibration")),
        misconception_support=_int_or_none(rubric.get("misconception_support")),
    )


def _h2_rows(
    base: RatingRowBase, rating: EvaluationRating, packet: EvaluationPacket
) -> list[H2RatingRow]:
    sections = rating.section_scores or {}
    rows: list[H2RatingRow] = []
    for section_id, scores in sections.items():
        raw = scores if isinstance(scores, dict) else {}
        # New shape nests candidate/base; old rows are flat (candidate-only).
        nested = isinstance(raw.get("candidate"), dict)
        section = raw["candidate"] if nested else raw
        base_section = raw["base"] if nested and isinstance(raw.get("base"), dict) else {}
        rows.append(
            H2RatingRow(
                **base.model_dump(),
                focal_learner_id=packet.experiment_focal_case_id,
                section_id=section_id,
                packet_score=rating.overall_score,
                learner_state_suitability=_float_or_none(section.get("learner_state_suitability")),
                scaffolding_appropriateness=_float_or_none(
                    section.get("scaffolding_appropriateness")
                ),
                challenge_calibration=_float_or_none(section.get("challenge_calibration")),
                misconception_support=_float_or_none(section.get("misconception_support")),
                objective_preservation=_float_or_none(section.get("objective_preservation")),
                section_score=_float_or_none(section.get("section_score")),
                base_learner_state_suitability=_float_or_none(
                    base_section.get("learner_state_suitability")
                ),
                base_scaffolding_appropriateness=_float_or_none(
                    base_section.get("scaffolding_appropriateness")
                ),
                base_challenge_calibration=_float_or_none(
                    base_section.get("challenge_calibration")
                ),
                base_misconception_support=_float_or_none(
                    base_section.get("misconception_support")
                ),
                base_objective_preservation=_float_or_none(
                    base_section.get("objective_preservation")
                ),
                base_section_score=_float_or_none(base_section.get("section_score")),
            )
        )
    return rows


class DatasetProjector:
    """Read-only construction of the flat evaluation analysis dataset."""

    def __init__(
        self,
        repository: DatasetData,
        *,
        experiment_repository: DatasetExperiments,
    ) -> None:
        self.repository = repository
        self.experiment_repository = experiment_repository

    async def export_experiment_dataset(
        self,
        *,
        experiment_id: str,
    ) -> ExperimentDataset:
        """Flat rating rows for analysis (Final Evaluation Protocol §8 export schemas).

        Emits H1, H2, and source-audit rows. ``condition_code`` is present (researcher
        export); a ``synthetic`` flag lets the analyst exclude dry-run proxy ratings.
        """
        experiment = await self.experiment_repository.get_experiment(experiment_id)
        if experiment is None:
            raise EvaluationApplicationError(404, "experiment_not_found")
        executions = await self.experiment_repository.list_executions_for_experiment(experiment.id)
        execution_ids = [execution.id for execution in executions]
        packets = await self.experiment_repository.list_packets_for_executions(
            execution_db_ids=execution_ids
        )
        condition_runs = await self.experiment_repository.list_condition_runs_for_executions(
            execution_db_ids=execution_ids
        )
        run_code = {run.experiment_condition_run_id: run.condition_code for run in condition_runs}
        packet_by_id = {packet.id: packet for packet in packets}
        ratings = await self.repository.list_all_ratings_for_packets(
            evaluation_packet_db_ids=[packet.id for packet in packets]
        )

        h1_rows: list[H1RatingRow] = []
        h2_rows: list[H2RatingRow] = []
        for rating in ratings:
            packet = packet_by_id.get(rating.evaluation_packet_db_id)
            if packet is None:
                continue
            base = RatingRowBase(
                experiment_id=experiment_id,
                lesson_id=experiment_id,
                condition_code=run_code.get(packet.primary_condition_run_id),
                packet_id=packet.evaluation_packet_id,
                rater_id=str(rating.rater_db_id),
                synthetic=is_synthetic(rating),
            )
            if rating.hypothesis == Hypothesis.H1:
                h1_rows.append(_h1_row(base, rating))
            else:
                h2_rows.extend(_h2_rows(base, rating, packet))

        items = await self.repository.list_audit_items_for_executions(
            execution_db_ids=[execution.id for execution in executions]
        )
        item_by_id = {item.id: item for item in items}
        audit_ratings = await self.repository.list_audit_ratings_for_items(
            audit_item_db_ids=[item.id for item in items]
        )
        audit_rows: list[SourceAuditRow] = []
        for audit_rating in audit_ratings:
            item = item_by_id.get(audit_rating.audit_item_db_id)
            if item is None:
                continue
            audit_rows.append(
                SourceAuditRow(
                    audit_item_id=item.audit_item_id,
                    lesson_id=experiment_id,
                    condition_code=item.condition_code,
                    generated_excerpt=item.generated_excerpt,
                    source_ref=item.source_ref,
                    source_excerpt=item.source_excerpt,
                    rater_id=str(audit_rating.rater_db_id),
                    source_relevance=audit_rating.source_relevance,
                    support_sufficiency=audit_rating.support_sufficiency,
                    faithfulness=audit_rating.faithfulness,
                    scope_correctness=audit_rating.scope_correctness,
                    source_grounding_score=audit_rating.source_grounding_score,
                    synthetic=bool((audit_rating.notes or {}).get("synthetic")),
                )
            )

        return ExperimentDataset(
            experiment_id=experiment_id,
            h1_ratings=h1_rows,
            h2_ratings=h2_rows,
            source_audit=audit_rows,
        )
