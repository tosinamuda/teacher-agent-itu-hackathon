"""Generation backends for the architecture axis (pre-registration §3 axis B).

Two architectures compete on the same scored path:

  * ``staged``     — the production MULTI-signature pipeline (KC extraction ->
                     per-objective drafting -> global steps), made cold-start
                     tolerant so the no-records stratum (S3) can run without
                     touching production code.
  * ``monolithic`` — a SINGLE-signature one-call drafter (see
                     ``monolithic_signature``).

Both implement the ``GenerationBackend`` protocol (``generate_scored`` returning a
``ScoredGeneration``) so strategy cells and the runner are backend-agnostic.

Cold-start handling (shared by both): when there are no textbook records, inject a
single synthetic, curriculum-derived ``exposition`` record with id
``curriculum-only``. The default record routing maps every passed record to the
current subtopic, so this record reaches KC extraction; and because it is the only
support record, ``normalize_candidate_kcs_for_support`` downgrades every KC to
``concept`` (concept KCs need only a concept record), so the unmodified staged
pipeline runs end to end with no spurious ``reused_modeling_record`` (there are no
modeling records). This faithfully implements the owner's "ground purely on the
curriculum" intent for cold-start.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    PreparedGenerationInputs,
    prepare_generation_inputs,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import (
    normalize_textbook_records,
)
from app.shared.json_types import JsonObject

from .generation import ScoredGeneration, ScoredLessonGenerationService
from .monolithic_signature import MonolithicLessonGenerationModule
from .reasoning import normalize_reasoning

ARCHITECTURES: frozenset[str] = frozenset({"staged", "monolithic"})

# The synthetic cold-start record id, kept in sync with the monolithic signature's
# cold-start instruction so both architectures use the same placeholder.
COLD_START_RECORD_ID = "curriculum-only"


class GenerationBackend(Protocol):
    """A scored generation backend the strategy cells / runner can drive."""

    async def generate_scored(
        self,
        session_context: JsonObject,
        curriculum_context: JsonObject,
        reference_context: list[JsonObject],
        evidence_selection_strategy: str | None = ...,
    ) -> ScoredGeneration: ...


def _curriculum_objective_texts(curriculum_context: JsonObject) -> list[str]:
    texts: list[str] = []
    for objective in curriculum_context.get("curriculum_objectives") or []:
        if isinstance(objective, Mapping):
            text = str(objective.get("objective_text") or "").strip()
        else:
            text = str(objective or "").strip()
        if text:
            texts.append(text)
    return texts


def synthetic_curriculum_record(
    session_context: JsonObject,
    curriculum_context: JsonObject,
) -> JsonObject:
    """One curriculum-derived ``exposition`` record for the cold-start case."""
    subtopic = str(
        session_context.get("subtopic") or curriculum_context.get("subtopic") or ""
    ).strip()
    objective_texts = _curriculum_objective_texts(curriculum_context)
    content = (
        "\n".join(objective_texts) or f"Curriculum objectives for {subtopic or 'this lesson'}."
    )
    return {
        # `type` MUST be "textbook_record" or normalize_textbook_records drops it
        # (and the empty-records guard in prepare_generation_inputs would fire).
        "type": "textbook_record",
        "record_id": COLD_START_RECORD_ID,
        "section_ref": COLD_START_RECORD_ID,
        "title": subtopic or "Curriculum",
        "content": content,
        "record_type": "exposition",
        "is_primary": True,
    }


def _prepare_inputs_cold_start_tolerant(
    service: ScoredLessonGenerationService,
    *,
    session_context: JsonObject,
    curriculum_context: JsonObject,
    reference_context: list[JsonObject],
    requested_strategy: str | None,
) -> PreparedGenerationInputs:
    """Production input prep, but inject a synthetic record when none exist.

    Cold-start (S3) can arrive with a non-empty reference_context that holds only
    subject-level refs (type "textbook" with no chunks), which normalize_textbook_
    records drops -> the empty-records guard would fire. So we inject the synthetic
    curriculum record whenever no REAL textbook records survive normalisation, not
    merely when the list is empty.
    """
    references = list(reference_context)
    if not normalize_textbook_records(references):
        references = [*references, synthetic_curriculum_record(session_context, curriculum_context)]
    return prepare_generation_inputs(
        session_context=session_context,
        curriculum_context=curriculum_context,
        reference_context=references,
        requested_strategy=requested_strategy,
        default_strategy=service.default_evidence_selection_strategy,
    )


class StagedScoredService(ScoredLessonGenerationService):
    """Staged (multi-signature) backend, cold-start tolerant.

    Identical to production for S1/S2 (records present); for S3 (no records) it
    injects the synthetic curriculum record so the pipeline runs.
    """

    def _prepare_inputs(
        self,
        *,
        session_context: JsonObject,
        curriculum_context: JsonObject,
        reference_context: list[JsonObject],
        requested_strategy: str | None,
    ) -> PreparedGenerationInputs:
        return _prepare_inputs_cold_start_tolerant(
            self,
            session_context=session_context,
            curriculum_context=curriculum_context,
            reference_context=reference_context,
            requested_strategy=requested_strategy,
        )


class MonolithicScoredService(ScoredLessonGenerationService):
    """Single-signature backend: one DSPy call drafts the whole plan."""

    def __init__(
        self,
        *,
        reasoning: str = "cot",
        final_writer_mode: str = "chain_of_thought",
    ) -> None:
        super().__init__(final_writer_mode=final_writer_mode)
        # Swap the staged generation program for the one-call drafter.
        self.generation_program = MonolithicLessonGenerationModule(
            reasoning=reasoning,
            final_writer_mode=self.final_writer_mode,
        )

    def _generation_program_kwargs(
        self,
        inputs: PreparedGenerationInputs,
        prior_violations: list[str] | None,
    ) -> dict[str, object]:
        # The monolithic signature has a prior_violations input -> refine feedback.
        return {"request": inputs, "prior_violations": prior_violations}

    def _prepare_inputs(
        self,
        *,
        session_context: JsonObject,
        curriculum_context: JsonObject,
        reference_context: list[JsonObject],
        requested_strategy: str | None,
    ) -> PreparedGenerationInputs:
        # Monolithic grounds on the curriculum natively, but the prod input-prep
        # still rejects empty records, so use the same synthetic-record bypass.
        return _prepare_inputs_cold_start_tolerant(
            self,
            session_context=session_context,
            curriculum_context=curriculum_context,
            reference_context=reference_context,
            requested_strategy=requested_strategy,
        )


def build_scored_service(
    architecture: str,
    *,
    reasoning: str = "cot",
    final_writer_mode: str | None = None,
) -> ScoredLessonGenerationService:
    """Construct the scored service for one (architecture, reasoning) cell."""
    arch = (architecture or "").strip().lower()
    name = normalize_reasoning(reasoning)
    if arch == "staged":
        # The staged pipeline's reasoning is its final-writer mode (predict/cot).
        # rlm is evaluated on the single-signature arm only (per-step RLM over the
        # multi-signature pipeline is not long-context and not meaningful); react
        # is a self-correction strategy cell, not a staged reasoning mode.
        if name in {"predict", "cot"}:
            mode = "predict" if name == "predict" else "chain_of_thought"
            return StagedScoredService(final_writer_mode=mode)
        raise NotImplementedError(
            f"staged backend + reasoning '{name}' is out of scope "
            "(rlm runs on the monolithic arm; react is a strategy cell)."
        )
    if arch == "monolithic":
        return MonolithicScoredService(
            reasoning=name,
            final_writer_mode=final_writer_mode or "chain_of_thought",
        )
    raise ValueError(
        f"unknown architecture: {architecture!r} (expected one of {sorted(ARCHITECTURES)})"
    )
