"""Build (or re-use) the rater evaluation packets for a finished execution.

The export is idempotent: if the persisted packet set already matches the
execution's condition runs, the existing packets are returned. Otherwise the
stale set is replaced.

Per-hypothesis emit policy:
- **H1**: one packet per main comparison condition (C0-C3). C4 is teacher-
  gated governance evidence and is NOT exported as a rater packet (June-5
  settled design). The H1 condition profile carries the teacher-validation
  flag, so adding/removing a gated condition needs no code change here.
- **H2**: two packets per ``ExperimentFocalCase``, one for P0 (reuse) and one
  for P1 (personalised). Both must be fully generated before export.

Distinct from execution lifecycle (creation + job queueing), C4 governance
(decision recording + summary), and results summary (read-only DTO). Depends
only on ``PacketExportStore`` and the condition registry in
``review_pack_study.conditions.profiles``.
"""

from __future__ import annotations

import uuid

from app.domains.evaluation.infrastructure.models import EvaluationPacket
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.packet_export_store import PacketExportStore
from app.domains.experiments.domain import ConditionCode, Hypothesis, PacketStatus
from app.domains.experiments.infrastructure.models import (
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.experiments.review_pack_study.conditions.profiles import (
    h1_main_condition_codes,
    profile_for,
)
from app.domains.learner_state.domain.models import misconception_codes_for_snapshot
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.time import utc_now


def _h1_condition_is_teacher_gated(condition_code: str) -> bool:
    """Return True when this H1 condition carries a teacher-validation gate (C4).

    Reads the single condition registry, so adding/removing a gated condition
    needs no change here.
    """
    try:
        profile = profile_for(Hypothesis.H1, ConditionCode(condition_code))
    except ValueError:
        return False
    return profile.teacher_validation.enabled


class PacketExportApplicationService:
    """Own the idempotent packet-export policy for an execution (H1 main / H2 paired)."""

    def __init__(
        self,
        store: PacketExportStore[
            ExperimentExecution,
            EvaluationPacket,
            ExperimentConditionRun,
            ExperimentFocalCase,
        ],
    ) -> None:
        self.store = store
        self.packet_exports = store.packet_exports

    async def export_packets(
        self,
        *,
        execution_id: str,
    ) -> list[EvaluationPacket]:
        """Return the rater packets for the execution — re-use if fresh, else rebuild."""
        try:
            packets = await self._stage_or_reuse_packets(execution_id=execution_id)
            await self.store.commit()
        except BaseException:
            await self.store.rollback()
            raise
        return packets

    async def _stage_or_reuse_packets(self, *, execution_id: str) -> list[EvaluationPacket]:
        """Lock, validate, and stage the complete replacement packet set."""
        # Serialize concurrent exports for this execution. The lock is the FIRST
        # statement so the transaction's read view forms after it (and after any
        # rival export has committed); otherwise two exports both read "stale" and
        # double-delete each other's freshly-inserted packets.
        await self.packet_exports.lock_execution_by_public_id(execution_id)
        execution = await self.packet_exports.get_execution(execution_id)
        if execution is None:
            raise ExperimentApplicationError(404, "execution_not_found")
        existing_packets = await self.packet_exports.list_packets(execution.id)
        condition_runs = await self.packet_exports.list_condition_runs(execution.id)
        # Resolve each run's current pack once via the back-pointer; the rest of
        # the export keys off this map instead of a stored id on the run. A run
        # absent from the map has no generated pack yet (export not ready).
        packs = await self.packet_exports.current_artefacts_by_condition_run(
            [run.experiment_condition_run_id for run in condition_runs]
        )
        pack_ids = {run_id: artefact.artefact_id for run_id, artefact in packs.items()}
        if existing_packets and self._packets_match_execution(
            execution=execution,
            condition_runs=condition_runs,
            packets=existing_packets,
            pack_ids=pack_ids,
        ):
            return sorted(existing_packets, key=lambda packet: packet.created_at)
        if existing_packets:
            # Never silently destroy real expert ratings on re-export. Synthetic
            # dry-run ratings (rater.user_id IS NULL) are disposable and get cleared;
            # a real rating blocks the rebuild so the researcher decides explicitly.
            real_ratings = await self.packet_exports.count_real_ratings_for_packets(
                packet_ids=[packet.id for packet in existing_packets]
            )
            if real_ratings:
                raise ExperimentApplicationError(409, "reexport_blocked_expert_ratings_exist")
            await self.packet_exports.delete_packets(
                packet_ids=[packet.id for packet in existing_packets]
            )
        if execution.hypothesis == Hypothesis.H1.value:
            return await self._export_h1_packets(
                execution=execution, condition_runs=condition_runs, pack_ids=pack_ids
            )
        focal_cases = await self.packet_exports.list_focal_cases(execution.id)
        return await self._export_h2_packets(
            execution=execution,
            condition_runs=condition_runs,
            focal_cases=focal_cases,
            pack_ids=pack_ids,
        )

    async def _export_h1_packets(
        self,
        *,
        execution: ExperimentExecution,
        condition_runs: list[ExperimentConditionRun],
        pack_ids: dict[str, str],
    ) -> list[EvaluationPacket]:
        """Emit one packet per main H1 condition (C0-C3). C4 is teacher-gated, not exported."""
        main_codes = h1_main_condition_codes()
        order = {code.value: index for index, code in enumerate(main_codes)}
        main_runs = [
            run for run in condition_runs if not _h1_condition_is_teacher_gated(run.condition_code)
        ]
        sorted_runs = sorted(
            main_runs,
            key=lambda run: order.get(run.condition_code, len(order)),
        )
        if len(sorted_runs) != len(main_codes):
            raise ExperimentApplicationError(409, "h1_packet_export_condition_count_mismatch")

        # Main conditions (C0-C3) are ungated, so each must be fully generated
        # before export — a run absent from the pack map has no pack yet.
        for run in sorted_runs:
            if run.experiment_condition_run_id not in pack_ids:
                raise ExperimentApplicationError(409, "execution_packets_not_ready")

        packets: list[EvaluationPacket] = []
        for run in sorted_runs:
            packets.append(
                EvaluationPacket(
                    evaluation_packet_id=new_public_id(PublicIdPrefix.EVALUATION_PACKET),
                    execution_db_id=execution.id,
                    packet_code=new_public_id(PublicIdPrefix.EVALUATION_PACKET),
                    hypothesis=execution.hypothesis,
                    status=PacketStatus.READY.value,
                    primary_condition_run_id=run.experiment_condition_run_id,
                    experiment_focal_case_id=None,
                    export_refs={
                        "condition_code": run.condition_code,
                        "artefact_ids": [pack_ids[run.experiment_condition_run_id]],
                    },
                    condition_run_ids=[run.experiment_condition_run_id],
                    created_at=utc_now(),
                    updated_at=utc_now(),
                )
            )
        return await self.packet_exports.save_packets(packets=packets)

    async def _export_h2_packets(
        self,
        *,
        execution: ExperimentExecution,
        condition_runs: list[ExperimentConditionRun],
        focal_cases: list[ExperimentFocalCase],
        pack_ids: dict[str, str],
    ) -> list[EvaluationPacket]:
        """Emit ONE paired packet per focal case (primary = P1, runs = [P0, P1]).

        The rater sees both packs inside this single packet as blinded anonymous
        candidates (see ``evaluation.candidate_blinding``) and scores each — so a
        separate P0-primary packet would be a redundant single-candidate duplicate
        (2026-06-10 dress-rehearsal finding). The P0 run stays reachable through
        ``condition_run_ids`` for de-anonymisation and analysis.
        """
        focal_case_by_id = {focal_case.id: focal_case for focal_case in focal_cases}
        runs_by_focal_case: dict[uuid.UUID, dict[str, ExperimentConditionRun]] = {}
        for run in condition_runs:
            if run.focal_case_db_id is None:
                continue
            runs_by_focal_case.setdefault(run.focal_case_db_id, {})[run.condition_code] = run

        packets: list[EvaluationPacket] = []
        for focal_case in focal_cases:
            run_pair = runs_by_focal_case.get(focal_case.id, {})
            p0_run = run_pair.get(ConditionCode.P0.value)
            p1_run = run_pair.get(ConditionCode.P1.value)
            if p0_run is None or p1_run is None:
                raise ExperimentApplicationError(409, "h2_packet_export_condition_pair_missing")
            p0_pack_id = pack_ids.get(p0_run.experiment_condition_run_id)
            p1_pack_id = pack_ids.get(p1_run.experiment_condition_run_id)
            if p0_pack_id is None or p1_pack_id is None:
                raise ExperimentApplicationError(409, "execution_packets_not_ready")

            packets.append(
                EvaluationPacket(
                    evaluation_packet_id=new_public_id(PublicIdPrefix.EVALUATION_PACKET),
                    execution_db_id=execution.id,
                    packet_code=new_public_id(PublicIdPrefix.EVALUATION_PACKET),
                    hypothesis=execution.hypothesis,
                    status=PacketStatus.READY.value,
                    primary_condition_run_id=p1_run.experiment_condition_run_id,
                    experiment_focal_case_id=focal_case.experiment_focal_case_id,
                    export_refs={
                        "condition_code": p1_run.condition_code,
                        "focal_case_type": focal_case.focal_case_type,
                        "misconception_codes": misconception_codes_for_snapshot(
                            focal_case.learner_state_snapshot
                        ),
                        "artefact_ids": [p0_pack_id, p1_pack_id],
                    },
                    condition_run_ids=[
                        p0_run.experiment_condition_run_id,
                        p1_run.experiment_condition_run_id,
                    ],
                    created_at=utc_now(),
                    updated_at=utc_now(),
                )
            )

        if len(packets) != len(focal_case_by_id):
            raise ExperimentApplicationError(409, "h2_packet_export_count_mismatch")
        return await self.packet_exports.save_packets(packets=packets)

    def _packets_match_execution(
        self,
        *,
        execution: ExperimentExecution,
        condition_runs: list[ExperimentConditionRun],
        packets: list[EvaluationPacket],
        pack_ids: dict[str, str],
    ) -> bool:
        """Return True when the persisted packets are still in sync with the runs (cache-validity policy)."""  # noqa: E501
        matcher = self._MATCHER_BY_HYPOTHESIS[Hypothesis(execution.hypothesis)]
        return matcher(condition_runs=condition_runs, packets=packets, pack_ids=pack_ids)

    @staticmethod
    def _h1_packets_match(
        *,
        condition_runs: list[ExperimentConditionRun],
        packets: list[EvaluationPacket],
        pack_ids: dict[str, str],
    ) -> bool:
        """H1 cache validity: one packet per main comparison run (C0-C3, C4 excluded).

        ``pack_ids`` is the run→current-pack map; a run is "generated" iff it has
        an entry (resolved via the back-pointer, replacing the old stored id).
        """
        expected_run_ids = {
            run.experiment_condition_run_id
            for run in condition_runs
            if run.experiment_condition_run_id in pack_ids
            and not _h1_condition_is_teacher_gated(run.condition_code)
        }
        if len(expected_run_ids) != len(h1_main_condition_codes()):
            return False
        actual_run_ids = {packet.primary_condition_run_id for packet in packets}
        return actual_run_ids == expected_run_ids

    @staticmethod
    def _h2_packets_match(
        *,
        condition_runs: list[ExperimentConditionRun],
        packets: list[EvaluationPacket],
        pack_ids: dict[str, str],
    ) -> bool:
        """H2 cache validity: ONE paired packet per focal case, led by its P1 run.

        Legacy two-packet exports (a P0-primary twin per focal case) fail this
        check on purpose, so the next export rebuilds them into the paired shape.
        """
        focal_cases_with_pair: set[uuid.UUID] = set()
        p1_run_ids: set[str] = set()
        focal_case_runs: dict[uuid.UUID, set[str]] = {}
        for run in condition_runs:
            if run.focal_case_db_id is None or run.experiment_condition_run_id not in pack_ids:
                continue
            focal_case_runs.setdefault(run.focal_case_db_id, set()).add(run.condition_code)
            if run.condition_code == ConditionCode.P1.value:
                p1_run_ids.add(run.experiment_condition_run_id)
        focal_cases_with_pair = {
            focal_case_db_id
            for focal_case_db_id, codes in focal_case_runs.items()
            if {ConditionCode.P0.value, ConditionCode.P1.value} <= codes
        }
        if len(packets) != len(focal_cases_with_pair):
            return False
        seen_focal_cases: set[str] = set()
        for packet in packets:
            if not packet.experiment_focal_case_id:
                return False
            if packet.primary_condition_run_id not in p1_run_ids:
                return False
            if len(packet.condition_run_ids or []) != 2:
                return False
            seen_focal_cases.add(packet.experiment_focal_case_id)
        return len(seen_focal_cases) == len(packets)

    # Hypothesis-keyed dispatch — adding a hypothesis adds one entry, not a new
    # `if hyp == H1` branch in ``_packets_match_execution``.
    _MATCHER_BY_HYPOTHESIS = {
        Hypothesis.H1: _h1_packets_match,
        Hypothesis.H2: _h2_packets_match,
    }
