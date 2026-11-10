"""File-backed cache for the lesson-plan infrastructure-planning step.

Cache invalidation contract
===========================

The cache is **content-addressed**: each subtopic's entry is keyed (implicitly,
via stored ``CacheMetadata``) by every input that could change the planning
output. An entry is a **hit** only when ALL of the following match:

- ``subtopic_id`` (the directory key — slugified)
- ``infrastructure_version`` — module-level constant ``INFRASTRUCTURE_VERSION``.
  Bump this when the planning pipeline's *shape* changes (new fields on a
  cached model, new pass added, etc.). Any bump invalidates EVERY entry on
  next read.
- ``textbook_hash`` — content hash of the textbook records fed into the
  pipeline. Any change to expert_content (new chunk, edit, reorder) yields a
  different hash and forces recompute.
- ``curriculum_hash`` — content hash of curriculum_objectives +
  evaluation_guide + entry_behaviour + instructional_materials + topic_key +
  subtopic_id. Any change to the curriculum row for this subtopic yields a
  different hash and forces recompute.
- ``model_name`` — the LLM the pipeline runs against. Switching models
  (e.g. gpt-4o → gpt-4o-mini) invalidates entries computed with the
  previous model.

Any input that DOESN'T appear above is implicitly assumed not to affect
the output. If that ever changes (e.g. you add a new piece of context),
add it to one of the hashes (or bump ``INFRASTRUCTURE_VERSION``).

What writes invalidate the cache
================================

- ``curriculum_topics`` / ``curriculum_subtopics`` row updated → the next
  pipeline run computes a different ``curriculum_hash`` and misses.
- ``expert_content`` textbook chunks updated → the next pipeline run
  computes a different ``textbook_hash`` and misses.
- LLM model swap → ``model_name`` differs from the entry's metadata and
  misses.
- Code change to a cached pipeline pass (``kc_extractor``,
  ``objective_atomizer``, ``assessment_designer`` — anything that changes
  what gets serialised) → bump ``INFRASTRUCTURE_VERSION`` and every
  entry misses on next read.
- Researcher decision "re-plan this subtopic from scratch" → call
  ``invalidate(subtopic_id)``. Whole-cache wipe: ``invalidate_all()``.

There is no DB-side write that triggers a callback into the cache; the
content-hash mechanism is the invalidation. The two explicit APIs below
(``invalidate`` / ``invalidate_all``) exist for the manual case only.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

from app.config import CONFIG
from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.types import (
    CacheMetadata,
    KCPlanningResult,
    Violation,
    slugify,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.kc_compression import (
    LessonStructure,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    AtomicObjective,
    CandidateKC,
    CandidateKCPlan,
    CoreStepBlueprint,
    LessonPlanObjective,
    StepEvidencePlan,
)
from app.shared.json_types import JsonObject

INFRASTRUCTURE_VERSION = "v2"


class InfrastructureArtifactCache:
    def __init__(
        self,
        cache_dir: Path | None = None,
        *,
        model_name: str | None = None,
    ) -> None:
        self._dir = cache_dir or CONFIG.lesson_plan.infrastructure_cache_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._model_name = model_name

    def _load_json_file(self, path: Path, *, default: object) -> object:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def _load_json_object(self, path: Path) -> JsonObject:
        payload = self._load_json_file(path, default={})
        if not isinstance(payload, dict):
            return {}
        return cast(JsonObject, payload)

    def _load_json_object_list(self, path: Path) -> list[JsonObject]:
        payload = self._load_json_file(path, default=[])
        if not isinstance(payload, list):
            return []
        return [cast(JsonObject, item) for item in payload if isinstance(item, dict)]

    @staticmethod
    def _optional_str(value: object) -> str | None:
        normalized = str(value or "").strip()
        return normalized or None

    def _load_metadata(self, subtopic_dir: Path) -> CacheMetadata | None:
        metadata_path = subtopic_dir / "metadata.json"
        if not metadata_path.exists():
            return None
        return CacheMetadata.model_validate_json(metadata_path.read_text(encoding="utf-8"))

    def _load_lesson_structure(self, lesson_structure_path: Path) -> LessonStructure:
        lesson_structure_payload = self._load_json_object(lesson_structure_path)
        objective_payloads = lesson_structure_payload.get("objectives")
        blueprint_payloads = lesson_structure_payload.get("blueprints")
        kc_payloads = lesson_structure_payload.get("kcs_by_objective_id")
        objective_rows = objective_payloads if isinstance(objective_payloads, list) else []
        blueprint_rows = blueprint_payloads if isinstance(blueprint_payloads, list) else []
        kc_rows = kc_payloads.items() if isinstance(kc_payloads, dict) else []

        objectives = [
            LessonPlanObjective.model_validate(item)
            for item in objective_rows
            if isinstance(item, dict)
        ]
        blueprints = [
            CoreStepBlueprint.model_validate(item)
            for item in blueprint_rows
            if isinstance(item, dict)
        ]
        kcs_by_objective_id = {
            str(lesson_objective_id): CandidateKC.model_validate(candidate_kc)
            for lesson_objective_id, candidate_kc in kc_rows
            if isinstance(candidate_kc, dict)
        }
        return LessonStructure(
            objectives=objectives,
            blueprints=blueprints,
            objectives_by_id={objective.lesson_objective_id: objective for objective in objectives},
            kcs_by_objective_id=kcs_by_objective_id,
        )

    def _load_atomic_artifacts(
        self,
        *,
        subtopic_dir: Path,
        atomic_objectives: list[AtomicObjective],
    ) -> tuple[
        dict[str, CandidateKCPlan],
        dict[str, list[AssessmentItem]],
        dict[str, list[Violation]],
        list[Violation],
    ]:
        kc_plans: dict[str, CandidateKCPlan] = {}
        assessment_items_by_atomic_objective: dict[str, list[AssessmentItem]] = {}
        violations_by_atomic_objective: dict[str, list[Violation]] = {}
        violations: list[Violation] = []

        for atomic_objective in atomic_objectives:
            atomic_dir = self._atomic_objective_dir(subtopic_dir, atomic_objective)
            decomposition_path = atomic_dir / "kc_decomposition.json"
            assessment_items_path = atomic_dir / "assessment_items.json"
            verification_path = atomic_dir / "verification.json"

            if decomposition_path.exists():
                kc_plans[atomic_objective.atomic_objective_id] = (
                    CandidateKCPlan.model_validate_json(
                        decomposition_path.read_text(encoding="utf-8")
                    )
                )
            assessment_items_by_atomic_objective[atomic_objective.atomic_objective_id] = [
                AssessmentItem.model_validate(item)
                for item in self._load_json_object_list(assessment_items_path)
            ]
            current_violations = [
                Violation(
                    code=str(item.get("code") or ""),
                    message=str(item.get("message") or ""),
                    severity=str(item.get("severity") or "error"),
                    atomic_objective_id=self._optional_str(item.get("atomic_objective_id")),
                    kc_id=self._optional_str(item.get("kc_id")),
                )
                for item in self._load_json_object_list(verification_path)
            ]
            violations_by_atomic_objective[atomic_objective.atomic_objective_id] = (
                current_violations
            )
            violations.extend(current_violations)

        return (
            kc_plans,
            assessment_items_by_atomic_objective,
            violations_by_atomic_objective,
            violations,
        )

    def get(
        self,
        *,
        subtopic_id: str,
        topic_key: str,
        textbook_hash: str,
        curriculum_hash: str,
    ) -> KCPlanningResult | None:
        subtopic_dir = self._subtopic_dir(subtopic_id)
        metadata = self._load_metadata(subtopic_dir)
        if metadata is None:
            return None
        if metadata.infrastructure_version != INFRASTRUCTURE_VERSION:
            return None
        if metadata.textbook_hash != textbook_hash or metadata.curriculum_hash != curriculum_hash:
            return None
        # Model swap invalidates: the previous entry was generated by a possibly
        # different model whose outputs (KC names, assessment items) we can't
        # guarantee match the current model's. Stored model_name was previously
        # written but never compared; this closes that gap.
        if metadata.model_name != self._model_name:
            return None

        atomic_objectives_path = subtopic_dir / "atomic_objectives.json"
        combined_kc_plan_path = subtopic_dir / "combined_kc_plan.json"
        lesson_structure_path = subtopic_dir / "lesson_structure.json"
        lesson_assessments_path = subtopic_dir / "lesson_assessment_items.json"
        step_evidence_plans_path = subtopic_dir / "step_evidence_plans.json"
        if not (
            atomic_objectives_path.exists()
            and combined_kc_plan_path.exists()
            and lesson_structure_path.exists()
            and step_evidence_plans_path.exists()
        ):
            return None

        atomic_objectives = [
            AtomicObjective.model_validate(item)
            for item in self._load_json_object_list(atomic_objectives_path)
        ]
        combined_kc_plan = CandidateKCPlan.model_validate_json(
            combined_kc_plan_path.read_text(encoding="utf-8")
        )
        lesson_structure = self._load_lesson_structure(lesson_structure_path)
        step_evidence_plans = {
            str(item["lesson_objective_id"]): StepEvidencePlan.model_validate(item)
            for item in self._load_json_object_list(step_evidence_plans_path)
            if item.get("lesson_objective_id")
        }
        assessment_items = {
            str(item["lesson_objective_id"]): AssessmentItem.model_validate(item)
            for item in self._load_json_object_list(lesson_assessments_path)
            if item.get("lesson_objective_id")
        }
        (
            kc_plans,
            assessment_items_by_atomic_objective,
            violations_by_atomic_objective,
            violations,
        ) = self._load_atomic_artifacts(
            subtopic_dir=subtopic_dir,
            atomic_objectives=atomic_objectives,
        )

        return KCPlanningResult(
            subtopic_id=subtopic_id,
            topic_key=topic_key,
            atomic_objectives=atomic_objectives,
            kc_plans=kc_plans,
            step_evidence_plans=step_evidence_plans,
            assessment_items_by_atomic_objective=assessment_items_by_atomic_objective,
            assessment_items=assessment_items,
            lesson_structure=lesson_structure,
            combined_kc_plan=combined_kc_plan,
            resolved_kcs=list(lesson_structure.kcs_by_objective_id.values()),
            violations_by_atomic_objective=violations_by_atomic_objective,
            violations=violations,
            from_cache=True,
            cache_metadata=metadata,
            planning_duration_ms=0,
            llm_calls_planning=0,
        )

    def put(
        self,
        *,
        subtopic_id: str,
        textbook_hash: str,
        curriculum_hash: str,
        planning_result: KCPlanningResult,
    ) -> CacheMetadata:
        subtopic_dir = self._subtopic_dir(subtopic_id)
        subtopic_dir.mkdir(parents=True, exist_ok=True)
        metadata = CacheMetadata(
            infrastructure_version=INFRASTRUCTURE_VERSION,
            textbook_hash=textbook_hash,
            curriculum_hash=curriculum_hash,
            model_name=self._model_name,
            computed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        (subtopic_dir / "metadata.json").write_text(
            metadata.model_dump_json(indent=2), encoding="utf-8"
        )
        (subtopic_dir / "atomic_objectives.json").write_text(
            json.dumps(
                [item.model_dump() for item in planning_result.atomic_objectives],
                indent=2,
            ),
            encoding="utf-8",
        )
        (subtopic_dir / "combined_kc_plan.json").write_text(
            planning_result.combined_kc_plan.model_dump_json(indent=2),
            encoding="utf-8",
        )
        (subtopic_dir / "lesson_structure.json").write_text(
            json.dumps(
                {
                    "objectives": [
                        objective.model_dump()
                        for objective in planning_result.lesson_structure.objectives
                    ],
                    "blueprints": [
                        blueprint.model_dump()
                        for blueprint in planning_result.lesson_structure.blueprints
                    ],
                    "kcs_by_objective_id": {
                        lesson_objective_id: candidate_kc.model_dump()
                        for lesson_objective_id, candidate_kc in (
                            planning_result.lesson_structure.kcs_by_objective_id.items()
                        )
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        (subtopic_dir / "lesson_assessment_items.json").write_text(
            json.dumps(
                [item.model_dump() for item in planning_result.assessment_items.values()],
                indent=2,
            ),
            encoding="utf-8",
        )
        (subtopic_dir / "step_evidence_plans.json").write_text(
            json.dumps(
                [item.model_dump() for item in planning_result.step_evidence_plans.values()],
                indent=2,
            ),
            encoding="utf-8",
        )

        for atomic_objective in planning_result.atomic_objectives:
            atomic_dir = self._atomic_objective_dir(subtopic_dir, atomic_objective)
            atomic_dir.mkdir(parents=True, exist_ok=True)
            kc_plan = planning_result.kc_plans.get(atomic_objective.atomic_objective_id)
            if kc_plan is not None:
                (atomic_dir / "kc_decomposition.json").write_text(
                    kc_plan.model_dump_json(indent=2),
                    encoding="utf-8",
                )
            (atomic_dir / "assessment_items.json").write_text(
                json.dumps(
                    [
                        item.model_dump()
                        for item in planning_result.assessment_items_by_atomic_objective.get(
                            atomic_objective.atomic_objective_id,
                            [],
                        )
                    ],
                    indent=2,
                ),
                encoding="utf-8",
            )
            (atomic_dir / "verification.json").write_text(
                json.dumps(
                    [
                        violation.__dict__
                        for violation in planning_result.violations_by_atomic_objective.get(
                            atomic_objective.atomic_objective_id,
                            [],
                        )
                    ],
                    indent=2,
                ),
                encoding="utf-8",
            )
        return metadata

    def invalidate(self, subtopic_id: str) -> bool:
        """Drop the cache entry for one subtopic, so the next ``get`` is a miss.

        Idempotent: returns ``True`` if a directory was removed, ``False`` if
        no entry existed for ``subtopic_id``. Use for researcher-triggered
        "re-plan this subtopic from scratch" — for any input change covered
        by the content-hash contract, you don't need to call this at all
        (the hash mismatch already invalidates).
        """
        subtopic_dir = self._subtopic_dir(subtopic_id)
        if not subtopic_dir.exists():
            return False
        shutil.rmtree(subtopic_dir)
        return True

    def invalidate_all(self) -> None:
        """Drop every cached subtopic.

        For wholesale recomputes (e.g. expert content overhaul outside the
        textbook_hash domain, or a manual reset after editing prompt
        templates that don't carry their own version key). Equivalent to
        ``rm -rf .cache/lesson-plan-infrastructure/*`` — preserves the
        outer cache dir itself.
        """
        for child in self._dir.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    def _subtopic_dir(self, subtopic_id: str) -> Path:
        return self._dir / slugify(subtopic_id)

    def _atomic_objective_dir(self, subtopic_dir: Path, atomic_objective: AtomicObjective) -> Path:
        return subtopic_dir / f"ao-{atomic_objective.objective_order:02d}"
