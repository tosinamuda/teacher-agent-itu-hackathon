from __future__ import annotations

import json
from pathlib import Path

from app.config import BACKEND_DIR
from app.shared.json_types import JsonObject


class ArtefactStore:
    """Filesystem-backed artefact export storage."""

    def __init__(self, root: Path | None = None) -> None:
        if root is None:
            root = BACKEND_DIR / ".artefacts"
        self.root = root

    def export_review_pack(self, artefact_id: str, manifest: JsonObject) -> JsonObject:
        export_dir = self.root / "exports" / "review-packs" / artefact_id
        export_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = export_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return {
            "manifest_path": str(manifest_path),
            "export_dir": str(export_dir),
        }
