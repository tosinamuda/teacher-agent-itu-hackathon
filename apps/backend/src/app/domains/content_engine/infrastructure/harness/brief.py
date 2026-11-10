"""What a harness is told: the DSPy writer's and checker's own instructions and inputs.

A harness replaces only the loop. So its system prompt is the signature's instructions, with
each input described as the signature describes it, and its message is the same inputs,
skills pinned in the brief included.
"""

from __future__ import annotations

import json
import re

import dspy
from pydantic import BaseModel, Field, ValidationError
from pydantic.fields import FieldInfo

from app.domains.content_engine.infrastructure.checker import CheckerStoppedError, CheckPart
from app.domains.content_engine.infrastructure.tools import WRITER_TOOLS
from app.domains.content_engine.infrastructure.writer import WriteContent
from app.shared.json_types import JsonObject


def _desc(field: FieldInfo) -> str:
    """What a DSPy field says it holds."""
    extra = field.json_schema_extra
    desc = (
        next((v for k, v in extra.items() if k == "desc"), None)
        if isinstance(extra, dict)
        else None
    )
    return desc if isinstance(desc, str) else ""


def _described(signature: type[dspy.Signature]) -> str:
    fields = "\n".join(
        f"- {name}: {_desc(field)}" for name, field in signature.input_fields.items()
    )
    return f"{signature.instructions}\n\nThe message gives these inputs:\n{fields}"


def as_named_by(text: str, prefix: str) -> str:
    """`text` with each writer tool named as a harness exposes it, such as `engine_revise_part`.

    A harness puts its server's name before each tool, and a model asked to call `revise_part`
    sometimes calls exactly that, which the harness does not have.
    """
    return re.sub(rf"\b({'|'.join(WRITER_TOOLS)})\b", rf"{prefix}\1", text)


def _message(values: dict[str, object]) -> str:
    return "\n\n".join(
        f"## {name}\n{value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)}"
        for name, value in values.items()
    )


#: The checker's model calls: it answers once, and a turn more lets a harness ask again for
#: a malformed answer. Past that it stops rather than asking forever.
CHECKER_STEPS = 3

#: The writer's system prompt: fill the draft with the tools, one part per unit.
WRITER_PROMPT = _described(WriteContent)

_BRIEF_SKILLS = "follow every\nskill the brief gives, each where its use_when says it applies."
_OWN_SKILLS = (
    "start with the skill the message names as entry_skill: load it with your skill tool "
    "before you write anything, and follow it, including when it sends you to read one of "
    "its files. Load any other skill you have where its description says it applies."
)


def _with_skills_found_by_the_harness(prompt: str) -> str:
    """The writer's prompt for a harness that finds the skills itself, not in the brief."""
    if _BRIEF_SKILLS not in prompt:
        raise ValueError("the writer's instructions no longer say where the skills come from")
    return prompt.replace(_BRIEF_SKILLS, _OWN_SKILLS)


#: The writer's system prompt when the harness loads the skills, not the brief.
NATIVE_SKILLS_WRITER_PROMPT = _with_skills_found_by_the_harness(WRITER_PROMPT)

#: The checker's system prompt: work the part through and list its real errors.
CHECKER_PROMPT = _described(CheckPart)


def entry_skill(draft: JsonObject) -> str | None:
    """The skill a writer starts with: the first skill the draft's type pins."""
    pinned = draft.get("pinned_skills")
    first = pinned[0] if isinstance(pinned, list) and pinned else None
    return str(first["skill"]) if isinstance(first, dict) else None


def writer_message(
    draft: JsonObject, lesson: JsonObject, feedback: str, *, entry: str | None = None
) -> str:
    """The writer's inputs, as the DSPy writer is given them; ``entry`` names its first skill.

    A draft that revises content already holds its parts, which the writer is given, so it
    changes them and does not write them again from nothing.
    """
    return _message(
        {
            "draft_id": draft["draft_id"],
            **({"entry_skill": entry} if entry is not None else {}),
            "brief": draft["brief"],
            "part_schemas": draft["part_schemas"],
            "units": draft["units"],
            **({"parts": draft["parts"]} if draft.get("parts") else {}),
            "lesson": lesson,
            "source": draft.get("source", "") or "",
            "feedback": feedback,
        }
    )


def follow_up_message(draft: JsonObject, feedback: str) -> str:
    """What a writer that already has its brief is sent next: the draft to use, and the feedback."""
    return _message(
        {
            "draft_id": draft["draft_id"],
            "feedback": feedback,
            "note": (
                "This draft is open for you with the parts of the latest version. Use this "
                "draft_id with your tools from now on. Carry on from where you were: apply "
                "the feedback with revise_part, and write any part still missing with add_part."
            ),
        }
    )


def checker_message(brief: JsonObject, unit: dict[str, object], part: JsonObject) -> str:
    """The checker's inputs, as the DSPy checker is given them."""
    return _message({"brief": brief, "unit": unit, "part": part})


def turns_for(draft: JsonObject) -> int:
    """How many model turns a writer has on a draft: the DSPy writer's ``max_iters``."""
    units = draft["units"]
    return 2 * len(units) + 6 if isinstance(units, list) else 6


class Verdict(BaseModel):
    """The checker's answer, as the DSPy checker's output field describes it."""

    errors: list[str] = Field(description=_desc(CheckPart.output_fields["errors"]))


def written_answer(text: str) -> object:
    """A checker's answer the model wrote as text instead of calling its answer tool.

    gpt-oss often writes the verdict as JSON in its reply: the JSON, when it is, else the text
    (which the Verdict schema then refuses). Every loop reads a written answer the same way,
    so one that cannot read it is not held against the loop.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text.strip() or None


def refusal(answer: object) -> str | None:
    """Why the Verdict schema refuses a checker's answer; nothing when it allows it."""
    try:
        Verdict.model_validate(answer if isinstance(answer, dict) else {"errors": answer})
    except ValidationError as error:
        return str(error)
    return None


def answer_again(reason: str) -> str:
    """What a checker is told, once, after an answer the Verdict schema refused.

    Each loop sends a refused answer back with the reason, as the engine's draft tools do a
    refused part, within the checker's model calls.
    """
    return (
        f"Your answer was refused: {reason}\n"
        "Answer again with your answer tool. errors is a list of strings: each one a real "
        "error, where it is, and the correction."
    )


def verdict_of(answer: object) -> list[str]:
    """The errors a checker's answer lists.

    An answer the Verdict schema does not allow is refused rather than read as "no errors":
    gpt-oss can ignore a required answer tool, or answer with objects where strings belong.
    """
    try:
        verdict = Verdict.model_validate(answer if isinstance(answer, dict) else {"errors": answer})
    except ValidationError as error:
        raise CheckerStoppedError(f"the checker gave no list of errors: {answer!r:.300}") from error
    return [error for error in verdict.errors if error.strip()]
