"""The seed corpus fetched from the Hub: placed only when every file checks, and nothing deleted."""

from __future__ import annotations

import fnmatch
import hashlib
import json
from collections.abc import Callable
from pathlib import Path

from scripts.fetch_datasets import main

REPO = "owner/ng-jss1-math-curriculum"
REVISION = "0" * 40
PLACES = {"curriculum": "dataset/processed/curriculum"}


def _lock(root: Path, places: dict[str, str] = PLACES, include: list[str] | None = None) -> None:
    lock = root / "dataset" / "datasets.lock.json"
    lock.parent.mkdir(parents=True)
    entry: dict[str, object] = {"repo": REPO, "revision": REVISION, "places": places}
    if include:
        entry["include"] = include
    lock.write_text(json.dumps({"datasets": [entry]}), encoding="utf-8")


def _hub(
    files: dict[str, bytes],
    recorded: dict[str, bytes] | None = None,
    extra: dict[str, bytes] | None = None,
) -> Callable[..., str]:
    """A stand-in for ``snapshot_download`` serving one dataset, as the Hub lays it out on disk."""
    listed = files if recorded is None else recorded

    def snapshot(
        *,
        repo_id: str,
        repo_type: str,
        revision: str,
        local_dir: str,
        allow_patterns: list[str] | None = None,
    ) -> str:
        assert (repo_id, repo_type, revision) == (REPO, "dataset", REVISION)
        folder = Path(local_dir)
        served = {**files, **(extra or {}), "README.md": b"card", ".cache/huggingface/x": b"hub"}
        for path, body in served.items():
            if allow_patterns and not any(fnmatch.fnmatchcase(path, p) for p in allow_patterns):
                continue
            (folder / path).parent.mkdir(parents=True, exist_ok=True)
            (folder / path).write_bytes(body)
        entries = [{"path": p, "sha256": hashlib.sha256(b).hexdigest()} for p, b in listed.items()]
        (folder / "PROVENANCE.json").write_text(json.dumps({"files": entries}), encoding="utf-8")
        return local_dir

    return snapshot


def test_every_file_lands_where_the_lock_places_its_folder(tmp_path):
    _lock(tmp_path)
    files = {"curriculum/jss1_topics.json": b"[1]", "curriculum/topics/01.json": b"{}"}
    assert main(["--root", str(tmp_path)], snapshot=_hub(files)) == 0
    placed = tmp_path / "dataset/processed/curriculum"
    assert (placed / "jss1_topics.json").read_bytes() == b"[1]"
    assert (placed / "topics/01.json").read_bytes() == b"{}"
    assert not (placed / "README.md").exists()


def test_a_file_unlike_its_recorded_digest_refuses_the_fetch_and_writes_nothing(tmp_path):
    _lock(tmp_path)
    hub = _hub(
        {"curriculum/jss1_topics.json": b"[1]"}, recorded={"curriculum/jss1_topics.json": b"[2]"}
    )
    assert main(["--root", str(tmp_path)], snapshot=hub) == 1
    assert not (tmp_path / "dataset/processed").exists()


def test_a_downloaded_file_the_provenance_does_not_list_refuses_the_fetch(tmp_path):
    _lock(tmp_path)
    hub = _hub({"curriculum/jss1_topics.json": b"[1]"}, extra={"curriculum/stray.json": b"x"})
    assert main(["--root", str(tmp_path)], snapshot=hub) == 1
    assert not (tmp_path / "dataset/processed").exists()


def test_a_folder_the_lock_gives_no_place_refuses_the_fetch(tmp_path):
    _lock(tmp_path)
    files = {"curriculum/jss1_topics.json": b"[1]", "scheme-of-work/jss1_scheme.json": b"{}"}
    assert main(["--root", str(tmp_path)], snapshot=_hub(files)) == 1
    assert not (tmp_path / "dataset/processed").exists()


def test_a_file_in_place_that_the_dataset_does_not_have_is_reported_and_kept(tmp_path):
    _lock(tmp_path)
    old = tmp_path / "dataset/processed/curriculum/retired.json"
    old.parent.mkdir(parents=True)
    old.write_bytes(b"kept")
    assert main(["--root", str(tmp_path)], snapshot=_hub({"curriculum/a.json": b"[1]"})) == 1
    assert old.read_bytes() == b"kept"
    assert (tmp_path / "dataset/processed/curriculum/a.json").read_bytes() == b"[1]"


def test_a_stray_file_is_reported_even_when_its_path_matches_another_folder_s_file(tmp_path):
    _lock(tmp_path, {**PLACES, "scheme-of-work": "dataset/processed/scheme-of-work"})
    stray = tmp_path / "dataset/processed/curriculum/scheme-of-work/jss1_scheme.json"
    stray.parent.mkdir(parents=True)
    stray.write_bytes(b"stray")
    files = {"curriculum/a.json": b"[1]", "scheme-of-work/jss1_scheme.json": b"{}"}
    assert main(["--root", str(tmp_path)], snapshot=_hub(files)) == 1
    assert stray.read_bytes() == b"stray"


def test_a_lock_can_place_a_folder_inside_the_dataset_and_take_only_some_of_its_files(tmp_path):
    _lock(tmp_path, {"ratings/delivered": "human_rating/delivered"}, ["ratings/delivered/*.docx"])
    kept = tmp_path / "human_rating/delivered/README.md"
    kept.parent.mkdir(parents=True)
    kept.write_bytes(b"ours")
    files = {
        "ratings/delivered/R1/a.docx": b"doc",
        "ratings/delivered/README.md": b"theirs",
        "ratings/ratings.csv": b"x",
        "runs/h1/run.json": b"{}",
    }
    assert main(["--root", str(tmp_path)], snapshot=_hub(files)) == 0
    assert (tmp_path / "human_rating/delivered/R1/a.docx").read_bytes() == b"doc"
    assert kept.read_bytes() == b"ours"
    assert not (tmp_path / "human_rating/delivered/ratings.csv").exists()
