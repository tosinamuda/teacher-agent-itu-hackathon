"""List one rater's ready evaluation packet queue.

The query states its complete read path: identity, assignment scope, readiness,
blinding, ordering, batched ratings, and response rows.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict

from app.domains.evaluation.application.assignment_scope import AssignmentScope

# WeasyPrint is the active renderer for the expert rater packs (HTML/CSS -> PDF):
# it renders reading-note / excerpt markdown natively and carries full Unicode, so
# no ``■`` missing-glyph boxes. The reportlab modules (``audit_pack_pdf``,
# ``h1_worksheet_pdf``) are kept in place as a fallback; ``H1_MAJOR_ISSUE_FLAGS``
# still lives in (and is imported from) ``h1_worksheet_pdf`` as its source of truth.
from app.domains.evaluation.application.candidate_blinding import (
    BlindedCandidate,
    Candidate,
    blind_candidate_groups,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.packet_payloads import rating_payload
from app.domains.evaluation.application.packet_ports import PacketQueueDependencies
from app.domains.evaluation.application.packet_runtime import (
    PacketRuntime,
)
from app.domains.evaluation.application.rating_validation import RatingValidationService
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRating,
)
from app.shared.experiment_enums import Hypothesis


async def list_packet_queue(
    dependencies: PacketQueueDependencies,
    *,
    hypothesis: Hypothesis,
    rater_id: str,
) -> list[dict[str, object]]:
    """List this rater's assigned, ready packets in stable blinded order."""
    runtime = PacketRuntime(
        dependencies.data,
        experiment_repository=dependencies.experiments,
        experiment_context_service=dependencies.context,
    )
    validation = RatingValidationService(dependencies.artefacts)
    assignments = AssignmentScope(
        dependencies.data,
        experiment_repository=dependencies.experiments,
    )
    rater = await runtime.rater_or_error(rater_id=rater_id)
    packets = await dependencies.data.list_packets(hypothesis=hypothesis.value)
    assigned = await assignments.filter_assigned_packets(
        packets=packets,
        hypothesis=hypothesis,
        rater_db_id=rater.id,
    )
    ready = [
        packet
        for packet in assigned
        if await _packet_is_rater_ready(packet, runtime=runtime, validation=validation)
    ]
    blinded = _blind_h1_packets(hypothesis, ready, rater_id=rater.rater_id)
    ordered = _ordered_packets(ready, blinded=blinded, rater_id=rater.rater_id)
    ratings = {
        rating.evaluation_packet_db_id: rating
        for rating in await dependencies.data.list_ratings_for_packets(
            evaluation_packet_db_ids=[packet.id for packet in ordered],
            rater_db_id=rater.id,
        )
    }
    return [
        _queue_item_payload(
            packet,
            rating=ratings.get(packet.id),
            rater_id=rater.rater_id,
            blinded=blinded.get(packet.evaluation_packet_id),
        )
        for packet in ordered
    ]


async def _packet_is_rater_ready(
    packet: EvaluationPacket,
    *,
    runtime: PacketRuntime,
    validation: RatingValidationService,
) -> bool:
    try:
        context = await runtime.load_packet_runtime(packet=packet)
        primary_run = validation.primary_run_or_error(runtime=context, packet=packet)
        await validation.artefact_for_run(run=primary_run)
        if packet.hypothesis == Hypothesis.H2.value:
            if context.focal_case_by_id.get(packet.experiment_focal_case_id or "") is None:
                return False
            base_run = validation.h2_base_run_or_error(runtime=context, packet=packet)
            base_artefact = await validation.artefact_for_run(run=base_run)
            candidate_artefact = await validation.artefact_for_run(run=primary_run)
            await validation.h2_section_payloads(
                runtime=context,
                base_artefact=base_artefact,
                base_manifest=validation.review_pack_or_error(base_artefact),
                candidate_artefact=candidate_artefact,
                candidate_manifest=validation.review_pack_or_error(candidate_artefact),
            )
        return True
    except EvaluationApplicationError:
        return False


def _blind_h1_packets(
    hypothesis: Hypothesis,
    packets: list[EvaluationPacket],
    *,
    rater_id: str,
) -> dict[str, BlindedCandidate]:
    if hypothesis != Hypothesis.H1:
        return {}
    groups: dict[str, list[Candidate]] = defaultdict(list)
    for packet in packets:
        groups[str(packet.execution_db_id)].append(
            Candidate(
                candidate_id=packet.evaluation_packet_id,
                condition_code=str((packet.export_refs or {}).get("condition_code") or ""),
            )
        )
    return blind_candidate_groups(rater_id=rater_id, candidates_by_group=groups)


def _ordered_packets(
    packets: list[EvaluationPacket],
    *,
    blinded: dict[str, BlindedCandidate],
    rater_id: str,
) -> list[EvaluationPacket]:
    if blinded:
        return sorted(
            packets,
            key=lambda packet: (
                _packet_sort_key(str(packet.execution_db_id), rater_id),
                blinded[packet.evaluation_packet_id].display_order,
            ),
        )
    return sorted(packets, key=lambda packet: _packet_sort_key(packet.packet_code, rater_id))


def _packet_sort_key(packet_code: str, rater_id: str) -> str:
    return hashlib.sha256(f"{rater_id}:{packet_code}".encode()).hexdigest()


def _queue_item_payload(
    packet: EvaluationPacket,
    *,
    rating: EvaluationRating | None,
    rater_id: str,
    blinded: BlindedCandidate | None,
) -> dict[str, object]:
    rendered_rating = rating_payload(rating, rater_id=rater_id, packet=packet)
    if rendered_rating is not None and packet.hypothesis == Hypothesis.H2.value:
        rendered_rating["section_scores"] = None
    return {
        "evaluation_packet_id": packet.evaluation_packet_id,
        "packet_code": packet.packet_code,
        "hypothesis": Hypothesis(packet.hypothesis),
        "status": packet.status,
        "created_at": packet.created_at,
        "rating": rendered_rating,
        "candidate_label": blinded.label if blinded else None,
        "group_key": str(packet.execution_db_id) if blinded else None,
    }
