"""A harness run never writes into a folder another run wrote, unless it is resuming it."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from experiments.run_folders import open_run, run_label


def test_a_run_is_named_for_the_second_it_started_in_utc() -> None:
    started = datetime(2026, 9, 25, 18, 30, 5, tzinfo=timezone.utc)

    assert run_label("c0c3", started) == "c0c3-20260925T183005Z"


def test_each_new_run_gets_a_folder_of_its_own(tmp_path) -> None:
    label, folder = open_run(tmp_path, stem="h2", resume=None)

    assert folder == tmp_path / label and folder.is_dir()
    assert label.startswith("h2-") and label.endswith("Z")


def test_a_run_never_writes_into_a_folder_that_exists(tmp_path, monkeypatch) -> None:
    started = datetime(2026, 9, 25, 18, 30, 5, tzinfo=timezone.utc)
    (tmp_path / run_label("h2", started)).mkdir()
    monkeypatch.setattr(
        "experiments.run_folders.datetime",
        type("_Frozen", (), {"now": staticmethod(lambda _tz: started)}),
    )

    with pytest.raises(SystemExit):
        open_run(tmp_path, stem="h2", resume=None)


def test_resuming_carries_on_in_the_named_run_and_only_one_that_exists(tmp_path) -> None:
    (tmp_path / "h2-20260925T183005Z").mkdir()

    assert open_run(tmp_path, stem="ignored", resume="h2-20260925T183005Z") == (
        "h2-20260925T183005Z",
        tmp_path / "h2-20260925T183005Z",
    )
    with pytest.raises(SystemExit):
        open_run(tmp_path, stem="ignored", resume="h2-never")


def test_a_resumed_run_keeps_the_traces_it_already_took(tmp_path) -> None:
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy import tracing

    traces = tmp_path / "traces.jsonl"
    traces.write_text('{"earlier": true}\n', encoding="utf-8")

    tracing.start_capture(stream_to=traces)
    tracing.drain()

    assert traces.read_text(encoding="utf-8") == '{"earlier": true}\n'
