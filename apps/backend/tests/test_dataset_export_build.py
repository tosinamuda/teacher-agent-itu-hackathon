"""Where committed files land in a dataset, and what verification refuses to let through."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from experiments.dataset_export.build import destination
from experiments.dataset_export.sources import PHOTOGRAPHS, Repository, Source
from experiments.dataset_export.verify import verify

REPO = Repository("test", Path("/repo"))


def test_a_directory_source_keeps_the_layout_beneath_it_under_its_landing():
    source = Source(REPO, "HEAD", "apps/backend/experiments/h1_condition_eval/runs", "runs/h1")
    member = "apps/backend/experiments/h1_condition_eval/runs/c0c3-prism-objective/run.json"
    assert destination(source, member) == "runs/h1/c0c3-prism-objective/run.json"


def test_a_file_source_lands_exactly_where_it_is_told_to():
    source = Source(
        REPO,
        "HEAD",
        "apps/backend/experiments/h1_condition_eval/eval_set.json",
        "inputs/eval_set.json",
    )
    assert destination(source, source.path) == "inputs/eval_set.json"


def test_the_two_comparison_photographs_are_left_out_and_the_typeset_renders_are_not():
    source = Source(
        REPO, "HEAD", "transcripts", "transcripts", keep=lambda rel: rel not in PHOTOGRAPHS
    )
    for photograph in PHOTOGRAPHS:
        assert destination(source, f"transcripts/{photograph}") is None
    assert destination(source, "transcripts/_render/page-1.png") == "transcripts/_render/page-1.png"


def _built(tmp_path: Path, files: dict[str, bytes]) -> Path:
    root = tmp_path / "lpcg-test"
    entries = []
    for name, body in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes(body)
        entries.append(
            {
                "path": name,
                "source": "test",
                "sha256": hashlib.sha256(body).hexdigest(),
                "rewritten": False,
            }
        )
    (root / "PROVENANCE.json").write_text(json.dumps({"dataset": "lpcg-test", "files": entries}))
    return root


def test_verification_passes_a_recorded_tool_call_id_that_happens_to_spell_the_school(tmp_path):
    root = _built(tmp_path, {"runs/traces.jsonl": b'{"id": "call_00_zpQGTC4xk7Hq"}\n'})
    assert verify(root).problems == []


def test_verification_refuses_the_school_left_standing_as_a_word(tmp_path):
    root = _built(tmp_path, {"lessons/t2-w09.xml": b'<lesson session-id="gtc-t2-w09"/>'})
    assert any("abbreviation" in problem for problem in verify(root).problems)


def test_verification_refuses_the_letters_inside_a_short_token(tmp_path):
    root = _built(tmp_path, {"notes/x.md": b"see xgtc for detail"})
    assert any("outside an opaque id" in problem for problem in verify(root).problems)


def test_verification_notices_a_file_changed_after_it_was_recorded(tmp_path):
    root = _built(tmp_path, {"curriculum/theme.md": b"Whole Numbers"})
    (root / "curriculum/theme.md").write_bytes(b"Whole Numbers, edited")
    assert any("recorded digest" in problem for problem in verify(root).problems)


def test_verification_notices_a_file_nobody_recorded(tmp_path):
    root = _built(tmp_path, {"curriculum/theme.md": b"Whole Numbers"})
    (root / "curriculum/stray.md").write_bytes(b"not in the provenance")
    assert any("not in PROVENANCE.json" in problem for problem in verify(root).problems)
