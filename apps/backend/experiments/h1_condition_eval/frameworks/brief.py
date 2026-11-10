"""The `compose-v2` contract, rendered for a framework that does not read dspy signatures.

`ComposeSection` builds its instructions and its inputs from a dspy signature; langgraph,
ADK and deepagents each take a system prompt and a message. The brief is therefore ASKED
FROM `ComposeSection` rather than re-authored, so what differs between these arms and
`compose-v2` is the loop driving the tools, not the task the model was set.

One thing is deliberately not carried over: dspy's field-marker envelope. The ChatAdapter
also instructs the model to reply in `[[ ## field ## ]]` blocks, and these arms have no
such reply to make — they finish by having called the tools. Reproducing it would set them
a task they are not scored on.
"""

from __future__ import annotations

import json
from typing import Any

import dspy
from pydantic import BaseModel

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (  # noqa: E501
    ComposeSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    ContractMode,
)
from app.infra.dspy_lm import build_dspy_lm


def composed_brief(
    *,
    request: ReviewPackRequest,
    unit: SectionGenerationUnit,
    signatures: ContractMode,
) -> tuple[str, str]:
    """The instructions `compose-v2` is given, and its inputs as one message.

    The LM handed to `ComposeSection` is never called: the module is constructed only to
    be asked which contract this condition renders and which inputs fill it, which is the
    pair that has to stay identical for the comparison to be about the framework.
    """
    composer = ComposeSection(lm=build_dspy_lm(), contract_mode=signatures)
    contract = composer.contract(request)
    return contract.instructions, _rendered(contract, composer.inputs(request, unit, contract))


def _rendered(contract: type[dspy.Signature], inputs: dict[str, Any]) -> str:
    """Each input field under its own heading, described as the contract describes it."""
    return "\n\n".join(
        f"## {name}{_described(contract.input_fields[name])}\n\n{_as_text(value)}"
        for name, value in inputs.items()
    )


def _described(field: Any) -> str:
    description = (field.json_schema_extra or {}).get("desc", "")
    return f" — {description}" if description else ""


def _as_text(value: Any) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json", exclude_none=True)
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=2, ensure_ascii=False, default=str)
