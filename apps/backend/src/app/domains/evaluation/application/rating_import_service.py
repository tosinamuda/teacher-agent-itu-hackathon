"""Bulk-import offline rater ratings — the research-manager batch path.

Each ``OfflineRatingRow`` resolves its packet by code + rater by display name
and upserts a single ``EvaluationRating``. Distinct from the interactive
``save_rating`` flow (which goes through full H1/H2 validation): bulk import
treats the source spreadsheet as authoritative and only reports per-row errors
via the ``RatingImportResult`` rollup.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.rater_identity import (
    RaterIdentityConflictError,
    stage_rater_identity,
)
from app.domains.evaluation.application.rating_ports import RatingImportStore
from app.domains.evaluation.application.result_schemas import RatingImportResult
from app.domains.evaluation.domain.records import RaterIdentity
from app.domains.evaluation.infrastructure.models import EvaluationRating
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.time import utc_now


@dataclass(frozen=True)
class OfflineRatingRow:
    """One row of an offline (bulk) rating import."""

    packet_code: str
    rater_name: str
    overall_score: float
    rubric_scores: dict[str, float]
    notes: str | None = None


class RatingImportApplicationService:
    """Own the bulk offline-import workflow (per-row resolve + upsert + error rollup)."""

    def __init__(self, store: RatingImportStore) -> None:
        self.store = store

    async def import_ratings(
        self,
        *,
        rows: list[OfflineRatingRow],
    ) -> RatingImportResult:
        """Process every row, returning ``(imported, updated, skipped, errors)``."""
        imported = 0
        updated = 0
        skipped = 0
        errors: list[str] = []
        for index, row in enumerate(rows):
            try:
                outcome = await self._upsert_row(row=row, row_index=index)
            except EvaluationApplicationError as error:
                await self.store.rollback()
                skipped += 1
                errors.append(f"row {index + 1}: {error.detail}")
                continue
            except IntegrityError:
                # Safety net: a concurrent writer won a unique key for this row and
                # _upsert_row's own conflict handling didn't absorb it. Roll back so
                # the session is usable for the next row — never let one row poison
                # the whole batch (the loop must complete + report).
                await self.store.rollback()
                skipped += 1
                errors.append(f"row {index + 1}: concurrent write conflict")
                continue
            if outcome is None:
                await self.store.rollback()
                skipped += 1
                errors.append(f"row {index + 1}: unknown packet_code {row.packet_code}")
            elif outcome == "imported":
                imported += 1
            else:
                updated += 1
        return RatingImportResult(
            imported=imported,
            updated=updated,
            skipped=skipped,
            errors=errors,
        )

    async def _upsert_row(
        self,
        *,
        row: OfflineRatingRow,
        row_index: int,
    ) -> str | None:
        """Resolve packet + rater for one row and upsert; ``None`` if the packet is unknown."""
        del row_index  # carried for symmetry with the caller's error-prefix concern
        persistence = self.store.rating_imports
        packet = await persistence.get_packet_by_code(packet_code=row.packet_code)
        if packet is None:
            return None
        # Snapshot packet fields to plain values BEFORE any rollback. _identify_rater
        # and the rating insert both roll back on a unique-key race, which expires
        # every ORM object in the session — a later ``packet.hypothesis`` read would
        # then trigger a refresh (async I/O under sync attribute access = MissingGreenlet).
        packet_id = packet.id
        packet_hypothesis = packet.hypothesis
        rater_id = (await self._identify_rater(display_name=row.rater_name)).id
        notes = self._build_notes(row.notes)
        existing = await persistence.get_rating(
            evaluation_packet_db_id=packet_id, rater_db_id=rater_id
        )
        if existing is None:
            try:
                await persistence.stage_rating(
                    EvaluationRating(
                        rating_id=new_public_id(PublicIdPrefix.EVALUATION_RATING),
                        evaluation_packet_db_id=packet_id,
                        rater_db_id=rater_id,
                        hypothesis=packet_hypothesis,
                        overall_score=float(row.overall_score),
                        rubric_scores=dict(row.rubric_scores),
                        notes=notes,
                        created_at=utc_now(),
                        updated_at=utc_now(),
                        submitted_at=utc_now(),
                    ),
                )
                await self.store.commit()
                return "imported"
            except IntegrityError:
                # Concurrent writer inserted this (packet, rater) rating first
                # (uq_evaluation_ratings_packet_rater) — roll back and fall through to
                # update the winner's row instead of failing the import.
                await self.store.rollback()
                existing = await persistence.get_rating(
                    evaluation_packet_db_id=packet_id, rater_db_id=rater_id
                )
                if existing is None:
                    raise
        existing.overall_score = float(row.overall_score)
        existing.rubric_scores = dict(row.rubric_scores)
        existing.notes = notes
        existing.updated_at = utc_now()
        existing.submitted_at = utc_now()
        await persistence.stage_rating(existing)
        await self.store.commit()
        return "updated"

    async def _identify_rater(
        self,
        *,
        display_name: str,
    ) -> RaterIdentity:
        """Find or create the rater for an offline import row (display-name keyed)."""
        normalized = display_name.strip()
        if len(normalized) < 2:
            raise EvaluationApplicationError(422, "rater_name_too_short")
        persistence = self.store.rating_imports
        try:
            return await stage_rater_identity(persistence, display_name=normalized)
        except RaterIdentityConflictError:
            # Concurrent import created the same-named rater first (display_name is
            # unique) — roll back and return the winner so both converge on one rater.
            await self.store.rollback()
            existing = await persistence.rater_identity_by_name(display_name=normalized)
            if existing is None:
                raise
            return existing

    @staticmethod
    def _build_notes(raw_notes: str | None) -> JsonObject:
        """Mark each imported rating as ``source=offline_import`` (+ optional notes text)."""
        notes: JsonObject = {"source": "offline_import"}
        if raw_notes:
            notes["notes"] = raw_notes
        return notes
