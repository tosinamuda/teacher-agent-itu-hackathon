"""Source-grounding audit lane (C2-C4).

Materialise audit items, render the offline audit pack, and run the rater
audit queue / detail / save flow.
"""

from __future__ import annotations

import re
import uuid
from typing import Protocol

from app.config import CONFIG
from app.domains.evaluation.application.assignment_scope import AssignmentScope
from app.domains.evaluation.application.audit_ports import AuditPresentationData
from app.domains.evaluation.application.constants import (
    SOURCE_AUDIT_CRITERIA,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.source_record_format import friendly_source_record_id

# WeasyPrint is the active renderer for the expert rater packs (HTML/CSS -> PDF):
# it renders reading-note / excerpt markdown natively and carries full Unicode, so
# no ``■`` missing-glyph boxes. The reportlab modules (``audit_pack_pdf``,
# ``h1_worksheet_pdf``) are kept in place as a fallback; ``H1_MAJOR_ISSUE_FLAGS``
# still lives in (and is imported from) ``h1_worksheet_pdf`` as its source of truth.
from app.domains.evaluation.application.worksheet_html.audit_renderer import (
    render_source_audit_pack_html_pdf,
)
from app.domains.evaluation.infrastructure.models import (
    EvaluationAuditItem,
    EvaluationAuditRating,
)
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.shared.json_types import JsonObject
from app.shared.time import as_utc


class AuditPresentationExperiments(Protocol):
    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def get_execution_by_db_id(
        self, execution_db_id: uuid.UUID
    ) -> ExperimentExecution | None: ...

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...


# Rater-facing audit excerpt cleanup. Inline ``REF-N`` markers and the LLM's
# editorial parenthesised ``(Sources: REF-1 for X; REF-2 for Y.)`` annotation
# are stripped from the excerpt the API returns — the rater anchors against
# the right-column cited source label, so the markers add noise without help.
# Mirrors the worksheet renderer's strip on the PDF side so both surfaces
# present the same text.
_AUDIT_INLINE_REF_RE = re.compile(
    r"\s*(?:\(\s*REF-\d+\s*\)|\[\s*REF-\d+\s*\]|\bREF-\d+\b)",
    re.IGNORECASE,
)
_AUDIT_EDITORIAL_SOURCES_RE = re.compile(
    r"\s*\(\s*sources?\s*:[^()]*\)",
    re.IGNORECASE,
)
_AUDIT_SOURCES_LINE_RE = re.compile(
    r"^[ \t]*_?\s*sources?\s*:.*?_?[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)


def _strip_audit_excerpt(text: str | None) -> str | None:
    """Strip REF-N markers + editorial sources from an audit excerpt for display."""
    if text is None:
        return None
    cleaned = _AUDIT_EDITORIAL_SOURCES_RE.sub("", text)
    cleaned = _AUDIT_SOURCES_LINE_RE.sub("", cleaned)
    cleaned = _AUDIT_INLINE_REF_RE.sub("", cleaned)
    return cleaned.strip() or None


class AuditPresenter:
    def __init__(
        self,
        repository: AuditPresentationData,
        *,
        experiment_repository: AuditPresentationExperiments,
    ) -> None:
        self.repository = repository
        self.experiment_repository = experiment_repository
        self.assignment_scope = AssignmentScope(
            self.repository, experiment_repository=self.experiment_repository
        )

    async def export_source_audit_pack(
        self,
        *,
        experiment_id: str,
    ) -> tuple[bytes, str]:
        """Render the offline source-grounding audit pack PDF for an experiment."""
        experiment = await self.experiment_repository.get_experiment(experiment_id)
        if experiment is None:
            raise EvaluationApplicationError(404, "experiment_not_found")
        executions = await self.experiment_repository.list_executions_for_experiment(experiment.id)
        items = await self.repository.list_audit_items_for_executions(
            execution_db_ids=[execution.id for execution in executions]
        )
        detail = {
            "textbook_name": CONFIG.textbook_name,
            "items": [
                {
                    "audit_item_id": item.audit_item_id,
                    "condition_code": item.condition_code,
                    "lesson_objective_id": item.lesson_objective_id,
                    "objective_text": item.objective_text,
                    "generated_excerpt": item.generated_excerpt,
                    "source_ref": item.source_ref,
                    "source_record_id": item.source_record_id,
                    "source_excerpt": item.source_excerpt,
                    "figure_url": item.figure_url,
                    "figure_caption": item.figure_caption,
                    "scope_boundary": item.scope_boundary,
                }
                for item in items
            ],
        }
        pdf_bytes = render_source_audit_pack_html_pdf(detail)
        return pdf_bytes, f"{experiment_id}-source-audit-pack.pdf"

    async def list_audit_queue(
        self,
        *,
        rater_id: str,
    ) -> list[JsonObject]:
        """This rater's *assigned* source-audit items (empty when none assigned).

        Scoped to ``rater_assignments`` (hypothesis ``audit``, ``scope_id`` ==
        ``audit_item_id``); an unassigned rater — or one with no rater identity —
        gets an empty queue rather than every item in the pool.
        """
        rater = await self.repository.get_rater(rater_id=rater_id)
        if rater is None:
            return []
        assigned_item_ids = await self.assignment_scope.assigned_audit_item_ids(
            rater_db_id=rater.id
        )
        items = [
            item
            for item in await self.repository.list_audit_items()
            if item.audit_item_id in assigned_item_ids
        ]
        ratings = await self.repository.list_audit_ratings_for_items(
            audit_item_db_ids=[item.id for item in items]
        )
        my_rating_item_ids = {
            rating.audit_item_db_id for rating in ratings if rating.rater_db_id == rater.id
        }
        return [
            {
                "audit_item_id": item.audit_item_id,
                "condition_code": item.condition_code,
                "lesson_objective_id": item.lesson_objective_id,
                # Surface the friendly objective text so the rater-facing queue
                # can show "Common multiples · cited REF-1" instead of "lop01".
                "objective_text": item.objective_text,
                "source_ref": item.source_ref,
                "status": item.status,
                "rated": item.id in my_rating_item_ids,
            }
            for item in items
        ]

    async def get_audit_item_detail(
        self,
        *,
        audit_item_id: str,
        rater_id: str,
    ) -> dict[str, object]:
        item = await self.repository.get_audit_item(audit_item_id=audit_item_id)
        if item is None:
            raise EvaluationApplicationError(404, "audit_item_not_found")
        existing = await self._existing_audit_rating(item=item, rater_id=rater_id)
        # Rater-facing display: friendly source label and the excerpt with
        # inline REF-N markers stripped (the rater anchors against the
        # right-column cited source). The raw `item.source_record_id` stays
        # in the DB / analysis paths.
        return {
            "audit_item_id": item.audit_item_id,
            "condition_code": item.condition_code,
            "lesson_objective_id": item.lesson_objective_id,
            "objective_text": item.objective_text,
            "generated_excerpt": _strip_audit_excerpt(item.generated_excerpt),
            "source_ref": item.source_ref,
            "source_record_id": friendly_source_record_id(item.source_record_id),
            "source_excerpt": item.source_excerpt,
            "figure_url": item.figure_url,
            "figure_caption": item.figure_caption,
            "scope_boundary": item.scope_boundary,
            "criteria": list(SOURCE_AUDIT_CRITERIA),
            "existing_rating": self._audit_rating_payload(existing),
        }

    async def _existing_audit_rating(
        self,
        *,
        item: EvaluationAuditItem,
        rater_id: str,
    ) -> EvaluationAuditRating | None:
        rater = await self.repository.get_rater(rater_id=rater_id)
        if rater is None:
            return None
        return await self.repository.get_audit_rating(
            audit_item_db_id=item.id, rater_db_id=rater.id
        )

    def _audit_rating_payload(self, rating: EvaluationAuditRating | None) -> JsonObject | None:
        if rating is None:
            return None
        return {
            "rating_id": rating.rating_id,
            "source_relevance": rating.source_relevance,
            "support_sufficiency": rating.support_sufficiency,
            "faithfulness": rating.faithfulness,
            "scope_correctness": rating.scope_correctness,
            "source_grounding_score": rating.source_grounding_score,
            "submitted_at": (
                as_utc(rating.submitted_at).isoformat() if rating.submitted_at else None
            ),
        }
