"""The Part 2 analysis handoff: every expected rating, its provenance, and nothing derived.

An external analyst cannot check a conclusion they cannot re-derive. This writes the
snapshot they need: one row per criterion cell that was *assigned*, answered or not, with
the rater's own words kept beside the number the analysis used, and the A/B mapping that
turns one into the other.

Three identities matter and are easy to lose. A *panel* is one learner-lesson-objective
comparison and is shared by the two raters who judged it, even though each saw a
different blind packet id and the opposite A/B order; joining on the packet id alone
silently makes two independent ratings look like two different targets. A *case* is one
learner-lesson pair, and its P0 side is a single pack reused across every learner in that
lesson, so the cases are not independent artefacts. A *learner* recurs across lessons,
which is the dependency the case-level analysis missed.

Nothing here decides an analysis. Derived scores are carried in their own columns, marked
with the coding that produced them, so a reader can reproduce the existing numbers before
choosing to disagree with them.

Run with::

    uv run python -m experiments.human_rating.export "<delivered folder>" <out dir>
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.domains.evaluation.domain.study_instrument import H2_CRITERIA

from . import mapping, panels, reference, sources
from .results import DOCUMENT, answers, students

RUN = "h2-deepseek-clean"
#: The five response options, and the score the existing analysis gave each one. Positive
#: favours P1. Recorded here rather than inline so a row can name the coding it used.
FIVE_POINT = {"clearly better": 2, "slightly better": 1}
SCORE_CODING = "five_point_signed_v1"


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


@dataclass(frozen=True)
class Artefacts:
    """The generated materials behind one case, addressed by content rather than by label."""

    p0_hash: str
    p1_hash: str
    evidence: dict[str, str]
    """Per objective id, whether the personaliser had learner state for it."""


def artefacts(run: str = RUN) -> dict[tuple[str, str], Artefacts]:
    record = json.loads((sources.H2_RUNS / run / "run.json").read_text())
    by: dict[tuple[str, str], dict[str, Any]] = {}
    for case in record["cases"]:
        by.setdefault((case["lesson"], case["student"]), {})[case["condition"]] = case
    out = {}
    for key, sides in by.items():
        p1 = sides["P1"]
        out[key] = Artefacts(
            p0_hash=_sha(sides["P0"]["sections"]),
            p1_hash=_sha(p1["sections"]),
            evidence={
                row["lesson_objective_id"]: row["outcome"]
                for row in (p1.get("personalisation") or [])
            },
        )
    return out


def _objectives(lesson: str, plans: dict[str, Any]) -> list[str]:
    return [oid for oid, _ in reference.objectives(plans[lesson])]


def _case_id(lesson: str, student: str) -> str:
    return f"{lesson}/{student}"


def _score(option: str, arm_a: str, arm_b: str) -> tuple[str, int | None]:
    """The arm the rater chose, and the signed score the existing analysis gave it.

    The rater's own mark is only a tick — "Yes", "yes" or a check glyph. The response is
    which *column* carries it, so the option label is what has to be read.
    """
    side = next((s for s in "AB" if option.startswith(f"{s} ")), "")
    arm = {"A": arm_a, "B": arm_b}.get(side, "neither")
    text = option.lower()
    if "same" in text:
        return arm, 0
    size = next((v for k, v in FIVE_POINT.items() if k in text), None)
    if size is None:
        return arm, None
    return arm, size if arm == "P1" else -size


def ratings_long(folder: Path, plans: dict[str, Any], run: str = RUN) -> list[dict[str, Any]]:
    """Every criterion cell that was assigned, answered or not."""
    key = {(a.rater, a.external_id): a for a in mapping.load_h2()}
    packs = artefacts(run)
    rows: list[dict[str, Any]] = []
    for path in sorted(folder.glob("Part 2*/Rater */*.docx")):
        match = DOCUMENT.match(path.name)
        if not match:
            continue
        job = key[(f"rater-{match['rater']}", match["external"])]
        marks, sheets, _ = answers(path)
        given = {(m.objective, m.criterion): m for m in marks}
        # The document names its own objective. Its ordinal does not: only objectives the
        # student has class work for get a panel, so panel 1 is whichever of those comes
        # first in curriculum order. Reading position instead misidentified 36 of 70.
        shown = {p.ordinal: p for p in panels.displayed(path, plans[job.lesson])}
        legacy = _objectives(job.lesson, plans)
        pack = packs[(job.lesson, job.student)]
        for sheet in range(1, sheets + 1):
            panel = shown.get(sheet)
            objective = (panel.objective_id or "") if panel else ""
            for criterion in range(1, len(H2_CRITERIA) + 1):
                mark = given.get((sheet, criterion))
                arm, score = _score(mark.column, job.a, job.b) if mark else ("", None)
                rows.append(
                    {
                        "judgement_id": f"{job.rater}/{job.external_id}/o{sheet}/c{criterion}",
                        "assignment_id": f"{job.rater}/{job.external_id}",
                        "panel_id": f"{_case_id(job.lesson, job.student)}/obj{sheet}",
                        "case_id": _case_id(job.lesson, job.student),
                        "learner_id": job.student,
                        "lesson_id": job.lesson,
                        "objective_id": objective,
                        "objective_resolved_from": "document heading" if panel else "not found",
                        "objective_id_legacy_positional": (
                            legacy[sheet - 1] if sheet <= len(legacy) else ""
                        ),
                        "panel_ordinal": sheet,
                        "rater_id": job.rater,
                        "criterion_id": H2_CRITERIA[criterion - 1].id,
                        "criterion_index": criterion,
                        "rubric_version": "h2_comparative_2026-09-04",
                        "external_packet_id": job.external_id,
                        "internal_packet_id": job.internal_id,
                        "condition_a": job.a,
                        "condition_b": job.b,
                        "artifact_a_id": f"{run}/{job.lesson}/{job.student}/{job.a}",
                        "artifact_b_id": f"{run}/{job.lesson}/{job.student}/{job.b}",
                        "presentation_order": job.order,
                        "response_raw": mark.column if mark else "",
                        "response_mark_typed": mark.value if mark else "",
                        "response_code_raw": "",
                        "response_status": "answered" if mark else "blank",
                        "missing_reason": "" if mark else "unknown",
                        "chosen_arm": arm,
                        "score_used": "" if score is None else score,
                        "score_coding_id": SCORE_CODING if mark else "",
                        # What the personaliser held, not what the rater saw and not
                        # whether the learner demonstrated anything. Three different
                        # questions; only this one is answerable from the run record.
                        "model_learner_state": {
                            "personalised": "state_present",
                            "no_learner_state": "state_absent",
                        }.get(pack.evidence.get(objective, ""), "unknown"),
                        "rater_reference_id": f"{job.external_id}-lm",
                        "submitted_at": "",
                        "comment": (mark.comment if mark else "").strip(),
                        "source_file": str(path.relative_to(folder)),
                        "source_record_id": f"table{sheet}/row{criterion}",
                    }
                )
    return rows


def learner_rows() -> list[dict[str, Any]]:
    """The nine learners, with the provenance of the stratum used to split the analysis."""
    return [
        {
            "learner_id": row["student"],
            "reconstructed_attainment_group": row["ability_stratum"],
            "original_sampling_stratum": "unknown",
            "attainment_rank": row["ability_rank"],
            "attainment_score": row["mean_share_correct"],
            "attainment_score_definition": "mean share correct across the lessons sat",
            "lessons_sat": row["lessons_sat"],
            "population_ranked": "the nine selected learners, NOT the class of forty",
            "attainment_source": "teacher's marks on the three study lessons' class work",
            "attainment_measured": "same class work that produced the P1 learner state",
            "group_definition": "reconstructed post hoc: rank thirds of the nine",
            "group_recorded_at_sampling": "no",
            "selection_method": "stratified random from three teacher-assigned ability "
            "categories in a class of forty; the categories were not recorded",
            "eligible_stratum_population_n": "",
            "inclusion_probability": "",
        }
        for row in students()
    ]


def case_rows(run: str = RUN) -> list[dict[str, Any]]:
    """Every planned learner-lesson comparison, with what produced each side."""
    record = json.loads((sources.H2_RUNS / run / "run.json").read_text())
    packs = artefacts(run)
    planned = {(a.lesson, a.student) for a in mapping.load_h2()}
    rated = {(a.lesson, a.student) for a in mapping.load_h2()}
    generated = {(c["lesson"], c["student"]) for c in record["cases"]}
    rows = []
    for lesson, student in sorted(generated | planned):
        pack = packs.get((lesson, student))
        rows.append(
            {
                "case_id": _case_id(lesson, student),
                "learner_id": student,
                "lesson_id": lesson,
                "case_status": "rated" if (lesson, student) in rated else "generated_not_assigned",
                "missing_reason": "",
                "p0_artifact_id": f"{run}/{lesson}/{student}/P0",
                "p1_artifact_id": f"{run}/{lesson}/{student}/P1",
                "p0_content_sha256": pack.p0_hash if pack else "",
                "p1_content_sha256": pack.p1_hash if pack else "",
                "p0_source_run": record["base"]["run"],
                "p0_source_condition": record["base"]["condition"],
                "p0_source_repeat": record["base"]["repeat"],
                "p1_run": run,
                "p1_model": record.get("model", ""),
                "p1_policy_condition": record.get("policy_condition", ""),
                "objectives_with_learner_state": sum(
                    1 for v in (pack.evidence.values() if pack else []) if v == "personalised"
                ),
                "objectives_without_learner_state": sum(
                    1 for v in (pack.evidence.values() if pack else []) if v == "no_learner_state"
                ),
                "learner_state_input": f"classwork {lesson} / {student}"
                " (not exported: minors' work)",
            }
        )
    return rows


def _commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return "unknown"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def manifest(out: Path, folder: Path, ratings: list[dict[str, Any]]) -> dict[str, Any]:
    answered = [r for r in ratings if r["response_status"] == "answered"]
    return {
        "export_created_utc": datetime.now(UTC).isoformat(),
        "ratings_cutoff": "live Google Drive folder as read at export time",
        "collection_complete": False,
        "collection_note": "rater-4 has 11 unanswered cells; all other raters complete",
        "code_commit": _commit(),
        # The delivered folder sits under a personal cloud-storage path carrying the
        # researcher's address. The bundle circulates; the path does not.
        "source_folder": f".../{folder.name}",
        "part2_run": RUN,
        "counts": {
            "assigned_criterion_cells": len(ratings),
            "answered_criterion_cells": len(answered),
            "blank_criterion_cells": len(ratings) - len(answered),
            "objective_panels_per_rater": len({(r["rater_id"], r["panel_id"]) for r in ratings}),
            "distinct_panels": len({r["panel_id"] for r in ratings}),
            "cases": len({r["case_id"] for r in ratings}),
            "learners": len({r["learner_id"] for r in ratings}),
            "lessons": len({r["lesson_id"] for r in ratings}),
            "raters": len({r["rater_id"] for r in ratings}),
        },
        "the_199": "199 is the count of ANSWERED CRITERION CELLS. It is not panels: there "
        "are 70 rater-panels and 210 assigned criterion cells.",
        "known_missing_metadata": [
            "submitted_at: Google Docs does not expose a per-cell timestamp",
            "missing_reason: never recorded; all blanks are 'unknown'",
            "response_code_raw: the form stores free text, not a code",
            "the sampling strata were not recorded at selection and are reconstructed",
            "evidence_in_prompt: whether learner state reached the prompt is recorded "
            "nowhere and is NOT inferred from the generation outcome",
        ],
        "not_included": [
            "P0/P1 pack text and learner class work — real minors' data, held back "
            "pending an explicit sharing decision by the researcher",
        ],
    }


def bundle(folder: Path, out: Path) -> Path:
    plans = sources.plans()
    ratings = ratings_long(folder, plans)
    write_csv(out / "part2" / "ratings_long.csv", ratings)
    write_csv(out / "part2" / "learners.csv", learner_rows())
    write_csv(out / "part2" / "cases.csv", case_rows())
    (out / "manifest.json").write_text(json.dumps(manifest(out, folder, ratings), indent=2))
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    print(f"wrote {bundle(Path(sys.argv[1]), Path(sys.argv[2]))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
