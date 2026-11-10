"""DSPy-specific prompt fingerprinting at the model-call boundary."""

import hashlib
import json
from typing import cast

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.prompt_provenance import (
    record_prompt_fingerprint,
)


def record_prompt(component: str, signature: type[dspy.Signature]) -> None:
    record_prompt_fingerprint(component, fingerprint_signature(signature))


def fingerprint_signature(signature: type[dspy.Signature]) -> str:
    """Hash every prompt-reaching instruction, field description, and schema."""
    parts = [str(signature.instructions)]
    for name, model_field in {**signature.input_fields, **signature.output_fields}.items():
        raw = model_field.json_schema_extra
        extra = cast("dict[str, object]", raw) if isinstance(raw, dict) else {}
        description = extra.get("desc")
        parts.append(f"{name}:{description if isinstance(description, str) else ''}")
    parts.append(json.dumps(signature.model_json_schema(), sort_keys=True, default=str))
    digest = hashlib.sha256("\n".join(parts).encode()).hexdigest()
    return f"prompt-{digest[:12]}"
