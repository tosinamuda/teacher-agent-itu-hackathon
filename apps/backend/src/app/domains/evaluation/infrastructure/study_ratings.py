"""The study's ratings read from the tables the import wrote them to."""

from __future__ import annotations

from collections import defaultdict

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.evaluation.application.study_ratings import (
    ComparativeJudgement,
    CriterionScore,
    RatingDocument,
    StudyRatings,
    StudyRatingsTally,
)
from app.domains.evaluation.infrastructure.models import EvaluationRater
from app.domains.evaluation.infrastructure.study_rating_models import (
    StudyComparativeJudgement,
    StudyCriterionScore,
    StudyRatingDocument,
)


class SqlAlchemyStudyRatings:
    async def _objectives(self, db: AsyncSession, note_id: str) -> dict[str, str]:
        """The note's lesson objectives by id, worded as its plan words them."""
        plan = await db.scalar(
            select(PlanVersion.session_plan)
            .join(Artefact, Artefact.plan_version_id == PlanVersion.version_id)
            .where(Artefact.artefact_id == note_id)
        )
        return {
            str(objective["lesson_objective_id"]): str(objective.get("objective_text") or "")
            for objective in (plan or {}).get("lesson_plan_objectives") or []
        }

    async def for_note(self, db: AsyncSession, note_id: str) -> StudyRatings:
        objectives = await self._objectives(db, note_id)
        scores = await db.execute(
            select(StudyCriterionScore)
            .where(StudyCriterionScore.artefact_id == note_id)
            .order_by(
                StudyCriterionScore.rater,
                StudyCriterionScore.objective_index,
                StudyCriterionScore.criterion_id,
            )
        )
        judgements = await db.execute(
            select(StudyComparativeJudgement)
            .where(
                or_(
                    StudyComparativeJudgement.artefact_a_id == note_id,
                    StudyComparativeJudgement.artefact_b_id == note_id,
                )
            )
            .order_by(
                StudyComparativeJudgement.rater,
                StudyComparativeJudgement.objective_index,
                StudyComparativeJudgement.criterion_id,
            )
        )
        documents = await db.execute(
            select(StudyRatingDocument, EvaluationRater.display_name)
            .join(EvaluationRater, EvaluationRater.id == StudyRatingDocument.rater_db_id)
            .where(
                or_(
                    StudyRatingDocument.artefact_a_id == note_id,
                    StudyRatingDocument.artefact_b_id == note_id,
                )
            )
            .order_by(StudyRatingDocument.rater)
        )
        return StudyRatings(
            scores=[
                CriterionScore(
                    rater=row.rater,
                    packet=row.packet,
                    objective_index=row.objective_index,
                    lesson_objective_id=row.lesson_objective_id,
                    objective_text=objectives.get(row.lesson_objective_id),
                    criterion_id=row.criterion_id,
                    score=row.score,
                    comment=row.comment,
                )
                for row in scores.scalars()
            ],
            judgements=[
                ComparativeJudgement(
                    rater=row.rater,
                    packet=row.packet,
                    shown_as="A" if row.artefact_a_id == note_id else "B",
                    other_note_id=row.artefact_b_id
                    if row.artefact_a_id == note_id
                    else row.artefact_a_id,
                    objective_index=row.objective_index,
                    lesson_objective_id=row.lesson_objective_id,
                    objective_text=objectives.get(row.lesson_objective_id or ""),
                    criterion_id=row.criterion_id,
                    choice=row.choice,
                    favoured_condition=row.favoured_condition,
                    comment=row.comment,
                )
                for row in judgements.scalars()
            ],
            documents=[
                RatingDocument(
                    rater=row.rater,
                    rater_name=rater_name,
                    packet=row.packet,
                    shown_as=None
                    if row.artefact_b_id is None
                    else ("A" if row.artefact_a_id == note_id else "B"),
                    state=row.state,
                    marks=row.marks,
                    rows_unanswered=row.rows_unanswered,
                    date_completed=row.date_completed,
                    closing_comment=row.closing_comment,
                )
                for row, rater_name in documents.all()
            ],
        )

    async def tally(self, db: AsyncSession, plan_version_ids: list[str]) -> list[StudyRatingsTally]:
        """Per lesson, the scores and judgements on its notes and the raters who made them."""
        scores = await db.execute(
            select(Artefact.plan_version_id, StudyCriterionScore.rater)
            .join(Artefact, Artefact.artefact_id == StudyCriterionScore.artefact_id)
            .where(Artefact.plan_version_id.in_(plan_version_ids))
        )
        judgements = await db.execute(
            select(Artefact.plan_version_id, StudyComparativeJudgement.rater)
            .join(Artefact, Artefact.artefact_id == StudyComparativeJudgement.artefact_a_id)
            .where(Artefact.plan_version_id.in_(plan_version_ids))
        )
        counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
        raters: dict[str, set[str]] = defaultdict(set)
        for column, rows in enumerate((scores.all(), judgements.all())):
            for plan_version_id, rater in rows:
                counts[plan_version_id][column] += 1
                raters[plan_version_id].add(rater)
        return [
            StudyRatingsTally(
                plan_version_id=version,
                scores=counts[version][0],
                judgements=counts[version][1],
                raters=len(raters[version]),
            )
            for version in plan_version_ids
            if version in counts
        ]
