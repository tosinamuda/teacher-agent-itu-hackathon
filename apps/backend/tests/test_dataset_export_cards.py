"""Each dataset's card: filled from the build, complete, and clean of what must not ship."""

from __future__ import annotations

from experiments.dataset_export.build import Entry, Release
from experiments.dataset_export.cards import TEMPLATES, cards, missing_tables, viewer_tables
from experiments.dataset_export.sources import datasets
from experiments.dataset_export.verify import SCHOOL_LETTERS


def _release(name: str, files: int) -> Release:
    entries = tuple(Entry(f"data/{index}.json", b"{}", b"{}") for index in range(files))
    return Release(name, (), entries, ())


def test_every_dataset_has_a_card_and_no_card_is_left_without_a_dataset():
    templated = {path.name.split(".")[0] for path in TEMPLATES.glob("*.md")}
    assert templated == {dataset.name for dataset in datasets()}


def test_a_card_opens_with_hub_metadata_and_leaves_no_placeholder_unfilled():
    for dataset in datasets():
        readme = cards(_release(dataset.name, 3820), replaced=14)["README.md"]
        assert readme.startswith("---\n"), dataset.name
        metadata, _, body = readme.removeprefix("---\n").partition("\n---\n")
        for field in ("pretty_name:", "license:", "- 1K<n<10K"):
            assert field in metadata, (dataset.name, field)
        assert "$" not in readme, dataset.name
        assert body.strip(), dataset.name


def test_a_card_either_turns_the_viewer_off_or_names_the_tables_it_shows():
    for dataset in datasets():
        readme = cards(_release(dataset.name, 10), replaced=0)["README.md"]
        assert ("viewer: false" in readme) != bool(viewer_tables(readme)), dataset.name


def test_a_viewer_table_the_dataset_does_not_hold_is_reported(tmp_path):
    (tmp_path / "README.md").write_text(
        "---\nconfigs:\n- config_name: rows\n  data_files:\n  - split: train\n"
        "    path: data/rows.jsonl\n  - split: test\n    path: data/held.jsonl\n---\nBody\n",
        encoding="utf-8",
    )
    (tmp_path / "data").mkdir()
    (tmp_path / "data/held.jsonl").write_text("{}\n", encoding="utf-8")
    assert missing_tables(tmp_path) == ["data/rows.jsonl"]


def test_a_card_that_licenses_by_file_ships_the_file_it_links():
    for dataset in datasets():
        files = cards(_release(dataset.name, 10), replaced=0)
        if "license: other" in files["README.md"]:
            assert "license_link: LICENSE.md" in files["README.md"], dataset.name
            assert "LICENSE.md" in files, dataset.name


def test_no_card_carries_the_school_s_abbreviation():
    for dataset in datasets():
        for name, text in cards(_release(dataset.name, 10), replaced=0).items():
            assert not SCHOOL_LETTERS.search(text), (dataset.name, name)
