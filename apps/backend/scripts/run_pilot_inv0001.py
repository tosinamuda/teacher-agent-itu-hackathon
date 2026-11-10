"""Drive the full research pipeline for the lessons in an investigation.

Idempotent pilot runner: for each lesson scoped by an investigation it ensures
an approved lesson plan, an experiment, a succeeded H1 execution, synthetic
learner evidence, focal selection, a succeeded H2 execution, and exported
evaluation packets — then prints the resulting blinded rater queue.

Each step checks current state first, so re-running never regenerates work that
already exists (it never spends LLM budget twice). Synthetic STUDENTS seed H2
learner evidence; raters stay real (no synthetic ratings here).

Usage:
    uv run python scripts/run_pilot_inv0001.py [--dry-run] \
        [--investigation INV-9b18...] [--focal 4] [--synth 6]
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from typing import Any

BASE = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json", "x-teacher-code": "uncle-tosin"}
TERMINAL = {"succeeded", "failed"}


class ApiError(Exception):
    def __init__(self, code: int, detail: str) -> None:
        super().__init__(f"HTTP {code}: {detail}")
        self.code = code
        self.detail = detail


def api(method: str, path: str, body: dict | None = None, timeout: float = 60.0) -> dict[str, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, method=method, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raise ApiError(exc.code, exc.read().decode()) from exc


def generate_plan_with_retry(lesson_period_id: str, attempts: int = 3) -> str:
    """Generate a lesson plan, retrying any residual stochastic validator rejection.

    Lesson-plan generation is non-deterministic. The >4-objective cap is now a
    deterministic check the in-loop refine self-corrects on (it feeds a
    "merge/drop to <=4" violation back into the drafter), so the strict validator
    should rarely reject for that reason. This retry stays as a thin backstop for
    the rare draft that still trips the final safety net.
    """
    last = ""
    for attempt in range(1, attempts + 1):
        try:
            body = {"session_id": lesson_period_id}
            gen = api("POST", "/artefacts/lesson-plans/generate", body, timeout=900)
            return str(gen["version_id"])
        except ApiError as exc:
            last = exc.detail
            log(f"    generate attempt {attempt}/{attempts} rejected: {exc.detail[:160]}")
    raise SystemExit(f"  ! plan generation failed after {attempts} attempts: {last}")


def log(msg: str) -> None:
    print(msg, flush=True)


def poll_execution(experiment_id: str, hypothesis: str, *, timeout: float = 1500.0) -> str:
    """Poll the experiment until its latest <hypothesis> execution is terminal."""
    deadline = time.monotonic() + timeout
    last = ""
    while time.monotonic() < deadline:
        detail = api("GET", f"/experiments/{experiment_id}")
        runs = [e for e in detail.get("executions", []) if e.get("hypothesis") == hypothesis]
        if runs:
            status = str(runs[0].get("status", ""))
            if status != last:
                log(f"      {hypothesis} execution: {status}")
                last = status
            if status in TERMINAL:
                return status
        time.sleep(8)
    raise SystemExit(f"  ! timed out waiting for {hypothesis} on {experiment_id}")


def latest_succeeded(detail: dict[str, Any], hypothesis: str) -> str | None:
    for e in detail.get("executions", []):
        if e.get("hypothesis") == hypothesis and e.get("status") == "succeeded":
            execution_id = e.get("execution_id")
            return None if execution_id is None else str(execution_id)
    return None


def evidence_candidates(detail: dict[str, Any]) -> list[dict[str, Any]]:
    return [c for c in detail.get("focal_learner_candidates", []) if c.get("has_evidence")]


def run_lesson(
    lesson: dict[str, Any], workspace_id: str, focal_n: int, synth_n: int, dry: bool
) -> str:
    title = lesson.get("lesson_title")
    lp = lesson["lesson_period_id"]
    log(f"\n=== Lesson: {title}  (period {lp}) — status={lesson.get('status')} ===")

    # 1. Approved lesson plan ------------------------------------------------
    version_id = lesson.get("latest_approved_version_id")
    if not version_id:
        if dry:
            log("  [plan] would generate + approve a lesson plan")
        else:
            log("  [plan] generating (synchronous DSPy, may take minutes)…")
            version_id = generate_plan_with_retry(lp)
            plans = api("GET", f"/content?plan_version_id={version_id}&type=lesson-plan")
            plan = plans[0]  # type: ignore[index]
            api("POST", f"/content/{plan['id']}/approvals", {"expected_version": plan["version"]})
            api("POST", "/content", {"plan_version_id": version_id, "type": "class-test"})
            log(f"  [plan] approved {version_id}, class test drafted")
    else:
        log(f"  [plan] approved already: {version_id}")
    if dry:
        return "(dry-run)"

    # 2. Experiment ----------------------------------------------------------
    experiment_id = str(lesson.get("experiment_id") or "")
    if not experiment_id:
        created = api(
            "POST",
            "/experiments",
            {"teacher_workspace_id": workspace_id, "plan_version_id": version_id},
        )
        experiment_id = str(created["experiment_id"])
        log(f"  [experiment] created {experiment_id}")
    else:
        log(f"  [experiment] exists: {experiment_id}")

    detail = api("GET", f"/experiments/{experiment_id}")

    # 3. H1 (C0–C4) ----------------------------------------------------------
    if latest_succeeded(detail, "H1"):
        log("  [H1] already succeeded")
    else:
        log("  [H1] launching C0–C4 execution…")
        api("POST", f"/experiments/{experiment_id}/executions", {"hypothesis": "H1"})
        if poll_execution(experiment_id, "H1") != "succeeded":
            raise SystemExit("  ! H1 failed")

    # 4. Synthetic learner evidence (for H2) ---------------------------------
    detail = api("GET", f"/experiments/{experiment_id}")
    cands = evidence_candidates(detail)
    if len(cands) < focal_n:
        log(f"  [evidence] {len(cands)} < {focal_n} with evidence; seeding {synth_n} synthetic…")
        api("POST", f"/experiments/{experiment_id}/synthetic-students?n={synth_n}")
        deadline = time.monotonic() + 1200
        while time.monotonic() < deadline:
            detail = api("GET", f"/experiments/{experiment_id}")
            cands = evidence_candidates(detail)
            if len(cands) >= focal_n:
                break
            time.sleep(8)
        log(f"  [evidence] now {len(cands)} learners with evidence")
    else:
        log(f"  [evidence] {len(cands)} learners already have evidence")
    if len(cands) < focal_n:
        raise SystemExit(f"  ! only {len(cands)} learners with evidence; need {focal_n}")

    # 5. Focal selection -----------------------------------------------------
    focal_ids = [c["learner_id"] for c in cands[:focal_n]]
    api("PUT", f"/experiments/{experiment_id}/focal-learners", {"learner_ids": focal_ids})
    log(f"  [focal] selected {len(focal_ids)}: {', '.join(focal_ids)}")

    # 6. H2 (P0/P1) ----------------------------------------------------------
    detail = api("GET", f"/experiments/{experiment_id}")
    if latest_succeeded(detail, "H2"):
        log("  [H2] already succeeded")
    else:
        log("  [H2] launching P0/P1 personalisation…")
        api(
            "POST",
            f"/experiments/{experiment_id}/executions",
            {"hypothesis": "H2", "focal_case_count": focal_n},
        )
        if poll_execution(experiment_id, "H2") != "succeeded":
            raise SystemExit("  ! H2 failed")

    # 7. Export evaluation packets (H1 + H2) ---------------------------------
    detail = api("GET", f"/experiments/{experiment_id}")
    for ex in detail.get("executions", []):
        if ex.get("status") == "succeeded":
            packets = api("POST", f"/experiments/executions/{ex['execution_id']}/packets/export")
            log(f"  [export] {ex['hypothesis']} -> {len(packets)} packets")
    return experiment_id


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--investigation", default="INV-9b181705ad024c8e9ad04826f70ee931")
    ap.add_argument("--focal", type=int, default=4)
    ap.add_argument("--synth", type=int, default=6)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    inv = api("GET", f"/experiments/investigations/{args.investigation}")
    ws = inv["teacher_workspace_id"]
    log(f"Investigation {inv['investigation_code']} — {inv['title']}")
    log(f"Workspace {ws} · {inv['lesson_count']} lessons · dry_run={args.dry_run}")

    experiment_ids = []
    for lesson in inv["lessons"]:
        experiment_ids.append(run_lesson(lesson, ws, args.focal, args.synth, args.dry_run))

    if args.dry_run:
        return

    # Final: the blinded rater queue ----------------------------------------
    rater = api("POST", "/evaluation/raters/session", {"display_name": "Pilot Queue Check"})
    rid = rater.get("rater_id", "")
    h1 = api("GET", f"/evaluation/h1/packets?rater_id={rid}")
    h2 = api("GET", f"/evaluation/h2/packets?rater_id={rid}")
    log(f"\n=== Rater queue ===\n  H1 packets: {len(h1)}\n  H2 packets: {len(h2)}")
    log(f"  experiments: {', '.join(e for e in experiment_ids if e)}")
    print("DONE", flush=True)


if __name__ == "__main__":
    try:
        main()
    except ApiError as exc:
        raise SystemExit(f"  ! API error: {exc}") from exc
