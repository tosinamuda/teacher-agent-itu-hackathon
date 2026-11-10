"""A digest recorded of a file the export rewrote must not give the original back."""

from __future__ import annotations

import hashlib
import itertools
import json
import string
import subprocess
from pathlib import Path
from typing import Any

from experiments.dataset_export.build import Entry, Release, collect, write
from experiments.dataset_export.rewrite import published
from experiments.dataset_export.seal import seal
from experiments.dataset_export.sources import Dataset, Repository, Source
from experiments.dataset_export.verify import against, leaks, verify

LESSON = "t9-w01"


def _plan(question: str, school: str = "gtc", **judged: object) -> dict[str, Any]:
    step = {"question": question, **judged}
    return {"plan_id": "plan-1", "session_id": f"{school}-{LESSON}", "steps": [step]}


def _unjudged(plan: dict[str, Any]) -> dict[str, Any]:
    steps = [{k: v for k, v in step.items() if k != "sets_work"} for step in plan["steps"]]
    return {**plan, "steps": steps}


def _as_written(plan: dict[str, Any]) -> str:
    return json.dumps(plan, indent=2, ensure_ascii=False) + "\n"


def _digest(text: str, length: int) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:length]


def _entry(path: str, text: str) -> Entry:
    original = text.encode()
    return Entry(path, original, published(path, original))


def _sealed(*entries: Entry) -> tuple[Entry, ...]:
    seal([Release("test", (), entries, ())])
    return entries


def test_a_plan_digest_and_the_digest_of_it_follow_the_published_plan():
    plan_text = _as_written(_plan("How many sides has a hexagon?"))
    recorded = _digest(plan_text, 16)
    plan, run, fingerprint = _sealed(
        _entry(f"transcripts/{LESSON}/session-plan.json", plan_text),
        _entry("runs/r1/run.json", json.dumps({"plans": {LESSON: recorded}})),
        _entry(
            "runs/r1/fingerprint.json",
            json.dumps({"inputs": {f"plan.{LESSON}": _digest(recorded, 12)}}),
        ),
    )
    shipped = _digest(plan.body.decode(), 16)
    assert json.loads(run.body)["plans"][LESSON] == shipped
    assert json.loads(fingerprint.body)["inputs"][f"plan.{LESSON}"] == _digest(shipped, 12)


def test_a_superseded_plan_named_by_its_digest_is_renamed_to_the_published_digest():
    question = "How many triangles has an octagon?"
    recorded = _digest(_as_written(_plan(question)), 16)
    case = {"lesson": LESSON, "plan_sha256": recorded, "plan": _plan(question)}
    (frozen,) = _sealed(_entry(f"frozen/{LESSON}-{recorded}.json", json.dumps(case, indent=2)))
    digest = _digest(_as_written(_plan(question, school="sch")), 16)
    assert json.loads(frozen.body)["plan_sha256"] == digest
    assert frozen.path == f"frozen/{LESSON}-{digest}.json"


def test_a_plan_frozen_with_a_judgement_added_after_its_digest_still_has_its_digest_replaced():
    question = "How many triangles has an octagon?"
    recorded = _digest(_as_written(_plan(question)), 16)
    case = {"lesson": LESSON, "plan_sha256": recorded, "plan": _plan(question, sets_work=True)}
    (frozen,) = _sealed(_entry(f"frozen/{LESSON}-{recorded}.json", json.dumps(case, indent=2)))
    digest = _digest(_as_written(_plan(question, school="sch")), 16)
    assert json.loads(frozen.body)["plan_sha256"] == digest
    assert frozen.path == f"frozen/{LESSON}-{digest}.json"


def test_a_hex_run_that_is_no_digest_of_an_original_is_left_as_it_was():
    record = json.dumps({"candidate": "cand-1a2b3c4d", "commit": "0517aced4533"})
    _, run = _sealed(
        _entry(f"transcripts/{LESSON}/session-plan.json", _as_written(_plan("Name the polygon."))),
        _entry("runs/r1/run.json", record),
    )
    assert run.body == record.encode()
    assert not run.rewritten


def _commit(repo: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text, encoding="utf-8")
    git = ["git", "-C", str(repo), "-c", "user.name=fixture", "-c", "user.email=f@example.com"]
    subprocess.run([*git, "init", "-q"], check=True)
    subprocess.run([*git, "add", "-A"], check=True)
    subprocess.run([*git, "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"], check=True)


def _reproduces(text: str, letters: str, published_runs: set[str]) -> bool:
    guess = _digest(text.replace("sch-", f"{letters}-"), 16)
    return guess in published_runs or _digest(guess, 12) in published_runs


def _study_repository(repo: Path) -> None:
    """A lesson re-frozen once, recorded the way the study records it."""
    current, old = "How many triangles has an octagon, from one vertex?", "How many triangles?"
    now, before = _digest(_as_written(_plan(current)), 16), _digest(_as_written(_plan(old)), 16)
    frozen = {"lesson": LESSON, "plan_sha256": before, "plan": _plan(old, sets_work=True)}
    case = {"lesson": LESSON, "plan_sha256": now, "plan": _plan(current, sets_work=True)}
    _commit(
        repo,
        {
            f"transcripts/{LESSON}/session-plan.json": _as_written(_plan(current)),
            "eval_set.json": json.dumps({"cases": [case]}, indent=2),
            f"frozen/{LESSON}-{before}.json": json.dumps(frozen, indent=2),
            "frozen/README.md": f"| `{LESSON}-{before}.json` | superseded |\n",
            "runs/earlier/run.json": json.dumps({"plans": {LESSON: before}}),
            "runs/earlier/fingerprint.json": json.dumps({"inputs": {"plan": _digest(before, 12)}}),
            "runs/later/run.json": json.dumps({"plans": {LESSON: now}}),
            "runs/later/fingerprint.json": json.dumps({"inputs": {"plan": _digest(now, 12)}}),
        },
    )


def test_no_three_letters_but_the_replacement_reproduce_a_digest_in_the_built_release(tmp_path):
    _study_repository(tmp_path / "repo")
    fixture = Repository("fixture", tmp_path / "repo")
    releases = [
        collect(Dataset("plans", (Source(fixture, "HEAD", "transcripts", "transcripts"),))),
        collect(
            Dataset(
                "ratings",
                (
                    Source(fixture, "HEAD", "eval_set.json", "inputs/eval_set.json"),
                    Source(fixture, "HEAD", "frozen", "inputs/frozen"),
                    Source(fixture, "HEAD", "runs", "runs"),
                ),
            )
        ),
    ]
    seal(releases)
    out = tmp_path / "out"
    reports = []
    for release in releases:
        write(release, out)
        report = verify(out / release.name)
        report.problems.extend(against(release, out / release.name))
        reports.append(report)

    assert [report.problems for report in reports] == [[], []]
    assert leaks(reports, releases) == []
    published_runs = set().union(*(report.hex_runs for report in reports))
    plans = [json.loads((out / "plans/transcripts" / LESSON / "session-plan.json").read_text())]
    plans += [
        json.loads(path.read_text())["plan"]
        for path in (out / "ratings/inputs/frozen").glob("*.json")
    ]
    plans += [
        case["plan"]
        for case in json.loads((out / "ratings/inputs/eval_set.json").read_text())["cases"]
    ]
    texts = {_as_written(form) for plan in plans for form in (plan, _unjudged(plan))}
    recovered = {
        letters
        for letters in map("".join, itertools.product(string.ascii_lowercase, repeat=3))
        for text in texts
        if _reproduces(text, letters, published_runs)
    }
    assert recovered == {"sch"}
