"""Pure builders for the rater packet-detail view — no I/O, just shape typed.

inputs (session plan, focal-case snapshot, review pack) into the detail payloads.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.evaluation.application.lesson_reference import (
    lesson_reference,
    reference_sheet,
)
from app.domains.evaluation.infrastructure.models import EvaluationPacket, EvaluationRating
from app.domains.learner_state.domain.models import humanise_misconception_code

# WeasyPrint is the active renderer for the expert rater packs (HTML/CSS -> PDF):
# it renders reading-note / excerpt markdown natively and carries full Unicode, so
# no ``■`` missing-glyph boxes. The reportlab modules (``audit_pack_pdf``,
# ``h1_worksheet_pdf``) are kept in place as a fallback; ``H1_MAJOR_ISSUE_FLAGS``
# still lives in (and is imported from) ``h1_worksheet_pdf`` as its source of truth.
from app.shared.experiment_enums import FocalCaseType, Hypothesis
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


def _stripped_text_or_none(value: object) -> str | None:
    """Return ``value`` stripped + non-empty, or ``None`` otherwise.

    Local replacement for the retired ``json_coerce.as_text``.
    """
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _first_stripped_text(raw: JsonObject, keys: tuple[str, ...]) -> str | None:
    """First key in ``keys`` whose value is a non-empty text, else ``None``.

    Local replacement for the retired ``json_coerce.first_text``.
    """
    for key in keys:
        text = _stripped_text_or_none(raw.get(key))
        if text is not None:
            return text
    return None


def _stripped_str_list(value: object) -> list[str]:
    """Strip-and-filter narrow on a list of strings; ``[]`` if not a list.

    Local replacement for the retired ``json_coerce.as_str_list``.
    """
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _dict_list(value: object) -> list[JsonObject]:
    """Filter a list down to its dict items; ``[]`` if not a list.

    Local replacement for the retired ``json_coerce.as_objects``.
    """
    if not isinstance(value, list):
        return []
    return [cast(JsonObject, item) for item in value if isinstance(item, dict)]


if TYPE_CHECKING:
    from app.domains.experiments.infrastructure.models import ExperimentFocalCase

# Rater rubrics per the Final Evaluation Protocol (§6). H1 = 4 pack-level dimensions;
# H2 = 5 section-level dimensions. All scored 1-5. Textbook factual fidelity / source
# support are deliberately NOT H1 dimensions — they are checked in the separate
# source-grounding audit. There is no separate H2 clarity diagnostic.


_REFERENCE_IDENTITY_FIELDS = ("subject", "grade", "term", "week", "topic", "subtopic", "theme")


def rating_payload(
    rating: EvaluationRating | None,
    *,
    rater_id: str | None,
    packet: EvaluationPacket,
) -> dict[str, object] | None:
    """Render a stored rating to the rater-facing packet payload."""
    if rating is None:
        return None
    return {
        "rating_id": rating.rating_id,
        "evaluation_packet_id": packet.evaluation_packet_id,
        "rater_id": rater_id or "",
        "hypothesis": Hypothesis(rating.hypothesis),
        "overall_score": rating.overall_score,
        "rubric_scores": dict(rating.rubric_scores or {}),
        "section_scores": rating.section_scores,
        "diagnostic_scores": rating.diagnostic_scores,
        "notes": rating.notes,
        "created_at": rating.created_at,
        "updated_at": rating.updated_at,
        "submitted_at": rating.submitted_at,
    }


def _coalesced_identity(
    session_plan: SessionPlanView, pack_manifest: PostClassReviewPack | None
) -> dict[str, object]:
    """Prefer the session-plan value per identity field, else the pack manifest's."""
    identity: dict[str, object] = {}
    for field in _REFERENCE_IDENTITY_FIELDS:
        value = getattr(session_plan, field)
        if not value and pack_manifest is not None:
            value = getattr(pack_manifest, field)
        identity[field] = value
    return identity


class PacketDetailPayloads:
    """Stateless payload builders composed by the packet-detail path."""

    def learner_state_card_payload(
        self,
        *,
        focal_case: ExperimentFocalCase,
        session_plan: SessionPlanView,
    ) -> dict[str, object]:
        raw_snapshot = focal_case.learner_state_snapshot
        snapshot: JsonObject = raw_snapshot if isinstance(raw_snapshot, dict) else {}
        raw_prefs = snapshot.get("preferences")
        preferences: JsonObject | None = raw_prefs if isinstance(raw_prefs, dict) else None
        raw_profile = snapshot.get("curriculum_profile")
        curriculum_profile: JsonObject | None = (
            raw_profile if isinstance(raw_profile, dict) else None
        )
        mastered_step_ids = _stripped_str_list(snapshot.get("mastered_step_ids"))
        step_index = {step.step_id: step for step in session_plan.steps if step.step_id}
        objective_text_by_id = self.objective_text_by_id(session_plan)
        mastered_sections: list[JsonObject] = []
        for mastered_step_id in mastered_step_ids:
            step = step_index.get(mastered_step_id)
            if step is None:
                mastered_sections.append({"step_id": mastered_step_id})
                continue
            mastered_sections.append(
                {
                    "step_id": step.step_id,
                    "title": step.title,
                    "lesson_objective_id": step.lesson_objective_id,
                    "objective_text": (
                        objective_text_by_id.get(step.lesson_objective_id or "")
                        if step.lesson_objective_id
                        else None
                    ),
                }
            )
        return {
            "focal_case_type": FocalCaseType(focal_case.focal_case_type),
            "curriculum_profile": curriculum_profile,
            "preferences": preferences,
            "mastered_sections": mastered_sections,
            "objective_states": self.objective_states_payload(
                snapshot=snapshot,
                objective_text_by_id=objective_text_by_id,
            ),
            # Session-level Interest/Affect (1-5) from the post-class survey — a
            # pack-level fit signal the rater should see alongside the per-objective
            # state. Absent on older snapshots.
            "session_survey": (
                snapshot.get("session_survey")
                if isinstance(snapshot.get("session_survey"), dict)
                else None
            ),
            "selection_metadata": focal_case.selection_metadata,
        }

    def objective_states_payload(
        self,
        *,
        snapshot: JsonObject,
        objective_text_by_id: dict[str, str],
    ) -> list[dict[str, object]]:
        """Per-objective learner state for the H2 learner-state card (Protocol §4).

        Reads the ``objective_states`` recorded on the focal case's learner-state
        snapshot (a ``LearnerState.model_dump``); one row per lesson objective with
        the assigned band (remediate/reinforce/extend), confidence, perceived
        difficulty, and any recorded misconception + evidence. The objective text is
        resolved from the session plan so the card reads without an objective lookup.
        """
        rows: list[dict[str, object]] = []
        for raw_state in _dict_list(snapshot.get("objective_states")):
            lesson_objective_id = _stripped_text_or_none(raw_state.get("lesson_objective_id"))
            if lesson_objective_id is None:
                continue
            rows.append(
                {
                    "lesson_objective_id": lesson_objective_id,
                    "objective_text": objective_text_by_id.get(lesson_objective_id),
                    "band": _stripped_text_or_none(raw_state.get("band")),
                    "mastery_score": raw_state.get("mastery_score"),
                    "confidence": _stripped_text_or_none(raw_state.get("confidence")),
                    "perceived_difficulty": _stripped_text_or_none(
                        raw_state.get("perceived_difficulty")
                    ),
                    "misconception_code": _stripped_text_or_none(
                        raw_state.get("misconception_code")
                    ),
                    # Older snapshots carry only the distractor code — derive prose
                    # so a recorded misconception is never shown as "none recorded".
                    "misconception_description": (
                        _stripped_text_or_none(raw_state.get("misconception_description"))
                        or (
                            humanise_misconception_code(code)
                            if (code := _stripped_text_or_none(raw_state.get("misconception_code")))
                            else None
                        )
                    ),
                    "evidence_refs": _stripped_str_list(raw_state.get("evidence_refs")),
                }
            )
        return rows

    def objective_text_by_id(self, session_plan: SessionPlanView) -> dict[str, str]:
        texts: dict[str, str] = {}
        for objective in session_plan.lesson_plan_objectives:
            if not objective.lesson_objective_id:
                continue
            texts[objective.lesson_objective_id] = (
                objective.objective_text or objective.lesson_objective_id
            )
        return texts

    def objectives_payload(self, session_plan: SessionPlanView) -> list[dict[str, str | None]]:
        return [
            {
                "lesson_objective_id": objective.lesson_objective_id,
                "objective_text": objective.objective_text or objective.lesson_objective_id,
            }
            for objective in session_plan.lesson_plan_objectives
            if objective.lesson_objective_id
        ]

    def reference_sheet_payload(
        self,
        session_plan: SessionPlanView,
        *,
        pack_manifest: PostClassReviewPack | None,
    ) -> dict[str, object]:
        """The lesson as the rater is shown it: one reference, rendered here as the drawer.

        Built by ``lesson_reference`` and rendered by ``reference_sheet``, the same
        pair the worksheet PDF and the LLM judge's packet render from, so that the
        three surfaces describe one lesson. The pack manifest fills an identity field
        or the objective list only where the plan left it empty.

        Textbook references are NOT shown to H1/H2 raters (Final Evaluation Protocol
        §6/§9). Source faithfulness is checked in the separate source-grounding audit,
        which reads references from the condition run.
        """
        sheet = reference_sheet(lesson_reference(session_plan))
        sheet.update(_coalesced_identity(session_plan, pack_manifest))
        if not sheet["curriculum_objectives"] and pack_manifest is not None:
            sheet["curriculum_objectives"] = [
                text
                for raw in pack_manifest.curriculum_objectives
                if (
                    text := _first_stripped_text(
                        raw, ("objective_text", "text", "description", "title")
                    )
                )
                is not None
            ]
        if not sheet["instructional_materials"] and pack_manifest is not None:
            sheet["instructional_materials"] = list(pack_manifest.instructional_materials)
        return sheet

    def review_pack_payload(
        self,
        *,
        artefact: Artefact,
        manifest: PostClassReviewPack,
    ) -> dict[str, object]:
        return {
            "scope": artefact.scope,
            "manifest": self.review_pack_manifest_payload(manifest),
        }

    def review_pack_manifest_payload(
        self,
        manifest: PostClassReviewPack,
    ) -> JsonObject:
        return {
            "subject": manifest.subject,
            "track": manifest.track,
            "grade": manifest.grade,
            "term": manifest.term,
            "week": manifest.week,
            "topic": manifest.topic,
            "subtopic": manifest.subtopic,
            "theme": manifest.theme,
            "misconceptions": list(manifest.misconceptions),
            "steps": [
                cast(JsonObject, step.model_dump(mode="json", exclude_none=True))
                for step in manifest.steps
            ],
            "instructional_materials": list(manifest.instructional_materials),
            # Textbook references are deliberately ABSENT from rater-facing pack
            # payloads: grounded conditions carry citations and ungrounded ones
            # don't, so exposing them would unblind the condition. Citations are
            # judged in the separate source-grounding audit.
        }
