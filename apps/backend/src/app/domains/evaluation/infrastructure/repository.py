from __future__ import annotations

import uuid
from typing import cast

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.evaluation.application.rater_identity import RaterIdentityConflictError
from app.domains.evaluation.domain.records import (
    AssignmentRecord,
    AuditItemRecord,
    AuditRatingRecord,
    RaterIdentity,
    RatingRecord,
)
from app.domains.evaluation.infrastructure.models import (
    EvaluationAuditItem,
    EvaluationAuditRating,
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
    RaterAssignment,
)
from app.shared.experiment_enums import PacketStatus


class EvaluationRepository:
    """Evaluation persistence bound to one SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_rater(
        self,
        *,
        rater_id: str,
    ) -> EvaluationRater | None:
        result = await self._session.execute(
            select(EvaluationRater).where(EvaluationRater.rater_id == rater_id)
        )
        return result.scalars().first()

    async def rater_identity(self, *, rater_id: str) -> RaterIdentity | None:
        return self._identity(await self.get_rater(rater_id=rater_id))

    async def rater_identity_for_user(self, *, user_id: uuid.UUID) -> RaterIdentity | None:
        return self._identity(await self.get_rater_by_user_id(user_id=user_id))

    async def rater_identity_by_name(self, *, display_name: str) -> RaterIdentity | None:
        return self._identity(await self.get_rater_by_name(display_name=display_name))

    async def stage_rater_identity(self, identity: RaterIdentity) -> RaterIdentity:
        row = EvaluationRater(
            id=identity.id,
            rater_id=identity.rater_id,
            display_name=identity.display_name,
            user_id=identity.user_id,
            created_at=identity.created_at,
            updated_at=identity.updated_at,
        )
        self._session.add(row)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise RaterIdentityConflictError from exc
        return identity

    async def list_raters(self) -> list[EvaluationRater]:
        """Every rater the app can assign, by name — drives the admin picker."""
        result = await self._session.execute(
            select(EvaluationRater)
            .where(EvaluationRater.origin == "app")
            .order_by(EvaluationRater.display_name.asc())
        )
        return list(result.scalars().all())

    async def list_rater_identities(self) -> list[RaterIdentity]:
        identities: list[RaterIdentity] = []
        for row in await self.list_raters():
            identity = self._identity(row)
            if identity is not None:
                identities.append(identity)
        return identities

    async def get_rater_by_name(
        self,
        *,
        display_name: str,
    ) -> EvaluationRater | None:
        result = await self._session.execute(
            select(EvaluationRater).where(EvaluationRater.display_name == display_name)
        )
        return result.scalars().first()

    async def get_rater_by_user_id(
        self,
        *,
        user_id: uuid.UUID,
    ) -> EvaluationRater | None:
        """The human rater profile bound to this login user (None for synthetic)."""
        result = await self._session.execute(
            select(EvaluationRater).where(EvaluationRater.user_id == user_id)
        )
        return result.scalars().first()

    async def stage_rater(self, rater: EvaluationRater) -> EvaluationRater:
        """Stage a rater in the caller-owned transaction."""
        self._session.add(rater)
        await self._session.flush()
        await self._session.refresh(rater)
        return rater

    @staticmethod
    def _identity(row: EvaluationRater | None) -> RaterIdentity | None:
        if row is None:
            return None
        return RaterIdentity(
            id=row.id,
            rater_id=row.rater_id,
            display_name=row.display_name,
            user_id=row.user_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def list_packets(
        self,
        *,
        hypothesis: str,
    ) -> list[EvaluationPacket]:
        result = await self._session.execute(
            select(EvaluationPacket)
            .where(
                EvaluationPacket.hypothesis == hypothesis,
                EvaluationPacket.status == PacketStatus.READY.value,
            )
            .order_by(EvaluationPacket.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_packet(
        self,
        *,
        evaluation_packet_id: str,
    ) -> EvaluationPacket | None:
        result = await self._session.execute(
            select(EvaluationPacket).where(
                EvaluationPacket.evaluation_packet_id == evaluation_packet_id
            )
        )
        return result.scalars().first()

    async def get_packet_by_code(
        self,
        *,
        packet_code: str,
    ) -> EvaluationPacket | None:
        result = await self._session.execute(
            select(EvaluationPacket).where(EvaluationPacket.packet_code == packet_code)
        )
        return result.scalars().first()

    async def get_rating(
        self,
        *,
        evaluation_packet_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> EvaluationRating | None:
        result = await self._session.execute(
            select(EvaluationRating).where(
                EvaluationRating.evaluation_packet_db_id == evaluation_packet_db_id,
                EvaluationRating.rater_db_id == rater_db_id,
            )
        )
        return result.scalars().first()

    async def find(
        self,
        *,
        evaluation_packet_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> RatingRecord | None:
        return self._rating_record(
            await self.get_rating(
                evaluation_packet_db_id=evaluation_packet_db_id,
                rater_db_id=rater_db_id,
            )
        )

    async def list_ratings_for_packets(
        self,
        *,
        evaluation_packet_db_ids: list[uuid.UUID],
        rater_db_id: uuid.UUID,
    ) -> list[EvaluationRating]:
        if not evaluation_packet_db_ids:
            return []
        result = await self._session.execute(
            select(EvaluationRating).where(
                EvaluationRating.evaluation_packet_db_id.in_(evaluation_packet_db_ids),
                EvaluationRating.rater_db_id == rater_db_id,
            )
        )
        return list(result.scalars().all())

    async def list_all_ratings_for_packets(
        self,
        *,
        evaluation_packet_db_ids: list,
    ) -> list[EvaluationRating]:
        """Every rater's rating for the given packets (for results aggregation)."""
        if not evaluation_packet_db_ids:
            return []
        result = await self._session.execute(
            select(EvaluationRating).where(
                EvaluationRating.evaluation_packet_db_id.in_(evaluation_packet_db_ids)
            )
        )
        return list(result.scalars().all())

    async def stage_rating(self, rating: EvaluationRating) -> EvaluationRating:
        """Stage a rating in the caller-owned transaction."""
        self._session.add(rating)
        await self._session.flush()
        await self._session.refresh(rating)
        return rating

    async def stage(self, rating: RatingRecord) -> RatingRecord:
        row = await self._session.get(EvaluationRating, rating.id)
        if row is None:
            row = EvaluationRating(id=rating.id, rating_id=rating.rating_id)
        row.evaluation_packet_db_id = rating.evaluation_packet_db_id
        row.rater_db_id = rating.rater_db_id
        row.hypothesis = rating.hypothesis
        row.overall_score = rating.overall_score
        row.rubric_scores = rating.rubric_scores
        row.section_scores = cast("dict | None", rating.section_scores)
        row.diagnostic_scores = rating.diagnostic_scores
        row.notes = rating.notes
        row.created_at = rating.created_at
        row.updated_at = rating.updated_at
        row.submitted_at = rating.submitted_at
        self._session.add(row)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            from app.domains.evaluation.application.rating_commands import RatingConflictError

            raise RatingConflictError from exc
        return rating

    @staticmethod
    def _rating_record(row: EvaluationRating | None) -> RatingRecord | None:
        if row is None:
            return None
        return RatingRecord(
            id=row.id,
            rating_id=row.rating_id,
            evaluation_packet_db_id=row.evaluation_packet_db_id,
            rater_db_id=row.rater_db_id,
            hypothesis=row.hypothesis,
            overall_score=row.overall_score,
            rubric_scores=dict(row.rubric_scores or {}),
            section_scores=row.section_scores,
            diagnostic_scores=row.diagnostic_scores,
            notes=row.notes,
            created_at=row.created_at,
            updated_at=row.updated_at,
            submitted_at=row.submitted_at,
        )

    # --- Source-grounding audit ---

    async def count_audit_items_for_execution(
        self,
        *,
        execution_db_id: uuid.UUID,
    ) -> int:
        result = await self._session.execute(
            select(EvaluationAuditItem.id).where(
                EvaluationAuditItem.execution_db_id == execution_db_id
            )
        )
        return len(list(result.scalars().all()))

    async def stage_audit_items(
        self, items: tuple[AuditItemRecord, ...]
    ) -> tuple[AuditItemRecord, ...]:
        for item in items:
            self._session.add(
                EvaluationAuditItem(
                    id=item.id,
                    audit_item_id=item.audit_item_id,
                    execution_db_id=item.execution_db_id,
                    condition_run_id=item.condition_run_id,
                    condition_code=item.condition_code,
                    lesson_id=item.lesson_id,
                    lesson_objective_id=item.lesson_objective_id,
                    objective_text=item.objective_text,
                    generated_excerpt=item.generated_excerpt,
                    source_ref=item.source_ref,
                    source_record_id=item.source_record_id,
                    source_excerpt=item.source_excerpt,
                    figure_url=item.figure_url,
                    figure_caption=item.figure_caption,
                    scope_boundary=item.scope_boundary,
                    status=item.status,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                )
            )
        await self._session.flush()
        return items

    async def list_audit_items(self) -> list[EvaluationAuditItem]:
        result = await self._session.execute(
            select(EvaluationAuditItem).order_by(EvaluationAuditItem.created_at.asc())
        )
        return list(result.scalars().all())

    async def list_audit_items_for_executions(
        self,
        *,
        execution_db_ids: list,
    ) -> list[EvaluationAuditItem]:
        if not execution_db_ids:
            return []
        result = await self._session.execute(
            select(EvaluationAuditItem)
            .where(EvaluationAuditItem.execution_db_id.in_(execution_db_ids))
            .order_by(EvaluationAuditItem.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_audit_item(
        self,
        *,
        audit_item_id: str,
    ) -> EvaluationAuditItem | None:
        result = await self._session.execute(
            select(EvaluationAuditItem).where(EvaluationAuditItem.audit_item_id == audit_item_id)
        )
        return result.scalars().first()

    async def audit_item_record(self, *, audit_item_id: str) -> AuditItemRecord | None:
        return self._audit_item_record(await self.get_audit_item(audit_item_id=audit_item_id))

    async def get_audit_rating(
        self,
        *,
        audit_item_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> EvaluationAuditRating | None:
        result = await self._session.execute(
            select(EvaluationAuditRating).where(
                EvaluationAuditRating.audit_item_db_id == audit_item_db_id,
                EvaluationAuditRating.rater_db_id == rater_db_id,
            )
        )
        return result.scalars().first()

    async def audit_rating_record(
        self,
        *,
        audit_item_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> AuditRatingRecord | None:
        return self._audit_rating_record(
            await self.get_audit_rating(
                audit_item_db_id=audit_item_db_id,
                rater_db_id=rater_db_id,
            )
        )

    async def list_audit_ratings_for_items(
        self,
        *,
        audit_item_db_ids: list,
    ) -> list[EvaluationAuditRating]:
        if not audit_item_db_ids:
            return []
        result = await self._session.execute(
            select(EvaluationAuditRating).where(
                EvaluationAuditRating.audit_item_db_id.in_(audit_item_db_ids)
            )
        )
        return list(result.scalars().all())

    async def stage_audit_rating(self, rating: AuditRatingRecord) -> AuditRatingRecord:
        row = await self._session.get(EvaluationAuditRating, rating.id)
        if row is None:
            row = EvaluationAuditRating(id=rating.id, rating_id=rating.rating_id)
        row.audit_item_db_id = rating.audit_item_db_id
        row.rater_db_id = rating.rater_db_id
        row.source_relevance = rating.source_relevance
        row.support_sufficiency = rating.support_sufficiency
        row.faithfulness = rating.faithfulness
        row.scope_correctness = rating.scope_correctness
        row.source_grounding_score = rating.source_grounding_score
        row.notes = rating.notes
        row.created_at = rating.created_at
        row.updated_at = rating.updated_at
        row.submitted_at = rating.submitted_at
        self._session.add(row)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            from app.domains.evaluation.application.audit_commands import (
                AuditRatingConflictError,
            )

            raise AuditRatingConflictError from exc
        return rating

    async def audit_item_is_assigned(self, *, audit_item_id: str, rater_db_id: uuid.UUID) -> bool:
        result = await self._session.execute(
            select(RaterAssignment.id).where(
                RaterAssignment.rater_db_id == rater_db_id,
                RaterAssignment.hypothesis == "audit",
                RaterAssignment.scope_id == audit_item_id,
            )
        )
        return result.scalar_one_or_none() is not None

    @staticmethod
    def _audit_item_record(row: EvaluationAuditItem | None) -> AuditItemRecord | None:
        if row is None:
            return None
        return AuditItemRecord(
            id=row.id,
            audit_item_id=row.audit_item_id,
            execution_db_id=row.execution_db_id,
            condition_run_id=row.condition_run_id,
            condition_code=row.condition_code,
            lesson_id=row.lesson_id,
            lesson_objective_id=row.lesson_objective_id,
            objective_text=row.objective_text,
            generated_excerpt=row.generated_excerpt,
            source_ref=row.source_ref,
            source_record_id=row.source_record_id,
            source_excerpt=row.source_excerpt,
            figure_url=row.figure_url,
            figure_caption=row.figure_caption,
            scope_boundary=row.scope_boundary,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    @staticmethod
    def _audit_rating_record(row: EvaluationAuditRating | None) -> AuditRatingRecord | None:
        if row is None:
            return None
        return AuditRatingRecord(
            id=row.id,
            rating_id=row.rating_id,
            audit_item_db_id=row.audit_item_db_id,
            rater_db_id=row.rater_db_id,
            source_relevance=row.source_relevance,
            support_sufficiency=row.support_sufficiency,
            faithfulness=row.faithfulness,
            scope_correctness=row.scope_correctness,
            source_grounding_score=row.source_grounding_score,
            notes=row.notes,
            created_at=row.created_at,
            updated_at=row.updated_at,
            submitted_at=row.submitted_at,
        )

    # --- Rater assignments (Phase H) ---

    async def find_assignment(
        self,
        *,
        experiment_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
    ) -> RaterAssignment | None:
        """One assignment by its unique (experiment, rater, hypothesis, scope) key."""
        result = await self._session.execute(
            select(RaterAssignment).where(
                RaterAssignment.experiment_db_id == experiment_db_id,
                RaterAssignment.rater_db_id == rater_db_id,
                RaterAssignment.hypothesis == hypothesis,
                RaterAssignment.scope_id == scope_id,
            )
        )
        return result.scalars().first()

    async def assignment_record(
        self,
        *,
        experiment_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
    ) -> AssignmentRecord | None:
        result = await self._session.execute(
            select(RaterAssignment)
            .where(
                RaterAssignment.experiment_db_id == experiment_db_id,
                RaterAssignment.rater_db_id == rater_db_id,
                RaterAssignment.hypothesis == hypothesis,
                RaterAssignment.scope_id == scope_id,
            )
            .with_for_update()
        )
        return self._assignment_record(result.scalars().first())

    async def assignment_count(
        self,
        *,
        experiment_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
        exclude_adjudicators: bool = False,
        adjudicators_only: bool = False,
    ) -> int:
        return await self.count_assignments_for_scope(
            experiment_db_id=experiment_db_id,
            hypothesis=hypothesis,
            scope_id=scope_id,
            exclude_adjudicators=exclude_adjudicators,
            adjudicators_only=adjudicators_only,
        )

    async def count_assignments_for_scope(
        self,
        *,
        experiment_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
        exclude_adjudicators: bool = False,
        adjudicators_only: bool = False,
    ) -> int:
        """How many raters are already on this scope.

        ``exclude_adjudicators`` and ``adjudicators_only`` are mutually
        exclusive partitions — exactly one slot or all rows.

        This count gates a cap and runs inside the serialized assignment path
        (the caller holds the experiment-row ``FOR UPDATE`` lock), so it MUST be
        a **locking read**. Under MySQL's default REPEATABLE READ a plain
        ``COUNT`` reads the transaction's snapshot — fixed at the caller's first
        read, *before* a rival's assignment committed — so every racer would see
        "under cap" and overflow it even while serialized. ``FOR UPDATE`` reads
        the latest committed rows instead. We count rows in Python rather than
        ``COUNT(*) ... FOR UPDATE`` because aggregate locking reads are an
        ambiguous corner; selecting the ids to lock is unambiguous.
        """
        stmt = select(RaterAssignment.id).where(
            RaterAssignment.experiment_db_id == experiment_db_id,
            RaterAssignment.hypothesis == hypothesis,
            RaterAssignment.scope_id == scope_id,
        )
        if exclude_adjudicators:
            stmt = stmt.where(RaterAssignment.is_adjudicator.is_(False))
        elif adjudicators_only:
            stmt = stmt.where(RaterAssignment.is_adjudicator.is_(True))
        return len((await self._session.execute(stmt.with_for_update())).scalars().all())

    async def stage_assignment_record(self, assignment: AssignmentRecord) -> AssignmentRecord:
        row = RaterAssignment(
            id=assignment.id,
            assignment_id=assignment.assignment_id,
            experiment_db_id=assignment.experiment_db_id,
            rater_db_id=assignment.rater_db_id,
            hypothesis=assignment.hypothesis,
            scope_id=assignment.scope_id,
            is_adjudicator=assignment.is_adjudicator,
            assigned_by=assignment.assigned_by,
            created_at=assignment.created_at,
        )
        self._session.add(row)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            from app.domains.evaluation.application.assignment_commands import (
                AssignmentConflictError,
            )

            raise AssignmentConflictError from exc
        return assignment

    async def audit_assignment_target(self, *, audit_item_id: str) -> uuid.UUID | None:
        result = await self._session.execute(
            select(EvaluationAuditItem.execution_db_id).where(
                EvaluationAuditItem.audit_item_id == audit_item_id
            )
        )
        return result.scalar_one_or_none()

    async def audit_item_ids_for_executions(
        self, *, execution_ids: tuple[uuid.UUID, ...]
    ) -> tuple[str, ...]:
        if not execution_ids:
            return ()
        result = await self._session.execute(
            select(EvaluationAuditItem.audit_item_id).where(
                EvaluationAuditItem.execution_db_id.in_(execution_ids)
            )
        )
        return tuple(result.scalars().all())

    @staticmethod
    def _assignment_record(row: RaterAssignment | None) -> AssignmentRecord | None:
        if row is None:
            return None
        return AssignmentRecord(
            id=row.id,
            assignment_id=row.assignment_id,
            experiment_db_id=row.experiment_db_id,
            rater_db_id=row.rater_db_id,
            hypothesis=row.hypothesis,
            scope_id=row.scope_id,
            is_adjudicator=row.is_adjudicator,
            assigned_by=row.assigned_by,
            created_at=row.created_at,
        )

    async def list_assignments_for_rater(self, *, rater_db_id: uuid.UUID) -> list[RaterAssignment]:
        """Every active assignment for a rater (drives /my-queue)."""
        result = await self._session.execute(
            select(RaterAssignment)
            .where(RaterAssignment.rater_db_id == rater_db_id)
            .order_by(RaterAssignment.created_at.asc())
        )
        return list(result.scalars().all())

    async def list_assignments_for_experiment(
        self, *, experiment_db_id: uuid.UUID
    ) -> list[RaterAssignment]:
        result = await self._session.execute(
            select(RaterAssignment)
            .where(RaterAssignment.experiment_db_id == experiment_db_id)
            .order_by(RaterAssignment.hypothesis.asc(), RaterAssignment.created_at.asc())
        )
        return list(result.scalars().all())
