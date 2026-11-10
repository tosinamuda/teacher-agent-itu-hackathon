"""Persistable fingerprints of prompts used to generate a review pack."""

import hashlib
import json

from pydantic import BaseModel, ConfigDict, Field


class PromptProvenance(BaseModel):
    """Prompt components that materially contributed to one generated result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    components: dict[str, str] = Field(default_factory=dict)

    @property
    def composite_fingerprint(self) -> str | None:
        if not self.components:
            return None
        encoded = json.dumps(self.components, sort_keys=True, separators=(",", ":")).encode()
        return f"prompt-{hashlib.sha256(encoded).hexdigest()[:12]}"
