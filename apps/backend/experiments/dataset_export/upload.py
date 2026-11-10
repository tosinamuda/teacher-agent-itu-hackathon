"""Put the built datasets on the Hugging Face Hub, private, gathered in one collection.

Each repository is created private and mirrors its build exactly: a file the build no longer
produces is deleted from the repository rather than left behind. Going public is a decision
taken on the Hub, after the uploaded datasets have been read there.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from huggingface_hub import HfApi

NAMESPACE = "tosinamuda"
COLLECTION_TITLE = "LPCG datasets"
COLLECTION_DESCRIPTION = (
    "Curriculum, textbook linkage, lesson plans and alignment ratings from the LPCG study of "
    "JSS1 mathematics in Nigeria."
)


@dataclass(frozen=True)
class Uploaded:
    repo_id: str
    commit: str
    url: str


def upload(roots: Iterable[Path], api: HfApi | None = None) -> tuple[list[Uploaded], str]:
    """Mirror each built dataset to its repository; return what went up and the collection URL."""
    hub = api or HfApi()
    uploaded = [_mirror(hub, root) for root in roots]
    collection = hub.create_collection(
        COLLECTION_TITLE,
        namespace=NAMESPACE,
        description=COLLECTION_DESCRIPTION,
        private=True,
        exists_ok=True,
    )
    for item in uploaded:
        hub.add_collection_item(collection.slug, item.repo_id, "dataset", exists_ok=True)
    return uploaded, collection.url


def _mirror(hub: HfApi, root: Path) -> Uploaded:
    repo_id = f"{NAMESPACE}/{root.name}"
    hub.create_repo(repo_id, repo_type="dataset", private=True, exist_ok=True)
    commit = hub.upload_folder(
        repo_id=repo_id,
        folder_path=root,
        repo_type="dataset",
        commit_message=f"Publish {root.name} as built and verified",
        delete_patterns="*",
    )
    return Uploaded(repo_id, commit.oid, commit.commit_url)
