"""Load H1 and H2 evaluation packet details.

Each public function states its own read path and response assembly.
"""

from __future__ import annotations

# WeasyPrint is the active renderer for the expert rater packs (HTML/CSS -> PDF):
# it renders reading-note / excerpt markdown natively and carries full Unicode, so
# no ``■`` missing-glyph boxes. The reportlab modules (``audit_pack_pdf``,
# ``h1_worksheet_pdf``) are kept in place as a fallback; ``H1_MAJOR_ISSUE_FLAGS``
# still lives in (and is imported from) ``h1_worksheet_pdf`` as its source of truth.
from app.domains.evaluation.application.candidate_blinding import (
    Candidate,
    blind_candidate_groups,
)
from app.domains.evaluation.application.constants import (
    H1_ALIGNMENT_GUIDANCE,
    H1_RUBRIC,
    H2_RUBRIC,
    rubric_for_display,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.h1_worksheet_pdf import H1_MAJOR_ISSUE_FLAGS
from app.domains.evaluation.application.h2_blinded_detail import (
    h2_blind_rating_payload,
    h2_blinded_candidates,
    h2_blinded_sections,
)
from app.domains.evaluation.application.packet_payloads import (
    PacketDetailPayloads,
    rating_payload,
)
from app.domains.evaluation.application.packet_ports import (
    H1PacketDetailDependencies,
    H2PacketDetailDependencies,
)
from app.domains.evaluation.application.packet_runtime import (
    PacketRuntime,
    PacketRuntimeContext,
    packet_or_error,
)
from app.domains.evaluation.application.rating_validation import RatingValidationService
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRating,
)
from app.shared.experiment_enums import Hypothesis


async def get_h1_packet_detail(
    dependencies: H1PacketDetailDependencies,
    *,
    evaluation_packet_id: str,
    rater_id: str,
) -> dict[str, object]:
    runtime_reader = PacketRuntime(
        dependencies.data,
        experiment_repository=dependencies.experiments,
        experiment_context_service=dependencies.context,
    )
    rater = await runtime_reader.rater_or_error(rater_id=rater_id)
    packet = await packet_or_error(dependencies.data, evaluation_packet_id=evaluation_packet_id)
    _assert_hypothesis(packet, Hypothesis.H1)
    runtime = await runtime_reader.load_packet_runtime(packet=packet)
    rating = await dependencies.data.get_rating(
        evaluation_packet_db_id=packet.id,
        rater_db_id=rater.id,
    )
    siblings = [
        sibling
        for sibling in await dependencies.data.list_packets(hypothesis=Hypothesis.H1.value)
        if sibling.execution_db_id == packet.execution_db_id
    ]
    return await _h1_detail_payload(
        packet=packet,
        runtime=runtime,
        rating=rating,
        rater_id=rater.rater_id,
        siblings=siblings,
        validation=RatingValidationService(dependencies.artefacts),
    )


async def _h1_detail_payload(
    *,
    packet: EvaluationPacket,
    runtime: PacketRuntimeContext,
    rating: EvaluationRating | None,
    rater_id: str,
    siblings: list[EvaluationPacket],
    validation: RatingValidationService,
) -> dict[str, object]:
    """Assemble the H1 packet detail DTO (pack-level rubric + candidate pack).

    The packet is presented as one anonymous candidate of its lesson block.
    """
    primary_run = validation.primary_run_or_error(runtime=runtime, packet=packet)
    candidate_artefact = await validation.artefact_for_run(run=primary_run)
    candidate_manifest = validation.review_pack_or_error(candidate_artefact)
    blinded = blind_candidate_groups(
        rater_id=rater_id,
        candidates_by_group={
            str(packet.execution_db_id): [
                Candidate(
                    candidate_id=sibling.evaluation_packet_id,
                    condition_code=str((sibling.export_refs or {}).get("condition_code") or ""),
                )
                for sibling in siblings
            ]
        },
    ).get(packet.evaluation_packet_id)
    payloads = PacketDetailPayloads()
    return {
        "evaluation_packet_id": packet.evaluation_packet_id,
        "packet_code": packet.packet_code,
        "hypothesis": Hypothesis.H1,
        "status": packet.status,
        "candidate_label": blinded.label if blinded else None,
        "candidate_count": len(siblings),
        "lesson_title": runtime.experiment_context.lesson_title,
        "lesson_subtitle": runtime.experiment_context.lesson_subtitle,
        "objectives": payloads.objectives_payload(runtime.session_plan),
        "reference_sheet": payloads.reference_sheet_payload(
            runtime.session_plan,
            pack_manifest=candidate_manifest,
        ),
        "candidate_pack": payloads.review_pack_payload(
            artefact=candidate_artefact,
            manifest=candidate_manifest,
        ),
        "rubric": rubric_for_display(H1_RUBRIC),
        "rating_guidance": list(H1_ALIGNMENT_GUIDANCE),
        "major_issue_flags": [
            {"key": key, "label": label, "description": gloss}
            for key, label, gloss in H1_MAJOR_ISSUE_FLAGS
        ],
        "existing_rating": rating_payload(rating, rater_id=rater_id, packet=packet),
    }


async def get_h2_packet_detail(
    dependencies: H2PacketDetailDependencies,
    *,
    evaluation_packet_id: str,
    rater_id: str,
) -> dict[str, object]:
    runtime_reader = PacketRuntime(
        dependencies.data,
        experiment_repository=dependencies.experiments,
        experiment_context_service=dependencies.context,
    )
    rater = await runtime_reader.rater_or_error(rater_id=rater_id)
    packet = await packet_or_error(dependencies.data, evaluation_packet_id=evaluation_packet_id)
    _assert_hypothesis(packet, Hypothesis.H2)
    runtime = await runtime_reader.load_packet_runtime(packet=packet)
    rating = await dependencies.data.get_rating(
        evaluation_packet_db_id=packet.id,
        rater_db_id=rater.id,
    )
    return await _h2_detail_payload(
        packet=packet,
        runtime=runtime,
        rating=rating,
        rater_id=rater.rater_id,
        validation=RatingValidationService(dependencies.artefacts),
    )


async def _h2_detail_payload(
    *,
    packet: EvaluationPacket,
    runtime: PacketRuntimeContext,
    rating: EvaluationRating | None,
    rater_id: str,
    validation: RatingValidationService,
) -> dict[str, object]:
    """Assemble the H2 packet detail DTO as blinded candidates.

    The existing rating is re-keyed by candidate ID so prefill stays blinded.
    """
    primary_run = validation.primary_run_or_error(runtime=runtime, packet=packet)
    candidate_artefact = await validation.artefact_for_run(run=primary_run)
    candidate_manifest = validation.review_pack_or_error(candidate_artefact)
    focal_case = runtime.focal_case_by_id.get(packet.experiment_focal_case_id or "")
    if focal_case is None:
        raise EvaluationApplicationError(404, "focal_case_not_found")
    base_run = validation.h2_base_run_or_error(runtime=runtime, packet=packet)
    base_artefact = await validation.artefact_for_run(run=base_run)
    base_manifest = validation.review_pack_or_error(base_artefact)
    p0_run_id = base_run.experiment_condition_run_id
    p1_run_id = primary_run.experiment_condition_run_id
    sections = await validation.h2_section_payloads(
        runtime=runtime,
        base_artefact=base_artefact,
        base_manifest=base_manifest,
        candidate_artefact=candidate_artefact,
        candidate_manifest=candidate_manifest,
    )
    payloads = PacketDetailPayloads()
    return {
        "evaluation_packet_id": packet.evaluation_packet_id,
        "packet_code": packet.packet_code,
        "hypothesis": Hypothesis.H2,
        "status": packet.status,
        "lesson_title": runtime.experiment_context.lesson_title,
        "lesson_subtitle": runtime.experiment_context.lesson_subtitle,
        "objectives": payloads.objectives_payload(runtime.session_plan),
        "focal_learner": payloads.learner_state_card_payload(
            focal_case=focal_case,
            session_plan=runtime.session_plan,
        ),
        "candidates": h2_blinded_candidates(
            rater_id=rater_id,
            packet_public_id=packet.evaluation_packet_id,
            p0_run_id=p0_run_id,
            p1_run_id=p1_run_id,
            pack_manifest_by_run={
                p0_run_id: payloads.review_pack_manifest_payload(base_manifest),
                p1_run_id: payloads.review_pack_manifest_payload(candidate_manifest),
            },
        ),
        "sections": h2_blinded_sections(sections, p0_run_id=p0_run_id, p1_run_id=p1_run_id),
        "rubric": rubric_for_display(H2_RUBRIC),
        "existing_rating": h2_blind_rating_payload(
            rating_payload(rating, rater_id=rater_id, packet=packet),
            p0_run_id=p0_run_id,
            p1_run_id=p1_run_id,
        ),
    }


def _assert_hypothesis(packet: EvaluationPacket, expected: Hypothesis) -> None:
    if packet.hypothesis != expected.value:
        raise EvaluationApplicationError(409, "packet_hypothesis_mismatch")
