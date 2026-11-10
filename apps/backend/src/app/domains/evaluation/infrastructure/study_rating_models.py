"""The MSc study's ratings, kept in the study's own instrument.

The study rated on paper documents with its own criteria (``domain.study_instrument``): Part 1
scored each class revision note 1–5 per objective on three criteria; Part 2 judged a learner's
two notes against each other. Neither fits the app's rubric, so each is kept here as
the study recorded it, beside the revision notes it rated, and never changed.
"""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID


class StudyCriterionScore(Base):
    """One Part 1 score: a rater's 1–5 on one criterion, for one objective of one note."""

    __tablename__ = "study_criterion_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artefact_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("artefacts.artefact_id", name="fk_study_scores_artefact_id"),
        index=True,
    )
    rater: Mapped[str] = mapped_column(String(32))
    rater_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_raters.id", name="fk_study_scores_rater_db_id"),
        index=True,
    )
    delivery_order: Mapped[int] = mapped_column(Integer)
    packet: Mapped[str] = mapped_column(String(32))
    objective_index: Mapped[int] = mapped_column(Integer)
    lesson_objective_id: Mapped[str] = mapped_column(String(64))
    #: The study's own criterion id, e.g. ``curriculum_objective_alignment``.
    criterion_id: Mapped[str] = mapped_column(String(64))
    score: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    #: The returned rating document the score was read from, as the dataset names it.
    document: Mapped[str] = mapped_column(String(512))


class StudyComparativeJudgement(Base):
    """One Part 2 judgement: which of a learner's two notes a rater found better, and how much."""

    __tablename__ = "study_comparative_judgements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #: The notes as the rater saw them, A then B; which is P0 and which P1 was hidden from them.
    artefact_a_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("artefacts.artefact_id", name="fk_study_judgements_a_id"), index=True
    )
    artefact_b_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("artefacts.artefact_id", name="fk_study_judgements_b_id"), index=True
    )
    rater: Mapped[str] = mapped_column(String(32))
    rater_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_raters.id", name="fk_study_judgements_rater_db_id"),
        index=True,
    )
    delivery_order: Mapped[int] = mapped_column(Integer)
    packet: Mapped[str] = mapped_column(String(32))
    ability_stratum: Mapped[str] = mapped_column(String(16))
    #: The objective's number among those the set compared: only the objectives the learner
    #: had class work for were compared, so this is not the lesson's own numbering.
    objective_index: Mapped[int] = mapped_column(Integer)
    #: The lesson objective the comparison page named.
    lesson_objective_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    criterion_id: Mapped[str] = mapped_column(String(64))
    #: As the rater wrote it: "A clearly better" … "About the same" … "B clearly better".
    choice: Mapped[str] = mapped_column(String(32))
    #: The condition the choice favoured once unblinded, P0 or P1; none for "About the same".
    favoured_condition: Mapped[str | None] = mapped_column(String(8), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    document: Mapped[str] = mapped_column(String(512))


class StudyRatingDocument(Base):
    """One returned rating document: how much came back answered, when, and the closing comment.

    Part 1's document rated one note; Part 2's compared two, shown to the rater as A and B.
    """

    __tablename__ = "study_rating_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document: Mapped[str] = mapped_column(String(512), unique=True)
    rater: Mapped[str] = mapped_column(String(32))
    rater_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_raters.id", name="fk_study_documents_rater_db_id"),
        index=True,
    )
    delivery_order: Mapped[int] = mapped_column(Integer)
    packet: Mapped[str] = mapped_column(String(32))
    artefact_a_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("artefacts.artefact_id", name="fk_study_documents_a_id"),
        index=True,
    )
    artefact_b_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("artefacts.artefact_id", name="fk_study_documents_b_id"),
        nullable=True,
        index=True,
    )
    part: Mapped[int] = mapped_column(Integer)
    answer_sheets: Mapped[int] = mapped_column(Integer)
    marks: Mapped[int] = mapped_column(Integer)
    rows_unanswered: Mapped[int] = mapped_column(Integer)
    #: ``complete``, ``partial`` or ``untouched``: how much of the set came back answered.
    state: Mapped[str] = mapped_column(String(16))
    #: As the rater wrote it on the document, where they did.
    date_completed: Mapped[str | None] = mapped_column(String(64), nullable=True)
    closing_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
