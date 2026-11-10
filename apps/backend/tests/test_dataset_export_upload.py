"""What an upload asks of the Hub: private repositories, exact mirrors, one private collection."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from experiments.dataset_export.upload import NAMESPACE, upload


class _Hub:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def create_repo(self, repo_id: str, **options: Any) -> str:
        self.calls.append(("create_repo", repo_id, options))
        return f"https://huggingface.co/datasets/{repo_id}"

    def upload_folder(self, **options: Any) -> SimpleNamespace:
        self.calls.append(("upload_folder", options["repo_id"], options))
        url = f"https://huggingface.co/datasets/{options['repo_id']}/commit/{'a' * 40}"
        return SimpleNamespace(oid="a" * 40, commit_url=url)

    def create_collection(self, title: str, **options: Any) -> SimpleNamespace:
        self.calls.append(("create_collection", title, options))
        slug = f"{NAMESPACE}/lpcg-datasets-0123"
        return SimpleNamespace(slug=slug, url=f"https://huggingface.co/collections/{slug}")

    def add_collection_item(self, slug: str, item_id: str, item_type: str, **options: Any) -> None:
        self.calls.append(("add_collection_item", item_id, {"slug": slug, "type": item_type}))

    def made(self, call: str) -> list[tuple[str, dict[str, Any]]]:
        return [(target, options) for name, target, options in self.calls if name == call]


def test_every_dataset_goes_up_private_as_an_exact_mirror_and_joins_one_private_collection():
    hub = _Hub()
    roots = [Path("/out/ng-jss1-math-curriculum"), Path("/out/ng-jss1-math-alignment-ratings")]
    uploaded, collection = upload(roots, api=hub)  # type: ignore[arg-type]

    expected = [
        f"{NAMESPACE}/ng-jss1-math-curriculum",
        f"{NAMESPACE}/ng-jss1-math-alignment-ratings",
    ]
    assert [target for target, _ in hub.made("create_repo")] == expected
    assert all(
        o["private"] is True and o["repo_type"] == "dataset" for _, o in hub.made("create_repo")
    )
    assert [target for target, _ in hub.made("upload_folder")] == expected
    assert all(options["delete_patterns"] == "*" for _, options in hub.made("upload_folder"))
    ((_, collection_options),) = hub.made("create_collection")
    assert collection_options["private"] is True
    assert [target for target, _ in hub.made("add_collection_item")] == expected
    assert [item.repo_id for item in uploaded] == expected
    assert collection.endswith("/lpcg-datasets-0123")
